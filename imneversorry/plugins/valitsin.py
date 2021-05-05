import random
import re
import datetime
import json
import hashlib

from pyrogram import Client, filters
from pyrogram.types import Message
from ..imneversorry import Imneversorry

vai_filter = filters.create(lambda _, __, update: set(
    update.text.lower().split()[1::2]) == {'vai'})


@Imneversorry.on_message(filters.chat(Imneversorry.whitelist) & filters.text & vai_filter)
def vai_handler(client: Client, message: Message):
    now = datetime.datetime.now()
    alternatives = message.text.split()[::2]
    data = [
        message.from_user.id,
        now.day,
        now.month,
        now.year,
        alternatives
    ]
    seed = hashlib.md5(json.dumps(
        data, sort_keys=True).encode('utf-8')).hexdigest()
    rigged = random.Random(seed)
    if rigged.randint(0, 49) == 0:
        if (len(alternatives) > 2):
            answers = ['Kaikki :D', 'Ei mitään >:(']
        else:
            answers = ['Molemmat :D', 'Ei kumpaakaan >:(']
        client.send_message(chat_id=message.chat.id,
                            text=rigged.choice(answers))
    else:
        client.send_message(chat_id=message.chat.id,
                            text=rigged.choice(alternatives))


@Imneversorry.on_message(filters.chat(Imneversorry.whitelist) & filters.regex("^onko pakko .+$", re.IGNORECASE))
def onko_pakko_handler(client: Client, message: Message):
    now = datetime.datetime.now()

    groups = re.match(r"^onko pakko ([^?]+)(\??)$",
                      message.text.lower(), re.IGNORECASE)
    data = [
        message.from_user.id, +
        now.day,
        now.month,
        now.year,
        groups.group(1)
    ]
    seed = hashlib.md5(json.dumps(
        data, sort_keys=True).encode('utf-8')).hexdigest()
    rigged = random.Random(seed)
    if rigged.randint(0, 1) == 0:
        client.send_message(chat_id=message.chat.id,
                            text='ei ole pakko {}'.format(groups.group(1)))
    else:
        client.send_message(chat_id=message.chat.id,
                            text='on pakko {}'.format(groups.group(1)))
