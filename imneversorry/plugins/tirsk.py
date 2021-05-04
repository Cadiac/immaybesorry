import re
import random

from pyrogram import Client, filters
from pyrogram.types import Message
from ..imneversorry import Imneversorry

tirsk = filters.create(lambda _, __, ___: random.randint(1, 10000) == 1)
rigged = filters.create(lambda _, __, ___: random.randint(1, 50) == 1)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.text & filters.regex(r"^.+\?$") & rigged)
def neuroverkko_handler(client: Client, message: Message):
    client.send_message(
        chat_id=message.chat.id,
        text=((lambda _, __: _(_, __))(
            lambda _, __: chr(__ % 256) + _(_, __ // 256) if __ else "",
            random.sample([3041605, 779117898, 17466, 272452313416, 7022364615740061032, 2360793474633670572049331836447094], 1)[0]))
    )


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.text & tirsk)
def tirsk_handler(client: Client, message: Message):
    chat_id = message.chat.id
    client.send_message(chat_id=chat_id, text=random.choice(
        ("tirsk", "Tirsk", "tirsk :D", "(tirsk)", "[tirsk]")))


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.text & filters.regex(r"\beb\S*"))
def ebin_handler(client: Client, message: Message):
    chat_id = message.chat.id
    jebin = "j" + re.search(r"\beb\S*", message.text).group(0)
    client.send_message(chat_id=chat_id, text=jebin)
