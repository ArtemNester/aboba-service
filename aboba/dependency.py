from config import settings
from infrastructure.broker import (
    get_kafka_consumer,
    get_kafka_producer,
)
from minio import Minio
from notification.repository import (
    BrokerRepositoryConsumer,
    BrokerRepositoryProducer,
)
from notification.service import BrokerService


def get_broker_repository_consumer() -> BrokerRepositoryConsumer:
    consumer = get_kafka_consumer()
    return BrokerRepositoryConsumer(
        consumer=consumer,
        aboba_topic=settings.ABOBA_TOPIC,
    )


def get_broker_repository_producer() -> BrokerRepositoryProducer:
    producer = get_kafka_producer()
    return BrokerRepositoryProducer(
        producer=producer,
        aboba_topic=settings.ABOBA_TOPIC,
    )


def get_broker_service() -> BrokerService:
    producer = get_broker_repository_producer()
    consumer = get_broker_repository_consumer()
    return BrokerService(
        consumer=consumer,
        producer=producer,
    )


def get_s3_client() -> Minio:
    return Minio(
        endpoint=settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE,
    )
