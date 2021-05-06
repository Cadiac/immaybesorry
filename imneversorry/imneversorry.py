import time
import os
import logging

from pyrogram.types import Message
from pyrogram.raw.all import layer
from pyrogram.handlers import MessageHandler
from pyrogram import __version__
from pyrogram import Client, filters

from datetime import datetime
from imneversorry.config import Config

logger = logging.getLogger('imneversorry')


class Imneversorry(Client):
    whitelist = [-270475963]

    def __init__(self):
        name = self.__class__.__name__.lower()

        super().__init__(
            Config.TELEGRAM_SESSION_STR,
            api_id=Config.TELEGRAM_API_ID,
            api_hash=Config.TELEGRAM_API_HASH,
            plugins=dict(
                root=f"{name}.plugins",
                exclude=[]
            ),
            sleep_threshold=Config.SLEEP_THRESHOLD
        )

        self.admins = [Config.CREATOR_ID]
        self.uptime_reference = time.monotonic_ns()
        self.start_datetime = datetime.utcnow()

        self.set_parse_mode("markdown")
        # Ignore all bot messages and stop their propagation
        self.add_handler(MessageHandler(self.ignore_message, filters.bot))
        self.add_handler(MessageHandler(
            self.logger, filters.chat(Imneversorry.whitelist)), -1)

    async def start(self):
        await super().start()

        me = await self.get_me()
        logger.info(
            f"Imneversorry using Pyrogram v{__version__} (Layer {layer}) started on @{me.username}. hyy-vä")

    async def stop(self, *args):
        await super().stop()
        logger.info("Imneversorry stopped. tapan sut")

    def is_admin(self, message: Message) -> bool:
        user_id = message.from_user.id
        return user_id in self.admins

    def ignore_message(self, _, message: Message):
        message.stop_propagation()

    def logger(self, _, message: Message):
        user_name = message.from_user.username or (
            f"{message.from_user.first_name} {message.from_user.last_name}")
        chat_title = message.chat.title
        logger.info(
            f"[@Imneversorry] [{chat_title}] [{user_name}]: {message.text}")
        logger.debug(
            f"[@Imneversorry] [{chat_title}] [{user_name}]: {message}")
