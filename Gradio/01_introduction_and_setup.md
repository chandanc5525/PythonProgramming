# 01 — Introduction to Gradio & Environment Setup

## What You'll Learn
- What Gradio is and the problem it solves
- How Gradio's model differs from Streamlit's "rerun everything" approach
- Installing Gradio and building your first `Interface`
- The function-in, function-out mental model

---

## The Scenario

You've just trained a small machine learning model — say, a function that predicts a train ticket's fare given route distance and travel class. Your team wants to **try it interactively**: type in numbers, see a prediction, without writing a single line of frontend code, and ideally with a **public shareable link** they can test from their phones today.

This is exactly Gradio's home turf: **wrap any Python function in an interactive web UI in a few lines**, with first-class support for ML/AI demos (images, audio, chatbots) out of the box.

---

## The Core Idea (Logic First)

Where Streamlit thinks in terms of "rerun the whole script on every interaction" (Module 01 of the Streamlit course), Gradio thinks in terms of **components wired to a Python function**:

1. You define **input components** (a slider, a textbox, an image uploader).
2. You define **output components** (a label, an image, a plot).
3. You provide a **plain Python function** that takes the inputs and returns the outputs.
4. Gradio wires it together: whenever an input changes (or a button is clicked, depending on configuration), it calls your function **once**, with the current input values, and pushes the return value into the output components.

This is much closer to a **traditional event-driven callback model** than Streamlit's rerun-everything approach — your function is only called when needed, not your entire script.

---

## Installation

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install gradio
```

---

## Your First App

```python
import gradio as gr

def greet(name, excited):
    greeting = f"Hello, {name}!"
    return greeting + " 🎉" if excited else greeting

demo = gr.Interface(
    fn=greet,
    inputs=[gr.Textbox(label="Your name"), gr.Checkbox(label="Excited?")],
    outputs=gr.Textbox(label="Greeting"),
    title="PyRail Greeter",
)

demo.launch()
```

Run it:

```bash
python app.py
```

Gradio starts a local server (usually `http://127.0.0.1:7860`) and opens it in your browser.

### Logic Behind the Code

- `gr.Interface(fn=..., inputs=..., outputs=...)` is the **highest-level Gradio abstraction** — you give it a function and describe its inputs/outputs as a list of components, and it auto-generates a complete, reasonably polished UI (labels, a "Submit" button, a "Clear" button) without you touching layout code at all.
- The **order** of `inputs` in the list must match the **order of parameters** in `greet(name, excited)` — Gradio calls your function positionally, `greet(textbox_value, checkbox_value)`.
- `demo.launch()` starts a local web server (built on FastAPI + Uvicorn under the hood) and blocks, keeping the app running until you stop the process.
- Notice there's no equivalent of Streamlit's "reruns the whole script" concern here — `greet` is called fresh, in isolation, each time, with no leftover state from previous calls unless you explicitly manage it (covered in Module 05, State Management).

---

## Instant Public Sharing

```python
demo.launch(share=True)
```

This prints a temporary public URL (`https://xxxxx.gradio.live`) that tunnels to your local machine, valid for 72 hours — extremely useful for quickly sharing a prototype with a teammate without any deployment step at all. (We cover permanent deployment in Module 12.)

---

## Recommended Project Structure

```
gradio-course/
├── venv/
├── requirements.txt
└── app.py
```

`requirements.txt`:

```
gradio>=4.0
numpy
pillow
```

---

## Try It Yourself

1. Modify `greet` to also accept a `gr.Slider(0, 100, label="Excitement level")` and use it to add that many `!` characters to the greeting.
2. Change `outputs` to `gr.Textbox(label="Greeting", lines=3)` and observe how component *arguments* (not just types) shape the UI.
3. Launch with `share=True`, open the public link on your phone, and confirm it updates in real time as you interact from your laptop's copy — this demonstrates that both clients are talking to the *same* running Python process.

**Next up:** `02_basic_interfaces_inputs_outputs.md` — every core input/output component and interface configuration option.
