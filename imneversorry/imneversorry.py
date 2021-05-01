import time
from datetime import datetime
import os
from configparser import ConfigParser

from pyrogram import Client, filters
from pyrogram import __version__
from pyrogram.raw.all import layer
from pyrogram.types import Message

class Imneversorry(Client):
    chats = [-270475963]

    CREATOR_ID = os.environ.get('CREATOR_ID')
    TELEGRAM_API_ID = int(os.environ.get('TELEGRAM_API_ID'))
    TELEGRAM_API_HASH = os.environ.get('TELEGRAM_API_HASH')
    TELEGRAM_USERNAME = os.environ.get('TELEGRAM_USERNAME')

    def __init__(self):
        name = self.__class__.__name__.lower()

        super().__init__(
            Imneversorry.TELEGRAM_USERNAME,
            api_id=Imneversorry.TELEGRAM_API_ID,
            api_hash=Imneversorry.TELEGRAM_API_HASH,
            workers=16,
            plugins=dict(
                root=f"{name}.plugins",
                exclude=["foobar"]
            ),
            sleep_threshold=180
        )

        self.admins = [Imneversorry.CREATOR_ID]

        self.uptime_reference = time.monotonic_ns()
        self.start_datetime = datetime.utcnow()

    async def start(self):
        await super().start()

        me = await self.get_me()
        print(f"[INFO]: Imneversorry using Pyrogram v{__version__} (Layer {layer}) started on @{me.username}. hyy-vä")

    async def stop(self, *args):
        await super().stop()
        print("[INFO]: Imneversorry stopped. tapan sut")

    def is_admin(self, message) -> bool:
        user_id = message.from_user.id
        return user_id in self.admins
