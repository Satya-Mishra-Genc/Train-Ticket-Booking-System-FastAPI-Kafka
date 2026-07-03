from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Generator, List
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy import desc
import random

from pydantic import BaseModel

from database import SessionLocal, engine
from models import User, Ticket
from auth import hash_password, verify_password, create_token
from kafka_producer import producer
from data_store import trains, seat_availability

#  DB INIT
User.metadata.create_all(bind=engine)
Ticket.metadata.create_all(bind=engine)

app = FastAPI(title="IRCTC Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  DATE VALIDATION

def validate_journey_date(journey_date: str):
    date_obj = None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            date_obj = datetime.strptime(journey_date, fmt).date()
            break
        except ValueError:
            continue

    if not date_obj:
        return None, "Invalid date format. Use YYYY-MM-DD"

    today = datetime.today().date()
    if date_obj > today + timedelta(days=120):
        return None, "Allowed only up to 120 days"

    return date_obj, None


#  REQUEST MODELS

class PassengerRequest(BaseModel):
    name: str
    age: int
    gender: str
    contact: str
    berth: str

class BookingRequest(BaseModel):
    passengers: List[PassengerRequest]
    train_no: str
    journey_date: str
    seat_class: str


#  AUTH

@app.post("/signup")
def signup(email: str, password: str, db: Session = Depends(get_db)):
    if not email.endswith("@irctc.com"):
        raise HTTPException(400, "Only @irctc.com allowed")

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "User already exists")

    user = User(email=email, password=hash_password(password))
    db.add(user)
    db.commit()
    producer.send_event("USER_REGISTERED", {"email": email})
    return {"message": "Signup successful"}

@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(401, "Invalid credentials")

    token = create_token(email)
    producer.send_event("USER_LOGGED_IN", {"email": email})
    return {"access_token": token}


#  TRAIN DETAILS

@app.get("/train/{train_no}")
def train_details(train_no: str, journey_date: str):
    journey_dt, err = validate_journey_date(journey_date)
    if err:
        return {"message": err}

    train = next((t for t in trains if t["train_no"] == train_no), None)
    if not train:
        return {"message": "Train not found"}

    day = journey_dt.strftime("%a")
    if "Daily" not in train["running_days"] and day not in train["running_days"]:
        return {"message": f"Train does not run on {day}"}

    return train


#  AVAILABILITY

@app.get("/availability/{train_no}")
def availability(train_no: str, journey_date: str):

    journey_dt, err = validate_journey_date(journey_date)
    if err:
        return {"message": err}

    train = next((t for t in trains if t["train_no"] == train_no), None)
    if not train:
        return {"message": "Train not found"}

    day = journey_dt.strftime("%a")
    today = datetime.today().date()

    #  1. TRAIN RUNNING CHECK
    if "Daily" not in train["running_days"] and day not in train["running_days"]:
        return {"message": f"Train does not run on {day}"}

    #  2. NO MORE BOOKING RULE (IMPORTANT)
    if journey_dt == today:
        return {
            "message": "Train Scheduled – No more booking",
            "status": "CLOSED"
        }

    #  3. FUTURE DATE → NORMAL AVAILABILITY
    return seat_availability.get(train_no, {})


#  RUNNING STATUS

