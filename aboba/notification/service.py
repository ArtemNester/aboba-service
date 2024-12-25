from dataclasses import dataclass

import orjson

from .repository import (
    BrokerRepositoryConsumer,
    BrokerRepositoryProducer,
)


@dataclass
class BrokerService:
    consumer: BrokerRepositoryConsumer
    producer: BrokerRepositoryProducer

    def consume_event(self):
        self.consumer.open_connection()
        try:
            for raw_message in self.consumer.consume_messages():
                orjson.loads(raw_message)
                ...
        except Exception as e:
            print(f"Unknown error: {e}")
        finally:
            self.consumer.close_connection()

    def process_event(self, event_data: dict):
        """
        Логика обработки события.
        """
        print(f"Processing event: {event_data}")
        self._send_event(event_data)

    def _send_event(self, event_data: dict):
        try:
            self.producer.send_event(event_data=event_data)
            print("Event sent successfully: {event_data}")
        except Exception as e:
            print(f"Error sending event: {e}")
