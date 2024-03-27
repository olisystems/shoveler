import json
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from app.utils import add_timestamp_to_payload, create_queue, create_rmq_connection, pika


class TestUtils(unittest.TestCase):
    @patch("pika.BlockingConnection")
    @patch("pika.ConnectionParameters")
    @patch("pika.PlainCredentials")
    def test_create_rmq_connection(self, mock_credentials, mock_parameters, mock_connection):
        connection_mock, channel_mock = create_rmq_connection()
        mock_connection.assert_called_once()
        self.assertIsNotNone(connection_mock)
        self.assertIsNotNone(channel_mock)

    @patch("pika.BlockingConnection")
    @patch("time.sleep")
    def test_connection_retry(self, mock_sleep, mock_blocking_connection):
        mock_blocking_connection.side_effect = [pika.exceptions.AMQPConnectionError] * 5 + [
            MagicMock()
        ]

        connection, channel = create_rmq_connection()

        self.assertEqual(mock_blocking_connection.call_count, 6)
        self.assertEqual(mock_sleep.call_count, 5)

    def test_max_retries_exceeded(self):
        with self.assertRaises(Exception):
            create_rmq_connection(retries=10)

    @patch("app.utils.create_rmq_connection")
    @patch("app.utils.logger")
    def test_create_queue(self, mock_logger, mock_create_connection):
        connection_mock = MagicMock()
        channel_mock = MagicMock()
        mock_create_connection.return_value = (connection_mock, channel_mock)
        create_queue("test_queue")
        channel_mock.queue_declare.assert_called_once_with(
            queue="test_queue", durable=True, arguments={"x-queue-type": "classic"}
        )


class TestAddTimestampToPayload(unittest.TestCase):

    def test_add_timestamp_to_payload(self):
        payload_str = '{"name":"b","type":"INTEGER","c":"RO","text":"","x":"W","value":0}'
        updated_payload_str = add_timestamp_to_payload(payload_str)

        self.assertTrue(updated_payload_str)

        try:
            updated_payload = json.loads(updated_payload_str)
        except json.JSONDecodeError:
            self.fail("Updated payload string is not valid JSON")

        current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.assertEqual(updated_payload["timestamp"], current_timestamp)

        expected_payload = json.loads(payload_str)

        del updated_payload["timestamp"]

        self.assertDictEqual(updated_payload, expected_payload)