@app.get("/status/{train_no}")
def running_status(train_no: str, journey_date: str):

    train = next((t for t in trains if t["train_no"] == train_no), None)
    if not train:
        return {"message": "Train not found"}

    journey_dt, err = validate_journey_date(journey_date)
    if err:
        return {"message": err}

    #  STRICT RUNNING DAY CHECK
    day = journey_dt.strftime("%a")

    if "Daily" not in train["running_days"] and day not in train["running_days"]:
        return {"message": f"Train does not run on {day}"}

    today = datetime.today().date()

    #  PAST
    if journey_dt < today:
        return {
            "status": "Completed",
            "current_station": train["destination"],
            "delay": "No delay"
        }

    #  FUTURE
    if journey_dt > today:
        return {
            "status": "Yet to start",
            "current_station": train["source"],
            "delay": "N/A"
        }

    #  TODAY → LIVE TRACKING
    now = datetime.now()
    prev_stop = None
    next_stop = None

    for stop in train["stops"]:
        arr = stop.get("arr", "").strip()

        if arr in ("", "-", "--"):
            prev_stop = stop
            continue

        try:
            arr_time = datetime.combine(
                journey_dt,
                datetime.strptime(arr, "%H:%M").time()
            )
        except ValueError:
            prev_stop = stop
            continue

        if now < arr_time:
            next_stop = stop
            break

        prev_stop = stop

    if not next_stop:
        return {
            "status": "Arrived",
            "current_station": train["destination"],
            "delay": "On time"
        }

    return {
        "status": "Running",
        "current_station": prev_stop["station"] if prev_stop else train["source"],
        "next_station": next_stop["station"],
        "scheduled_arrival": next_stop["arr"],
        "delay": "On time"
    }

@app.put("/web-checkin/{pnr}")
def web_checkin(pnr: str, db: Session = Depends(get_db)):

    tickets = db.query(Ticket).filter(Ticket.pnr == pnr).all()
    if not tickets:
        raise HTTPException(404, "PNR not found")

    first = tickets[0]

    # ✅ TRAIN MUST BE FETCHED EARLY (CRITICAL FIX)
    train = next((t for t in trains if t["train_no"] == first.train_no), None)
    if not train:
        raise HTTPException(404, "Train not found")

    # ✅ CALCULATE FARE (simple logic – interview friendly)
    fare_map = {
        "Sleeper": 500,
        "3A": 1200,
        "2A": 1800,
        "1A": 3000,
        "Tatkal": 2000
    }
    amount = fare_map.get(first.seat_class, 500) * len(tickets)

    # ✅ CASE 1: ALREADY CHECKED-IN (IDEMPOTENT PUT)
    if first.status == "CHECKED_IN":
        return {
            "status": "ALREADY_CHECKED_IN",
            "pnr": pnr,
            "train_no": first.train_no,
            "train_name": train["name"],
            "source": first.source,
            "destination": first.destination,
            "journey_date": first.journey_date,
            "seat_class": first.seat_class,
            "amount": amount,
            "status_text": "CHECKED_IN",
            "passengers": [
                {
                    "name": t.passenger_name,
                    "age": t.age,
                    "gender": t.gender,
                    "coach": t.coach,
                    "seat_no": t.seat_no,
                    "berth": t.berth
                }
                for t in tickets
            ]
        }

    # ✅ CASE 2: NOT CONFIRMED
    if first.status != "CONFIRMED":
        return {
            "status": "FAILED",
            "reason": "Ticket not confirmed"
        }

    # ✅ DATE VALIDATION
    journey_date = datetime.strptime(first.journey_date, "%Y-%m-%d").date()
    today = datetime.today().date()
    if journey_date != today:
        return {
            "status": "FAILED",
            "reason": "Web check-in allowed only on journey date"
        }

    # ✅ TIME VALIDATION
    dep_time = train["stops"][0]["dep"]
    dep_dt = datetime.combine(today, datetime.strptime(dep_time, "%H:%M").time())

    if datetime.now() > dep_dt - timedelta(hours=1):
        return {
            "status": "FAILED",
            "reason": "Web check-in closed (1 hour before departure)"
        }

    # ✅ UPDATE STATUS
    for t in tickets:
        t.status = "CHECKED_IN"

    db.commit()

    # ✅ KAFKA EVENT
    producer.send_event(
        "WEB_CHECKIN_COMPLETED",
        {
            "pnr": pnr,
            "train_no": first.train_no,
            "journey_date": first.journey_date
        }
    )

    # ✅ SUCCESS RESPONSE (SAME STRUCTURE)
    return {
        "status": "SUCCESS",
        "pnr": pnr,
        "train_no": first.train_no,
        "train_name": train["name"],
        "source": first.source,
        "destination": first.destination,
        "journey_date": first.journey_date,
        "seat_class": first.seat_class,
        "amount": amount,
        "status_text": "CHECKED_IN",
        "passengers": [
            {
                "name": t.passenger_name,
                "age": t.age,
                "gender": t.gender,
                "coach": t.coach,
                "seat_no": t.seat_no,
                "berth": t.berth
            }
            for t in tickets
        ]
    }


