# 05 — Train Schedule & Search

## Scenario

A user opens PyRail and wants: *"Show me trains from Delhi to Mumbai."*
The system needs to store a collection of trains and filter them by route.

## Logic: a service that manages many `Train` objects

```python
# train_service.py

from models import Train, Station


class TrainService:
    def __init__(self):
        self._trains: dict[str, Train] = {}   # train_id -> Train

    def add_train(self, train: Train) -> None:
        self._trains[train.train_id] = train

    def get_train(self, train_id: str) -> Train | None:
        return self._trains.get(train_id)

    def search(self, source_code: str, destination_code: str) -> list[Train]:
        results = []
        for train in self._trains.values():
            if (train.source.code == source_code
                    and train.destination.code == destination_code):
                results.append(train)
        return results

    def all_trains(self) -> list[Train]:
        return list(self._trains.values())
```

The same dictionary-by-ID pattern from Module 04 — consistency across your
codebase makes it predictable to read.

### The search logic, step by step

```python
def search(self, source_code: str, destination_code: str) -> list[Train]:
    results = []
    for train in self._trains.values():          # look at every train
        if (train.source.code == source_code      # does it start here?
                and train.destination.code == destination_code):  # and end here?
            results.append(train)                 # if both, it's a match
    return results
```

This is a **linear search** — checking every item once. For a learning
project with dozens or hundreds of trains, this is perfectly fine. (Real
systems with millions of records use a database with an *index* for this —
same idea as an index in a book, so you don't have to search page by page.)

### A more Pythonic version (list comprehension)

Once the loop version makes sense, this is the same logic written more
concisely — an intermediate-level habit worth building:

```python
def search(self, source_code: str, destination_code: str) -> list[Train]:
    return [
        t for t in self._trains.values()
        if t.source.code == source_code and t.destination.code == destination_code
    ]
```

Both versions do exactly the same thing. Use whichever reads more clearly
to you — readability beats cleverness.

## Putting it together

```python
delhi = Station("NDLS", "New Delhi")
mumbai = Station("BCT", "Mumbai Central")
jaipur = Station("JP", "Jaipur")

t1 = Train("12951", "Rajdhani Express", delhi, mumbai, "16:00", 100)
t2 = Train("12952", "Duronto Express", delhi, jaipur, "09:00", 80)

service = TrainService()
service.add_train(t1)
service.add_train(t2)

results = service.search("NDLS", "BCT")
for train in results:
    print(train)
# [12951] Rajdhani Express: New Delhi (NDLS) → Mumbai Central (BCT) at 16:00 (100/100 seats free)
```

## Why search returns a list, even for zero/one result

Always returning a `list[Train]` (even if empty) rather than sometimes
returning `None` and sometimes a single `Train` keeps the calling code
simple — it always loops or checks `len(results)`, with no special cases to
remember. This consistency is a small thing that prevents a lot of bugs.

## Try it yourself

1. Add 4–5 trains covering different routes.
2. Search for a route that doesn't exist — confirm you get `[]`, not a
   crash.
3. **Challenge:** add a `search_by_train_name(self, keyword)` method that
   returns trains whose `name` contains `keyword` (case-insensitive). Hint:
   `keyword.lower() in train.name.lower()`.

**Next:** `06_seat_availability_and_booking_logic.md`
