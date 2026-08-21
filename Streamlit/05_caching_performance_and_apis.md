# 05 — Caching, Performance & Connecting to APIs/Databases

## 🎯 What You'll Learn
- Why the rerun model can silently make your app slow
- `st.cache_data` vs `st.cache_resource` — what each is for and why they're different
- Fetching live data from an external API or database safely

---

## 📌 The Scenario

PyRail Dashboards now loads a 500,000-row CSV of historical bookings and calls a live currency-conversion API to show fares in USD. On the first load this takes 4 seconds. The problem: because of the rerun model (Module 01), **that 4-second load re-executes every time the user touches any widget on the page** — including something as trivial as toggling a checkbox. Users will not tolerate a 4-second freeze on every click.

---

## 🧠 Logic: Two Kinds of Expensive Things

Streamlit distinguishes between two categories of "expensive" operations, because they need to be cached differently:

| Category | Example | Decorator |
|---|---|---|
| **Data** — something you compute and can serialize/copy | Loading a CSV, querying an API, running a groupby | `@st.cache_data` |
| **Resource** — something that should exist as a single shared object | A DB connection, a loaded ML model, a thread pool | `@st.cache_resource` |

The core reasoning: `st.cache_data` returns a **new copy** of the cached value to each caller, so it's safe for mutable objects like DataFrames (one script accidentally mutating the cached DataFrame won't corrupt what other sessions see). `st.cache_resource` returns the **exact same object** every time — appropriate (and necessary) for things like a database connection, which you *want* shared, not copied.

---

## 💻 Caching Expensive Data Loading

```python
import streamlit as st
import pandas as pd
import time

@st.cache_data
def load_bookings(path: str) -> pd.DataFrame:
    time.sleep(4)  # simulate a slow load
    return pd.read_csv(path)

st.title("PyRail Dashboards")
df = load_bookings("data/bookings_history.csv")
st.write(f"Loaded {len(df):,} rows.")
st.dataframe(df.head())
```

### 🔍 Logic Behind the Code

- The first time `load_bookings("data/bookings_history.csv")` runs, Streamlit executes the function body (the full 4-second sleep + read), then stores the result **keyed by the function's arguments**.
- On every subsequent rerun — no matter what widget the user touched — calling `load_bookings("data/bookings_history.csv")` **again** with the *same argument* returns the cached result instantly, skipping the function body entirely.
- If you call it with a *different* `path`, that's treated as a cache miss, and it runs (and caches) fresh — the cache key is derived from the function's inputs, not just its name.
- This is why writing "expensive setup code directly at the top of your script" is a Streamlit anti-pattern — always wrap it in a `@st.cache_data` function instead.

---

## 💻 Caching a Shared Resource (DB Connection)

```python
import streamlit as st
import sqlite3

@st.cache_resource
def get_connection():
    return sqlite3.connect("pyrail.db", check_same_thread=False)

conn = get_connection()
bookings = pd.read_sql("SELECT * FROM bookings WHERE status = 'Confirmed'", conn)
st.dataframe(bookings)
```

### 🔍 Logic Behind the Code

- `check_same_thread=False` is needed because Streamlit may serve widget interactions from a different thread than the one that created the connection — a detail specific to how Streamlit's server dispatches script reruns.
- Using `@st.cache_data` here (instead of `@st.cache_resource`) would be a bug: SQLite connection objects generally aren't safely copyable/picklable, and even if they were, you'd end up opening a *new* connection every cache key lookup instead of reusing one — defeating the purpose and potentially exhausting connections under load.

---

## 💻 Cache Expiry & Manual Invalidation

```python
@st.cache_data(ttl=300)  # cache expires after 5 minutes
def get_live_fx_rate(base="USD", target="INR"):
    import requests
    resp = requests.get(f"https://api.exchangerate.host/latest?base={base}&symbols={target}")
    return resp.json()["rates"][target]

rate = get_live_fx_rate()
st.metric("USD → INR", f"₹{rate:.2f}")

if st.button("Force refresh rate"):
    get_live_fx_rate.clear()   # wipes this function's cache
    st.rerun()
```

### 🔍 Logic Behind the Code

- `ttl=300` (time-to-live, in seconds) means Streamlit automatically treats the cached value as stale after 5 minutes and re-runs the function on the next call — appropriate for data that changes slowly but does change (exchange rates, weather, leaderboards).
- `.clear()` is a method Streamlit attaches to every `@st.cache_data`-decorated function, letting you manually invalidate its cache — useful for an explicit "Refresh" button rather than waiting on the TTL.
- `st.rerun()` forces an immediate script rerun from inside the callback — necessary here because clearing the cache alone doesn't re-display anything; the script needs to actually run again to call `get_live_fx_rate()` a second time and show the new value.

---

## 💻 Showing Progress on Long Operations

```python
import streamlit as st
import time

if st.button("Run nightly reconciliation"):
    progress = st.progress(0, text="Starting...")
    for i in range(1, 101):
        time.sleep(0.02)
        progress.progress(i, text=f"Reconciling batch {i}/100")
    progress.empty()
    st.success("Reconciliation complete.")
```

- `st.progress(i, text=...)` **mutates the existing progress element in place** rather than creating a new one each loop iteration — this is one of the few Streamlit patterns that behaves like "traditional" imperative UI updates, made possible because you're holding a reference (`progress`) to the specific element returned when it was first created.
- `.empty()` clears that element from the page once the work is done, so a completed progress bar doesn't linger.

---

## 📝 Try It Yourself

1. Wrap a `pd.read_csv` call for a large file in `@st.cache_data` and time the difference (using `time.time()`) between the first and second load.
2. Deliberately cache a mutable object (a list) with `@st.cache_data`, mutate the *returned* list in your script, then call the cached function again — confirm the cache wasn't corrupted (this demonstrates the "copy" behavior).
3. Build a small live-data widget: cache a call to any free public API (e.g., a joke API, a weather API) with `ttl=60`, and add a manual "Refresh now" button using `.clear()`.

**Next up:** `06_file_handling_and_multipage_apps.md` — uploads/downloads and structuring a real multi-page application.
