import os
import sys
import logging

logger = logging.getLogger('imneversorry')

CREATOR_ID_MISSING = """
    CREATOR_ID environment variable is missing

    Find your telegram account id by for instance by talking to @RawDataBot.

    See README.md for more setup instructions.
"""

TELEGRAM_API_ID_MISSING = """
    TELEGRAM_API_ID environment variable is missing

    Go to https://my.telegram.org/apps and register a new application.

    See README.md for more setup instructions.
"""

TELEGRAM_API_HASH_MISSING = """
    TELEGRAM_API_HASH environment variable is missing

    Go to https://my.telegram.org/apps and register a new application.

    See README.md for more setup instructions.
"""

TELEGRAM_SESSION_STR_MISSING = """
    TELEGRAM_SESSION_STR environment variable is missing.

    Before starting the bot run `python scripts/create_new_session.py`, which
    prompts you to login to your user bot's account and prints out the secret session string.
    Store this string at your .env file and make sure you set the environment variables
    by running `source .env` before starting the bot!

    See README.md for more setup instructions.
"""


class Config:
    CREATOR_ID = os.environ.get('CREATOR_ID')
    if CREATOR_ID is None:
        logger.error(CREATOR_ID_MISSING)
        sys.exit(1)
    CREATOR_ID = int(CREATOR_ID)

    TELEGRAM_API_ID = os.environ.get('TELEGRAM_API_ID')
    if TELEGRAM_API_ID is None:
        logger.error(TELEGRAM_API_ID_MISSING)
        sys.exit(1)
    TELEGRAM_API_ID = int(TELEGRAM_API_ID)

    TELEGRAM_API_HASH = os.environ.get('TELEGRAM_API_HASH')
    if TELEGRAM_API_HASH is None:
        logger.error(TELEGRAM_API_HASH_MISSING)
        sys.exit(1)

    TELEGRAM_SESSION_STR = os.environ.get('TELEGRAM_SESSION_STR')
    if TELEGRAM_SESSION_STR is None:
        logger.error(TELEGRAM_SESSION_STR_MISSING)
        sys.exit(1)

    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    LOGLEVEL_PYROGRAM = os.environ.get('LOGLEVEL_PYROGRAM', 'WARNING').upper()
    SLEEP_THRESHOLD = int(os.environ.get('SLEEP_THRESHOLD', 180))
    STICKERS = {
        "jep": "CAADBAADJgADiR7LDbglwFauETpzFgQ",
        "ei käy": "CAADBAADPwADiR7LDV1aPNns0V1YFgQ",
        "onnea": "CAADBAADuAADQAGFCMDNfgtXUw0QFgQ"
    }
