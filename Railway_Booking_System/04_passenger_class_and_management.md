# 04 — `Passenger` Class & Managing a List of Objects

## Scenario

PyRail needs to know *who* is booking tickets — name, age, and a unique ID
to tell two "Rahul Kumar"s apart. It also needs a way to register new
passengers and look them up later.

## Logic: modeling a passenger

```python
# models.py (add this below Station and Train)

class Passenger:
    def __init__(self, passenger_id: str, name: str, age: int,
                 gender: str, contact: str):
        self.passenger_id = passenger_id
        self.name = name
        self.age = age
        self.gender = gender
        self.contact = contact

    def __str__(self):
        return f"{self.name} ({self.age}, {self.gender}) — ID: {self.passenger_id}"
```

Nothing new here structurally — it's the same pattern as `Station`. The
interesting part is **managing many passengers**, which introduces a common
intermediate-level pattern: a **service class that wraps a list**.

### Why not just use a plain list everywhere?

You *could* keep a bare list of `Passenger` objects and write search/add
code wherever you need it. The problem: that logic gets duplicated across
your program. Instead, wrap it once in a dedicated class.

```python
# passenger_service.py

import uuid
from models import Passenger


class PassengerService:
    def __init__(self):
        self._passengers: dict[str, Passenger] = {}   # id -> Passenger

    def register(self, name: str, age: int, gender: str, contact: str) -> Passenger:
        passenger_id = str(uuid.uuid4())[:8]   # short unique id
        passenger = Passenger(passenger_id, name, age, gender, contact)
        self._passengers[passenger_id] = passenger
        return passenger

    def get(self, passenger_id: str) -> Passenger | None:
        return self._passengers.get(passenger_id)

    def all_passengers(self) -> list[Passenger]:
        return list(self._passengers.values())
```

### Key ideas here

- **Dictionary over list for lookup-by-ID.** If we stored passengers in a
  plain list, finding one by ID means looping through every item —
  `O(n)`. A dictionary keyed by ID gives near-instant lookup — `O(1)`. This
  matters more as data grows; it's a habit worth building now.
- **`uuid.uuid4()`** generates a random, essentially-unique ID — this
  mirrors how real systems generate passenger/order IDs without needing a
  central counter.
- **The leading underscore** in `self._passengers` is a Python convention
  meaning "internal — don't touch this directly from outside the class."
  Other code should go through `register()` / `get()` / `all_passengers()`,
  not reach into `_passengers` directly. Python doesn't *enforce* this
  (unlike private fields in Java/C++), but the convention communicates
  intent clearly.
- **`Passenger | None`** is a modern type hint meaning "this returns either
  a Passenger, or None if not found." It documents behavior for anyone
  reading your code, including future-you.

## Try it yourself

1. Create a `PassengerService`, register 3 passengers.
2. Fetch one back by the ID returned from `register()` and print them.
3. Try `service.get("does-not-exist")` — confirm it returns `None` instead
   of crashing.
4. **Challenge:** add a `find_by_name(self, name)` method that searches
   `_passengers.values()` for a case-insensitive name match and returns a
   list of matches (there could be more than one "Rahul Kumar").

**Next:** `05_train_schedule_and_search.md`
