import re
import random
import requests
import urllib
import time
import datetime
import json
import hashlib
import emoji
import itertools

from emoji import unicode_codes
from pyrogram import Client, filters
from pyrogram.types import Message
from ..utils import db
from ..imneversorry import Imneversorry

URLS = {
    "vituttaa": "https://fi.wikipedia.org/wiki/Toiminnot:Satunnainen_sivu",
    "urbaani_rnd": "https://urbaanisanakirja.com/random/",
    "urbaani_word": "https://urbaanisanakirja.com/word/",
    "slangopedia": "http://www.slangopedia.se/slumpa/",
    "uutine": "https://www.is.fi/api/laneitems/392841/multilist",
    "sukunimi": "https://fi.wiktionary.org/wiki/Toiminnot:Satunnainen_kohde_luokasta/Luokka:Suomen_kielen_sukunimet"
}

STICKERS = {
    "jep": "CAADBAADJgADiR7LDbglwFauETpzFgQ",
    "ei käy": "CAADBAADPwADiR7LDV1aPNns0V1YFgQ"
}

viisaudet = db.read_viisaudet()
sanat = db.read_sanat()
diagnoosit = db.read_diagnoosit()
maidot = db.read_maidot()
nimet = db.read_nimet()
kalat = db.read_kalat()
vihanneet = db.read_vihanneet()
planetoidit = db.read_planetoidit()
kulkuneuvot = db.read_kulkuneuvot()
linnut = db.read_linnut()
sotilasarvot = db.read_sotilasarvot()
sotilasnimet = db.read_sotilasnimet()
ennustukset = db.read_ennustukset()
nakutukset = db.read_nakutukset()

last_vitun = {}
last_pottiin = {}


# Integrations

def fetch_urbaani():
    webpage = urllib.request.urlopen(
        URLS["urbaani_rnd"]).read().decode("utf-8")
    title = str(webpage).split('<title>')[1].split('</title>')[0]
    sana = title.split(" |")[0]
    return sana


def fetch_urbaani_selitys(word):
    webpage = urllib.request.urlopen(
        URLS["urbaani_word"] + word + '/').read().decode("utf-8")
    meaning = str(webpage).split(
        '<meta name="description" content="')[1].split('">')[0]
    meaning = meaning[meaning.find('.')+2:]
    return meaning


def fetch_slango():
    r = requests.get(URLS["slangopedia"])
    url = urllib.parse.unquote_plus(r.url, encoding='ISO-8859-1').split('/')
    return str(url[-1].split('=')[-1].lower())


# REGEX handlers

@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex("vittuilu", re.IGNORECASE))
def vittuilu_handler(client: Client, message: Message):
    chat_id = message.chat.id
    if random.randint(0, 4) == 0:
        client.send_message(chat_id=chat_id, text="TÖRKEÄÄ SOLVAAMISTA")
    else:
        client.send_message(
            chat_id=chat_id, text=f"vittuilu{random.sample(sanat, 1)[0][0]}")


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & (filters.regex("hakemus", re.IGNORECASE)) | filters.regex("hacemus", re.IGNORECASE) | filters.regex("hakemsu", re.IGNORECASE))
def hakemus_handler(client: Client, message: Message):
    chat_id = message.chat.id

    # https://t.me/c/1363070040/153134
    if 'hacemus' in message.text.lower():
        txtHyyva = 'hy-wae'
        txtTapanSut = 'i cill u'
        txtTapanKaikki = 'HEADSHOT'
    elif 'hakemsu' in message.text.lower():
        txtHyyva = 'hvy-ää'
        txtTapanSut = 'tapna stu'
        txtTapanKaikki = 'TAPNA KIKKI'
    else:
        txtHyyva = 'hyy-vä'
        txtTapanSut = 'tapan sut'
        txtTapanKaikki = 'TAPAN KAIKKI'

    if random.randint(0, 9) == 0:
        if random.randint(0, 200) == 0:
            client.send_sticker(chat_id=chat_id, sticker=STICKERS["jep"])
        else:
            client.send_message(chat_id=chat_id, text=txtHyyva)
    else:
        if random.randint(0, 1000) == 0:
            client.send_sticker(chat_id=chat_id, sticker=STICKERS["ei käy"])
        elif random.randint(0, 600) == 0:
            client.send_message(chat_id=chat_id, text=txtTapanKaikki)
        else:
            client.send_message(chat_id=chat_id, text=txtTapanSut)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex("viisaus", re.IGNORECASE))
