import re
import random
import logging

from pyrogram import Client, filters
from pyrogram.types import Message
from ..utils import db
from ..imneversorry import Imneversorry

rips = db.read_rips()
waiting_rip = {}

logger = logging.getLogger('imneversorry')


def is_newrip_or_delrip(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    key = str(user_id) + str(chat_id)
    if key in waiting_rip:
        return True
    else:
        return message.caption is not None and ("newrip" in message.caption or "delrip" in message.caption)


def save_rip(client: Client, chat_id: int, user_id: int, type: str, rip: str, message_id: int):
    if chat_id not in rips:
        rips[chat_id] = {}

    old_rip = db.find_rip(type, rip, chat_id)

    if old_rip is not None:
        client.send_message(chat_id=chat_id, text="Already in rips")
    else:
        rips[chat_id][(type, rip)] = message_id
        db.add_rip(type, rip, chat_id, user_id, message_id)


def remove_rip(client: Client, chat_id: int, type: str, rip: str):
    if chat_id not in rips:
        rips[chat_id] = {}
        client.send_message(chat_id=chat_id, text="Couldn't find rip")

    old_rip = db.find_rip(type, rip, chat_id)

    if (type, rip) not in rips[chat_id]:
        client.send_message(chat_id=chat_id, text="Couldn't find rip")
    else:
        del rips[chat_id][(type, rip)]
        db.del_rip(type, rip)


@Imneversorry.on_message(filters.chat(Imneversorry.whitelist) & filters.command("newrip") & filters.text)
def newrip_handler(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.message_id

    if len(message.command) == 1:
        key = str(user_id) + str(chat_id)
        waiting_rip[key] = "newrip"
        client.send_message(
            chat_id=chat_id, text="Usage: /newrip <ripmessage> or send mediafile for newrip")
        return

    type = "text"
    rip = " ".join(message.command[1:])

    save_rip(client, chat_id, user_id, type, rip, message_id)


@Imneversorry.on_message(filters.chat(Imneversorry.whitelist) & filters.command("delrip") & filters.text)
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
    rip = " ".join(message.command[1:])

    remove_rip(client, chat_id, type, rip)


@Imneversorry.on_message(filters.chat(Imneversorry.whitelist) & filters.command("rips"))
def rips_count_handler(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id not in rips:
        rips[chat_id] = {}
    client.send_message(chat_id=chat_id, text=f"{len(rips[chat_id])} rips")


@Imneversorry.on_message(filters.chat(Imneversorry.whitelist) & ~filters.text)
def waiting_rip_handler(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.message_id

    if is_newrip_or_delrip(message):
        if message.photo is not None:
            type, rip = "photo", message.photo.file_id
        elif message.document is not None:
            type, rip = "document", message.document.file_id
        elif message.voice is not None:
            type, rip = "voice", message.voice.file_id
        elif message.location is not None:
            type, rip = "location", (str(message.location.longitude) +
                                     ',' + str(message.location.latitude))
        elif message.video is not None:
            type, rip = "video", message.video.file_id
        elif message.audio is not None:
            type, rip = "audio", message.audio.file_id
        elif message.sticker is not None:
            type, rip = "sticker", message.sticker.file_id
        elif message.animation is not None:
            type, rip = "animation", message.animation.file_id
        elif message.video_note is not None:
            type, rip = "video_note", message.video_note.file_id
        else:
            # Text messages are handled by the newrip_handler
            return

        key = str(user_id) + str(chat_id)

        if key in waiting_rip:
            if waiting_rip[key] == "newrip":
                save_rip(client, chat_id, user_id, type, rip, message_id)

            elif waiting_rip[key] == "delrip":
                remove_rip(client, chat_id, type, rip)

            waiting_rip.pop(key)

        elif message.caption is not None:
            if "newrip" in message.caption:
                save_rip(client, chat_id, user_id, type, rip, message_id)

            elif "delrip" in message.caption:
                remove_rip(client, chat_id, type, rip)


@Imneversorry.on_message(filters.chat(Imneversorry.whitelist) & filters.regex("rip", re.IGNORECASE))
def rip_handler(client: Client, message: Message):
    chat_id = message.chat.id

    if chat_id not in rips:
        rips[chat_id] = {}

    if len(rips[chat_id]) == 0:
        client.send_message(chat_id=chat_id, text="rip in pepperoni")
        return

    ((type, rip), message_id) = random.sample(rips[chat_id].items(), 1)[0]

    if type == "text":
        client.send_message(chat_id=chat_id, text=f"rip in {rip}")
    elif type == "photo":
        file_id = rip

        if message_id is not None:
            orig_message = client.get_messages(
                chat_id=chat_id, message_ids=message_id, replies=0)
            file_id = orig_message.photo.file_id

        client.send_photo(chat_id=chat_id, photo=file_id, caption="rip in")
    elif type == "voice":
        client.send_voice(chat_id=chat_id, voice=rip, caption='rip in')
    elif type == "video":
        client.send_video(chat_id=chat_id, video=rip, caption='rip in')
    elif type == "audio":
        client.send_audio(chat_id=chat_id, audio=rip, caption='rip in')
    elif type == "document":
        client.send_document(chat_id=chat_id, document=rip, caption='rip in')
    elif type == "animation":
        client.send_animation(
            chat_id=chat_id, animation=rip, caption='rip in')
    elif type == "location":
        loc = rip.split(',')
        client.send_message(chat_id=chat_id, text="rip in")
        client.send_location(chat_id=chat_id, longitude=float(
            loc[0]), latitude=float(loc[1]))
    elif type == "sticker":
        client.send_message(chat_id=chat_id, text="rip in")
        client.send_sticker(chat_id=chat_id, sticker=rip)
    elif type == "video_note":
        client.send_message(chat_id=chat_id, text="rip in")
        client.send_video_note(chat_id=chat_id, video_note=rip)
    else:
        print(f"[ERROR]: riptype {type} not supported, pls fix")
