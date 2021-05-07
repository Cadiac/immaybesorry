import sqlite3 as sq
import datetime as dt

from contextlib import contextmanager
from rapidfuzz import fuzz
from rapidfuzz import process


@contextmanager
def cursor():
    try:
        conn = sq.connect('bot.db')
        cur = conn.cursor()
        yield cur
        conn.commit()
    finally:
        conn.close()


def add_rip(type, rip, chat_id, user_id, message_id):
    with cursor() as cur:
        date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute('INSERT INTO Rip values(?, ?, ?, ?, ?, ?)',
                    (rip, type, date, chat_id, user_id, message_id))


def find_rip(type, rip, chat_id):
    with cursor() as cur:
        cur.execute(
            'SELECT * FROM Rip WHERE type = ? and rip = ? and channel = ?', (type, rip, chat_id))
        return cur.fetchone()


def del_rip(type, rip):
    with cursor() as cur:
        cur.execute('DELETE FROM Rip WHERE type = ? and rip = ?', (type, rip))


def read_rips():
    with cursor() as cur:
        cur.execute('SELECT type, rip, channel, message_id from Rip')
        rows = cur.fetchall()
        data = {}
        for row in rows:
            type, rip, channel, message_id = row
            if channel not in data:
                data[channel] = {}
            data[channel][(type, rip)] = message_id
        return data


def read_viisaudet():
    with cursor() as cur:
        cur.execute('SELECT viisaus from Viisaus')
        rows = cur.fetchall()
        return set(rows)


def read_sanat():
    with cursor() as cur:
        cur.execute('SELECT sana from Sana')
        rows = cur.fetchall()
        return set(rows)


def upsert_oppi(keyword, definition, channel, creator):
    with cursor() as cur:
        date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute('INSERT OR REPLACE INTO Oppi values(?, ?, ?, ?, ?)',
                    (keyword, definition, date, channel, creator))


def find_oppi(keyword, channel):
    with cursor() as cur:
        cur.execute(
            'SELECT definition FROM Oppi WHERE keyword=? and channel=?', (keyword, channel))
        return cur.fetchone()


def search_oppi(keyword, user, channels):
    search = '%' + keyword + '%'
    results = []
    for channel in channels:
        with cursor() as cur:
            cur.execute(
                'SELECT keyword, definition FROM Oppi WHERE (keyword LIKE ? OR definition LIKE ?) AND channel=? LIMIT 50', (search, search, channel))
            results = results + [(item[0], item[1]) for item in cur.fetchall()]
    opis = {}
    keys = []
    for item in results:
        opis[item[0]] = item[1]
        keys.append(item[0])
    keys = list(set(keys))
    fuzzed = process.extract(keyword, keys, limit=50)
    output = []
    for item in fuzzed:
        output.append((item[0], opis[item[0]]))
    return output


def get_channels():
    with cursor() as cur:
        cur.execute('SELECT DISTINCT channel FROM Oppi')
        return [item[0] for item in cur.fetchall()]


def count_opis(channel):
    with cursor() as cur:
        cur.execute(
            'SELECT COUNT(*) AS count FROM Oppi WHERE channel=?', (channel,))
        count = cur.fetchone()
        return count


def random_oppi(channel):
    with cursor() as cur:
        cur.execute(
            'SELECT keyword, definition FROM Oppi WHERE channel=? ORDER BY RANDOM() LIMIT 1', (channel,))
        return cur.fetchone()


def insert_quote(quote, quotee, channel, creator):
    with cursor() as cur:
        date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute('INSERT INTO Quote values(?, ?, ?, ?, ?)',
                    (quote, quotee, date, channel, creator))


def find_quotes(channel, quotee=None):
    with cursor() as cur:
        if quotee is not None:
            cur.execute(
                'SELECT quote, quotee FROM Quote WHERE channel=? AND upper(quotee) = upper(?)', (channel, quotee))
            return cur.fetchall()
        else:
            cur.execute(
                'SELECT quote, quotee FROM Quote WHERE channel=?', (channel,))
            return cur.fetchall()


def count_quotes(channel):
    with cursor() as cur:
        cur.execute(
            'SELECT count(quote) FROM Quote WHERE channel=?', (channel,))
        return cur.fetchone()[0]


def read_diagnoosit():
    with cursor() as cur:
        cur.execute('SELECT diagnoosi from Diagnoosi')
        rows = cur.fetchall()
        return set(rows)


def read_maidot():
    with cursor() as cur:
        cur.execute('SELECT maito from Maito')
        rows = cur.fetchall()
        return set(rows)


def read_nimet():
    with cursor() as cur:
        cur.execute('SELECT nimi from Nimi')
        rows = cur.fetchall()
        return set(rows)


