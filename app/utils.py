import json
import logging
import time
from datetime import datetime

import pika

from .config import (
    CONNECTION_RETRY_DELAY,
    MAX_RETRIES,
    RMQ_PASS,
    RMQ_PORT,
    RMQ_SERVER_IP,
    RMQ_USER,
    RMQ_VHOST,
)

logger = logging.getLogger(__name__)


def create_rmq_connection(retries=0):
    """
    Function to create a connection with the RabbitMQ server.
    """

    if retries > MAX_RETRIES:
        raise Exception("Maximum number of retries exceeded")

    credentials = pika.PlainCredentials(RMQ_USER, RMQ_PASS)
    parameters = pika.ConnectionParameters(
        RMQ_SERVER_IP, RMQ_PORT, RMQ_VHOST, credentials=credentials
    )

    try:

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        return connection, channel
    except pika.exceptions.AMQPConnectionError:
        time.sleep(CONNECTION_RETRY_DELAY)
        return create_rmq_connection(retries + 1)

    except Exception:
        raise


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
