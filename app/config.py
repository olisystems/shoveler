import os

from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT = os.getenv("API_ENDPOINT")
API_USER = os.getenv("API_USER")
API_PASS = os.getenv("API_PASS")

RMQ_SERVER_IP = os.getenv("RMQ_SERVER_IP")
RMQ_PORT = os.getenv("RMQ_PORT")
RMQ_VHOST = os.getenv("RMQ_VHOST")
RMQ_USER = os.getenv("RMQ_USER")
RMQ_PASS = os.getenv("RMQ_PASS")
RMQ_QUEUE_NAME = os.getenv("RMQ_QUEUE_NAME")

MAX_RETRIES = 5
CONNECTION_RETRY_DELAY = 3
