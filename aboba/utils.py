import logging
from typing import BinaryIO

from dependency import (
    get_broker_service,
    get_s3_client,
)


def send_event_to_broker(event_data: dict) -> None:
    try:
        broker_service = get_broker_service()

        logging.debug(f'Received stargazer data: {event_data}')

        broker_service.process_event(event_data=event_data)
    except Exception as e:
        logging.error(f'Kafcon error: {e}')
        raise


def upload_media_to_s3(
    bucket_name: str,
    file_key: str,
    file: BinaryIO,
    file_size: int,
) -> None:
    try:
        s3_client = get_s3_client()
        s3_client.put_object(
            bucket_name=bucket_name,
            object_name=file_key,
            data=file,
            length=file_size,
        )
    except Exception as e:
        logging.error(f'S3Con error: {e}')
        raise
