# 🚆 Railway Booking System — A Python Learning Project

This folder is a step-by-step course that builds a **console-based Railway
Ticket Booking System** in Python, one concept at a time. Each `.md` file
covers a single topic: a real-world **scenario**, the **logic** behind the
solution, and **working Python code** you can copy, run, and modify.

It's aimed at learners who know basic Python syntax (variables, loops, `if`)
and want to move from **beginner → intermediate** by building something real,
instead of solving isolated exercises.

## How to use this folder

1. Go through the files **in numeric order** — each module builds on the
   code from the previous one.
2. Type the code out yourself instead of copy-pasting — it sticks better.
3. Every file ends with **"Try it yourself"** exercises. Do them before
   moving on.
4. By the end (`14_final_project_full_source_code.md`) you'll have a
   complete, runnable railway booking application.

## Roadmap

| # | File | Concept Focus |
|---|------|----------------|
| 01 | `01_introduction_and_requirements.md` | Understanding the problem, requirements gathering |
| 02 | `02_setup_and_project_structure.md` | Project structure, planning modules |
| 03 | `03_oop_basics_station_and_train.md` | Classes, objects, `__init__`, `__str__` |
| 04 | `04_passenger_class_and_management.md` | Classes with lists, CRUD operations |
| 05 | `05_train_schedule_and_search.md` | Lists of objects, searching/filtering |
| 06 | `06_seat_availability_and_booking_logic.md` | State management, core booking logic |
| 07 | `07_fare_calculation.md` | Functions, conditionals, calculations |
| 08 | `08_ticket_generation.md` | Combining objects, formatted output, unique IDs |
| 09 | `09_cancellation_and_refund.md` | Business rules, refund policies |
| 10 | `10_file_handling_json_persistence.md` | Saving/loading data with JSON |
| 11 | `11_exception_handling_and_validation.md` | try/except, input validation |
| 12 | `12_cli_menu_integration.md` | Tying everything into a menu-driven app |
| 13 | `13_unit_testing.md` | Testing your logic with `unittest` |
| 14 | `14_final_project_full_source_code.md` | The complete, assembled application |

## The scenario used throughout

You're building the backend logic for **"PyRail"**, a small railway booking
service. It needs to:

- Store trains, their routes, schedule, and seat capacity
- Let passengers search trains between two stations
- Book a seat, generate a ticket with a fare
- Cancel a ticket and process a refund based on how early it was cancelled
- Persist all data to disk so it isn't lost when the program closes
- Handle bad input gracefully instead of crashing

Every module solves one piece of this system.

## Prerequisites

- Python 3.9+
- No external libraries — everything uses the standard library
  (`json`, `datetime`, `uuid`, `unittest`)

Start with `01_introduction_and_requirements.md`.
