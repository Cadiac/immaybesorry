# Immaybesorry

User bot based on [Pyrogram](https://github.com/pyrogram/pyrogram/).

## Quick start

```bash
$ git clone https://github.com/Cadiac/immaybesorry.git
$ cd immaybesorry
$ cp .env.sample .env
$ source .env

$ python -m venv immaybesorry
$ pip install -r requirements.txt
$ sqlite3 bot.db < sql/00-init.sql

$ python scripts/create_new_session.py
$ python scripts/seed.py

$ python -m imneversorry.py
```

[Environment variables](https://devcenter.heroku.com/articles/node-best-practices#be-environmentally-aware) are used to configure this bot.
Make a copy of the `.env.sample` file as `.env` and fill in the blanks.

## Registering Telegram application

Go to https://my.telegram.org/apps and register a new application. I've used the type "Other".
Save the generated `api_id` and `api_hash` to your `.env` file as `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` variables.

## Creating a new session

With `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` environment variables (`source .env`) set run:

```python
python scripts/create_new_session.py
```

and follow the instructions. Once login is successful, the secret session string is printed to your console.
Save this string to your `.env` file as `TELEGRAM_SESSION_STRING` variable.

You need to be able to access Telegram or the phone number of your user at this point, but
after the session is created this access is not actively required.

**NOTE**: *Telegram doesn't allow the session at multiple instances simultaneously*, so make sure you don't accidentally do that.

You can have up to 10 different active sessions. The active sessions are listed at the Telegram application, and you can end unnecessary sessions manually.

## Supported features

- [x] rips.py
- [x] teekkari.py
- [x] valitsin.py
- [X] kilometri.py
- [x] oppija.py
- [x] quote.py
- [x] tagaaja.py
- [x] tirsk.py
- [x] Creating session on server
- [x] ebin
- [x] better migration scripts
- [ ] newrip stale file_ids
- [ ] Inline /opi search
- [ ] Refactor database usage at quote.py
- [ ] TEK/TUNI handler better regex match
- [ ] mainari.py

