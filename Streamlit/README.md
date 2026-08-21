# Streamlit Course — Beginner to Advanced

Part of the [PythonProgramming](https://github.com/chandanc5525/PythonProgramming) repository.

A step-by-step, hands-on course for building interactive Python web apps with **Streamlit** — no HTML, CSS, or JavaScript required. Every module follows the same format: a real-world **scenario**, the **logic** behind the solution, **working code**, and **"Try it yourself"** exercises.

The course is built around one running example — **PyRail Dashboards**, an operations dashboard for a fictional railway booking service — so each module adds a real feature to a real (small) product instead of a disconnected toy example.

---

## Roadmap

| # | File | Level | Concept Focus |
|---|------|-------|----------------|
| 01 | [`01_introduction_and_setup.md`](./01_introduction_and_setup.md) | Beginner | What Streamlit is, the rerun execution model, installation |
| 02 | [`02_layout_text_and_widgets.md`](./02_layout_text_and_widgets.md) | Beginner | Columns, sidebar, tabs, and every core input widget |
| 03 | [`03_data_display_and_charts.md`](./03_data_display_and_charts.md) | Beginner–Intermediate | DataFrames, editable tables, built-in and Plotly charts |
| 04 | [`04_session_state_and_forms.md`](./04_session_state_and_forms.md) | Intermediate | `st.session_state`, multi-step wizards, `st.form`, callbacks |
| 05 | [`05_caching_performance_and_apis.md`](./05_caching_performance_and_apis.md) | Intermediate | `st.cache_data` vs `st.cache_resource`, live APIs, DB connections |
| 06 | [`06_file_handling_and_multipage_apps.md`](./06_file_handling_and_multipage_apps.md) | Intermediate–Advanced | Uploads/downloads, `st.navigation`, real multipage structure |
| 07 | [`07_advanced_state_components_and_theming.md`](./07_advanced_state_components_and_theming.md) | Advanced | `st.fragment`, dynamic widget lists, theming, custom components |
| 08 | [`08_full_project_deployment.md`](./08_full_project_deployment.md) | Advanced | Assembling the full app, secrets, Streamlit Cloud & Docker deployment |

---

## How to Use This Folder

1. Work through the files **in numeric order** — each module builds on the app from the previous one.
2. Type the code yourself rather than copy-pasting.
3. Complete every **"Try it yourself"** section before moving on.
4. By Module 08 you'll have a deployed, multi-page, cached, themed Streamlit application.

## Prerequisites

- Python 3.9+
- Comfort with basic Python (functions, dicts, pandas basics)
- `pip install streamlit pandas plotly openpyxl`
