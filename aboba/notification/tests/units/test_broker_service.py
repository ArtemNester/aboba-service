import unittest
from unittest.mock import patch

from aboba.notification.service import BrokerService


class BrokerServiceTests(unittest.TestCase):
    @patch('aboba.notification.service.BrokerRepositoryConsumer')
    @patch('aboba.notification.service.BrokerRepositoryProducer')
    def consumes_event_successfully(self, mock_producer, mock_consumer):
        consumer_instance = mock_consumer.return_value
        producer_instance = mock_producer.return_value
        consumer_instance.consume_messages.return_value = [b'{"key": "value"}']
        service = BrokerService(consumer=consumer_instance, producer=producer_instance)

        service.consume_event()

        consumer_instance.open_connection.assert_called_once()
        consumer_instance.close_connection.assert_called_once()

    @patch('aboba.notification.service.BrokerRepositoryConsumer')
    @patch('aboba.notification.service.BrokerRepositoryProducer')
    def handles_consume_event_exception(self, mock_producer, mock_consumer):
        consumer_instance = mock_consumer.return_value
        producer_instance = mock_producer.return_value
        consumer_instance.consume_messages.side_effect = Exception("Test exception")
        service = BrokerService(consumer=consumer_instance, producer=producer_instance)

        service.consume_event()

        consumer_instance.open_connection.assert_called_once()
        consumer_instance.close_connection.assert_called_once()

    @patch('aboba.notification.service.BrokerRepositoryConsumer')
    @patch('aboba.notification.service.BrokerRepositoryProducer')
    def processes_event_successfully(self, mock_producer, mock_consumer):
        consumer_instance = mock_consumer.return_value
        producer_instance = mock_producer.return_value
        service = BrokerService(consumer=consumer_instance, producer=producer_instance)
        event_data = {"key": "value"}

        service.process_event(event_data)

        producer_instance.send_event.assert_called_once_with(event_data=event_data)

    @patch('aboba.notification.service.BrokerRepositoryConsumer')
    @patch('aboba.notification.service.BrokerRepositoryProducer')
    def handles_send_event_exception(self, mock_producer, mock_consumer):
        consumer_instance = mock_consumer.return_value
        producer_instance = mock_producer.return_value
        producer_instance.send_event.side_effect = Exception("Test exception")
        service = BrokerService(consumer=consumer_instance, producer=producer_instance)
        event_data = {"key": "value"}

        service._send_event(event_data)

        producer_instance.send_event.assert_called_once_with(event_data=event_data)
