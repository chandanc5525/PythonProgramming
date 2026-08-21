# 02 — Setup & Project Structure

## Scenario

You know *what* PyRail needs to do (Module 1). Now decide *how the code will
be organized* before writing logic — otherwise everything ends up dumped
into one 500-line `main.py`.

## Logic: why structure matters

A beginner script looks like this:

```
booking.py   (everything: classes, logic, menu, all mixed together)
```

An intermediate project looks like this:

```
railway_booking_system/
│
├── models.py          # Station, Train, Passenger, Booking classes
├── train_service.py   # search trains, check seats
├── booking_service.py # book, cancel, fare calculation
├── storage.py          # save/load JSON data
├── main.py             # the CLI menu that ties it all together
├── data/
│   └── trains.json     # persisted data
└── tests/
    └── test_booking.py # unit tests
```

**Why split files by responsibility?**

- If a bug is in fare calculation, you know to open `booking_service.py` —
  not scroll through 500 lines.
- Each file can be tested independently (Module 13).
- This is called **separation of concerns**: each module does one job.

This course builds the code **module by module** using this exact
structure. In your own editor, create these files as we go — by Module 12
you will have real working files, not just the code in this markdown.

## Setting up

```bash
mkdir railway_booking_system
cd railway_booking_system
mkdir data tests
touch models.py train_service.py booking_service.py storage.py main.py
touch tests/test_booking.py
```

Check your Python version (3.9+ recommended, since we use modern type
hints and f-strings):

```bash
python3 --version
```

No external packages are required — everything is built-in:

```python
import json        # for saving/loading data (Module 10)
import uuid         # for generating unique ticket IDs (Module 08)
from datetime import datetime, timedelta   # for schedules (Module 05, 09)
import unittest     # for testing (Module 13)
```

## Why we don't use a database yet

A real production system would use a database (PostgreSQL, SQLite). We
intentionally use a JSON file instead, because:

- It's readable in any text editor — great for learning
- It doesn't require installing/configuring a database server
- The *logic* (how booking, cancellation, fare rules work) is identical
  whether the data sits in JSON or a database — swapping storage later
  (Module 10 shows exactly where) doesn't change your business logic

This is a hint of a bigger principle: **keep your core logic independent of
how data is stored**, so you can change storage later without rewriting
everything else.

## Try it yourself

1. Create the folder structure above on your machine.
2. In `models.py`, just write `# models go here` for now — we'll fill it in
   next module.
3. Think about: why might `train_service.py` and `booking_service.py` be
   *separate* files instead of one `service.py`? (Hint: what's the single
   job of each?)

**Next:** `03_oop_basics_station_and_train.md`
