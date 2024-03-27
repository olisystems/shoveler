# Shoveler

This Python application facilitates real-time data transmission using `RabbitMQ`. It includes modules for data retrieval, transmission, configuration management, logging, utility functions, and testing.

- The `config.py` module manages application settings, including API credentials and `RabbitMQ` connection parameters.
- Data is fetched from the `API` endpoint using `data_fetch.py` and published to `RabbitMQ` using `data_publish.py`.
- Logging is configured with different levels and formats, and logs are stored in `app.log`.
- Common functions for managing `RabbitMQ` queues and connections are stored in `utils.py`.

## Setup and Installation

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Update the `.env` file with your specific configuration. Here is a sample `.env` file:
```
API_ENDPOINT=http://your_api_endpoint
API_USER=your_api_user
API_PASS=your_api_password

RMQ_SERVER_IP=your_rabbitmq_server_ip
RMQ_PORT=your_rabbitmq_port
RMQ_VHOST=your_rabbitmq_vhost
RMQ_USER=your_rabbitmq_username
RMQ_PASS=your_rabbitmq_password

RMQ_QUEUE_NAME=your_queue_name
```
4. Run the application with `python main.py`.
5. Run the tests with `python -m unittest discover -s tests`.
