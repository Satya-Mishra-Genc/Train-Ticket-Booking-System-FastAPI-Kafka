from sqlalchemy import Column, Integer, String
from database import Base


# ==========================
#  USER TABLE
# ==========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)


# ==========================
#  TICKET TABLE (IRCTC STYLE)
# ==========================
class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    pnr = Column(String(20), unique=True, nullable=False)

    # Passenger details
    passenger_name = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    contact = Column(String(20))

    # Journey details
    train_no = Column(String(10))
    source = Column(String(50))
    destination = Column(String(50))
    journey_date = Column(String(20))

    # Seat & class details
    seat_class = Column(String(20))
    seat_no = Column(String(20))
    berth = Column(String(20))
    coach = Column(String(10))

    # Ticket status
    status = Column(String(20))  # CONFIRMED / RAC / WAITING / CANCELLED