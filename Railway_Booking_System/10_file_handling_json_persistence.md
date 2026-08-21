# 10 — File Handling & JSON Persistence

## Scenario

Right now, every time PyRail exits, all trains, passengers, and bookings
vanish — everything lives only in memory (Python objects). We need to
**save data to disk** and **load it back** when the program restarts.

## Logic: why JSON, and the conversion problem

JSON is a text format that maps naturally to Python dicts/lists, is
human-readable, and needs no extra library (`json` is built into Python).

The catch: `json.dump()` can't serialize our custom classes (`Train`,
`Passenger`, `Booking`) directly — it only understands dicts, lists,
strings, numbers, booleans, and `None`. So we need to **convert objects to
dictionaries before saving**, and **rebuild objects from dictionaries after
loading**. This conversion is a very common intermediate-level pattern,
often called serialization / deserialization.

### Step 1: teach each model how to convert itself

```python
# models.py — add a to_dict() to each class

class Station:
    ...
    def to_dict(self):
        return {"code": self.code, "name": self.name}

    @staticmethod
    def from_dict(data):
        return Station(data["code"], data["name"])


class Train:
    ...
    def to_dict(self):
        return {
            "train_id": self.train_id,
            "name": self.name,
            "source": self.source.to_dict(),
            "destination": self.destination.to_dict(),
            "departure_time": self.departure_time,
            "total_seats": self.total_seats,
            "booked_seats": self.booked_seats,
        }

    @staticmethod
    def from_dict(data):
        train = Train(
            data["train_id"], data["name"],
            Station.from_dict(data["source"]),
            Station.from_dict(data["destination"]),
            data["departure_time"], data["total_seats"],
        )
        train.booked_seats = data["booked_seats"]
        return train
```

`Passenger.to_dict` / `from_dict` follow the same pattern (just plain
fields, no nested objects). `Booking.to_dict` nests `passenger.to_dict()`
and `train.to_dict()` the same way `Train` nests `Station`.

### Step 2: a storage module that saves/loads the whole system

```python
# storage.py

import json
from models import Train

DATA_FILE = "data/trains.json"


def save_trains(trains: list[Train], path: str = DATA_FILE) -> None:
    data = [train.to_dict() for train in trains]
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_trains(path: str = DATA_FILE) -> list[Train]:
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []   # no file yet — treat as an empty system
    return [Train.from_dict(item) for item in data]
```

### Key ideas here

- **`with open(...) as f:`** — the `with` block guarantees the file is
  properly closed even if an error happens partway through writing. Always
  prefer this over manual `f = open(...)` / `f.close()`.
- **`indent=2`** in `json.dump` makes the saved file human-readable —
  useful while learning, so you can open `trains.json` and see exactly
  what got saved.
- **Handling `FileNotFoundError`** on load, rather than crashing the whole
  program the very first time it runs (before any file exists). Returning
  an empty list is a sensible default — "no saved data yet" is a normal
  state, not an error.
- **Round-trip symmetry**: `to_dict()` and `from_dict()` are inverses of
  each other. A good sanity check while developing: `Train.from_dict(
  some_train.to_dict())` should recreate an equivalent train. Keeping the
  two methods next to each other in the code (as shown above) makes it
  easier to keep them in sync when you add a new field later.

## Try it yourself

1. Create 2 trains, save them with `save_trains`, then restart your Python
   shell/script and reload them with `load_trains` — print them to confirm
   the data survived.
2. Delete `data/trains.json` and run `load_trains` again — confirm you get
   `[]` instead of a crash.
3. **Challenge:** write `save_bookings` / `load_bookings` following the
   same pattern for `Booking` objects (remember: a `Booking` references a
   `Passenger` and a `Train` by full object, not just an ID — think about
   whether nesting the full objects in the JSON, or just storing their IDs
   and looking them up after loading, is a better design. Either is
   valid — try one and note the trade-off you notice).

**Next:** `11_exception_handling_and_validation.md`
