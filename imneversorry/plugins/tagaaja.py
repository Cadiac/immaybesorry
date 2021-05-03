import re
import random
import operator

from pyrogram import Client, filters
from pyrogram.types import Message
from ..imneversorry import Imneversorry
from ..utils import db


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.text & filters.command("tag"))
def add_tag_handler(client: Client, message: Message):
    chat_id = message.chat.id

    if len(message.command) < 3:
        client.send_message(chat_id=chat_id, text='Usage: /tag <asia> <tagi>')
        return

    target = message.command[1].strip('@')
    tag = message.command[2]
    db.upsert_tag(tag, target, chat_id, message.from_user.username)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.text & filters.command("tagged"))
def tagged_search_handler(client: Client, message: Message):
    chat_id = message.chat.id

    if len(message.command) < 2:
        client.send_message(chat_id=chat_id, text='Usage: /tagged <tagi>')
        return

    tag = message.command[1]
    tagged_rows = db.find_tagged(tag, chat_id)
    tagged = [row[0] for row in tagged_rows]

    client.send_message(chat_id=chat_id,
                        text=f'Tagged as "{tag}": {", ".join(tagged)}')


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.text & filters.command("tags"))
def tag_target_search_handler(client: Client, message: Message):
    chat_id = message.chat.id

    if len(message.command) < 2:
        client.send_message(chat_id=chat_id, text='Usage: /tags <asia>')
        return

    target = message.command[1].strip('@')
    tags_rows = db.find_target_tags(target, chat_id)
    tags = [row[0] for row in tags_rows]

    client.send_message(chat_id=chat_id,
                        text=f'"{target}": {", ".join(tags)}')