def viisaus_handler(client: Client, message: Message):
    client.send_message(chat_id=message.chat.id,
                        text=random.sample(viisaudet, 1)[0][0])


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex("vituttaa", re.IGNORECASE))
def vitutus_handler(client: Client, message: Message):
    r = requests.get(URLS["vituttaa"])
    url = urllib.parse.unquote_plus(r.url).split('/')
    vitutus = url[len(url)-1].replace('_', ' ') + " vituttaa"
    client.send_message(chat_id=message.chat.id, text=vitutus)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex("diagno", re.IGNORECASE))
def diagnoosi_handler(client: Client, message: Message):
    client.send_message(chat_id=message.chat.id,
                        text=random.sample(diagnoosit, 1)[0][0])


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex("nakuttaa", re.IGNORECASE))
def nakuttaa_handler(client: Client, message: Message):
    if random.randint(0, 100) == 0:
        client.send_message(chat_id=message.chat.id,
                            text="Mikä vitun Nakuttaja?")
    else:
        client.send_message(chat_id=message.chat.id,
                            text=random.sample(nakutukset, 1)[0][0] + " vaa")


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex("^halo", re.IGNORECASE))
def halo_handler(client: Client, message: Message):
    client.send_message(chat_id=message.chat.id,
                        text=random.choice(['Halo', 'Halo?', 'Halo?!']))


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex("^noppa", re.IGNORECASE))
def noppa_handler(client: Client, message: Message):
    client.send_dice(chat_id=message.chat.id)
    client.send_dice(chat_id=message.chat.id)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex("^vaihdan", re.IGNORECASE))
def vaihdan_handler(client: Client, message: Message):
    client.send_dice(chat_id=message.chat.id)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex("^vitun", re.IGNORECASE))
def vitun_handler(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    now = datetime.datetime.now().date()

    if (user_id not in last_vitun) or (last_vitun[user_id] != now):
        last_vitun[user_id] = now
        client.send_message(
            chat_id=chat_id, text=f"{fetch_urbaani().capitalize()} vitun {fetch_urbaani()}")


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex("^mikä vitun ", re.IGNORECASE))
def mika_vitun_handler(client: Client, message: Message):
    word = message.text[11:].lower().replace(
        ' ', '-').replace('ä', 'a').replace('ö', 'o').replace('å', 'a')
    word = re.sub(r"[^a-z0-9\-]", '', word)
    client.send_message(chat_id=message.chat.id,
                        text=fetch_urbaani_selitys(word))


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex("^helveten", re.IGNORECASE))
def helveten_handler(client: Client, message: Message):
    client.send_message(chat_id=message.chat.id,
                        text=fetch_slango().capitalize() + ' jävla ' + fetch_slango().lower())


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex(".*[tT]ek.*", re.IGNORECASE))
def TEK_handler(client: Client, message: Message):
    if random.randint(0, 50) == 0:
        for word in message.text.lower().split(' '):
            if re.match(r'.*tek.*', word) and word != 'tek':
                client.send_message(
                    chat_id=message.chat.id, text='ai ' + word.replace('tek', 'TEK') + ' xD')
                return


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex(".*[tT]uni.*", re.IGNORECASE))
def TUNI_handler(client: Client, message: Message):
    if random.randint(0, 50) == 0:
        for word in message.text.lower().split(' '):
            if re.match(r'.*tuni.*', word) and word != 'tuni':
                client.send_message(
                    chat_id=message.chat.id, text='ai ' + word.replace('tuni', 'TUNI') + ' xD')
                return


# TODO: emojis broken? use pyrogram.emoji?
@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex("horoskoop", re.IGNORECASE))
def horoskooppi_handler(client: Client, message: Message):
    now = datetime.datetime.now()
    data = [
        message.from_user.id,
        now.day,
        now.month,
        now.year
    ]
    seed = hashlib.md5(json.dumps(
        data, sort_keys=True).encode('utf-8')).hexdigest()
    rigged = random.Random(seed)
    ennustus = ""
    n = rigged.randint(0, 2)
    for _ in itertools.repeat(None, n):
        r = rigged.choice(tuple(unicode_codes.EMOJI_UNICODE))
        ennustus += emoji.emojize(r)
    n = rigged.randint(1, 4)
    for _ in itertools.repeat(None, n):
        ennustus += rigged.sample(ennustukset, 1)[0][0]+". "
        m = rigged.randint(0, 2)
        for _ in itertools.repeat(None, m):
            r = rigged.choice(tuple(unicode_codes.EMOJI_UNICODE))
            ennustus += emoji.emojize(r)
    ennustus = ennustus.replace('?.', '.')
    n = rigged.randint(1, 3)
    for _ in itertools.repeat(None, n):
        r = rigged.choice(tuple(unicode_codes.EMOJI_UNICODE))
        ennustus += emoji.emojize(r)
    client.send_message(chat_id=message.chat.id, text=ennustus)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.regex("uutine", re.IGNORECASE))
