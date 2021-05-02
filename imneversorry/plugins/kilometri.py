import collections
import math
import time

from pyrogram import Client, filters
from pyrogram.types import Message
from ..imneversorry import Imneversorry
from ..utils import db


def name_from_user_id(client: Client, chat_id: int, user_id: int):
    # TODO: Move this to imneversorry.py and use get_chat_members.
    # TODO: Query users from all channels on bot startup, and keep track of leaving/joining users.
    # TODO: Always read users from memory.

    chat_member = client.get_chat_member(chat_id=chat_id, user_id=user_id)
    if chat_member is None:
        return "Tuntematon"
    elif chat_member.user.username is None:
        return "%s %s" % (str(chat_member.user.first_name), str(chat_member.user.last_name))
    else:
        return chat_member.user.username


class Laji:
    def __init__(self, monikko, kerroin):
        self.monikko = monikko
        self.kerroin = kerroin

    def poista_skandit(self, s): return s.replace("ä", "a").replace(
        "Ä", "A").replace("ö", "o").replace("Ö", "O")

    def listauskasky(self):
        return self.poista_skandit(self.monikko)


class Kilometri:
    lajit = {
        "kavely": Laji("kävelyt", 1),
        "juoksu": Laji("juoksut", 3),
        "pyoraily": Laji("pyöräilyt", 0.4),
        "hiihto": Laji("hiihdot", 2),
    }

    def parsi_aika_lkm(self, message: Message):
        aikasuureet = {
            "s":   1,
            "sek": 1,
            "m":   60,
            "min": 60,
            "h":   60 * 60,
            "pv":  60 * 60 * 24,
            "d":   60 * 60 * 24,
            "kk":  60 * 60 * 24 * 30,
            "mo":  60 * 60 * 24 * 30,
            "v":   60 * 60 * 24 * 30 * 365,
            "y":   60 * 60 * 24 * 30 * 365,
        }

        aika = 3 * aikasuureet["kk"]
        aikanimi = "3kk"
        lkm = 30

        for arg in message.command[1:]:
            try:
                lkm = int(arg)
                continue
            except ValueError:
                pass

            for lyhenne, kerroin in aikasuureet.items():
                if (arg.endswith(lyhenne)):
                    try:
                        aika = float(arg.rstrip(lyhenne)) * kerroin
                        aikanimi = arg
                        break
                    except ValueError:
                        pass
            else:
                raise ValueError("Unrecognized '%s' in args" % arg)

        return (aika, aikanimi, lkm)

    def laji_handler(self, client: Client, message: Message, nimi):
        user_id = message.from_user.id
        chat_id = message.chat.id

        def printUsage():
            usage = "Usage: /%s <km>" % nimi
            client.send_message(chat_id=chat_id, text=usage)

        def invalidDistance(km): return math.isnan(km) or math.isinf(km)

        if (len(message.command) != 2):
            printUsage()
            return

        try:
            km = float(message.command[1].rstrip("km"))
            if (invalidDistance(km)):
                raise ValueError("invalid distance %f" % km)
        except ValueError:
            printUsage()
            return

        now = int(time.time())
        db.add_urheilu(user_id, chat_id, km, nimi, now)

    def laji_stats_handler(self, client: Client, message: Message, nimi):
        user_id = message.from_user.id
        chat_id = message.chat.id

        laji = self.lajit[nimi]
        try:
            aika, aikanimi, lkm = self.parsi_aika_lkm(message)
        except ValueError:
            usage = "Usage: /%s [lkm] [ajalta]" % laji.listauskasky()
            client.send_message(chat_id=chat_id, text=usage)
            return

        alkaen = time.time() - aika

        top_suoritukset = db.get_top_urheilut(chat_id, nimi, alkaen, lkm)
        lista = "\n".join("%s: %.1f km" %
                          (name_from_user_id(client, chat_id, user_id), km)
                          for uid, km in top_suoritukset)

        client.send_message(chat_id=message.chat.id,
                            text="Top %i %s viimeisen %s aikana:\n\n%s" %
                            (lkm, laji.monikko, aikanimi, lista))

    def pisteet_handler(self, client: Client, message: Message):
        chat_id = message.chat.id

        try:
            aika, aikanimi, lkm = self.parsi_aika_lkm(message)
        except ValueError:
            client.send_message(
                chat_id=chat_id, text="Usage: /pisteet [ajalta]")
            return

        alkaen = time.time() - aika
        pisteet = db.get_pisteet(chat_id, alkaen, lkm)

        # TODO: Get all chat members (with singler request) and search from them?
        piste_str = "\n".join("%s: %.1f pistettä" %
                              (name_from_user_id(client, chat_id, user_id), p) for user_id, p in pisteet)
        text = "Top %i pisteet viimeisen %s aikana:\n\n%s" % (
            lkm, aikanimi, piste_str)

        client.send_message(chat_id=chat_id, text=text)

    def kmstats_handler(self, client: Client, message: Message):
        def usage():
            client.send_message(chat_id=message.chat.id,
                                text="Usage: /kmstats [ajalta]")

        try:
            aika, aikanimi, _ = self.parsi_aika_lkm(message)
        except ValueError:
            usage()
            return

        alkaen = time.time() - aika

        user_id = message.from_user.id
        chat_id = message.chat.id

        name = name_from_user_id(client, chat_id, user_id)

        stats = db.get_user_urheilut(user_id, chat_id, alkaen)
        lajikohtaiset = ((nimi, km) for nimi, km, _ in stats)
        pisteet = sum(pisteet for _, _, pisteet in stats)

        lajit_str = ", ".join("%s %.1f km" % ln_km for ln_km in lajikohtaiset)
        stat_str = ("%s: Viimeisen %s aikana %.1f pistettä\n\n%s" %
                    (name, aikanimi, pisteet, lajit_str))

        client.send_message(chat_id=message.chat.id, text=stat_str)


kilometri = Kilometri()

# COMMAND handlers


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("pisteet"))
def pisteet_handler(client: Client, message: Message):
    kilometri.pisteet_handler(client, message)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("kmstats"))
def kmstats_handler(client: Client, message: Message):
    kilometri.kmstats_handler(client, message)


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("kavely"))
def kavely_handler(client: Client, message: Message):
    kilometri.laji_handler(client, message, "kavely")


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("kavelyt"))
def kavelyt_handler(client: Client, message: Message):
    kilometri.laji_stats_handler(client, message, "kavely")


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("juoksu"))
def juoksu_handler(client: Client, message: Message):
    kilometri.laji_handler(client, message, "juoksu")


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("juoksut"))
def juoksut_handler(client: Client, message: Message):
    kilometri.laji_stats_handler(client, message, "juoksu")


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("pyoraily"))
def pyoraily_handler(client: Client, message: Message):
    kilometri.laji_handler(client, message, "pyoraily")


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("pyorailyt"))
def pyorailyt_handler(client: Client, message: Message):
    kilometri.laji_stats_handler(client, message, "pyoraily")


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("hiihto"))
def hiihto_handler(client: Client, message: Message):
    kilometri.laji_handler(client, message, "hiihto")


@Imneversorry.on_message(filters.chat(Imneversorry.chats) & filters.command("hiihdot"))
def hiihdot_handler(client: Client, message: Message):
    kilometri.laji_stats_handler(client, message, "hiihto")
