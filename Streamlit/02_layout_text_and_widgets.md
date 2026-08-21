# 02 — Layout, Text Elements & Core Widgets

## 🎯 What You'll Learn
- Structuring a page with columns, containers, sidebars, and tabs
- Every commonly used input widget and when to reach for it
- How widget **keys** and **default values** work

---

## 📌 The Scenario

You're building the front page of **PyRail Dashboards** — a booking-analytics tool. The page needs: a sidebar for filters, a title, a couple of KPI numbers side-by-side, and a tabbed view for "Today" vs "This Week" data. Doing this with raw HTML/CSS would take a while; Streamlit gives you layout primitives that map almost 1:1 to these ideas.

---

## 🧠 Logic: Layout Containers

Streamlit renders elements **in the order you call them**, top to bottom, in the "main" area — unless you explicitly place them inside a **layout container** (`st.sidebar`, `st.columns`, `st.tabs`, `st.expander`, `st.container`). Containers are just Python context managers or objects you can call methods on — they don't change the rerun model, only *where on the page* something appears.

```python
import streamlit as st

st.set_page_config(page_title="PyRail Dashboards", layout="wide")

st.title("🚆 PyRail Dashboards")

# --- Sidebar: filters live here, separate from main content ---
with st.sidebar:
    st.header("Filters")
    route = st.selectbox("Route", ["Mumbai–Delhi", "Chennai–Bangalore", "Kolkata–Pune"])
    date_range = st.date_input("Date range")

# --- KPI row using columns ---
col1, col2, col3 = st.columns(3)
col1.metric("Tickets Sold", "1,204", "+12%")
col2.metric("Revenue", "₹8.4L", "+5%")
col3.metric("Cancellations", "37", "-3%")

# --- Tabbed views ---
tab_today, tab_week = st.tabs(["Today", "This Week"])
with tab_today:
    st.write("Today's bookings go here.")
with tab_week:
    st.write("This week's bookings go here.")
```

### 🔍 Logic Behind the Code

- `st.set_page_config(layout="wide")` **must be the first Streamlit command** in the script — it configures the page shell itself, so Streamlit needs to know about it before rendering anything else.
- `st.sidebar` can be used either as a context manager (`with st.sidebar:`) or by calling methods directly on it (`st.sidebar.selectbox(...)`) — both produce identical results; the `with` form is preferred when you have several sidebar elements, for readability.
- `st.columns(3)` returns a list-like object of column containers of **equal width by default**. Calling `.metric()` (or any element function) *on* a column object routes that element into that column instead of the main flow.
- `st.metric(label, value, delta)` is purpose-built for KPI displays — the `delta` argument automatically colors green/red and adds an up/down arrow, which is exactly what dashboards need without any manual styling.
- `st.tabs(...)` returns one container per tab label; whatever you `with`-block into each tab only renders when that tab is active, but note — **all tabs' code still runs on every rerun**; Streamlit just hides the inactive tab's DOM. This matters once you start doing expensive work inside a tab (covered in the caching module).

---

## 💻 Core Input Widgets Reference

```python
import streamlit as st

st.subheader("Text & Numbers")
name = st.text_input("Passenger name", placeholder="e.g. Asha Rao")
notes = st.text_area("Special requests")
age = st.number_input("Age", min_value=0, max_value=120, value=30, step=1)

st.subheader("Choices")
travel_class = st.selectbox("Class", ["Sleeper", "AC 3-Tier", "AC 2-Tier", "AC First"])
amenities = st.multiselect("Amenities", ["Meal", "Blanket", "Window seat"])
gender = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)

st.subheader("Toggles & Ranges")
insurance = st.checkbox("Add travel insurance (₹20)")
priority_boarding = st.toggle("Priority boarding")
fare_range = st.slider("Fare budget (₹)", 200, 5000, (500, 2000))

st.subheader("Dates & Files")
travel_date = st.date_input("Travel date")
ticket_pdf = st.file_uploader("Upload existing ticket (optional)", type=["pdf"])

st.subheader("Actions")
if st.button("Search Trains"):
    st.success(f"Searching {travel_class} tickets for {name} on {travel_date}...")
```

### 🔍 Logic Behind the Code

- **Every widget function returns its current value directly** — there's no `.value` property or event object to unpack, unlike most GUI frameworks. This is possible *because* of the rerun model: by the time this line executes, Streamlit already knows what the user selected from the previous interaction.
- `st.slider(..., value=(500, 2000))` — passing a **tuple** as the default makes it a *range* slider (two handles) instead of a single-value slider. This overload-by-argument-type pattern is common across Streamlit's API.
- `st.button("Search Trains")` returns `True` **only on the exact rerun triggered by that click**, then reverts to `False` on the next rerun (e.g., if the user changes an unrelated widget afterward). This trips up beginners constantly — it's why `if st.button(...):` blocks shouldn't be relied on to "remember" that a click happened; that's what `st.session_state` (Module 04) is for.
- `st.file_uploader(..., type=["pdf"])` restricts the file picker and gives you a file-like object (`BytesIO`) you can pass straight into libraries like `pandas.read_csv` or `PyPDF2`.

---

## 📝 Try It Yourself

1. Build a "Book a Ticket" page: sidebar for filters (route, class), main area split into two columns — left for passenger details (name, age, gender), right for a fare summary using `st.metric`.
2. Add an `st.expander("Terms & Conditions")` containing a wall of text, collapsed by default.
3. Experiment: put an `st.write("Tab A code ran")` inside a tab that isn't currently selected. Switch to the other tab and check your terminal — does the message still print? What does this tell you about how tabs actually work under the hood?

**Next up:** `03_data_display_and_charts.md` — showing DataFrames, tables, and building charts from real data.
