# Immaybesorry

## Getting started

```
$ git clone https://github.com/Cadiac/immaybesorry.git
$ cd immaybesorry

$ python -m venv immaybesorry
$ pip install -r requirements.txt
$ sqlite3 bot.db < sql/00-init.sql
$ python scripts/seed.py

$ python -m imneversorry.py
```

## Features / migration progress

- [x] rips.py
- [x] teekkari.py
- [x] valitsin.py
- [X] kilometri.py
- [ ] mainari.py
- [x] oppija.py
- [x] quote.py
- [x] tagaaja.py
- [x] tirsk.py
- [ ] Inline /opi search
- [ ] Refactor database usage at quote.py
- [ ] TEK/TUNI handler regex match
- [ ] Creating session on server
- [x] ebin
- [ ] newrip stale file_ids
- [ ] better migration scripts