def uutine_handler(client: Client, message: Message):
    uutineet = [[], []]

    # TODO: Ratelimit?
    req = requests.get(URLS["uutine"])
    uutineet_json = req.json()[0]

    for uutine in uutineet_json:
        if 'title' in uutine:
            otsikko = uutine['title']
            if ' – ' in otsikko:
                otsikko = otsikko.split(' – ')
                uutineet[0].append(otsikko[0])
                uutineet[1].append(otsikko[1])

    uutine = random.choice(uutineet[0]) + \
        ' – ' + random.choice(uutineet[1])
    client.send_message(chat_id=message.chat.id, text=uutine)


# COMMAND handlers

@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("sukunimi"))
def sukunimi_handler(client: Client, message: Message):
    r = requests.get(URLS["sukunimi"])
    url = urllib.parse.unquote_plus(r.url).split('/')
    vitutus = url[len(url)-1].replace('_', ' ')
    client.send_message(chat_id=message.chat.id, text=vitutus)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("maitonimi"))
def maitonimi_handler(client: Client, message: Message):
    maitoNimi = random.sample(
        maidot, 1)[0][0] + "-" + random.sample(nimet, 1)[0][0]
    client.send_message(chat_id=message.chat.id, text=maitoNimi)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("lintuslanginimi"))
def lintunimi_handler(client: Client, message: Message):
    lintu = random.sample(linnut, 1)[0][0]
    lintu = re.sub(r'nen$', 's', lintu)
    lintuNimi = lintu + "-" + random.sample(nimet, 1)[0][0]
    client.send_message(chat_id=message.chat.id, text=lintuNimi)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("kalanimi"))
def kalanimi_handler(client: Client, message: Message):
    client.send_message(chat_id=message.chat.id,
                        text=random.sample(kalat, 1)[0][0])


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("kurkkumoponimi"))
def moponimi_handler(client: Client, message: Message):
    kurkku = random.sample(vihanneet, 1)[0][0]
    mopo = random.sample(kulkuneuvot, 1)[0][0]
    kuu = random.sample(planetoidit, 1)[0][0]
    mopoNimi = kurkku + ("", "-")[kurkku[-1:] == mopo[0] and mopo[0] in ('a', 'e', 'i', 'o', 'u', 'y',
                                                                         'ä', 'ö')] + mopo + " eli " + kuu + ("", "-")[kuu[-1:] == 'e'] + 'eläin ' + kurkku + 'maasta'
    client.send_message(chat_id=message.chat.id, text=mopoNimi)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("sotanimi"))
def sotanimi_handler(client: Client, message: Message):
    arvo = random.sample(sotilasarvot, 1)[0][0]
    nimi = random.sample(sotilasnimet, 1)[0][0]
    if random.randint(0, 7) == 0:
        if message.from_user is not None:
            if message.from_user.last_name is not None:
                nimi = message.from_user.last_name
            elif message.from_user.first_name is not None:
                nimi = message.from_user.first_name
    sotaNimi = arvo + ' ' + nimi
    client.send_message(chat_id=message.chat.id, text=sotaNimi)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("pizza"))
def pizza_handler(client: Client, message: Message):
    client.send_message(chat_id=message.chat.id, text='Ananas kuuluu pizzaan!')


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("vaalikone"))
def vaalikone_handler(client: Client, message: Message):
    client.send_message(chat_id=message.chat.id,
                        text=f"Äänestä: {str(random.randint(1,424) + 1)}")


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("pottiin"))
def pottiin_handler(client: Client, message: Message):
    now = datetime.datetime.now().date()
    user_id = message.from_user.id
    msg = "Pottiin!" if (random.randint(0, 1) == 0) else "kottiin..."
    if user_id not in last_pottiin:
        last_pottiin[user_id] = now
        client.send_message(chat_id=message.chat.id, text=msg)
    elif last_pottiin[user_id] != now:
        last_pottiin[user_id] = now
        client.send_message(chat_id=message.chat.id, text=msg)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("addsikulla"))
def ban_hammer(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # TODO: Ratelimit?
    me = client.get_chat_member(chat_id=chat_id, user_id="me")
    if me.can_restrict_members:
        duration = datetime.datetime.now() + datetime.timedelta(minutes=1)
        print(
            f"[INFO]: Banning {user_id} in chat {chat_id} until {duration} for /addsikulla")
        client.kick_chat_member(
            chat_id=chat_id, user_id=user_id, until_date=duration)
