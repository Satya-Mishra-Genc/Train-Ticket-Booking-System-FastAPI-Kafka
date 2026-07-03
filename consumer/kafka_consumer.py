import json
import time
from datetime import datetime
from pathlib import Path


EVENT_LOG_FILE = Path("events.log")


class EventTypes:
    USER_REGISTERED = "USER_REGISTERED"
    USER_LOGGED_IN = "USER_LOGGED_IN"
    TRAIN_SEARCHED = "TRAIN_SEARCHED"
    SEAT_CHECKED = "SEAT_CHECKED"
    TICKET_BOOKED = "TICKET_BOOKED"
    TICKET_UPDATED = "TICKET_UPDATED"
    TICKET_CANCELLED = "TICKET_CANCELLED"
    VALIDATION_FAILED = "VALIDATION_FAILED"


class KafkaConsumerService:

    def __init__(self):
        self.analytics = {
            "bookings": 0,
            "cancellations": 0,
            "searches": 0,
            "seat_checks": 0,
            "failed": 0
        }

        self.offset = 0  # Simulated Kafka offset

    def process_event(self, event: dict):
        event_type = event.get("event_type")

        print("\n EVENT RECEIVED")
        print(json.dumps(event, indent=2))

        if event_type == EventTypes.TICKET_BOOKED:
            self.analytics["bookings"] += 1
            print(" Ticket booked")

        elif event_type == EventTypes.TICKET_CANCELLED:
            self.analytics["cancellations"] += 1
            print(" Ticket cancelled")

        elif event_type == EventTypes.TRAIN_SEARCHED:
            self.analytics["searches"] += 1

        elif event_type == EventTypes.SEAT_CHECKED:
            self.analytics["seat_checks"] += 1

        elif event_type == EventTypes.VALIDATION_FAILED:
            self.analytics["failed"] += 1

        self.print_analytics()

    def print_analytics(self):
        print("\n LIVE ANALYTICS")
        for k, v in self.analytics.items():
            print(f"{k}: {v}")
        print("-" * 30)

    def start(self):
        print(" Kafka Consumer Started (FILE‑STREAM MODE)")
        print("Listening for events...\n")

        EVENT_LOG_FILE.touch(exist_ok=True)

        with EVENT_LOG_FILE.open("r", encoding="utf-8") as f:
            f.seek(self.offset)

            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue

                self.offset = f.tell()

                try:
                    event = json.loads(line.strip())
                    self.process_event(event)
                except Exception as e:
                    print(" Invalid event:", e)


if __name__ == "__main__":
    consumer = KafkaConsumerService()
    consumer.start()