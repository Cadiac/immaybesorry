PRAGMA foreign_keys = ON;
PRAGMA encoding = 'UTF-8';

BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS Rip(
    rip text not null,
    type text,
    created date,
    channel integer not null,
    creator text,
    primary key (rip, channel)
);

CREATE TABLE IF NOT EXISTS Ripinfo(
    id integer primary key autoincrement,
    rip text references Rip(rip) not null,
    ripinfo text,
    creator text
);

CREATE TABLE IF NOT EXISTS Viisaus(viisaus text primary key);

CREATE TABLE IF NOT EXISTS Sana(sana text);

CREATE TABLE IF NOT EXISTS Oppi(
    keyword text not null,
    definition text not null,
    created date,
    channel integer not null,
    creator text,
    primary key (keyword, channel)
);

CREATE TABLE IF NOT EXISTS Quote(
    quote text not null,
    quotee text not null,
    created date,
    channel integer,
    creator text,
    primary key(quote, channel)
);

CREATE TABLE IF NOT EXISTS Diagnoosi(diagnoosi text);

CREATE TABLE IF NOT EXISTS Maito(maito text);

CREATE TABLE IF NOT EXISTS Nimi(nimi text);

CREATE TABLE IF NOT EXISTS Kalat(kala text);

CREATE TABLE IF NOT EXISTS Vihannes(nimi text);

CREATE TABLE IF NOT EXISTS Kulkuneuvo(nimi text);

CREATE TABLE IF NOT EXISTS Planetoidi(nimi text);

CREATE TABLE IF NOT EXISTS Linnut(nimi text);

CREATE TABLE IF NOT EXISTS Arvonimet(nimi text);

CREATE TABLE IF NOT EXISTS Sotilasnimet(nimi text);

CREATE TABLE IF NOT EXISTS Ennustus(rivi text);

CREATE TABLE IF NOT EXISTS Nakutukset(nakutus text);

CREATE TABLE IF NOT EXISTS Tagit(
    tag text not null,
    target text not null,
    channel integer not null,
    creator text,
    created date,
    primary key(tag, channel, target)
);

CREATE TABLE IF NOT EXISTS Urheilulajit(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nimi TEXT UNIQUE,
    kerroin FLOAT
);

CREATE TABLE IF NOT EXISTS Urheilut(
    uid INTEGER,
    chatid INTEGER,
    km FLOAT,
    type INTEGER,
    date INTEGER
);

CREATE VIEW IF NOT EXISTS UrheilutPisteilla(
    uid,
    chatid,
    km,
    date,
    pisteet,
    lajinnimi
) AS
SELECT u.uid,
    u.chatid,
    u.km,
    u.date,
    u.km * l.kerroin,
    l.nimi
FROM Urheilut as u
    JOIN Urheilulajit AS l ON u.type = l.id;

COMMIT;