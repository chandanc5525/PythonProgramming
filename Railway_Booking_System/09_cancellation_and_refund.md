# 09 — Cancellation & Refund

## Scenario

A passenger wants to cancel booking `8f3a1c9d`. PyRail's refund policy:

- Cancel **more than 3 days** before departure → 90% refund
- Cancel **1–3 days** before departure → 50% refund
- Cancel **less than 1 day** before departure → no refund
- Can't cancel a booking that's already cancelled

This is a classic case of **business rules expressed as branching logic**.

## Logic: implementing the refund policy

```python
# booking_service.py (add to BookingService)

class BookingNotFoundError(Exception):
    pass


class AlreadyCancelledError(Exception):
    pass


class BookingService:
    # ... book_ticket() from Module 06 ...

    def cancel_booking(self, booking_id: str, days_before_departure: int) -> float:
        booking = self._bookings.get(booking_id)
        if booking is None:
            raise BookingNotFoundError(f"No booking with ID {booking_id}")

        if booking.status == "CANCELLED":
            raise AlreadyCancelledError(
                f"Booking {booking_id} is already cancelled"
            )

        refund_amount = self._calculate_refund(booking.fare, days_before_departure)

        booking.status = "CANCELLED"
        booking.train.booked_seats -= 1   # free up the seat

        return refund_amount

    @staticmethod
    def _calculate_refund(fare: float, days_before_departure: int) -> float:
        if days_before_departure > 3:
            refund_rate = 0.90
        elif days_before_departure >= 1:
            refund_rate = 0.50
        else:
            refund_rate = 0.0
        return round(fare * refund_rate, 2)
```

### Key ideas here

- **Two specific exceptions** (`BookingNotFoundError`,
  `AlreadyCancelledError`) instead of one generic `Exception`. This lets
  the calling code (the CLI in Module 12) show a precise, helpful message
  for each situation instead of a vague "something went wrong."
- **`@staticmethod`** on `_calculate_refund` — this method doesn't need
  `self` (it doesn't touch any booking service state), so marking it static
  signals "this is a pure calculation, not tied to a specific service
  instance." It could just as easily be a free function outside the class
  — using a static method here just keeps related logic grouped together.
- **Freeing the seat**: `booking.train.booked_seats -= 1` is the mirror
  image of `book_ticket`'s `+= 1`. Whenever you increment a shared counter
  in one place, ask "where's the corresponding decrement?" — forgetting
  this is a very common bug (seats would appear permanently taken even
  after cancellation).
- **Order of checks matters again**: verify the booking exists → verify
  it isn't already cancelled → *then* calculate refund and mutate state.
  Same principle as Module 06's booking logic.

## Try it yourself

1. Book a ticket, then cancel it with `days_before_departure=5` — confirm
   you get 90% of the fare back and `train.available_seats` goes back up
   by 1.
2. Try cancelling the same booking again — confirm `AlreadyCancelledError`
   is raised.
3. **Challenge:** what if `days_before_departure` is negative (the train
   already departed)? Update `_calculate_refund` to treat that the same as
   "less than 1 day" (no refund), and add a comment explaining why.

**Next:** `10_file_handling_json_persistence.md`
