# 13 — Unit Testing

## Scenario

You've been manually testing by running `main.py` and typing input each
time. That's slow and error-prone — and every time you change fare rules
(Module 07) you'd have to manually re-check everything still works. We
need **automated tests** that run in a second and catch regressions.

## Logic: what makes a good unit test

A unit test checks **one small piece of behavior** in isolation, following
this shape:

1. **Arrange** — set up the objects/data you need
2. **Act** — call the function/method you're testing
3. **Assert** — check the result is what you expect

Python's built-in `unittest` module handles running tests and reporting
results — no external library needed.

```python
# tests/test_booking.py

import unittest
from models import Station, Train, Passenger
from train_service import TrainService
from passenger_service import PassengerService
from booking_service import BookingService, SeatUnavailableError
from fare_service import TravelClass


class TestBookingService(unittest.TestCase):
    def setUp(self):
        """Runs before every test method — fresh state each time."""
        self.train_service = TrainService()
        self.passenger_service = PassengerService()
        self.booking_service = BookingService(self.train_service, self.passenger_service)

        delhi = Station("NDLS", "New Delhi")
        mumbai = Station("BCT", "Mumbai Central")
        self.train = Train("12951", "Rajdhani Express", delhi, mumbai, "16:00", total_seats=1)
        self.train_service.add_train(self.train)

        self.passenger = self.passenger_service.register("Anita Rao", 29, "F", "9999999999")

    def test_booking_succeeds_when_seat_available(self):
        # Act
        booking = self.booking_service.book_ticket(
            self.passenger.passenger_id, self.train.train_id, 500, TravelClass.SLEEPER, 10
        )
        # Assert
        self.assertEqual(booking.status, "CONFIRMED")
        self.assertEqual(self.train.available_seats, 0)

    def test_booking_fails_when_train_full(self):
        # Arrange: fill the only seat
        self.booking_service.book_ticket(
            self.passenger.passenger_id, self.train.train_id, 500, TravelClass.SLEEPER, 10
        )
        # Act + Assert: the *next* booking should raise
        with self.assertRaises(SeatUnavailableError):
            self.booking_service.book_ticket(
                self.passenger.passenger_id, self.train.train_id, 500, TravelClass.SLEEPER, 10
            )

    def test_cancel_refunds_seat(self):
        booking = self.booking_service.book_ticket(
            self.passenger.passenger_id, self.train.train_id, 500, TravelClass.SLEEPER, 10
        )
        self.booking_service.cancel_booking(booking.booking_id, days_before_departure=5)

        self.assertEqual(self.train.available_seats, 1)
        self.assertEqual(booking.status, "CANCELLED")

    def test_cancel_gives_full_refund_rate_for_early_cancellation(self):
        booking = self.booking_service.book_ticket(
            self.passenger.passenger_id, self.train.train_id, 500, TravelClass.SLEEPER, 10
        )
        refund = self.booking_service.cancel_booking(booking.booking_id, days_before_departure=5)

        self.assertAlmostEqual(refund, booking.fare * 0.90, places=2)


if __name__ == "__main__":
    unittest.main()
```

Run it with:

```bash
python -m unittest tests/test_booking.py -v
```

### Key ideas here

- **`setUp()`** runs fresh before *every* single test method, so tests
  never leak state into each other — `test_cancel_refunds_seat` starts with
  a brand new train with 1 free seat, unaffected by anything the previous
  test did.
- **One behavior per test**, with a descriptive method name
  (`test_booking_fails_when_train_full`) that reads almost like a sentence.
  When this test fails later, the name alone tells you what broke, before
  you even read the code.
- **`assertRaises`** as a context manager (`with self.assertRaises(...)`)
  is how you test that an exception *should* happen — the test only passes
  if that exception is actually raised inside the `with` block.
- **`assertAlmostEqual`** instead of `assertEqual` for the refund check —
  floating-point math can produce tiny rounding differences
  (`449.99999999` vs `450.0`), so comparing "close enough" (to a number of
  decimal places) is the correct way to test money/float calculations.
- **Tests document behavior.** Reading through `test_booking.py` top to
  bottom tells a new developer exactly what the booking system is supposed
  to do — often more reliably than a written spec, because tests can't
  silently go out of date without failing.

## Why this matters for a beginner→intermediate jump

Beginners test by manually running code and eyeballing the output.
Intermediate developers write tests once and re-run them in seconds after
every change — this is what makes it *safe* to refactor code (like
Module 07's fare rules) without fear of silently breaking something else.

## Try it yourself

1. Run the test file above and confirm all 4 tests pass.
2. Intentionally break something (e.g., remove the `train.booked_seats -= 1`
   line from `cancel_booking`) and re-run the tests — confirm
   `test_cancel_refunds_seat` now fails, proving the test actually catches
   the bug.
3. **Challenge:** write a new test,
   `test_cancel_gives_no_refund_on_last_minute_cancellation`, that checks
   `days_before_departure=0` results in a refund of `0.0`.

**Next:** `14_final_project_full_source_code.md`
