# 03 — Displaying Data & Building Charts

## What You'll Learn
- Rendering pandas DataFrames as static and interactive tables
- Streamlit's built-in chart functions vs. Matplotlib/Plotly integration
- Editable data tables with `st.data_editor`

---

## The Scenario

PyRail's ops team wants to see a live table of today's bookings, sortable and searchable, plus a bar chart of tickets sold per route. They also want to be able to **manually correct a row** (e.g., fix a passenger's typo'd name) directly in the browser — no re-uploading a CSV.

---

## Logic: `st.write` vs `st.dataframe` vs `st.table`

| Function | Interactivity | Best for |
|---|---|---|
| `st.write(df)` | Same as `st.dataframe` (auto-detected) | Quick, "just show it" cases |
| `st.dataframe(df)` | Sortable columns, scrollable, resizable | Most tabular data |
| `st.table(df)` | None — fully static HTML table | Small tables meant for printing/screenshots |
| `st.data_editor(df)` | Fully editable, returns the **edited** DataFrame | Data entry / correction workflows |

The logic: **use the least powerful tool that satisfies the need.** `st.dataframe` is stateless from your script's perspective (sorting happens client-side and doesn't trigger a rerun), while `st.data_editor` gives you back a *new* DataFrame object every rerun reflecting the user's edits — which means you must explicitly decide what to do with those edits (save them, validate them, etc.).

---

## Displaying Data

```python
import streamlit as st
import pandas as pd

bookings = pd.DataFrame({
    "ticket_id": ["PYR001", "PYR002", "PYR003", "PYR004"],
    "passenger": ["Asha Rao", "Vikram Shah", "Meera Iyer", "Rohan Das"],
    "route": ["Mumbai–Delhi", "Chennai–Bangalore", "Mumbai–Delhi", "Kolkata–Pune"],
    "fare": [1450, 620, 1450, 890],
    "status": ["Confirmed", "Confirmed", "Cancelled", "Confirmed"],
})

st.subheader("All Bookings")
st.dataframe(
    bookings,
    use_container_width=True,
    hide_index=True,
    column_config={
        "fare": st.column_config.NumberColumn("Fare (₹)", format="₹%d"),
        "status": st.column_config.TextColumn("Status"),
    },
)
```

### Logic Behind the Code

- `column_config` lets you re-label columns, control number/date formatting, and even embed progress bars or images **without modifying the underlying DataFrame** — the config is purely presentational, keeping your data and its display separate.
- `hide_index=True` removes the default 0,1,2… row index, which is almost always what you want for business data that already has a meaningful ID column (`ticket_id` here).
- `use_container_width=True` makes the table stretch to fill its parent container (a column, a tab, etc.) instead of a fixed pixel width — essential for responsive layouts.

---

## Editable Tables

```python
st.subheader("Correct a Booking")
edited = st.data_editor(bookings, num_rows="dynamic", hide_index=True)

if not edited.equals(bookings):
    st.info("You have unsaved changes.")
    if st.button("Save changes"):
        bookings = edited
        st.success("Bookings updated!")
```

### Logic Behind the Code

- `num_rows="dynamic"` allows the user to add/delete rows via +/– controls in the UI; `"fixed"` (the default) locks the row count.
- Comparing `edited.equals(bookings)` is how you detect "did anything actually change" — necessary because `st.data_editor` re-returns a DataFrame **every single rerun**, whether or not the user touched anything, so you can't just assume "it returned something, so save it."
- The **save-on-button-click pattern** here previews an idea we formalize in Module 04 (Session State): separating "what the widget currently shows" from "what's actually been committed/persisted."

---

## Built-in Quick Charts

```python
import numpy as np

route_sales = bookings.groupby("route")["fare"].sum()

st.subheader("Revenue by Route")
st.bar_chart(route_sales)

trend = pd.DataFrame({
    "day": pd.date_range("2026-08-01", periods=14),
    "bookings": np.random.randint(50, 200, size=14),
})
st.line_chart(trend.set_index("day"))
```

`st.bar_chart`, `st.line_chart`, and `st.area_chart` are thin wrappers around **Vega-Lite** — great for fast exploratory visuals with almost no configuration, driven directly off a DataFrame's index and columns.

---

## Full Control with Plotly / Matplotlib

When the quick charts aren't expressive enough (custom tooltips, multiple axes, specific color scales), drop down to a real charting library:

```python
import plotly.express as px

fig = px.pie(bookings, names="route", values="fare", title="Revenue Share by Route",
             hole=0.4)
st.plotly_chart(fig, use_container_width=True)
```

### Logic Behind the Code

- `st.plotly_chart(fig)` simply **embeds the Plotly figure object** into the page — you build the chart exactly as you would in a Jupyter notebook, then hand it to Streamlit for rendering. This "build with the library you already know, then wrap in one Streamlit call" pattern applies identically to `st.pyplot(fig)` for Matplotlib and `st.altair_chart(chart)` for Altair.
- Plotly charts are interactive by default (hover tooltips, zoom) **without any extra code**, which is often why teams choose it over Matplotlib for dashboards.

---

## Try It Yourself

1. Load the `bookings` DataFrame and add a `st.metric` showing total revenue, computed with `bookings["fare"].sum()`.
2. Add a `st.selectbox` to filter `bookings` by `status` before displaying the table (hint: `bookings[bookings["status"] == chosen_status]`).
3. Build a Plotly bar chart comparing average fare per route, and place it in a `st.tabs` alongside the pie chart from this module.

**Next up:** `04_session_state_and_forms.md` — making widgets "remember" things across reruns, and batching inputs with forms.
