import unittest
from unittest.mock import (
    MagicMock,
    patch,
)

from aboba.notification.repository.consumer import BrokerRepositoryConsumer
from confluent_kafka import Consumer


class BrokerRepositoryConsumerTests(unittest.TestCase):
    def test_open_connection_subscribes_to_topic(self):
        consumer_mock = MagicMock(spec=Consumer)
        broker_consumer = BrokerRepositoryConsumer(
            consumer=consumer_mock,
            aboba_topic='test_topic',
        )

        broker_consumer.open_connection()

        consumer_mock.subscribe.assert_called_once_with(['test_topic'])

    def test_close_connection_closes_consumer(self):
        consumer_mock = MagicMock(spec=Consumer)
        broker_consumer = BrokerRepositoryConsumer(
            consumer=consumer_mock,
            aboba_topic='test_topic',
        )

        broker_consumer.close_connection()

        consumer_mock.close.assert_called_once()

    @patch('builtins.print')
    def test_consume_messages_yields_messages(self, mock_print):
        consumer_mock = MagicMock(spec=Consumer)
        msg_mock = MagicMock()
        msg_mock.value.return_value = b'test_message'
        consumer_mock.poll.side_effect = [msg_mock, None, KeyboardInterrupt]
        broker_consumer = BrokerRepositoryConsumer(
            consumer=consumer_mock,
            aboba_topic='test_topic',
        )

        messages = list(broker_consumer.consume_messages())

        self.assertEqual(messages, [b'test_message'])
        mock_print.assert_not_called()

    @patch('builtins.print')
    def test_consume_messages_handles_errors(self, mock_print):
        consumer_mock = MagicMock(spec=Consumer)
        error_mock = MagicMock()
        error_mock.error.return_value = 'Error'
        consumer_mock.poll.side_effect = [error_mock, None, KeyboardInterrupt]
        broker_consumer = BrokerRepositoryConsumer(
            consumer=consumer_mock,
            aboba_topic='test_topic',
        )

        messages = list(broker_consumer.consume_messages())

        self.assertEqual(messages, [])
        mock_print.assert_called_once_with("Consumer error: Error")
