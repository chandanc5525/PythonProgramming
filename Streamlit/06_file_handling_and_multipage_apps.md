# 06 — File Uploads/Downloads & Multipage Applications

## What You'll Learn
- Reading uploaded files directly into pandas without saving to disk
- Letting users download generated data/reports
- Structuring a real multipage app using the `pages/` convention and `st.navigation`

---

## The Scenario

PyRail's finance team wants to **upload a CSV of raw booking exports**, have the app clean/summarize it, and let them **download** a polished Excel report. Meanwhile, the whole PyRail Dashboards tool has grown — it now needs separate pages for "Bookings," "Revenue," and "Admin Settings," navigable from a sidebar, not crammed into one giant script.

---

## Logic: Uploaded Files Are In-Memory, Not On Disk

```python
import streamlit as st
import pandas as pd

uploaded = st.file_uploader("Upload bookings export (CSV)", type=["csv"])

if uploaded is not None:
    df = pd.read_csv(uploaded)
    st.write(f"{len(df)} rows loaded.")
    st.dataframe(df.head())
```

### Logic Behind the Code

- `st.file_uploader` returns `None` until a file is chosen, then an **`UploadedFile` object** — a file-like object (subclass of `BytesIO`) held **in memory**, not written to your server's disk automatically. This matters for both security (no stray files left behind) and simplicity (`pd.read_csv` accepts file-like objects directly, no temp-file juggling needed).
- Because it behaves like a file object, most "read a file" functions across pandas, openpyxl, PyPDF2, etc. accept it directly.
- **Gotcha**: an `UploadedFile`'s internal read-position is a pointer, like any stream — if you read it once (e.g., `pd.read_csv(uploaded)`), then try to read it *again* later in the same rerun, you'll get an empty result unless you call `uploaded.seek(0)` first to rewind it.

---

## Generating & Offering a Download

```python
import io
import pandas as pd
import streamlit as st

summary = df.groupby("route", as_index=False)["fare"].agg(["sum", "mean", "count"])

# Build an in-memory Excel file
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    summary.to_excel(writer, index=False, sheet_name="Route Summary")

st.download_button(
    label="Download Route Summary (Excel)",
    data=buffer.getvalue(),
    file_name="route_summary.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
```

### Logic Behind the Code

- `io.BytesIO()` creates an **in-memory binary buffer** — writing the Excel file "into" this buffer instead of an actual disk path avoids leaving temp files around on the server, which matters a lot for a multi-user hosted app (you don't want User A's temp file colliding with User B's).
- `st.download_button` needs raw `bytes` (`buffer.getvalue()`), a filename, and a correct MIME type so the browser knows how to handle the download and what icon/extension to show.
- Unlike `st.button`, a `download_button` click **does not require server-side logic to run after the click** — the bytes are already prepared and attached to the button *before* the user even clicks; the click just triggers the browser's native "save file" behavior.

---

## Logic: Structuring a Multipage App

Streamlit apps naturally sprawl. The modern, recommended structure uses explicit `Page` objects and `st.navigation`, giving you full control over grouping, icons, and ordering:

```
pyrail_dashboards/
├── app.py                  # entry point — defines navigation
├── pages/
│   ├── bookings.py
│   ├── revenue.py
│   └── admin_settings.py
└── shared/
    └── data_loader.py      # shared @st.cache_data functions
```

`app.py`:

```python
import streamlit as st

st.set_page_config(page_title="PyRail Dashboards", layout="wide")

bookings_page = st.Page("pages/bookings.py", title="Bookings", icon="🎫")
revenue_page  = st.Page("pages/revenue.py", title="Revenue", icon="💰")
admin_page    = st.Page("pages/admin_settings.py", title="Admin Settings", icon="⚙️")

nav = st.navigation({
    "Operations": [bookings_page, revenue_page],
    "System": [admin_page],
})
nav.run()
```

`pages/bookings.py` (a normal Streamlit script, just like everything so far):

```python
import streamlit as st
from shared.data_loader import load_bookings

st.title("🎫 Bookings")
df = load_bookings("data/bookings_history.csv")
st.dataframe(df, use_container_width=True)
```

### Logic Behind the Code

- Each entry in `pages/` is a **complete, independent Streamlit script** — Streamlit runs the *selected* page's script (and only that one) on each rerun, meaning navigating pages doesn't re-execute the code of pages you're not viewing.
- `st.navigation({...})` accepts a dict mapping **section headers** to lists of `st.Page` objects, which is how you get grouped sidebar navigation (e.g., "Operations" vs "System" as separate labeled groups) instead of one flat list.
- `nav.run()` is what actually renders the chosen page — nothing after this line in `app.py` will execute for that rerun, since control passes into the selected page's script.
- Putting shared caching functions in `shared/data_loader.py` and importing them from multiple pages means the `@st.cache_data` cache is **shared across pages** too — navigating from Bookings to Revenue and back doesn't reload the CSV, because the cache key (function + arguments) is identical regardless of which page called it.
- `st.session_state` is **also shared across all pages** in a single navigation app — a filter set on the Bookings page can be read on the Revenue page, which is extremely useful for cross-page filters (e.g., a persistent date-range selector).

---

## Try It Yourself

1. Add a "Cancellations" page that filters `bookings_history.csv` down to `status == "Cancelled"` and shows a `st.metric` of the cancellation rate.
2. On the Admin Settings page, add a text input for a "refresh interval" and store it in `st.session_state` — verify from the Bookings page that the value persists after switching pages.
3. Build a CSV → Excel converter as a standalone page: upload a raw CSV, clean it (drop nulls, rename columns), and offer the cleaned version as a downloadable Excel file.

**Next up:** `07_advanced_state_components_and_theming.md` — custom components, theming, and advanced session-state patterns.
