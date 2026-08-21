# 08 — Ticket Generation

## Scenario

A booking has just succeeded. Now the passenger wants a **ticket** they can
read — not a raw `Booking` object printed with default formatting.

## Logic: separating data from presentation

We already have all the information we need inside `Booking` (Module 06).
Ticket generation is really about **formatting** that data nicely — a
different responsibility from *creating* the booking. Keeping this as its
own function (rather than cramming formatting logic into
`BookingService.book_ticket`) means you could later add a PDF ticket, an
SMS version, or an email version, all using the same `Booking` object.

```python
# ticket_service.py

from models import Booking


def generate_ticket(booking: Booking) -> str:
    train = booking.train
    passenger = booking.passenger

    lines = [
        "=" * 40,
        "          PYRAIL — E-TICKET",
        "=" * 40,
        f"PNR / Booking ID : {booking.booking_id}",
        f"Passenger        : {passenger.name} ({passenger.age}, {passenger.gender})",
        f"Train            : {train.name} [{train.train_id}]",
        f"From             : {train.source}",
        f"To               : {train.destination}",
        f"Departure        : {train.departure_time}",
        f"Seat Number      : {booking.seat_number}",
        f"Fare Paid        : Rs. {booking.fare:.2f}",
        f"Status           : {booking.status}",
        "=" * 40,
    ]
    return "\n".join(lines)
```

```python
>>> ticket = generate_ticket(booking)
>>> print(ticket)
========================================
          PYRAIL — E-TICKET
========================================
PNR / Booking ID : 8f3a1c9d
Passenger        : Anita Rao (29, F)
Train            : Rajdhani Express [12951]
From             : New Delhi (NDLS)
To               : Mumbai Central (BCT)
Departure        : 16:00
Seat Number      : 1
Fare Paid        : Rs. 875.00
Status           : CONFIRMED
========================================
```

### Key ideas here

- **Build a list of strings, then `"\n".join(...)`** rather than repeatedly
  concatenating with `+=`. This is both more readable (you can see the
  ticket's structure at a glance) and more efficient — string
  concatenation in a loop creates a new string object every time, while
  `join` builds it once.
- **`f"{booking.fare:.2f}"`** — the `:.2f` format spec always shows exactly
  2 decimal places, so `875.0` displays as `875.00`, not `875.0`.
- **This function takes a `Booking` and returns a `str`.** It doesn't print
  anything itself, and it doesn't touch the booking service or the train
  service. A function that only depends on its inputs and produces an
  output — with no side effects — is called a **pure function**. Pure
  functions are easy to test (Module 13) because there's nothing to set up
  beyond the input.

## Try it yourself

1. Generate and print a ticket for a booking you create using the code from
   Module 06/07.
2. **Challenge:** add a `generate_ticket_json(booking)` function that
   returns the same information as a dictionary instead of a formatted
   string (hint: this will directly help with Module 10, saving data to
   JSON).

**Next:** `09_cancellation_and_refund.md`
