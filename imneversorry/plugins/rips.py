import re
import random

from pyrogram import Client, filters
from pyrogram.types import Message
from ..utils import db
from ..imneversorry import Imneversorry

rips = db.read_rips()
waiting_rip = {}


def is_newrip_or_delrip(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    key = str(user_id) + str(chat_id)
    if key in waiting_rip:
        return True
    else:
        return message.caption is not None and ("newrip" in message.caption or "delrip" in message.caption)


def save_rip(client: Client, chat_id: int, user_id: int, type: str, data: str):
    if chat_id not in rips:
        rips[chat_id] = set()
    elif (type, data) in rips[chat_id]:
        client.send_message(chat_id=chat_id, text="Already in rips")
    else:
        rips[chat_id].add((type, data))
        db.add_rip(type, data, chat_id, user_id)


def remove_rip(client: Client, chat_id: int, type: str, data: str):
    if chat_id not in rips:
        rips[chat_id] = set()
        client.send_message(chat_id=chat_id, text="Couldn't find rip")
    elif (type, data) not in rips[chat_id]:
        client.send_message(chat_id=chat_id, text="Couldn't find rip")
    else:
        rips[chat_id].remove((type, data))
        db.del_rip((type, data))


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("newrip") & filters.text)
def newrip_handler(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if len(message.command) == 1:
        key = str(user_id) + str(chat_id)
        waiting_rip[key] = "newrip"
        client.send_message(
            chat_id=chat_id, text="Usage: /newrip <ripmessage> or send mediafile for newrip")
        return

    type = "text"
    data = " ".join(message.command[1:])

    save_rip(client, chat_id, user_id, type, data)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("delrip") & filters.text)
def delrip_handler(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if len(message.command) == 1:
        key = str(user_id) + str(chat_id)
        waiting_rip[key] = "delrip"
        client.send_message(
            chat_id=chat_id, text="Usage: /delrip <ripname> or forward mediafile for delete")
        return

    type = "text"
    data = " ".join(message.command[1:])

    remove_rip(client, chat_id, type, data)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("rips"))
def rips_count_handler(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id not in rips:
        rips[chat_id] = set()
    client.send_message(chat_id=chat_id, text=f"{len(rips[chat_id])} rips")


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & ~filters.text)
def waiting_rip_handler(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if is_newrip_or_delrip(message):
        if message.photo is not None:
            rip = "photo", message.photo.file_id
        elif message.document is not None:
            rip = "document", message.document.file_id
        elif message.voice is not None:
            rip = "voice", message.voice.file_id
        elif message.location is not None:
            rip = "location", (str(message.location.longitude) +
                               ',' + str(message.location.latitude))
        elif message.video is not None:
            rip = "video", message.video.file_id
        elif message.audio is not None:
            rip = "audio", message.audio.file_id
        elif message.sticker is not None:
            rip = "sticker", message.sticker.file_id
        elif message.animation is not None:
            rip = "animation", message.animation.file_id
        elif message.video_note is not None:
            rip = "video_note", message.video_note.file_id
        else:
            # Text messages are handled by the newrip_handler
            return

        key = str(user_id) + str(chat_id)
        type, data = rip

        if key in waiting_rip:
            if waiting_rip[key] == "newrip":
                save_rip(client, chat_id, user_id, type, data)

            elif waiting_rip[key] == "delrip":
                remove_rip(client, chat_id, type, data)

            waiting_rip.pop(key)

        elif message.caption is not None:
            if "newrip" in message.caption:
                save_rip(client, chat_id, user_id, type, data)

            elif "delrip" in message.caption:
                remove_rip(client, chat_id, type, data)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex("rip", re.IGNORECASE))
def rip_handler(client: Client, message: Message):
    chat_id = message.chat.id

    if chat_id not in rips:
        rips[chat_id] = set()

    if len(rips[chat_id]) == 0:
        client.send_message(chat_id=chat_id, text="rip in pepperoni")
        return

    type, data = random.sample(rips[chat_id], 1)[0]

    if type == "text":
        client.send_message(chat_id=chat_id, text=f"rip in {data}")
    elif type == "photo":
        client.send_photo(chat_id=chat_id, photo=data, caption="rip in")
    elif type == "voice":
        client.send_voice(chat_id=chat_id, voice=data, caption='rip in')
    elif type == "video":
        client.send_video(chat_id=chat_id, video=data, caption='rip in')
    elif type == "audio":
        client.send_audio(chat_id=chat_id, audio=data, caption='rip in')
    elif type == "document":
        client.send_document(chat_id=chat_id, document=data, caption='rip in')
    elif type == "animation":
        client.send_animation(
            chat_id=chat_id, animation=data, caption='rip in')
    elif type == "location":
        loc = data.split(',')
        client.send_message(chat_id=chat_id, text="rip in")
        client.send_location(chat_id=chat_id, longitude=float(
            loc[0]), latitude=float(loc[1]))
    elif type == "sticker":
        client.send_message(chat_id=chat_id, text="rip in")
        client.send_sticker(chat_id=chat_id, sticker=data)
    elif type == "video_note":
        client.send_message(chat_id=chat_id, text="rip in")
        client.send_video_note(chat_id=chat_id, video_note=data)
    else:
        print(f"[ERROR]: riptype {type} not supported, pls fix")
