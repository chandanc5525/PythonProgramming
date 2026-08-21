# 04 — Session State & Forms

## What You'll Learn
- Why widget values normally "forget themselves" between logical steps
- `st.session_state`: Streamlit's per-user persistent dictionary
- `st.form` for batching multiple inputs into a single rerun
- Callbacks (`on_click`, `on_change`)

---

## The Scenario

You're building a **multi-step booking flow**: Step 1 collects passenger details, Step 2 collects seat preference, Step 3 shows a summary and a "Confirm Booking" button. The problem: every widget interaction reruns the *entire* script from top to bottom. Without something to hold state between reruns, you'd lose Step 1's answers the moment the user touches Step 2.

---

## Logic: Why State Is a Problem in the Rerun Model

Recall from Module 01: Streamlit reruns your whole script on every interaction, and local Python variables are **recreated from scratch** each time. A line like:

```python
cart_total = 0
```

resets `cart_total` back to `0` on *every single rerun* — it can never accumulate across interactions on its own. You need a place to store values that **survives** across reruns, scoped to that one user's browser session. That's `st.session_state`.

```python
import streamlit as st

st.session_state.setdefault("cart_total", 0)

if st.button("Add ₹100 fare"):
    st.session_state.cart_total += 100

st.write(f"Cart total: ₹{st.session_state.cart_total}")
```

### Logic Behind the Code

- `st.session_state` behaves like a Python `dict` (with attribute-style access too: `st.session_state.cart_total` is equivalent to `st.session_state["cart_total"]`), but it's **created once per browser session** and persists across reruns until the tab is closed or the app is manually reset.
- `.setdefault("cart_total", 0)` initializes the key **only if it doesn't already exist** — critical, because on every rerun this line executes again, and you don't want to wipe the accumulated value back to `0` each time.
- Clicking the button increments the *persisted* value, not a local variable — so the increment survives into the next rerun, and the one after that.

---

## Multi-Step Flow Using Session State

```python
import streamlit as st

st.session_state.setdefault("step", 1)
st.session_state.setdefault("passenger", {})

def go_to(step):
    st.session_state.step = step

if st.session_state.step == 1:
    st.header("Step 1: Passenger Details")
    name = st.text_input("Name", value=st.session_state.passenger.get("name", ""))
    age = st.number_input("Age", min_value=1, max_value=120,
                           value=st.session_state.passenger.get("age", 25))
    if st.button("Next →"):
        st.session_state.passenger = {"name": name, "age": age}
        go_to(2)

elif st.session_state.step == 2:
    st.header("Step 2: Seat Preference")
    seat = st.radio("Preference", ["Window", "Aisle", "No preference"])
    if st.button("Next →"):
        st.session_state.passenger["seat"] = seat
        go_to(3)
    if st.button("← Back"):
        go_to(1)

elif st.session_state.step == 3:
    st.header("Step 3: Confirm")
    st.write(st.session_state.passenger)
    if st.button("Confirm Booking"):
        st.success("Booking confirmed!")
        go_to(1)
        st.session_state.passenger = {}
```

### Logic Behind the Code

- `st.session_state.step` acts as a **finite state machine's current state** — the entire script becomes one big `if/elif` dispatcher based on that value, and each rerun re-evaluates which branch to show. This is the standard pattern for wizards, multi-page-feeling flows, and "confirm before submit" UIs.
- Notice `value=st.session_state.passenger.get("name", "")` on the `text_input` — pre-filling widgets with previously stored values so that going "← Back" doesn't lose what the user already typed.
- Calling `go_to(2)` mutates `st.session_state.step` and then the script naturally reruns (Streamlit reruns automatically after any widget interaction like a button click) — you don't need to manually call anything like `st.rerun()` here, though that function exists for cases where you want to force an immediate rerun from inside a callback.

---

## Forms: Batching Inputs Into One Rerun

Without a form, *each* widget interaction triggers its own rerun — meaning typing in a text box, then clicking a checkbox, then adjusting a slider fires **three separate reruns**. For a big form, that's wasteful and can feel janky (partial validation errors flashing, etc). `st.form` batches everything into a single rerun, triggered only by its submit button.

```python
import streamlit as st

with st.form("booking_form"):
    st.subheader("Book in One Go")
    name = st.text_input("Passenger name")
    travel_class = st.selectbox("Class", ["Sleeper", "AC 3-Tier", "AC 2-Tier"])
    insurance = st.checkbox("Add insurance")

    submitted = st.form_submit_button("Book Now")

if submitted:
    if not name:
        st.error("Name is required.")
    else:
        st.success(f"Booked {travel_class} for {name}" + (" with insurance." if insurance else "."))
```

### Logic Behind the Code

- Every widget inside `with st.form(...)`: **freezes** its value locally until `st.form_submit_button` is pressed — no reruns happen from individual keystrokes or selections inside the form.
- `submitted` is `True` only on the rerun where the submit button was clicked — identical semantics to a regular `st.button`, but now guaranteed to reflect *all* the form's fields simultaneously and consistently, avoiding the "half-filled state" problem you'd get validating field-by-field outside a form.

---

## Callbacks: `on_click` and `on_change`

```python
import streamlit as st

st.session_state.setdefault("log", [])

def record_change():
    st.session_state.log.append(st.session_state.route_choice)

st.selectbox(
    "Route",
    ["Mumbai–Delhi", "Chennai–Bangalore"],
    key="route_choice",
    on_change=record_change,
)

st.write("Selection history:", st.session_state.log)
```

### Logic Behind the Code

- `key="route_choice"` registers this widget's value **directly into `st.session_state`** under that name — you can read `st.session_state.route_choice` anywhere else in the script, and it's automatically kept in sync.
- `on_change=record_change` runs `record_change` **before** the main script body reruns, whenever this specific widget's value changes — useful for logging, side effects, or updating *other* session_state keys in response to one widget, without needing an `if` check to detect "did this widget just change."

---

## Try It Yourself

1. Extend the 3-step wizard with a 4th step that lets the user pick a payment method, stored in `st.session_state.passenger["payment"]`.
2. Convert the booking form to also compute and display a fare total *inside* the form, live, as the user picks a class — then explain in a comment why this is tricky with `st.form` (hint: forms don't rerun on every widget change, so "live" updates need `on_change` outside a form, or an `st.form_submit_button` inside).
3. Add a `st.button("Reset")` outside the form that clears `st.session_state` entirely using `st.session_state.clear()`.

**Next up:** `05_caching_performance_and_apis.md` — avoiding redundant work on every rerun, and pulling in live data.
