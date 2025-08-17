import json
from pathlib import Path
import socket

import yaml
from pymongo import AsyncMongoClient

MONGO_DB = "dummy_messages"
MONGO_DOCUMENT_NAME = "messages"
_callbacks: dict = {}


def get_callback(key: str):
    return _callbacks.get(key)


def callback(key: str):
    def decorator(func):
        _callbacks[key] = func
        return func

    return decorator


async def get_mongo_client():
    with Path(__file__).parent.joinpath("config.yaml").open("r") as file:
        config = yaml.safe_load(file)
        try:
            docker_host = socket.gethostbyname(config["docker_host"])
        except socket.gaierror:
            docker_host = None

        host = config["docker_host"] if docker_host else "127.0.0.1"
        port = config["docker_port"]
        return AsyncMongoClient(host, port)


async def send_response(response: dict | list[dict], socket_writer):
    byte_response = json.dumps(response).encode()
    socket_writer.write(byte_response)
    await socket_writer.drain()
