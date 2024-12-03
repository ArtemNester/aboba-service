from dataclasses import dataclass

from kafka import KafkaConsumer


@dataclass
class BrokerConsumer:
    consumer: KafkaConsumer
    aboba_topic: str

    def open_connection(self) -> None:
        self.consumer.subscribe([self.aboba_topic])

    def close_connection(self) -> None:
        self.consumer.close()

    def consume_callback_message(self) -> None:
        self.open_connection()
        try:
            for message in self.consumer:
                print(message.value)
        finally:
            self.close_connection()
