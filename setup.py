from setuptools import find_packages, setup

setup(
    name="shoveler",
    version="0.1.0",
    author="Muhammad Yahya",
    author_email="muhammad.yahya@my-oli.com",
    description="This app facilitates real-time data transmission using RabbitMQ.",
    packages=find_packages(),
    install_requires=[
        "pika",
        "requests",
        "python-dotenv",
    ],
    extras_require={
        "dev": [
            "black",
            "isort",
            "bandit",
        ]
    },
)
