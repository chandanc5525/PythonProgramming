# 04 — Events, State & Interactivity

## What You'll Learn
- The full event vocabulary (`.click`, `.change`, `.submit`, etc.) and when to use each
- Chaining events and updating multiple outputs from one trigger
- `gr.State` for data that should persist across interactions, per user session
- Dynamically updating a component's *properties* (not just its value) with `gr.update`

---

## The Scenario

PyRail's booking tab needs three behaviors that go beyond a single button click: (1) the fare should update **live** as the class dropdown changes, (2) a running "cart" of booked tickets needs to persist across multiple additions without a database, and (3) selecting "Sleeper" class should **disable** the "Add Insurance" checkbox, since PyRail doesn't offer insurance on Sleeper class.

---

## Logic: The Event Vocabulary

Every interactive Gradio component exposes **event methods** you can attach functions to — the ones you'll use constantly:

| Event | Fires when | Typical component |
|---|---|---|
| `.click()` | A button is clicked | `gr.Button` |
| `.change()` | A value changes (including programmatically) | Almost any input |
| `.submit()` | Enter is pressed | `gr.Textbox` |
| `.select()` | A user selects within a component (e.g., a Dataframe cell, a Gallery image) | `gr.Dataframe`, `gr.Gallery` |

```python
import gradio as gr

def update_fare(distance_km, travel_class):
    base_rate = {"Sleeper": 1.0, "AC 3-Tier": 2.5, "AC 2-Tier": 4.0, "AC First": 6.0}
    return round(distance_km * base_rate[travel_class], 2)

with gr.Blocks() as demo:
    distance = gr.Number(label="Distance (km)", value=500)
    travel_class = gr.Dropdown(["Sleeper", "AC 3-Tier", "AC 2-Tier", "AC First"], value="Sleeper")
    fare_out = gr.Number(label="Fare (₹)", interactive=False)

    # Fires whenever EITHER input changes — no button needed
    distance.change(update_fare, [distance, travel_class], fare_out)
    travel_class.change(update_fare, [distance, travel_class], fare_out)

demo.launch()
```

### Logic Behind the Code

- Attaching `.change()` to **both** `distance` and `travel_class`, pointing at the same function and same output, gives "live" fare updates without needing `live=True` on an `Interface` (which isn't available here anyway, since we're using `Blocks`) — each event is wired independently, but both happen to call the same handler.
- This is more granular than Streamlit's rerun model: you're choosing **exactly** which interactions trigger **exactly** which function, rather than "everything reruns, figure out what changed yourself."

---

## `gr.State` — Per-Session Data That Isn't a Visible Component

```python
import gradio as gr

def add_to_cart(item, price, cart):
    cart = cart + [(item, price)]
    total = sum(p for _, p in cart)
    summary = "\n".join(f"{i}: ₹{p}" for i, p in cart)
    return cart, summary, total

with gr.Blocks() as demo:
    cart_state = gr.State([])   # starts as an empty list, one per user session

    item = gr.Textbox(label="Item")
    price = gr.Number(label="Price (₹)")
    add_btn = gr.Button("Add to Cart")

    cart_display = gr.Textbox(label="Cart", interactive=False)
    total_display = gr.Number(label="Total (₹)", interactive=False)

    add_btn.click(
        fn=add_to_cart,
        inputs=[item, price, cart_state],
        outputs=[cart_state, cart_display, total_display],
    )

demo.launch()
```

### Logic Behind the Code

- `gr.State([])` creates an **invisible** component holding a Python object (here, a list) — it renders nothing in the UI but participates in the input/output wiring exactly like a visible component.
- Crucially, `gr.State` is **per-browser-session** — if two people open the app simultaneously, each gets their own independent `cart_state`, never seeing each other's cart. This is Gradio's direct equivalent to Streamlit's `st.session_state`, just expressed as an explicit component you thread through function signatures rather than a global dict.
- Notice `add_to_cart` takes `cart` **in** as a parameter and returns the **updated** `cart` as its first output, which is wired back into `cart_state` — this "read old state in, write new state out" pattern is how *all* state mutation in Gradio works, since plain function calls have no other way to "remember" the previous value between calls.

---

## `gr.update()` — Changing a Component's Properties, Not Just Its Value

```python
import gradio as gr

def toggle_insurance(travel_class):
    if travel_class == "Sleeper":
        return gr.update(value=False, interactive=False)
    return gr.update(interactive=True)

with gr.Blocks() as demo:
    travel_class = gr.Dropdown(["Sleeper", "AC 3-Tier", "AC 2-Tier", "AC First"], value="Sleeper")
    insurance = gr.Checkbox(label="Add Insurance")

    travel_class.change(toggle_insurance, inputs=travel_class, outputs=insurance)

demo.launch()
```

### Logic Behind the Code

- A normal function return sets a component's **value**. `gr.update(...)` lets you instead reconfigure **any property** of a component — its interactivity, visibility, choices, label, and more — from inside an event handler.
- Here, choosing "Sleeper" both **unchecks** and **disables** the insurance checkbox (business rule: no insurance on Sleeper), while any other class re-enables it — a UI behavior that would be awkward to express with a plain return value alone, since a plain `True`/`False` return can only set the checkbox's *value*, not its *enabled state*.

---

## Chaining Events

```python
distance.change(update_fare, [distance, travel_class], fare_out) \
        .then(lambda fare: f"Approx ${fare / 83:.2f} USD", fare_out, usd_out)
```

### Logic Behind the Code

- `.then(...)` chains a **second** function to run immediately after the first completes, receiving the same event trigger — useful for pipelines (compute fare → then convert currency → then log it) without cramming unrelated logic into one giant function.

---

## Try It Yourself

1. Extend the cart example with a "Clear Cart" button that resets `cart_state` back to `[]` and clears both display outputs.
2. Use `gr.update(choices=[...])` to make a "Route" dropdown's available "Class" options change dynamically (e.g., a hypothetical express route only offers AC classes, not Sleeper).
3. Chain three events with `.then()`: calculate fare → convert to USD → append a log line to a running `gr.State` list of all calculations performed this session.

**Next up:** `05_file_media_handling.md` — images, audio, video, and file uploads/downloads in Gradio.
