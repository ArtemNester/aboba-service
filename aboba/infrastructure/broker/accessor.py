from config import settings
from confluent_kafka import (
    Consumer,
    Producer,
)


def get_kafka_producer() -> Producer:
    return Producer({'bootstrap.servers': settings.BROKER_URL})


def get_kafka_consumer() -> Consumer:
    return Consumer(
        {
            'bootstrap.servers': settings.BROKER_URL,
            'group.id': settings.GROUP_ID,
            'auto.offset.reset': 'earliest',
        },
    )