#  BOOK TICKET GENERAL / TATKAL

@app.post("/book-ticket")
def book_ticket(booking: BookingRequest, db: Session = Depends(get_db)):

    journey_dt, err = validate_journey_date(booking.journey_date)
    if err:
        return {"status": "FAILED", "reason": err}

    train = next((t for t in trains if t["train_no"] == booking.train_no), None)
    if not train:
        return {"status": "FAILED", "reason": "Train not found"}

    day = journey_dt.strftime("%a")
    if "Daily" not in train["running_days"] and day not in train["running_days"]:
        return {"status": "FAILED", "reason": f"Train does not run on {day}"}

    while True:
        pnr = str(uuid4())[:8].upper()
        if not db.query(Ticket).filter(Ticket.pnr == pnr).first():
            break

    coach_map = {"Sleeper": "S1", "3A": "B1", "2A": "A1", "1A": "H1"}
    coach = coach_map.get(booking.seat_class, "S1")

    passengers_out = []

    for p in booking.passengers:
        seat_no = f"{coach}-{random.randint(1,72)}"

        db.add(Ticket(
            pnr=pnr,
            passenger_name=p.name,
            age=p.age,
            gender=p.gender,
            contact=p.contact,
            train_no=train["train_no"],
            source=train["source"],              
            destination=train["destination"],  
            journey_date=booking.journey_date,
            seat_class=booking.seat_class,
            seat_no=seat_no,
            berth=p.berth,
            coach=coach,
            status="CONFIRMED"
        ))

        passengers_out.append({
            "name": p.name,
            "age": p.age,
            "gender": p.gender,
            "seat_no": seat_no,
            "berth": p.berth,
            "coach": coach
        })

    db.commit()
    producer.send_event("TICKET_BOOKED", {"pnr": pnr})

    return {
        "pnr": pnr,
        "train_no": train["train_no"],
        "train_name": train["name"],
        "source": train["source"],
        "destination": train["destination"],
        "journey_date": booking.journey_date,
        "status": "CONFIRMED",
        "passengers": passengers_out
    }


#  PNR & HISTORY

@app.get("/pnr/history")
def booking_history(db: Session = Depends(get_db)):
    return db.query(Ticket).order_by(desc(Ticket.id)).all()


@app.get("/pnr/{pnr}")
def pnr_status(pnr: str, db: Session = Depends(get_db)):
    tickets = db.query(Ticket).filter(Ticket.pnr == pnr).all()
    if not tickets:
        return {"message": "Not found"}

    first = tickets[0]

    return {
        "pnr": pnr,
        "train_no": first.train_no,
        "source": first.source,
        "destination": first.destination,
        "journey_date": first.journey_date,
        "status": first.status,
        "passengers": [
            {
                "name": t.passenger_name,
                "age": t.age,
                "gender": t.gender,
                "seat_no": t.seat_no,
                "berth": t.berth,
                "coach": t.coach
            }
            for t in tickets
        ]
    }


# CANCEL PNR

@app.delete("/ticket/{pnr}")
def cancel_ticket(pnr: str, db: Session = Depends(get_db)):
    tickets = db.query(Ticket).filter(Ticket.pnr == pnr).all()
    if not tickets:
        return {"message": "Not found"}

    for t in tickets:
        t.status = "CANCELLED"

    db.commit()
    return {"message": "Cancelled successfully"}