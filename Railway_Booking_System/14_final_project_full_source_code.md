# 14 — Final Project: The Complete Source Code

## Scenario

You've built PyRail piece by piece across 13 modules. This file assembles
everything into the final file layout so you can run the whole system
end-to-end. Create each file below in your `railway_booking_system/`
project folder (from Module 02) exactly as shown.

```
railway_booking_system/
├── models.py
├── train_service.py
├── passenger_service.py
├── fare_service.py
├── booking_service.py
├── ticket_service.py
├── validators.py
├── storage.py
├── main.py
├── data/
└── tests/
    └── test_booking.py
```

---

### `models.py`

```python
class Station:
    def __init__(self, code: str, name: str):
        self.code = code
        self.name = name

    def __str__(self):
        return f"{self.name} ({self.code})"

    def to_dict(self):
        return {"code": self.code, "name": self.name}

    @staticmethod
    def from_dict(data):
        return Station(data["code"], data["name"])


class Train:
    def __init__(self, train_id: str, name: str, source: Station,
                 destination: Station, departure_time: str, total_seats: int):
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
        return (f"[{self.train_id}] {self.name}: {self.source} -> "
                f"{self.destination} at {self.departure_time} "
                f"({self.available_seats}/{self.total_seats} seats free)")

    def to_dict(self):
        return {
            "train_id": self.train_id, "name": self.name,
            "source": self.source.to_dict(),
            "destination": self.destination.to_dict(),
            "departure_time": self.departure_time,
            "total_seats": self.total_seats,
            "booked_seats": self.booked_seats,
        }

    @staticmethod
    def from_dict(data):
        train = Train(data["train_id"], data["name"],
                       Station.from_dict(data["source"]),
                       Station.from_dict(data["destination"]),
                       data["departure_time"], data["total_seats"])
        train.booked_seats = data["booked_seats"]
        return train


class Passenger:
    def __init__(self, passenger_id: str, name: str, age: int, gender: str, contact: str):
        self.passenger_id = passenger_id
        self.name = name
        self.age = age
        self.gender = gender
        self.contact = contact

    def __str__(self):
        return f"{self.name} ({self.age}, {self.gender}) - ID: {self.passenger_id}"

    def to_dict(self):
        return {"passenger_id": self.passenger_id, "name": self.name,
                "age": self.age, "gender": self.gender, "contact": self.contact}

    @staticmethod
    def from_dict(data):
        return Passenger(data["passenger_id"], data["name"], data["age"],
                          data["gender"], data["contact"])


class Booking:
    def __init__(self, booking_id: str, passenger: Passenger, train: Train,
                 seat_number: int, fare: float, status: str = "CONFIRMED"):
        self.booking_id = booking_id
        self.passenger = passenger
        self.train = train
        self.seat_number = seat_number
        self.fare = fare
        self.status = status

    def __str__(self):
        return (f"Booking {self.booking_id} - {self.passenger.name} - "
                f"Seat {self.seat_number} on {self.train.name} "
                f"- Rs.{self.fare} - {self.status}")
```

---

### `passenger_service.py`

```python
import uuid
from models import Passenger


class PassengerService:
    def __init__(self):
        self._passengers: dict[str, Passenger] = {}

    def register(self, name: str, age: int, gender: str, contact: str) -> Passenger:
        passenger_id = str(uuid.uuid4())[:8]
        passenger = Passenger(passenger_id, name, age, gender, contact)
        self._passengers[passenger_id] = passenger
        return passenger

    def get(self, passenger_id: str):
        return self._passengers.get(passenger_id)

    def all_passengers(self):
        return list(self._passengers.values())
```

---

### `train_service.py`

```python
from models import Train


class TrainService:
    def __init__(self):
        self._trains: dict[str, Train] = {}

    def add_train(self, train: Train) -> None:
        self._trains[train.train_id] = train

    def get_train(self, train_id: str):
        return self._trains.get(train_id)

    def search(self, source_code: str, destination_code: str):
        return [
            t for t in self._trains.values()
            if t.source.code == source_code and t.destination.code == destination_code
        ]

    def all_trains(self):
        return list(self._trains.values())
```

---

### `fare_service.py`

```python
from enum import Enum


class TravelClass(Enum):
    GENERAL = "GENERAL"
    SLEEPER = "SLEEPER"
    AC = "AC"


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

    if days_before_departure <= 1:
        base_fare *= 1.25
    elif days_before_departure <= 3:
        base_fare *= 1.10

    return round(max(base_fare, 50.0), 2)
```

---

### `booking_service.py`

