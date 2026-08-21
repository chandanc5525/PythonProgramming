# 03 — OOP Basics: `Station` and `Train`

## Scenario

PyRail needs to represent real-world things — stations and trains — as data
in the program. A beginner might use separate variables or dictionaries:

```python
train_name = "Rajdhani Express"
train_source = "Delhi"
train_destination = "Mumbai"
train_total_seats = 100
```

This gets messy fast once you have *many* trains. We need a way to bundle
related data + behavior together. That's what a **class** is for.

## Logic: classes model real-world entities

A class is a blueprint. An **object** (or instance) is one real thing built
from that blueprint.

```
Class: Train           →  the blueprint ("all trains have a name, route, seats")
Object: rajdhani_train →  one specific train built from that blueprint
```

### `Station` — the simplest class

```python
# models.py

class Station:
    def __init__(self, code: str, name: str):
        self.code = code          # e.g. "NDLS"
        self.name = name          # e.g. "New Delhi"

    def __str__(self):
        return f"{self.name} ({self.code})"
```

- `__init__` is the **constructor** — it runs automatically when you create
  a new `Station`.
- `self` refers to *this particular object* being created — it's how each
  station keeps its own `code` and `name` separate from every other one.
- `__str__` controls what `print(station)` displays. Without it, printing
  an object shows an ugly memory address like `<Station object at 0x7f...>`.

```python
>>> ndls = Station("NDLS", "New Delhi")
>>> print(ndls)
New Delhi (NDLS)
```

### `Train` — a class that uses other classes

```python
class Train:
    def __init__(self, train_id: str, name: str, source: Station,
                 destination: Station, departure_time: str,
                 total_seats: int):
        self.train_id = train_id
        self.name = name
        self.source = source
        self.destination = destination
        self.departure_time = departure_time   # e.g. "14:30"
        self.total_seats = total_seats
        self.booked_seats = 0                  # starts empty

    @property
    def available_seats(self) -> int:
        return self.total_seats - self.booked_seats

    def __str__(self):
        return (f"[{self.train_id}] {self.name}: "
                f"{self.source} → {self.destination} "
                f"at {self.departure_time} "
                f"({self.available_seats}/{self.total_seats} seats free)")
```

### Key ideas here

- **Composition**: `Train` *has a* `Station` (two of them, actually). This
  is more realistic than storing station names as plain strings, because a
  `Station` object can later grow (add platform info, city, etc.) without
  touching `Train` at all.
- **`@property`**: `available_seats` is *calculated*, not stored. We never
  want to accidentally set `available_seats` directly and have it go out of
  sync with `total_seats - booked_seats`. A property makes it read-only and
  always correct.
- We do **not** put booking logic (checking/reducing seats) inside `Train`
  itself yet — that belongs in `booking_service.py` (Module 06). `Train`
  should only know about *itself*, not how the booking process works. This
  keeps the class focused and easy to reason about.

## Full code so far (`models.py`)

```python
class Station:
    def __init__(self, code: str, name: str):
        self.code = code
        self.name = name

    def __str__(self):
        return f"{self.name} ({self.code})"


class Train:
    def __init__(self, train_id: str, name: str, source: Station,
                 destination: Station, departure_time: str,
                 total_seats: int):
        self.train_id = train_id
        self.name = name
        self.source = source
        self.destination = destination
        self.departure_time = departure_time
        self.total_seats = total_seats
        self.booked_seats = 0

    @property
    def available_seats(self) -> int:
        return self.total_seats - self.booked_seats

    def __str__(self):
        return (f"[{self.train_id}] {self.name}: "
                f"{self.source} → {self.destination} "
                f"at {self.departure_time} "
                f"({self.available_seats}/{self.total_seats} seats free)")
```

## Try it yourself

1. Create two `Station` objects (e.g. Delhi, Mumbai) and one `Train`
   connecting them with 50 total seats.
2. Print the train and confirm it shows `50/50 seats free`.
3. Manually set `train.booked_seats = 10` and print `train.available_seats`
   — confirm it updates automatically (this is the property in action).
4. **Challenge:** add a `duration_hours` attribute to `Train` and include it
   in `__str__`.

**Next:** `04_passenger_class_and_management.md`
