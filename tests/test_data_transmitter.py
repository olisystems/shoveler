import unittest
from unittest.mock import MagicMock, patch

from app.data_transmitter import DataTransmitter


class TestDataTransmitter(unittest.TestCase):

    @patch("app.data_transmitter.requests.get")
    @patch("app.data_transmitter.create_rmq_connection")
    def test_fetch_data_success(self, mock_create_rmq_connection, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "test data"
        mock_get.return_value = mock_response

        mock_conn = MagicMock()
        mock_channel = MagicMock()
        mock_create_rmq_connection.return_value = (mock_conn, mock_channel)

        transmitter = DataTransmitter()
        result = transmitter.fetch_data()
        self.assertEqual(result, "test data")

    @patch("app.data_transmitter.requests.get")
    @patch("app.data_transmitter.create_rmq_connection")
    def test_fetch_data_failure(self, mock_create_rmq_connection, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        mock_conn = MagicMock()
        mock_channel = MagicMock()
        mock_create_rmq_connection.return_value = (mock_conn, mock_channel)

        transmitter = DataTransmitter()
        result = transmitter.fetch_data()
        self.assertIsNone(result)

    @patch("app.data_transmitter.pika")
    @patch("app.data_transmitter.create_rmq_connection")
    def test_transmit_data(self, mock_create_rmq_connection, mock_pika):
        mock_conn = MagicMock()
        mock_channel = MagicMock()
        mock_create_rmq_connection.return_value = (mock_conn, mock_channel)

        transmitter = DataTransmitter()
        transmitter.transmit_data("test data")
        mock_channel.basic_publish.assert_called_once()
