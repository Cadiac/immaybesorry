import re
import random
import sqlite3 as sq

from pyrogram import Client, filters, emoji
from pyrogram.types import Message
from ..utils import db
from ..imneversorry import Imneversorry

rips = db.readRips()
waiting_rip = {}

def isNewRip(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    key = str(user_id) + str(chat_id)
    if key in waiting_rip:
        return True
    else:
        return message.caption is not None and ('newrip' in message.caption or 'delrip' in message.caption)

def saveRip(client: Client, chat_id: int, user_id: int, type: str, data: str):
    if chat_id not in rips:
        rips[chat_id] = set()
    elif (type, data) in rips[chat_id]:
        client.send_message(chat_id=chat_id, text='Already in rips')
    else:
        rips[chat_id].add((type, data))
        db.addRip(type, data, chat_id, user_id)

def removeRip(client: Client, chat_id: int, type: str, data: str):
    if chat_id not in rips:
        rips[chat_id] = set()
        client.send_message(chat_id=chat_id, text="Couldn't find rip")
    elif (type, data) not in rips[chat_id]:
        client.send_message(chat_id=chat_id, text="Couldn't find rip")
    else:
        rips[chat_id].remove((type, data))
        db.delRip((type, data))


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("newrip"))
def newripHandler(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if len(message.command) == 1:
        key = str(user_id) + str(chat_id)
        waiting_rip[key] = 'newrip'
        client.send_message(chat_id=chat_id, text='Usage: /newrip <ripmessage> or send mediafile for newrip')
        return

    type = 'text'
    data = ' '.join(message.command[1:])

    saveRip(client, chat_id, user_id, type, data)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("delrip"))
def delripHandler(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if len(message.command) == 1:
        key = str(user_id) + str(chat_id)
        waiting_rip[key] = 'delrip'
        client.send_message(chat_id=chat_id, text='Usage: /delrip <ripname> or forward mediafile for delete')
        return

    type = 'text'
    data = ' '.join(message.command[1:])

    removeRip(client, chat_id, type, data)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("rips"))
def ripsCountHandler(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id not in rips:
        rips[chat_id] = set()
    client.send_message(chat_id=chat_id, text=f"{len(rips[chat_id])} rips")


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex("rip", re.IGNORECASE))
def ripHandler(client: Client, message: Message):
    chat_id = message.chat.id

    if chat_id not in rips:
        rips[chat_id] = set()

    if len(rips[chat_id]) == 0:
        client.send_message(chat_id=chat_id, text="rip in pepperoni")
        return

    riptype, rip = random.sample(rips[chat_id], 1)[0]

    if riptype == 'text':
        client.send_message(chat_id=chat_id, text=f"rip in {rip}")
    else:
        print("riptype not implemented")

@Imneversorry.on_message(filters.chat(Imneversorry.chats))
def messageHandler(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if isNewRip(message):
        if message.photo is not None:
            rip = 'photo', message.photo.file_id
        elif message.document is not None:
            rip = 'document', message.document.file_id
        elif message.voice is not None:
            rip = 'voice', message.voice.file_id
        elif message.location is not None:
            rip = 'location', (str(message.location.longitude) +
                               ',' + str(message.location.latitude))
        elif message.video is not None:
            rip = 'video', message.video.file_id
        elif message.audio is not None:
            rip = 'audio', message.audio.file_id
        else:
            rip = None

        key = str(user_id) + str(chat_id)

        if key in waiting_rip:
            if rip is not None:
                type, data = rip

                if waiting_rip[key] == 'newrip':
                    saveRip(client, chat_id, user_id, type, data)

                elif waiting_rip[key] == 'delrip':
                    removeRip(client, chat_id, type, data)

            waiting_rip.pop(key)

        if message.caption is not None:
            type, data = rip

            if 'newrip' in message.caption:
                saveRip(client, chat_id, user_id, type, data)

            elif 'delrip' in message.caption:
                removeRip(client, chat_id, type, data)
