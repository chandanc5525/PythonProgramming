# 01 — Introduction & Requirements

## Scenario

You've been asked to build the backend for **PyRail**, a small railway
booking system. Before writing a single line of code, a good developer
always asks: *"What exactly does this system need to do?"*

Jumping straight to code without this step is the #1 reason beginner
projects turn into a tangled mess.

## Logic: turning a vague idea into requirements

"Build a railway booking system" is vague. We break it down into concrete,
testable pieces — this is called **requirements gathering**.

### Entities (the "nouns" in our system)

| Entity | What it represents |
|---|---|
| `Station` | A place a train stops (name, code) |
| `Train` | A train with a route, schedule, and total seats |
| `Passenger` | A person who books a ticket |
| `Booking` | A record linking a passenger to a train + seat + fare |

### Actions (the "verbs" — what the system must do)

1. Add/view trains and their routes
2. Search for trains between a source and destination
3. Check seat availability on a train
4. Book a ticket for a passenger (if seats are available)
5. Calculate the fare for a booking
6. Generate a ticket (a receipt) for a confirmed booking
7. Cancel a booking and calculate a refund
8. Save data so it survives a program restart
9. Handle invalid input (wrong station name, no seats left, etc.) without
   crashing

### Non-functional expectations

- Should run as a **command-line program** (no GUI needed for this project)
- Should use **only the Python standard library**
- Code should be organized into small, testable pieces — not one giant file

## Why we build it this way

Notice the actions map almost one-to-one to the modules in this course:

```
Requirements  →  Module
--------------------------------------------------
Station/Train modeling  →  03
Passenger modeling      →  04
Search trains           →  05
Seat availability       →  06
Fare calculation        →  07
Ticket generation       →  08
Cancellation/refund     →  09
Persistence             →  10
Error handling          →  11
Putting it together     →  12
```

This is a real habit professional developers use: **requirements drive
design, design drives code** — not the other way around.

## Try it yourself

Before moving to Module 2, write down (on paper or in a text file) your own
one-line answer to each:

1. What information does a `Train` need to have?
2. What information does a `Passenger` need to have?
3. What should happen if someone tries to book a seat on a full train?
4. What should happen if someone tries to cancel a ticket 2 minutes before
   departure vs. 2 days before?

There's no wrong answer yet — you'll compare your list to the design used
in the next modules.

**Next:** `02_setup_and_project_structure.md`
