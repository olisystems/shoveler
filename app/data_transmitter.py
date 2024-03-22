import time

import pika
import requests
from requests.exceptions import RequestException

from .config import API_ENDPOINT, API_PASS, API_USER, RMQ_QUEUE_NAME
from .logger import get_logger
from .utils import add_timestamp_to_payload, create_rmq_connection


class DataTransmitter:
    def __init__(self):
        """
        Initializes the DataTransmitter instance, creating a RabbitMQ connection and setting up logging.
        """
        self.logger = get_logger(__name__)
        self.connection, self.channel = create_rmq_connection()
        self.queue_name = RMQ_QUEUE_NAME

    def fetch_data(self):
        """
        Fetches data from the API endpoint using HTTP GET.
        Returns the response text on success, or None on failure.
        """
        try:
            response = requests.get(API_ENDPOINT, auth=(API_USER, API_PASS))
            if response.status_code == 200:
                self.logger.info(f"Successfully retrieved data from {API_ENDPOINT}")
                return response.text
            else:
                self.logger.error(
                    f"Request to {API_ENDPOINT} failed with status code {response.status_code}"
                )
                return None
        except RequestException as e:
            self.logger.error(f"Request to {API_ENDPOINT} failed due to an error: {e}")
            return None

    def transmit_data(self, data):
        """
        Sends the data to a specified RabbitMQ queue.
        Logs the outcome of the operation.
        """
        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=self.queue_name,
                body=data,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )
            self.logger.info(f"Sent: {data}")
        except Exception as e:
            self.logger.error(f"Data transmission failed due to an error: {e}")

    def run(self):
        """
        Continuously fetches data and transmits it using the RabbitMQ channel.
        Waits for 60 seconds between each operation.
        """
        while True:
            data = self.fetch_data()
            if data:
                self.transmit_data(add_timestamp_to_payload(data))
            time.sleep(60)
