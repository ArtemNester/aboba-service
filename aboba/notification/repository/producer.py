from dataclasses import dataclass

import orjson
from confluent_kafka import Producer


@dataclass
class BrokerRepositoryProducer:
    producer: Producer
    aboba_topic: str

    def send_event(self, event_data: dict) -> None:
        encoded_event_data = orjson.dumps(event_data)
        try:
            self.producer.produce(
                topic=self.aboba_topic,
                value=encoded_event_data,
                callback=self.delivery_report,
            )
            self.producer.flush()
        except Exception as e:
            print(f"Failed to send event: {e}")

    def delivery_report(self, err, msg):
        """
        Callback, вызывается после отправки сообщения.
        """
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
