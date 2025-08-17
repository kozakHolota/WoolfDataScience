import asyncio
import json
import string
import logging
import sys

from util import get_callback, send_response
import endpoints  # Імпорт для реєстрації callback-ів під час старту процесу

# Налаштування логування у stdout, щоб все було видно в docker logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    datefmt="%-Y-%m-%d %H:%M:%S" if sys.platform != "win32" else "%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)
logger = logging.getLogger(__name__)


class ClientConnectionHandler:
    """A class representing a client connection to the server."""

    async def read_loop(self):
        """Read messages up to \n and handle them."""
        not_found_message = {"message": "Not found"}
        invalid_json_message = {"message": "Invalid JSON: $message"}
        try:
            while True:
                msg = await self.reader.readline()
                if not msg:
                    logger.info(
                        "Client %s disconnected (EOF)", getattr(self, "addr", "unknown")
                    )
                    break
                text = msg.decode("utf-8", errors="replace").rstrip("\r\n")
                try:
                    data = json.loads(text)
                except json.JSONDecodeError:
                    message_text = string.Template(
                        invalid_json_message["message"]
                    ).substitute({"message": text[:200]})
                    logger.error(
                        "Invalid JSON from %s: %s",
                        getattr(self, "addr", "unknown"),
                        text[:200],
                    )
                    self.writer.write(json.dumps({"message": message_text}).encode())
                    await self.writer.drain()
                    continue

                request = data.get("request")
                send_data = data.get("data")

                if request is None:
                    logger.warning(
                        "Missing 'request' field from %s: %s",
                        getattr(self, "addr", "unknown"),
                        text[:200],
                    )
                    self.writer.write(json.dumps(not_found_message).encode())
                    await self.writer.drain()
                else:
                    callback = get_callback(request)
                    if callback is None:
                        logger.warning(
                            "No callback found for request '%s' from %s",
                            request,
                            getattr(self, "addr", "unknown"),
                        )
                        await send_response(
                            {"message": not_found_message["message"]}, self.writer
                        )
                    else:
                        try:
                            await callback(send_data, self.writer)
                        except Exception:
                            logger.exception(
                                "Error in callback for request '%s' from %s",
                                request,
                                getattr(self, "addr", "unknown"),
                            )
                            await send_response(
                                {"message": "Internal server error"}, self.writer
                            )

        except (
            ConnectionResetError,
            asyncio.CancelledError,
            asyncio.IncompleteReadError,
        ) as e:
            logger.info(
                "Connection closed for %s: %s",
                getattr(self, "addr", "unknown"),
                repr(e),
            )

    async def callback(self, reader, writer):
        """The underlying connection handler callback used when a new
        client connects to the server.
        """
        self.reader = reader
        self.writer = writer

        addr = self.writer.get_extra_info("peername")
        self.addr = addr
        logger.info("Client connected: %s", addr)
        try:
            await self.read_loop()
        finally:
            try:
                self.writer.close()
                await self.writer.wait_closed()
                logger.info("Connection closed: %s", addr)
            except Exception:
                logger.exception("Error while closing connection: %s", addr)


class Server:
    def __init__(self, host: str = "0.0.0.0", port: int = 5001):
        self.host = host
        self.port = port

    async def run(self):
        server = await asyncio.start_server(
            # Create a fresh handler instance per connection:
            client_connected_cb=lambda r, w: ClientConnectionHandler().callback(r, w),
            host=self.host,
            port=self.port,
        )
        addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
        print(f"Serving on {addrs}")
        await server.serve_forever()


if __name__ == "__main__":
    server = Server()
    asyncio.run(server.run())
