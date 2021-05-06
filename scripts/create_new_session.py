import os
import logging

from pyrogram import Client

TELEGRAM_API_ID = os.environ.get('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.environ.get('TELEGRAM_API_HASH')

if TELEGRAM_API_ID is None or TELEGRAM_API_HASH is None:
    message = """
    TELEGRAM_API_ID or TELEGRAM_API_HASH environment variables are missing.

    Register a new app at https://my.telegram.org/apps, copy the values to your .env
    file and run `source .env` before running this script.
    See README.md for more setup instructions.
    """
    print(message)

else:
    with Client(":memory:", api_id=int(TELEGRAM_API_ID), api_hash=TELEGRAM_API_HASH) as app:
        print("Your secret TELEGRAM_SESSION_STR is:")
        print(app.export_session_string())
