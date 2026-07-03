import json
import time
from uuid import uuid4
from datetime import datetime
from pathlib import Path


EVENT_LOG_FILE = Path("events.log")


class KafkaProducerService:

    def __init__(self):
        self.service_name = "train-ticket-booking-api"
        self.max_retries = 3

    def _create_event(self, event_type: str, payload: dict):
        return {
            "event_id": str(uuid4()),
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.service_name,
            "payload": payload
        }

    def send_event(self, event_type: str, payload: dict):
        event = self._create_event(event_type, payload)

        for attempt in range(1, self.max_retries + 1):
            try:
                print("\n KAFKA PRODUCER EVENT")
                print(json.dumps(event, indent=2))

                with EVENT_LOG_FILE.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(event) + "\n")

                return True

            except Exception as e:
                print(" Producer error:", e)
                time.sleep(1)

        return False


#  Singleton
producer = KafkaProducerService()