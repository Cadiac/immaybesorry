import os
import sys

SESSION_MISSING_MSG = """
    TELEGRAM_SESSION_STR environment variable is missing.

    Before starting the bot run `python scripts/create_new_session.py`, which
    prompts you to login to your user bot's account and prints out the secret session string.
    Store this string at your .env file and make sure you set the environment variables
    by running `source .env` before starting the bot!

    See README.md for more setup instructions.
    """


class Config:
    CREATOR_ID = int(os.environ.get('CREATOR_ID'))
    TELEGRAM_API_ID = int(os.environ.get('TELEGRAM_API_ID'))
    TELEGRAM_API_HASH = os.environ.get('TELEGRAM_API_HASH')
    TELEGRAM_SESSION_STR = os.environ.get('TELEGRAM_SESSION_STR')

    if TELEGRAM_SESSION_STR is None:
        print(SESSION_MISSING_MSG)
        sys.exit(1)

    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    LOGLEVEL_PYROGRAM = os.environ.get('LOGLEVEL_PYROGRAM', 'WARNING').upper()
    SLEEP_THRESHOLD = int(os.environ.get('SLEEP_THRESHOLD', 180))
    STICKERS = {
        "jep": "CAADBAADJgADiR7LDbglwFauETpzFgQ",
        "ei käy": "CAADBAADPwADiR7LDV1aPNns0V1YFgQ",
        "onnea": "CAADBAADuAADQAGFCMDNfgtXUw0QFgQ"
    }
