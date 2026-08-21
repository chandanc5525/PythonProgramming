# 06 — Seat Availability & Core Booking Logic

## Scenario

A passenger wants to book a seat on train `12951`. The system must:

1. Check if a seat is actually available
2. If yes, reserve it (increase `booked_seats`)
3. If no, refuse the booking with a clear reason

This is the **heart** of the whole application — get this logic wrong and
you either oversell seats or wrongly reject valid bookings.

## Logic: why booking logic doesn't live inside `Train`

You might be tempted to add a `book_seat()` method directly on `Train`.
That's reasonable for a simple case, but PyRail's booking involves *more*
than just seats — it needs a `Passenger`, produces a `Booking` record, and
later needs to calculate a fare (Module 07) and generate a ticket
(Module 08). Bundling all of that into `Train` would make it responsible
for too many things.

Instead, we introduce a `Booking` model and a `BookingService` that
coordinates between `Train` and `Passenger` — this is the **service layer
pattern**, common in real applications.

### The `Booking` model

```python
# models.py (add this)

class Booking:
    def __init__(self, booking_id: str, passenger: "Passenger",
                 train: "Train", seat_number: int, fare: float,
                 status: str = "CONFIRMED"):
        self.booking_id = booking_id
        self.passenger = passenger
        self.train = train
        self.seat_number = seat_number
        self.fare = fare
        self.status = status   # CONFIRMED, CANCELLED

    def __str__(self):
        return (f"Booking {self.booking_id} — {self.passenger.name} — "
                f"Seat {self.seat_number} on {self.train.name} "
                f"— ₹{self.fare} — {self.status}")
```

### The core booking logic

```python
# booking_service.py

import uuid
from models import Booking
from train_service import TrainService
from passenger_service import PassengerService


class SeatUnavailableError(Exception):
    """Raised when a train has no free seats left."""
    pass


class BookingService:
    def __init__(self, train_service: TrainService,
                 passenger_service: PassengerService):
        self.train_service = train_service
        self.passenger_service = passenger_service
        self._bookings: dict[str, Booking] = {}

    def book_ticket(self, passenger_id: str, train_id: str, fare: float) -> Booking:
        passenger = self.passenger_service.get(passenger_id)
        if passenger is None:
            raise ValueError(f"No passenger with ID {passenger_id}")

        train = self.train_service.get_train(train_id)
        if train is None:
            raise ValueError(f"No train with ID {train_id}")

        if train.available_seats <= 0:
            raise SeatUnavailableError(
                f"Train {train.name} is fully booked."
            )

        # Reserve the seat
        train.booked_seats += 1
        seat_number = train.booked_seats   # simple sequential seat numbering

        booking_id = str(uuid.uuid4())[:8]
        booking = Booking(booking_id, passenger, train, seat_number, fare)
        self._bookings[booking_id] = booking
        return booking

    def get_booking(self, booking_id: str) -> Booking | None:
        return self._bookings.get(booking_id)
```

### Key ideas here

- **Custom exceptions** (`SeatUnavailableError`) instead of returning
  `None` or `False` on failure. This is an important intermediate-level
  habit: a custom exception makes the *reason* for failure explicit and
  lets calling code handle different failure types differently (Module 11
  covers this properly with `try/except`).
- **Validate before mutating state.** Notice the order: check passenger
  exists → check train exists → check seats available → *then* modify
  `train.booked_seats`. If we incremented `booked_seats` before validating
  everything, a failed booking could leave the train in a bad
  (inconsistent) state.
- **The service coordinates, the models hold data.** `BookingService`
  doesn't know *how* a `Train` stores its seat count internally — it just
  calls `train.available_seats` and `train.booked_seats`. This separation
  means you could redesign `Train`'s internals later without breaking
  `BookingService`.

## Try it yourself

1. Wire up `TrainService`, `PassengerService`, and `BookingService`
   together, register a passenger, add a train with 2 seats, and book two
   tickets successfully.
2. Try booking a third ticket on the same train — confirm
   `SeatUnavailableError` is raised.
3. **Challenge:** what happens right now if you call `book_ticket` twice
   very quickly for the *same* passenger on the *same* train? Should that
   be allowed? There's no single right answer — but write down your
   reasoning; we'll revisit similar edge cases in Module 11.

**Next:** `07_fare_calculation.md`
