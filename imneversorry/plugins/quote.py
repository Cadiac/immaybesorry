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
        quotes = db.find_quotes(chat_id, quotee)
        # TODO: Wtf fix the SQL to return count, not all quotes...
        count = len(quotes)

    client.send_message(chat_id=chat_id, text=str(count) + ' quotes')


@Imneversorry.on_message(filters.chat(Imneversorry.whitelist) & filters.text & filters.command("quote"))
def user_quote_handler(client: Client, message: Message):
    chat_id = message.chat.id
    if len(message.command) == 1:
        quotes = db.find_quotes(chat_id)
    else:
        quotee = message.command[1].strip('@')
        quotes = db.find_quotes(chat_id, quotee)

    if len(quotes) == 0:
        return

    # TODO: Wtf also query for random quote at db, don't load them all
    quote = random.sample(quotes, 1)[0]

    formated_quote = '"{}" - {}'.format(*quote)
    client.send_message(chat_id=chat_id, text=formated_quote)
