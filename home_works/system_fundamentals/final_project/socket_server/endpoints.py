from datetime import datetime
import logging

from util import (
    callback,
    get_mongo_client,
    send_response,
    MONGO_DB,
    MONGO_DOCUMENT_NAME,
)

logger = logging.getLogger(__name__)


@callback("send_message")
async def send_message(data: dict, socket_writer):
    message = data.get("message")
    mongo_client = await get_mongo_client()
    if not message:
        logger.error(
            "Validation error in send_message: 'message' field is missing or empty. Payload: %r",
            data,
        )
        await send_response({"message": "message is not found"}, socket_writer)
    try:
        data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        await mongo_client[MONGO_DB][MONGO_DOCUMENT_NAME].insert_one(data)
        await send_response({"message": "Message sent successfully"}, socket_writer)
    except Exception as e:
        logger.exception("Mongo insert error in send_message with payload %r", data)
        await send_response({"message": f"mongo error: {str(e)}"}, socket_writer)


@callback("find_messages")
async def find_messages(data: dict, socket_writer):
    mongo_client = await get_mongo_client()
    try:
        messages = (
            await mongo_client[MONGO_DB][MONGO_DOCUMENT_NAME]
            .find(data)
            .to_list(length=None)
        )
        messages = list(
            map(lambda x: {k: v for k, v in x.items() if k != "_id"}, messages)
        )
        logger.info(f"Mesages: {messages}")
        await send_response(messages, socket_writer)

    except Exception as e:
        logger.exception("Mongo find error in find_messages with payload %r", data)
        await send_response({"message": f"mongo error: {str(e)}"}, socket_writer)
