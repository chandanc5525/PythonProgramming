# 11 — Exception Handling & Input Validation

## Scenario

So far our services *raise* good exceptions (`SeatUnavailableError`,
`BookingNotFoundError`, etc.), but nothing *catches* them. If a user types
an invalid train ID at a menu prompt, the whole program currently crashes
with an ugly traceback. We need to handle errors gracefully at the
boundary where the program talks to a human — the CLI.

## Logic: two different concerns — validation vs. exception handling

These are related but distinct:

- **Validation**: catching *bad input* before it causes a problem (e.g. an
  empty name, a negative age, letters typed where a number is expected).
- **Exception handling**: responding to failures that *can't* be prevented
  by validation alone (e.g. the train really is full, the booking really
  doesn't exist) — these are legitimate business-rule failures, not typos.

### Input validation helpers

```python
# validators.py

def validate_non_empty_string(value: str, field_name: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError(f"{field_name} cannot be empty")
    return value


def validate_positive_int(value: str, field_name: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise ValueError(f"{field_name} must be a whole number")
    if number <= 0:
        raise ValueError(f"{field_name} must be greater than zero")
    return number
```

Notice `validate_positive_int` **catches** a `ValueError` from `int()` and
**raises** a new, clearer `ValueError` with a message meant for the end
user. `int("abc")` alone gives a cryptic
`invalid literal for int() with base 10: 'abc'` — not something a
non-programmer using the CLI should ever see.

### Handling exceptions at the CLI boundary

This is where `try/except` earns its keep — wrapping the *risky* operation
and responding to each specific failure differently:

```python
# main.py (preview — full menu comes in Module 12)

from booking_service import SeatUnavailableError, BookingNotFoundError, AlreadyCancelledError

def handle_booking(booking_service, passenger_id, train_id, distance, travel_class, days_left):
    try:
        booking = booking_service.book_ticket(
            passenger_id, train_id, distance, travel_class, days_left
        )
        print(f"Booking confirmed! ID: {booking.booking_id}")

    except SeatUnavailableError as e:
        print(f"Sorry — {e}")

    except ValueError as e:
        print(f"Invalid input — {e}")

    except Exception as e:
        # A safety net for anything unexpected — should be rare if the
        # specific exceptions above are handled well.
        print(f"Unexpected error: {e}")
```

### Key ideas here

- **Catch specific exceptions first, generic `Exception` last.** Python
  checks `except` blocks top to bottom and uses the first match. If you put
  `except Exception` first, it would swallow *everything*, including the
  specific errors you wanted to handle differently — so order matters.
- **`except Exception as e` should be a last resort, not a habit.** Catching
  broad exceptions everywhere hides real bugs instead of fixing them. Use
  it sparingly, typically only at the outermost boundary of your program
  (like the CLI loop), never deep inside business logic.
- **Never use a bare `except:`** (with no exception type at all) — it
  catches *everything*, including things like `KeyboardInterrupt` (Ctrl+C),
  which means your program won't even respond to being stopped normally.
  Always name at least `Exception`.
- **Validation happens close to where input is entered** (the CLI); raised
  business exceptions happen close to where the business rule lives (the
  service classes). Keeping this separation makes it obvious where to look
  when something goes wrong.

## Try it yourself

1. Call `validate_positive_int("abc", "Age")` and confirm you get a clear
   `ValueError` message instead of Python's default cryptic one.
2. Wrap a call to `cancel_booking` with a `try/except` that separately
   handles `BookingNotFoundError` and `AlreadyCancelledError` with
   different printed messages.
3. **Challenge:** what real-world bad inputs could break `book_ticket` that
   we haven't guarded against yet (e.g., a passenger ID with extra
   whitespace, an age of `0`)? Pick one and add a validator for it.

**Next:** `12_cli_menu_integration.md`
