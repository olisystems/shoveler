import json
import logging
from datetime import datetime

import pika

from .config import RMQ_PASS, RMQ_PORT, RMQ_SERVER_IP, RMQ_USER, RMQ_VHOST

logger = logging.getLogger(__name__)


def create_rmq_connection():
    """
    Function to create a connection with the RabbitMQ server.
    """
    credentials = pika.PlainCredentials(RMQ_USER, RMQ_PASS)
    parameters = pika.ConnectionParameters(
        RMQ_SERVER_IP, RMQ_PORT, RMQ_VHOST, credentials=credentials
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    return connection, channel


def create_queue(queue_name):
    """
    Function to create a connection with the RabbitMQ server and declare a queue.
    """
    try:
        connection, channel = create_rmq_connection()

        channel.queue_declare(queue=queue_name, durable=True, arguments={"x-queue-type": "classic"})

        connection.close()

    except Exception as e:
        logger.error(f"Queue creation failed due to an error: {e}")


def add_timestamp_to_payload(payload_str):
    """
    Add a timestamp to the payload string.
    """
    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        return payload_str

    updated_payload = {"timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")}

    updated_payload.update(payload)

    updated_payload_str = json.dumps(updated_payload)
    return updated_payload_str
