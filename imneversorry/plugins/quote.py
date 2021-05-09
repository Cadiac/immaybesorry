import random

from pyrogram import Client, filters
from pyrogram.types import Message
from ..imneversorry import Imneversorry
from ..utils import db


@Imneversorry.on_message(filters.chat(Imneversorry.whitelist) & filters.text & filters.command("addq"))
def add_quote_handler(client: Client, message: Message):
    chat_id = message.chat.id
    if len(message.command) < 3:
        client.sendMessage(
            chat_id=chat_id, text='Usage: /addq <quotee> <quote>')
    else:
        quotee = message.command[1].strip('@')
        quote = ' '.join(message.command[2:])
        if quote[0] == '"' and quote[len(quote) - 1] == '"':
            quote = quote[1:len(quote) - 1]
        db.insert_quote(quote, quotee, chat_id, message.from_user.username)


@Imneversorry.on_message(filters.chat(Imneversorry.whitelist) & filters.text & filters.command("quotes"))
def quotes_count_handler(client: Client, message: Message):
    chat_id = message.chat.id
    if len(message.command) == 1:
        count = db.count_quotes(chat_id)
    else:
        quotee = message.command[1].strip('@')
        count = db.count_quotes(chat_id, quotee)

    client.send_message(chat_id=chat_id, text=f"{count} quotes")


@Imneversorry.on_message(filters.chat(Imneversorry.whitelist) & filters.text & filters.command("quote"))
def user_quote_handler(client: Client, message: Message):
    chat_id = message.chat.id
    if len(message.command) == 1:
        quote = db.random_quote(chat_id)
    else:
        quotee = message.command[1].strip('@')
        quote = db.random_quote(chat_id, quotee)

    if quote is None:
        return

    formated_quote = '"{}" - {}'.format(*quote)
    client.send_message(chat_id=chat_id, text=formated_quote)
