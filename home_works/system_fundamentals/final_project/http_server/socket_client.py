import asyncio
import json
import socket

import yaml


class SocketClient:
    def __init__(self):
        config = yaml.safe_load(open("config.yaml"))
        try:
            docker_host = socket.gethostbyname(config["docker_host"])
        except socket.gaierror:
            docker_host = None

        self.host = config["docker_host"] if docker_host else "127.0.0.1"
        self.port = config["docker_port"]
        self.reader = None
        self.writer = None

    async def connect(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        self.reader = reader
        self.writer = writer

    async def send_request(self, request: dict):
        if not (self.writer or self.reader):
            await self.connect()
        byte_request = json.dumps(request).encode() + b"\n"
        self.writer.write(byte_request)
        await self.writer.drain()
        response = await self.reader.read(1024)
        return response.decode()
