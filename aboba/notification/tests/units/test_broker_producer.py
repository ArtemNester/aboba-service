import unittest
from unittest.mock import (
    MagicMock,
    patch,
)

from aboba.notification.repository.producer import BrokerRepositoryProducer
from confluent_kafka import Producer


class BrokerRepositoryProducerTests(unittest.TestCase):
    def test_send_event_successfully(self):
        producer_mock = MagicMock(spec=Producer)
        event_data = {'key': 'value'}
        broker_producer = BrokerRepositoryProducer(
            producer=producer_mock,
            aboba_topic='test_topic',
        )

        broker_producer.send_event(event_data)

        producer_mock.produce.assert_called_once()
        producer_mock.flush.assert_called_once()

    @patch('builtins.print')
    def test_delivery_report_successful(self, mock_print):
        broker_producer = BrokerRepositoryProducer(
            producer=MagicMock(),
            aboba_topic='test_topic',
        )
        msg_mock = MagicMock()
        msg_mock.topic.return_value = 'test_topic'
        msg_mock.partition.return_value = 0

        broker_producer.delivery_report(None, msg_mock)

        mock_print.assert_called_once_with("Message delivered to test_topic [0]")

    @patch('builtins.print')
    def test_delivery_report_failed(self, mock_print):
        broker_producer = BrokerRepositoryProducer(
            producer=MagicMock(),
            aboba_topic='test_topic',
        )

        broker_producer.delivery_report("Error", None)

        mock_print.assert_called_once_with("Message delivery failed: Error")
