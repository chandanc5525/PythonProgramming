# 12 — CLI Menu Integration

## Scenario

Every piece exists now: models, train search, booking, fares, tickets,
cancellation, persistence, validation. It's time to give a human a way to
use all of it — a menu-driven command-line loop.

## Logic: the "controller" that connects UI to services

`main.py` should be thin. Its only job is: show a menu, read input,
validate it, call the right service, print the result. **All actual logic
stays in the service classes** — `main.py` never computes a fare or checks
seat counts itself. This separation means you could later swap the CLI for
a web interface without touching any business logic.

```python
# main.py

from models import Station, Train
from train_service import TrainService
from passenger_service import PassengerService
from booking_service import (
    BookingService, SeatUnavailableError,
    BookingNotFoundError, AlreadyCancelledError,
)
from fare_service import calculate_fare, TravelClass
from ticket_service import generate_ticket
from validators import validate_non_empty_string, validate_positive_int


def seed_demo_data(train_service: TrainService) -> None:
    """Preload a couple of trains so the menu has something to search."""
    delhi = Station("NDLS", "New Delhi")
    mumbai = Station("BCT", "Mumbai Central")
    jaipur = Station("JP", "Jaipur")

    train_service.add_train(Train("12951", "Rajdhani Express", delhi, mumbai, "16:00", 5))
    train_service.add_train(Train("12952", "Duronto Express", delhi, jaipur, "09:00", 3))


def print_menu():
    print("""
--- PyRail Menu ---
1. Search trains
2. Register passenger
3. Book a ticket
4. Cancel a booking
5. Exit
""")


def main():
    train_service = TrainService()
    passenger_service = PassengerService()
    booking_service = BookingService(train_service, passenger_service)
    seed_demo_data(train_service)

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            source = input("From station code: ").strip().upper()
            dest = input("To station code: ").strip().upper()
            results = train_service.search(source, dest)
            if not results:
                print("No trains found for that route.")
            for train in results:
                print(train)

        elif choice == "2":
            try:
                name = validate_non_empty_string(input("Name: "), "Name")
                age = validate_positive_int(input("Age: "), "Age")
                gender = validate_non_empty_string(input("Gender: "), "Gender")
                contact = validate_non_empty_string(input("Contact: "), "Contact")
                passenger = passenger_service.register(name, age, gender, contact)
                print(f"Registered! Your passenger ID is {passenger.passenger_id}")
            except ValueError as e:
                print(f"Invalid input — {e}")

        elif choice == "3":
            try:
                passenger_id = validate_non_empty_string(input("Passenger ID: "), "Passenger ID")
                train_id = validate_non_empty_string(input("Train ID: "), "Train ID")
                distance = validate_positive_int(input("Distance (km): "), "Distance")
                days_left = validate_positive_int(input("Days before departure: "), "Days before departure")
                booking = booking_service.book_ticket(
                    passenger_id, train_id, distance, TravelClass.SLEEPER, days_left
                )
                print(generate_ticket(booking))
            except (SeatUnavailableError, ValueError) as e:
                print(f"Booking failed — {e}")

        elif choice == "4":
            try:
                booking_id = validate_non_empty_string(input("Booking ID: "), "Booking ID")
                days_left = validate_positive_int(input("Days before departure: "), "Days before departure")
                refund = booking_service.cancel_booking(booking_id, days_left)
                print(f"Cancelled. Refund amount: Rs. {refund:.2f}")
            except (BookingNotFoundError, AlreadyCancelledError, ValueError) as e:
                print(f"Cancellation failed — {e}")

        elif choice == "5":
            print("Thanks for using PyRail. Goodbye!")
            break

        else:
            print("Invalid option, please choose 1-5.")


if __name__ == "__main__":
    main()
```

### Key ideas here

- **`if __name__ == "__main__":`** — this guard means `main()` only runs
  when you execute `python main.py` directly, not if some other file
  imports something from `main.py`. Standard Python practice for any
  runnable script.
- **The menu loop is a `while True` with an explicit `break`** on exit,
  rather than tracking a separate "should I keep running" boolean — a
  common, readable pattern for menu-driven programs.
- **Every risky action is wrapped in `try/except`** right where the user
  input happens, catching only the exception types that operation can
  realistically raise (Module 11's principle in action).
- **`seed_demo_data`** exists purely so you have something to search/book
  immediately, without manually typing train data every time you run the
  program. In Module 10's persistence, you'd load real saved data instead.

## Try it yourself

1. Run `main.py`, register a passenger, search a route, and book a ticket
   using the menu — confirm you see a formatted ticket.
2. Try booking with a train ID that doesn't exist — confirm you get a clean
   error message, not a crash.
3. **Challenge:** add a "6. Save & load data" option that calls the
   `save_trains` / `load_trains` functions from Module 10 so the seeded
   trains (plus any seat changes from bookings) persist between runs.

**Next:** `13_unit_testing.md`
