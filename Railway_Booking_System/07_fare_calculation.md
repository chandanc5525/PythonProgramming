# 07 — Fare Calculation

## Scenario

Right now `book_ticket()` takes `fare` as a plain argument someone has to
compute by hand. PyRail should calculate it automatically, based on:

- Distance between source and destination
- Travel class (Sleeper / AC / General)
- A small premium if booked close to departure (dynamic-pricing-style rule)

## Logic: keep calculation logic in its own function

Fare rules change often in real systems (new pricing policy, festival
surcharge, etc.). Isolating this in one function/module means you update
pricing in **one place**, not scattered through the codebase.

```python
# fare_service.py

from enum import Enum


class TravelClass(Enum):
    GENERAL = "GENERAL"
    SLEEPER = "SLEEPER"
    AC = "AC"


# Base rate per km, by class
RATE_PER_KM = {
    TravelClass.GENERAL: 0.5,
    TravelClass.SLEEPER: 1.0,
    TravelClass.AC: 2.5,
}


def calculate_fare(distance_km: float, travel_class: TravelClass,
                    days_before_departure: int) -> float:
    if distance_km <= 0:
        raise ValueError("Distance must be positive")

    base_fare = distance_km * RATE_PER_KM[travel_class]

    # Last-minute booking premium
    if days_before_departure <= 1:
        base_fare *= 1.25       # 25% premium
    elif days_before_departure <= 3:
        base_fare *= 1.10       # 10% premium

    # Minimum fare floor
    return round(max(base_fare, 50.0), 2)
```

### Key ideas here

- **`Enum` for `TravelClass`** instead of plain strings like `"AC"`. Why?
  With an Enum, typos are caught immediately — `TravelClass.AC` is either
  valid or a clear `AttributeError`; the string `"ac"` (wrong case) would
  silently fail a dictionary lookup and produce a confusing bug. Enums also
  make valid options **discoverable** — your editor can autocomplete them.
- **A dictionary for rate lookup** (`RATE_PER_KM`) instead of a chain of
  `if/elif`. This is a common upgrade from beginner to intermediate style:

  ```python
  # Beginner style — works, but grows awkward with more classes
  if travel_class == "GENERAL":
      rate = 0.5
  elif travel_class == "SLEEPER":
      rate = 1.0
  elif travel_class == "AC":
      rate = 2.5
  ```

  vs.

  ```python
  # Intermediate style — adding a class means one new dict entry
  rate = RATE_PER_KM[travel_class]
  ```

- **Guard clause at the top** (`if distance_km <= 0: raise ...`) — validate
  bad input immediately and exit early, rather than nesting the "happy
  path" logic inside an `if distance_km > 0:` block. This is a very common
  readability pattern.
- **`round(..., 2)`** — always round currency to 2 decimal places rather
  than leaving floating-point noise like `123.45600000000001` in your
  output.

## Wiring it into booking

Update `book_ticket` (Module 06) to calculate the fare itself instead of
receiving it as a raw argument:

```python
# booking_service.py

from fare_service import calculate_fare, TravelClass

def book_ticket(self, passenger_id: str, train_id: str,
                 distance_km: float, travel_class: TravelClass,
                 days_before_departure: int) -> Booking:
    ...
    fare = calculate_fare(distance_km, travel_class, days_before_departure)
    ...
```

This way, the caller (eventually, the CLI menu in Module 12) never
hand-computes a fare — it just supplies the raw facts (distance, class,
timing) and lets the fare service own the pricing rules.

## Try it yourself

1. Call `calculate_fare(500, TravelClass.SLEEPER, 10)` and
   `calculate_fare(500, TravelClass.SLEEPER, 1)` — confirm the second is
   25% higher.
2. Try `calculate_fare(-5, TravelClass.AC, 5)` — confirm it raises
   `ValueError`.
3. **Challenge:** add a `TravelClass.FIRST_AC` with a rate of `4.0` and
   confirm nothing else in the function needs to change — that's the payoff
   of using a dictionary instead of `if/elif`.

**Next:** `08_ticket_generation.md`
