# 01 — Introduction to Streamlit & Environment Setup

## What You'll Learn
- What Streamlit is and why it exists
- How Streamlit's execution model differs from a normal Python script
- How to install Streamlit and run your first app
- The "rerun on every interaction" mental model that underlies everything else in this course

---

## The Scenario

Imagine you've just finished a data analysis in a Jupyter notebook — some pandas wrangling, a couple of matplotlib charts, maybe a trained scikit-learn model. Your manager says: *"Can you turn this into something the sales team can click through themselves, without touching code?"*

Normally that means learning HTML, CSS, JavaScript, and a backend framework like Flask or Django just to expose a few buttons and a chart. **Streamlit exists to remove that entire detour.** You write plain Python top to bottom, and Streamlit turns it into a interactive web app.

---

## The Core Idea (Logic First)

Streamlit apps are **not** event-driven in the way JavaScript apps are (`onClick` handlers, callbacks that mutate a persistent DOM). Instead:

1. Streamlit runs your **entire Python script from top to bottom** every time something changes on the page (a button click, a slider drag, a text input).
2. Each rerun produces a fresh set of outputs, which Streamlit efficiently diffs against what's already on screen.
3. Because of this, **your script is basically a function that describes "what the page should look like right now,"** not a sequence of imperative UI mutation commands.

This "rerun model" is the single most important concept in Streamlit. Every later module (session state, caching, forms) exists specifically to work *with* or *around* this rerun behavior.

---

## Installation

```bash
# Create an isolated environment (recommended)
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate

# Install Streamlit
pip install streamlit

# Verify installation
streamlit hello
```

`streamlit hello` launches a bundled demo app in your browser — use it to confirm your install works before writing any code.

---

## Your First App

Create a file named `app.py`:

```python
import streamlit as st

st.title("Hello, PyRail Dashboards!")
st.write("This is my first Streamlit app.")

name = st.text_input("What's your name?")

if name:
    st.write(f"Nice to meet you, {name}! 👋")
```

Run it with:

```bash
streamlit run app.py
```

Your default browser opens automatically at `http://localhost:8501`.

### 🔍 Logic Behind the Code

- `st.title(...)` and `st.write(...)` are **output** commands — Streamlit renders whatever you pass in, inferring the right widget (text, dataframe, chart, etc.) based on the object's type. `st.write` is the "Swiss army knife" — it can render strings, numbers, DataFrames, Matplotlib figures, and more.
- `st.text_input(...)` is an **input widget**. It returns whatever the user has typed, *as a normal Python variable*, right there in your linear script — no callback registration needed.
- The `if name:` block only executes meaningfully after the *first* rerun triggered by the user typing something. Before that, `name` is an empty string, so the block is skipped — this is the rerun model in action, happening automatically without you writing any event-handling code.

---

## Recommended Project Structure

Even for this course, keep a consistent shape from the start:

```
streamlit-course/
├── venv/
├── requirements.txt
├── app.py                 # entry point for the current module
└── data/                  # any CSVs/sample datasets you use later
```

`requirements.txt`:

```
streamlit>=1.30
pandas
```

---

## Try It Yourself

1. Modify `app.py` so it also asks for the user's favorite programming language and prints a sentence combining both answers.
2. Add a second `st.text_input` and observe: does typing in the second box cause the *whole script* to rerun, or just part of it? Add a `print("Script ran!")` statement (visible in your terminal) to confirm.
3. Read the terminal output while interacting with the app — notice how often "Script ran!" appears. This is your first hands-on proof of the rerun model.

**Next up:** `02_layout_text_and_widgets.md` — building real page layouts and every core input widget.
