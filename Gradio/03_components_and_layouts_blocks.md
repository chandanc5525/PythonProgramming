# 03 — Custom Layouts with `gr.Blocks`

## 🎯 What You'll Learn
- Why `gr.Interface` eventually runs out of flexibility
- `gr.Blocks`: rows, columns, tabs, and free-form component placement
- Explicitly wiring events instead of relying on `Interface`'s auto-wiring

---

## 📌 The Scenario

`gr.Interface` was great for the single-function fare calculator, but PyRail's team now wants a **dashboard-like page**: a booking form on the left, a live-updating summary panel on the right, a separate tab for cancellations, and a button that's independent from the "auto-run on submit" pattern. This requires real layout control — that's `gr.Blocks`.

---

## 🧠 Logic: `Interface` vs `Blocks`

| | `gr.Interface` | `gr.Blocks` |
|---|---|---|
| Layout | Fixed: inputs left/top, outputs right/bottom | Fully custom: rows, columns, tabs, nesting |
| Wiring | Automatic (all inputs → one function → all outputs) | Explicit (`.click()`, `.change()`, etc., per event) |
| Multiple functions per page | No | Yes |
| Best for | A single function demo | Real multi-section apps |

The logic: `Interface` is a **convenience wrapper** that generates a `Blocks` layout and wiring for you under a specific, opinionated pattern. Once your app needs more than one function, custom arrangement, or partial updates, you drop down to `Blocks` directly — the same way you'd drop from Streamlit's quick charts to raw Plotly (Streamlit course, Module 03).

---

## 💻 A Two-Column Booking Layout

```python
import gradio as gr

def calculate_fare(distance_km, travel_class):
    base_rate = {"Sleeper": 1.0, "AC 3-Tier": 2.5, "AC 2-Tier": 4.0, "AC First": 6.0}
    return round(distance_km * base_rate[travel_class], 2)

with gr.Blocks(title="PyRail Booking") as demo:
    gr.Markdown("# 🚆 PyRail Booking Desk")

    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### Passenger Details")
            distance = gr.Number(label="Distance (km)", value=500)
            travel_class = gr.Dropdown(
                ["Sleeper", "AC 3-Tier", "AC 2-Tier", "AC First"],
                label="Class", value="Sleeper"
            )
            calculate_btn = gr.Button("Calculate Fare", variant="primary")

        with gr.Column(scale=1):
            gr.Markdown("### Summary")
            fare_output = gr.Number(label="Estimated Fare (₹)", interactive=False)

    calculate_btn.click(
        fn=calculate_fare,
        inputs=[distance, travel_class],
        outputs=fare_output,
    )

demo.launch()
```

### 🔍 Logic Behind the Code

- `with gr.Blocks(...) as demo:` opens a **layout context** — every component created inside it is placed into the page in the order declared, similar in spirit to how Streamlit renders top-to-bottom, but here you additionally control the *spatial* arrangement with `Row`/`Column`.
- `gr.Row()` places its children **side by side**; `gr.Column(scale=2)` inside that row claims twice the horizontal space of a `scale=1` column next to it — this is a flexbox-like proportional sizing system.
- **Nothing runs automatically here.** Unlike `Interface`, creating `distance`, `travel_class`, and `fare_output` does **not** wire them to `calculate_fare` — you must explicitly call `.click(fn=..., inputs=..., outputs=...)` on the button. This explicitness is the entire point of `Blocks`: you decide exactly which event triggers which function, writing to which outputs.
- `interactive=False` on `fare_output` makes it **read-only display** — the user can't type into it; it can only be set programmatically as a function's return value.

---

## 💻 Tabs for Multiple Sections

```python
import gradio as gr

def calculate_fare(distance_km, travel_class):
    base_rate = {"Sleeper": 1.0, "AC 3-Tier": 2.5, "AC 2-Tier": 4.0, "AC First": 6.0}
    return round(distance_km * base_rate[travel_class], 2)

def calculate_refund(fare, days_before_travel):
    if days_before_travel >= 7:
        pct = 0.9
    elif days_before_travel >= 2:
        pct = 0.5
    else:
        pct = 0.0
    return round(fare * pct, 2)

with gr.Blocks(title="PyRail Desk") as demo:
    gr.Markdown("# 🚆 PyRail Service Desk")

    with gr.Tabs():
        with gr.Tab("Book a Ticket"):
            distance = gr.Number(label="Distance (km)", value=500)
            travel_class = gr.Dropdown(["Sleeper", "AC 3-Tier", "AC 2-Tier", "AC First"], value="Sleeper")
            fare_out = gr.Number(label="Fare (₹)")
            gr.Button("Calculate").click(calculate_fare, [distance, travel_class], fare_out)

        with gr.Tab("Cancel & Refund"):
            fare_in = gr.Number(label="Original Fare Paid (₹)")
            days_before = gr.Slider(0, 30, step=1, label="Days before travel date")
            refund_out = gr.Number(label="Refund Amount (₹)")
            gr.Button("Calculate Refund").click(calculate_refund, [fare_in, days_before], refund_out)

demo.launch()
```

### 🔍 Logic Behind the Code

- `gr.Tabs()` / `gr.Tab("...")` groups components into switchable panels — like `gr.Blocks` generally, only the components inside the **active** tab are visible, but (similar to Streamlit tabs) all tabs' components exist in the page's DOM from the start; switching tabs is purely a visibility toggle, not a re-instantiation.
- Chaining `.click()` directly onto `gr.Button("Calculate")` without assigning it to a variable first is valid Python — the button is still created and placed in the layout; you're just skipping giving it a name since nothing else needs to reference it later.
- Two entirely **separate functions** (`calculate_fare`, `calculate_refund`) coexist on one page — something `gr.Interface` cannot do at all, since it's hard-wired to exactly one function.

---

## 📝 Try It Yourself

1. Add a third tab, "Route Lookup," with a `gr.Textbox` for a station name and a `gr.Dataframe` output listing (hardcoded, for now) trains from that station.
2. Change the booking tab's layout to use `gr.Row()`/`gr.Column()` so the form is on the left and the fare result is on the right, similar to the two-column example.
3. Add a `gr.Markdown` component between the two tabs' content that explains PyRail's refund policy — place it so it's visible on both tabs (hint: put it *outside* the `gr.Tabs()` block, either above or below).

**Next up:** `04_events_state_and_interactivity.md` — chaining events, multiple triggers, and Gradio's approach to state.
