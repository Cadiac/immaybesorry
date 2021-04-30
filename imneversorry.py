import os
from configparser import ConfigParser
from pyrogram import Client

cfg = ConfigParser()
cfg.read('env.cfg')

TELEGRAM_APP_ID = int(os.environ.get('TELEGRAM_APP_ID'))
TELEGRAM_APP_HASH = os.environ.get('TELEGRAM_APP_HASH')
TELEGRAM_USERNAME = os.environ.get('TELEGRAM_USERNAME')

with Client(TELEGRAM_USERNAME, TELEGRAM_APP_ID, TELEGRAM_APP_HASH) as app:
    app.send_message("me", "huutista")
