# PyRail — Railway Booking System (A Python Learning Project)

A step-by-step course that builds a **console-based Railway Ticket Booking System** in Python, one concept at a time. Each module covers a single topic through a real-world **scenario**, the **logic** behind the solution, and **working Python code** you can copy, run, and modify.

This project is aimed at learners who already know basic Python syntax (variables, loops, `if` statements) and want to move from **beginner → intermediate** by building something real, rather than solving isolated exercises.

---

## About the Project

You're building the backend logic for **"PyRail,"** a small railway booking service. By the end of the course, your application will be able to:

- Store trains, their routes, schedules, and seat capacity
- Let passengers search for trains between two stations
- Book a seat and generate a ticket with a calculated fare
- Cancel a ticket and process a refund based on how early it was cancelled
- Persist all data to disk so nothing is lost when the program closes
- Handle bad input gracefully instead of crashing

Each module in the roadmap below solves one piece of this system, building toward a complete, working application.

---

## Roadmap

| # | File | Concept Focus |
|----|------|----------------|
| 01 | [`01_introduction_and_requirements.md`](./01_introduction_and_requirements.md) | Understanding the problem, requirements gathering |
| 02 | [`02_setup_and_project_structure.md`](./02_setup_and_project_structure.md) | Project structure, planning modules |
| 03 | [`03_oop_basics_station_and_train.md`](./03_oop_basics_station_and_train.md) | Classes, objects, `__init__`, `__str__` |
| 04 | [`04_passenger_class_and_management.md`](./04_passenger_class_and_management.md) | Classes with lists, CRUD operations |
| 05 | [`05_train_schedule_and_search.md`](./05_train_schedule_and_search.md) | Lists of objects, searching and filtering |
| 06 | [`06_seat_availability_and_booking_logic.md`](./06_seat_availability_and_booking_logic.md) | State management, core booking logic |
| 07 | [`07_fare_calculation.md`](./07_fare_calculation.md) | Functions, conditionals, calculations |
| 08 | [`08_ticket_generation.md`](./08_ticket_generation.md) | Combining objects, formatted output, unique IDs |
| 09 | [`09_cancellation_and_refund.md`](./09_cancellation_and_refund.md) | Business rules, refund policies |
| 10 | [`10_file_handling_json_persistence.md`](./10_file_handling_json_persistence.md) | Saving and loading data with JSON |
| 11 | [`11_exception_handling_and_validation.md`](./11_exception_handling_and_validation.md) | `try` / `except`, input validation |
| 12 | [`12_cli_menu_integration.md`](./12_cli_menu_integration.md) | Tying everything into a menu-driven app |
| 13 | [`13_unit_testing.md`](./13_unit_testing.md) | Testing your logic with `unittest` |
| 14 | [`14_final_project_full_source_code.md`](./14_final_project_full_source_code.md) | The complete, assembled application |

---

## How to Use This Folder

1. **Work through the files in numeric order.** Each module builds directly on the code from the one before it.
2. **Type the code out yourself** instead of copy-pasting — it sticks better.
3. **Complete the exercises.** Every file ends with a "Try it yourself" section — do these before moving on to the next module.
4. **Reach the final project.** By `14_final_project_full_source_code.md`, you'll have a complete, runnable railway booking application.

---

## Prerequisites

- Python 3.9+
- Basic familiarity with Python syntax (variables, loops, conditionals)
- No external libraries required — everything uses the standard library:
  - `json`
  - `datetime`
  - `uuid`
  - `unittest`

---

## 🏁 Getting Started

Clone or download this folder, then open the first module:

```bash
cd pyrail-booking-system
```

Start with [`01_introduction_and_requirements.md`](./01_introduction_and_requirements.md) and work your way through the roadmap above.

---

## License

This project is intended for educational use. Feel free to fork, adapt, and build on it for your own learning.