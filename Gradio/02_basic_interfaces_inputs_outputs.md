# 02 — Core Input/Output Components & Interface Configuration

## What You'll Learn
- The most-used input and output components
- Multiple inputs/outputs and how return values map to them
- Live vs. submit-triggered interfaces
- Examples, flagging, and interface-level polish options

---

## The Scenario

You're building a **fare calculator** for PyRail: input route distance, class, number of passengers, and whether it's a festival-season booking; output the total fare, a breakdown table, and a colored "confidence" label about surge pricing.

---

## Logic: Function Signature ↔ Component List

The rule to internalize: **the number and order of `inputs` matches your function's parameters; the number and order of `outputs` matches your function's return values** (as a tuple, if there's more than one).

```python
import gradio as gr

def calculate_fare(distance_km, travel_class, passengers, festival_season):
    base_rate = {"Sleeper": 1.0, "AC 3-Tier": 2.5, "AC 2-Tier": 4.0, "AC First": 6.0}
    fare = distance_km * base_rate[travel_class] * passengers
    if festival_season:
        fare *= 1.25

    breakdown = f"Base: ₹{distance_km * base_rate[travel_class]:.0f} × {passengers} passengers"
    if festival_season:
        breakdown += " × 1.25 (festival surge)"

    surge_label = "High Demand ⚠️" if festival_season else "Normal"

    return round(fare, 2), breakdown, surge_label

demo = gr.Interface(
    fn=calculate_fare,
    inputs=[
        gr.Number(label="Distance (km)", value=500),
        gr.Dropdown(["Sleeper", "AC 3-Tier", "AC 2-Tier", "AC First"], label="Class", value="Sleeper"),
        gr.Slider(1, 6, step=1, label="Passengers", value=1),
        gr.Checkbox(label="Festival season?"),
    ],
    outputs=[
        gr.Number(label="Total Fare (₹)"),
        gr.Textbox(label="Breakdown"),
        gr.Label(label="Demand"),
    ],
    title="PyRail Fare Calculator",
    description="Estimate your ticket fare based on distance, class, and season.",
)

demo.launch()
```

### Logic Behind the Code

- `calculate_fare` returns a **3-tuple** `(fare, breakdown, surge_label)`, matching the 3 components in `outputs`, positionally — Gradio doesn't inspect names, only position and count.
- `gr.Number(value=500)` sets the widget's **default value**, shown before the user interacts at all — unlike Streamlit, defaults here don't interact with anything like a rerun model; they're just the initial component state.
- `gr.Label` is purpose-built for showing a short classification-style result, often with a confidence bar in ML use cases — using it for "Normal"/"High Demand ⚠️" leans on its visual styling (a colored pill) rather than plain text.
- `description=` (and `title=`) are **interface-level** metadata rendered above the components — this is the fastest way to add context without hand-building layout (covered properly with `gr.Blocks` in Module 04).

---

## Logic: Live Mode vs. Submit Button

By default, `gr.Interface` shows a **Submit** button — the function only runs when clicked (or an input's Enter key is pressed for text). For lightweight functions, you can make it fully **live**:

```python
demo = gr.Interface(
    fn=calculate_fare,
    inputs=[...],
    outputs=[...],
    live=True,   # runs on every input change, no Submit button
)
```

### Logic Behind the Code

- `live=True` wires **every** input component's `change` event directly to your function — appropriate for cheap, fast functions (a fare formula) but a poor choice for anything slow (an API call, a large model inference), since it will fire on every single slider drag or keystroke, similar in spirit to Streamlit's default rerun-on-every-interaction behavior, but opt-in here rather than default.
- The default (submit-triggered) mode exists specifically because Gradio assumes many use cases involve **expensive** functions (model inference) where firing on every keystroke would be wasteful or even costly (paid API calls).

---

## Built-In Examples & Flagging

```python
demo = gr.Interface(
    fn=calculate_fare,
    inputs=[...],
    outputs=[...],
    examples=[
        [500, "Sleeper", 1, False],
        [1200, "AC 2-Tier", 2, True],
        [300, "AC First", 4, False],
    ],
    flagging_mode="manual",
)
```

### Logic Behind the Code

- `examples=` renders a clickable table of preset inputs below the interface — clicking a row **auto-fills all inputs and runs the function**, which is invaluable for demoing edge cases or giving new users a starting point without them having to invent valid inputs themselves.
- `flagging_mode="manual"` adds a "Flag" button that lets a user save a specific input/output pair (e.g., "this fare looks wrong") to a local CSV log — originally designed for **collecting hard examples during model evaluation**, but equally useful for any app where you want structured user feedback on specific runs.

---

## Try It Yourself

1. Add a `gr.Radio(["Window", "Aisle", "No preference"], label="Seat preference")` input, and a fourth output `gr.Textbox` that echoes it back combined with the fare.
2. Convert the interface to `live=True` and note which inputs feel natural to interact with live (the slider) versus which feel jarring (typing in the Number box character-by-character).
3. Add 3 more rows to `examples=` representing realistic PyRail bookings, and click through them to confirm the outputs make sense.

**Next up:** `03_components_and_layouts_blocks.md` — moving beyond `Interface` into fully custom layouts with `gr.Blocks`.
