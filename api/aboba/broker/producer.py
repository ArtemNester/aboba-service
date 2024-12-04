from dataclasses import dataclass

import orjson
from kafka import KafkaProducer


@dataclass
class BrokerProducer:
    producer: KafkaProducer
    aboba_topic: str

    def close_connection(self) -> None:
        self.producer.close()

    def send_event(self, event_data: dict) -> None:
        encode_event_data = orjson.dumps(event_data)
        try:
            self.producer.send(topic=self.aboba_topic, value=encode_event_data)
            self.producer.flush()
        finally:
            self.close_connection()
