# 07 — Advanced State Patterns, Custom Components & Theming

## 🎯 What You'll Learn
- Fragments (`st.fragment`) to rerun only *part* of the page
- Dynamic/repeating widget lists driven by session state
- Theming via `config.toml`
- A primer on embedding third-party custom components

---

## 📌 The Scenario

PyRail Dashboards' Revenue page has an expensive chart that takes 2 seconds to redraw, sitting right next to a lightweight "search passenger" text box. Every keystroke in that search box currently re-renders the expensive chart too — because of the rerun model, the *whole page* reruns on every interaction. You need a way to isolate the cheap widget from the expensive one.

---

## 🧠 Logic: `st.fragment` — Reducing Rerun Scope

```python
import streamlit as st
import time

st.title("Revenue")

@st.fragment
def search_box():
    query = st.text_input("Search passenger")
    if query:
        st.write(f"Results for '{query}'...")

search_box()

st.subheader("Revenue Trend (expensive)")
time.sleep(2)  # simulate a heavy chart render
st.line_chart({"revenue": [100, 150, 130, 170, 200]})
```

### 🔍 Logic Behind the Code

- Functions decorated with `@st.fragment` get their own **mini rerun scope**: when a widget *inside* the fragment changes, **only the fragment's code reruns** — the rest of the page (including that 2-second chart render) is left untouched.
- Without `@st.fragment`, typing in the search box would re-trigger the full 2-second `time.sleep` on every keystroke, since the whole script reruns by default (Module 01). This decorator is the direct, modern answer to "how do I stop unrelated slow code from rerunning constantly."
- Fragments can still read/write `st.session_state`, and their reruns are still governed by the same top-to-bottom execution logic — just scoped to a smaller chunk of the script.

---

## 💻 Dynamic Widget Lists (Repeating Rows)

A common intermediate-level challenge: letting a user add an arbitrary number of passengers to one booking, each with their own set of fields.

```python
import streamlit as st

st.session_state.setdefault("passengers", [{"name": "", "age": 25}])

st.subheader("Add Passengers")

for i, p in enumerate(st.session_state.passengers):
    col1, col2, col3 = st.columns([3, 1, 1])
    p["name"] = col1.text_input("Name", value=p["name"], key=f"name_{i}")
    p["age"] = col2.number_input("Age", value=p["age"], min_value=1, key=f"age_{i}")
    if col3.button("🗑️", key=f"remove_{i}"):
        st.session_state.passengers.pop(i)
        st.rerun()

if st.button("+ Add another passenger"):
    st.session_state.passengers.append({"name": "", "age": 25})
    st.rerun()

st.write(st.session_state.passengers)
```

### 🔍 Logic Behind the Code

- **Every widget in a loop needs a unique `key`** (`f"name_{i}"`) — otherwise Streamlit can't tell the widgets in row 0 apart from row 1, and you'll get a `DuplicateWidgetID` error. The key is what lets Streamlit track each widget's identity across reruns even though the loop recreates the Python objects every time.
- The list `st.session_state.passengers` itself is the **source of truth**; widgets read their initial `value` from it and — critically — the code **mutates the dict directly** (`p["name"] = ...`) rather than reconstructing the list, so edits accumulate correctly across reruns.
- `.pop(i)` followed by `st.rerun()` is needed because removing an item changes *how many widgets* should exist — an explicit rerun forces Streamlit to immediately reflect the new (shorter) list, rather than waiting for the next natural interaction.

---

## 🧠 Logic: Callback Timing Nuance — Widget State Before Script Body

A subtlety that trips up intermediate learners: when a widget has a `key` and you also try to set `st.session_state[key] = ...` **later in the same script run**, you'll hit a `StreamlitAPIException`. Widgets "own" their keyed state once instantiated for that rerun — you can only pre-set a keyed value *before* the widget is created, or from within a callback (`on_change`), never after.

```python
# ❌ This raises an exception:
st.text_input("Name", key="passenger_name")
st.session_state.passenger_name = "Override"   # too late — widget already claimed this key

# ✅ Do this instead — mutate BEFORE creating the widget, or use a callback:
if st.button("Clear name"):
    st.session_state.passenger_name = ""
    st.rerun()
st.text_input("Name", key="passenger_name")
```

---

## 🎨 Theming with `config.toml`

Create `.streamlit/config.toml` in your project root:

```toml
[theme]
primaryColor = "#D62828"           # buttons, active tabs, sliders
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F4F4F4"  # sidebar, widget backgrounds
textColor = "#1A1A1A"
font = "sans serif"
```

### 🔍 Logic Behind the Code

- Streamlit reads `.streamlit/config.toml` **once at server start**, applying it globally — this is separate from `st.set_page_config`, which controls per-page metadata (title, icon, layout), not colors.
- Theming this way keeps branding **centralized and code-free** — designers can tweak colors without touching Python, and it applies consistently across every page in a multipage app.

---

## 🧩 Primer: Third-Party Custom Components

When built-in widgets aren't enough (e.g., a rich drag-and-drop file manager, a specialized map widget), the Streamlit ecosystem offers installable **custom components**, e.g.:

```bash
pip install streamlit-aggrid
```

```python
from st_aggrid import AgGrid
AgGrid(bookings)   # a fully interactive, Excel-like grid
```

### 🔍 Logic Behind the Code

- Custom components are built on a JS/React bridge that Streamlit exposes publicly — the community has published hundreds of them (rich grids, drawable canvases, maps, calendars). As a learner, the important mental model is simply: **they behave like any other Streamlit function** — you call them, they return a value, and the rerun model applies exactly the same way. You don't need to know React to *use* one, only to *build* one (out of scope for this course).

---

## 📝 Try It Yourself

1. Wrap the dynamic passenger list from this module in `@st.fragment` and confirm that adding/removing rows no longer reruns unrelated heavy code elsewhere on the page.
2. Create a custom `config.toml` theme matching PyRail's brand (pick any colors) and confirm it applies across all pages from Module 06.
3. Install `streamlit-aggrid` (or another component of your choice) and replace one `st.dataframe` call with it — compare the interactivity.

**Next up:** `08_full_project_deployment.md` — assembling everything into one deployable PyRail Dashboards app.