```python
import uuid
from models import Booking
from fare_service import calculate_fare, TravelClass


class SeatUnavailableError(Exception):
    pass


class BookingNotFoundError(Exception):
    pass


class AlreadyCancelledError(Exception):
    pass


class BookingService:
    def __init__(self, train_service, passenger_service):
        self.train_service = train_service
        self.passenger_service = passenger_service
        self._bookings: dict[str, Booking] = {}

    def book_ticket(self, passenger_id: str, train_id: str, distance_km: float,
                     travel_class: TravelClass, days_before_departure: int) -> Booking:
        passenger = self.passenger_service.get(passenger_id)
        if passenger is None:
            raise ValueError(f"No passenger with ID {passenger_id}")

        train = self.train_service.get_train(train_id)
        if train is None:
            raise ValueError(f"No train with ID {train_id}")

        if train.available_seats <= 0:
            raise SeatUnavailableError(f"Train {train.name} is fully booked.")

        fare = calculate_fare(distance_km, travel_class, days_before_departure)

        train.booked_seats += 1
        seat_number = train.booked_seats

        booking_id = str(uuid.uuid4())[:8]
        booking = Booking(booking_id, passenger, train, seat_number, fare)
        self._bookings[booking_id] = booking
        return booking

    def get_booking(self, booking_id: str):
        return self._bookings.get(booking_id)

    def cancel_booking(self, booking_id: str, days_before_departure: int) -> float:
        booking = self._bookings.get(booking_id)
        if booking is None:
            raise BookingNotFoundError(f"No booking with ID {booking_id}")
        if booking.status == "CANCELLED":
            raise AlreadyCancelledError(f"Booking {booking_id} is already cancelled")

        refund_amount = self._calculate_refund(booking.fare, days_before_departure)
        booking.status = "CANCELLED"
        booking.train.booked_seats -= 1
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

---

### `ticket_service.py`

```python
from models import Booking


def generate_ticket(booking: Booking) -> str:
    train = booking.train
    passenger = booking.passenger
    lines = [
        "=" * 40,
        "          PYRAIL - E-TICKET",
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

---

### `validators.py`

```python
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

---

### `storage.py`

```python
import json
from models import Train

DATA_FILE = "data/trains.json"


def save_trains(trains, path: str = DATA_FILE) -> None:
    data = [train.to_dict() for train in trains]
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_trains(path: str = DATA_FILE):
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    return [Train.from_dict(item) for item in data]
```

---

### `main.py`

```python
from models import Station, Train
from train_service import TrainService
from passenger_service import PassengerService
from booking_service import (
    BookingService, SeatUnavailableError,
    BookingNotFoundError, AlreadyCancelledError,
)
from fare_service import TravelClass
from ticket_service import generate_ticket
from validators import validate_non_empty_string, validate_positive_int


def seed_demo_data(train_service: TrainService) -> None:
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
                print(f"Invalid input - {e}")

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
                print(f"Booking failed - {e}")

        elif choice == "4":
            try:
                booking_id = validate_non_empty_string(input("Booking ID: "), "Booking ID")
                days_left = validate_positive_int(input("Days before departure: "), "Days before departure")
                refund = booking_service.cancel_booking(booking_id, days_left)
                print(f"Cancelled. Refund amount: Rs. {refund:.2f}")
            except (BookingNotFoundError, AlreadyCancelledError, ValueError) as e:
                print(f"Cancellation failed - {e}")

        elif choice == "5":
            print("Thanks for using PyRail. Goodbye!")
            break

        else:
            print("Invalid option, please choose 1-5.")


if __name__ == "__main__":
    main()
```

---

### `tests/test_booking.py`

See the full listing in `13_unit_testing.md` — copy it as-is into
`tests/test_booking.py`. You'll also need an empty `tests/__init__.py` (or
run tests with `python -m unittest discover`).

---

## Running the project

```bash
cd railway_booking_system
python main.py
```

Run the tests:

```bash
python -m unittest tests/test_booking.py -v
```

## Where to go from here

You now have a working, tested, persistable railway booking system built
from first principles. Natural next steps, roughly in order of difficulty:

1. **Wire up `storage.py`** fully into `main.py` — load trains at startup,
   save on exit (Module 10's "try it yourself" challenge).
2. **Add multiple travel classes** to the booking flow instead of hardcoding
   `TravelClass.SLEEPER` in `main.py`.
3. **Add seat-level detail** — instead of just a seat *number*, track which
   individual seats are taken so cancellations free the *specific* seat, not
   just decrement a counter.
4. **Move to a real database** (SQLite is a good next step — still no
   server to install) instead of JSON files, using the same
   `to_dict`/`from_dict` conversion ideas.
5. **Build a simple web interface** using Flask, reusing every service class
   here unchanged — this is the payoff of keeping business logic separate
   from the CLI in Module 12.

Congratulations — you've gone from beginner Python syntax to a structured,
tested, intermediate-level application.