def read_kalat():
    with cursor() as cur:
        cur.execute('SELECT kala from Kalat')
        rows = cur.fetchall()
        return set(rows)


def read_vihanneet():
    with cursor() as cur:
        cur.execute('SELECT nimi from Vihannes')
        rows = cur.fetchall()
        return set(rows)


def read_planetoidit():
    with cursor() as cur:
        cur.execute('SELECT nimi from Planetoidi')
        rows = cur.fetchall()
        return set(rows)


def read_kulkuneuvot():
    with cursor() as cur:
        cur.execute('SELECT nimi from Kulkuneuvo')
        rows = cur.fetchall()
        return set(rows)


def read_linnut():
    with cursor() as cur:
        cur.execute('SELECT nimi from Linnut')
        rows = cur.fetchall()
        return set(rows)


def read_sotilasarvot():
    with cursor() as cur:
        cur.execute('SELECT nimi from Arvonimet')
        rows = cur.fetchall()
        return set(rows)


def read_sotilasnimet():
    with cursor() as cur:
        cur.execute('SELECT nimi from Sotilasnimet')
        rows = cur.fetchall()
        return set(rows)


def read_ennustukset():
    with cursor() as cur:
        cur.execute('SELECT rivi from Ennustus')
        rows = cur.fetchall()
        return set(rows)


def read_nakutukset():
    with cursor() as cur:
        cur.execute('SELECT nakutus from Nakutukset')
        rows = cur.fetchall()
        return set(rows)


def read_definitions(channel):
    with cursor() as cur:
        cur.execute(
            'SELECT definition, keyword from Oppi where channel=?', (channel, ))
        rows = cur.fetchall()
        return rows


def upsert_tag(tag, target, channel, creator):
    with cursor() as cur:
        date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute('INSERT OR REPLACE INTO Tagit values(?, ?, ?, ?, ?)',
                    (tag, target, channel, creator, date))


def find_tagged(tag, channel):
    with cursor() as cur:
        cur.execute(
            'SELECT target FROM Tagit WHERE tag=? and channel=?', (tag, channel))
        rows = cur.fetchall()
        return rows


def find_target_tags(target, channel):
    with cursor() as cur:
        cur.execute(
            'SELECT tag FROM Tagit WHERE upper(target) = upper(?) and channel=?', (target, channel))
        rows = cur.fetchall()
        return rows


def add_urheilu(uid, chatid, km, lajinnimi, date):
    with cursor() as cur:
        query = ("INSERT INTO Urheilut (uid, chatid, km, type, date) VALUES (?, ?, ?, "
                 "(SELECT l.id FROM Urheilulajit AS l WHERE l.nimi = ?), ?)")
        params = (uid, chatid, km, lajinnimi, date)

        cur.execute(query, params)


def get_user_urheilut(uid, chatid, earliest_date):
    with cursor() as cur:
        query = ("SELECT up.lajinnimi AS lajinnimi, SUM(up.km) AS km, SUM(up.pisteet) AS pisteet "
                 "FROM UrheilutPisteilla AS up "
                 "WHERE up.uid = ? AND up.chatid = ? AND up.date >= ? "
                 "GROUP BY up.lajinnimi, up.uid")
        params = (uid, chatid, earliest_date)

        cur.execute(query, params)
        return cur.fetchall()


def get_top_urheilut(chatid, lajinnimi, earliest_date, limit):
    with cursor() as cur:
        query = ("SELECT uid, km from (SELECT up.uid AS uid, SUM(up.km) AS km "
                 "FROM UrheilutPisteilla AS up "
                 "WHERE up.chatid = ? AND up.date >= ? AND up.lajinnimi = ? "
                 "GROUP BY up.lajinnimi, up.uid) "
                 "ORDER BY km DESC LIMIT ?")
        params = (chatid, earliest_date, lajinnimi, limit)

        cur.execute(query, params)
        return cur.fetchall()


def get_pisteet(chatid, earliest_date, limit):
    with cursor() as cur:
        query = ("SELECT uid, pisteet from (SELECT up.uid AS uid, SUM(up.pisteet) AS pisteet "
                 "FROM UrheilutPisteilla AS up "
                 "WHERE up.chatid = ? AND up.date >= ? "
                 "GROUP BY up.uid) "
                 "ORDER BY pisteet DESC LIMIT ?")
        params = (chatid, earliest_date, limit)

        cur.execute(query, params)
        return cur.fetchall()


def add_urheilulaji(nimi, kerroin):
    with cursor() as cur:
        cur.execute("INSERT INTO Urheilulajit (nimi, kerroin) VALUES (?, ?) ON CONFLICT (nimi) DO UPDATE SET kerroin = ?",
                    (nimi, kerroin, kerroin))
