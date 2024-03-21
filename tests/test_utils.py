import unittest
from unittest.mock import MagicMock, patch

from app.utils import create_queue, create_rmq_connection


class TestUtils(unittest.TestCase):

    @patch("app.utils.pika.BlockingConnection")
    @patch("app.utils.pika.ConnectionParameters")
    @patch("app.utils.pika.PlainCredentials")
    def test_create_rmq_connection(self, mock_credentials, mock_parameters, mock_connection):
        connection_mock, channel_mock = create_rmq_connection()
        mock_connection.assert_called_once()
        self.assertIsNotNone(connection_mock)
        self.assertIsNotNone(channel_mock)

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
