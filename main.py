import sys

from app.data_transmitter import DataTransmitter
from app.logger import get_logger

logger = get_logger(__name__)


def main():
    """
    Main entry point of the application.
    """
    try:
        transmitter = DataTransmitter()
        transmitter.run()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
