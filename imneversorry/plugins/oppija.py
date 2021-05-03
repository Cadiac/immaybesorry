import re
import random
import operator
from uuid import uuid4

from pyrogram import Client, filters
from pyrogram.types import Message
from ..imneversorry import Imneversorry
from ..utils import db


def oppis_with_same_text(definitions, text):
    sameDefs = []
    for defin in definitions:
        if defin[0].lower() == text.lower():
            sameDefs.append(defin[1].lower())
    result = (text, sameDefs)
    return result


def invert_string_list(list):
    # Reference table for the Unicode chars: http://www.upsidedowntext.com/unicode
    chars_standard = "abcdefghijklmnopqrstuvwxyzåäö"
    chars_inverted = "ɐqɔpǝɟbɥıɾʞןɯuodbɹsʇnʌʍxʎzɐɐo"

    chars_standard += "_,;.?!/\\\"<>(){}[]`&"
    chars_inverted += "‾`؛˙¿¡\\/,><)(}{][,⅋"

    chars_standard += "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    chars_inverted += "∀qϽᗡƎℲƃHIſʞ˥WNOԀὉᴚS⊥∩ΛMXʎZ∀∀O"

    chars_standard += "0123456789"
    chars_inverted += "0ƖᄅƐㄣϛ9ㄥ86"

    inverted_list = []
    for string in list:
        inverted_string = ""

        for char in string:
            try:
                charIndex = chars_standard.index(char)
            except:
                inverted_string += char
                continue
            inverted_string += chars_inverted[charIndex]

        # Reverse the string to make it readable upside down
        inverted_list.append(inverted_string[::-1])

    return inverted_list


correct_oppi = {}

# Matches messages in formats "?? something" and "¿¿ something"
@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.text & (filters.regex(r"^(\?\?)\s(\S+)$") | filters.regex(r"^(\¿\¿)\s(\S+)$")))
def define_opi_handler(client: Client, message: Message):
    chat_id = message.chat.id

    question = re.match(r"^(\?\?)\s(\S+)$", message.text)
    inverted_question = re.match(r"^(\¿\¿)\s(\S+)$", message.text)
    inverted = inverted_question is not None

    definition = db.find_oppi(question.group(2), chat_id)

    if definition is not None:
        if inverted:
            inverted_definition = invert_string_list(definition)[0]
            inverted_question = invert_string_list([question.group(2)])[0]
            client.send_message(
                chat_id=chat_id, text=f"{inverted_definition} :{inverted_question}")
        else:
            client.send_message(
                chat_id=chat_id, text=f"{question.group(2)}: {definition[0]}")
    else:
        no_idea = "En tiedä"
        if inverted:
            no_idea = invert_string_list([no_idea])[0]

        client.send_message(chat_id=chat_id, text=no_idea)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.text & filters.command("opi"))
def opi_handler(client: Client, message: Message):
    chat_id = message.chat.id
    username = message.from_user.username

    if len(message.command) < 3:
        client.send_message(
            chat_id=chat_id, text="Usage: /opi <asia> <määritelmä>")
        return

    keyword = message.command[1]
    definition = " ".join(message.command[2:])
    db.upsert_oppi(keyword, definition, chat_id, username)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.text & filters.command("opis"))
def opis_count_handler(client: Client, message: Message):
    chat_id = message.chat.id
    result = db.count_opis(chat_id)
    client.send_message(chat_id=chat_id, text=f"{result[0]} opis")


# Matches message "?!" or "¡¿"
@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.text & (filters.regex(r"^(\?\!)$") | filters.regex(r"^(\¡\¿)$")))
def random_opi_handler(client: Client, message: Message):
    chat_id = message.chat.id
    inverted = re.match(r"^(\¡\¿)$", message.text) is not None

    if (inverted):
        opi = db.random_oppi(chat_id)
        inverted_opi = invert_string_list(opi)
        client.send_message(
            chat_id=chat_id, text=f"{inverted_opi[1]} :{inverted_opi[0]}")
    else:
        opi = db.random_oppi(chat_id)
        client.send_message(chat_id=chat_id, text=f"{opi[0]}: {opi[1]}")


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.text & filters.command("jokotai"))
def jokotai_handler(client: Client, message: Message):
    chat_id = message.chat.id

    sides = ["kruuna", "klaava"]
    maximal_rigging = random.choice(sides)
    definition = db.find_oppi(maximal_rigging, chat_id)

    if definition is None:
        client.send_message(chat_id=chat_id, text="En tiedä")
        return

    client.send_message(chat_id=chat_id, parse_mode="Markdown",
                        text="*♪ Se on kuulkaas joko tai, joko tai! ♪*")
    client.send_message(
        chat_id=chat_id, text=f"{maximal_rigging}: {definition and definition[0]}")


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.text & filters.command("alias"))
def alias_handler(client: Client, message: Message):
    chat_id = message.chat.id

    if chat_id not in correct_oppi:
        correct_oppi[chat_id] = None

    if correct_oppi[chat_id] is None:
        definitions = db.read_definitions(chat_id)

        correct = random.choice(definitions)
        correct_oppi[chat_id] = oppis_with_same_text(definitions, correct[0])

        message = "Arvaa mikä oppi: \"{}\"?".format(correct_oppi[chat_id][0])
        client.send_message(chat_id=chat_id, text=message)
    else:
        client.send_message(chat_id=chat_id,
                            text="Edellinen alias on vielä käynnissä! Selitys oli: \"{}\"?".format(correct_oppi[chat_id][0]))


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.text & filters.command("arvaa"))
def arvaa_handler(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id not in correct_oppi:
        correct_oppi[chat_id] = None
    if len(message.command) != 2:
        return
    elif correct_oppi[chat_id] is not None:
        if message.command[1].lower() in correct_oppi[chat_id][1]:
            correct_oppi[chat_id] = None
            client.send_sticker(
                chat_id=chat_id, sticker=Imneversorry.STICKERS["onnea"])


# TODO: Implement Separate bot to handle inline queries?
