import re
import logging
from pyrogram import Client, filters
from pyrogram.types import Message

from ..imneversorry import Imneversorry

# Enable pyrogram logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z"
)

logger = logging.getLogger('imneversorry')


# TODO: how to make this only act as a middleware, not handler?
@Imneversorry.on_message(filters.chat(Imneversorry.whitelist))
def whitelisted_chats_logger(_, message: Message):
    user_name = message.from_user.username or (
        f"{message.from_user.first_name} {message.from_user.last_name}")
    chat_title = message.chat.title
    logger.info(f"[@Imneversorry] [{chat_title}] [{user_name}]: {message}")
