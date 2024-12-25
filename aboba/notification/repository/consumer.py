from dataclasses import dataclass

from confluent_kafka import Consumer


@dataclass
class BrokerRepositoryConsumer:
    consumer: Consumer
    aboba_topic: str

    def open_connection(self) -> None:
        self.consumer.subscribe([self.aboba_topic])

    def close_connection(self) -> None:
        self.consumer.close()

    def consume_messages(self):
        """
        Метод для обработки сообщений из Kafka.
        """
        while True:
            msg = self.consumer.poll(timeout=1.0)  # Ждем сообщения
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            yield msg.value()
