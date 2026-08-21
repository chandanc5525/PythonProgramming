# 08 — Capstone: Assembling & Deploying the PyRail Gradio App

## What You'll Learn
- Combining every module into one multi-tab PyRail application
- Queueing and concurrency for slow functions under real traffic
- Deployment: Hugging Face Spaces (native home for Gradio) and Docker
- Production checklist

---

## The Scenario

Every piece is ready: fare calculation, booking form, cart state, ticket photo enhancement, and the support chatbot. This module assembles them into **one PyRail app** with tabs for each feature, and ships it publicly.

---

## Final Project Structure

```
pyrail_gradio/
├── app.py                  # entry point — builds the full Blocks layout
├── logic/
│   ├── __init__.py
│   ├── fares.py            # calculate_fare, calculate_refund
│   ├── chatbot.py          # pyrail_bot
│   └── media.py            # enhance_ticket_photo
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## `logic/fares.py`

```python
def calculate_fare(distance_km, travel_class, passengers=1, festival_season=False):
    base_rate = {"Sleeper": 1.0, "AC 3-Tier": 2.5, "AC 2-Tier": 4.0, "AC First": 6.0}
    fare = distance_km * base_rate[travel_class] * passengers
    if festival_season:
        fare *= 1.25
    return round(fare, 2)

def calculate_refund(fare, days_before_travel):
    if days_before_travel >= 7:
        pct = 0.9
    elif days_before_travel >= 2:
        pct = 0.5
    else:
        pct = 0.0
    return round(fare * pct, 2)
```

## `app.py` — Assembled Multi-Tab App

```python
import gradio as gr
from logic.fares import calculate_fare, calculate_refund
from logic.chatbot import pyrail_bot
from logic.media import enhance_ticket_photo

pyrail_theme = gr.themes.Soft(primary_hue="red").set(
    button_primary_background_fill="#D62828",
)

with gr.Blocks(theme=pyrail_theme, title="PyRail") as demo:
    gr.Markdown("# 🚆 PyRail — Booking, Refunds & Support")

    with gr.Tabs():
        with gr.Tab("Book a Ticket"):
            distance = gr.Number(label="Distance (km)", value=500)
            travel_class = gr.Dropdown(["Sleeper", "AC 3-Tier", "AC 2-Tier", "AC First"], value="Sleeper")
            passengers = gr.Slider(1, 6, step=1, label="Passengers", value=1)
            festival = gr.Checkbox(label="Festival season?")
            fare_out = gr.Number(label="Fare (₹)", interactive=False)
            gr.Button("Calculate Fare", variant="primary").click(
                calculate_fare, [distance, travel_class, passengers, festival], fare_out
            )

        with gr.Tab("Cancel & Refund"):
            fare_in = gr.Number(label="Original Fare Paid (₹)")
            days_before = gr.Slider(0, 30, step=1, label="Days before travel")
            refund_out = gr.Number(label="Refund Amount (₹)", interactive=False)
            gr.Button("Calculate Refund").click(calculate_refund, [fare_in, days_before], refund_out)

        with gr.Tab("Ticket Photo Enhancer"):
            photo_in = gr.Image(label="Upload ticket photo", type="numpy")
            brightness = gr.Slider(0.5, 2.0, value=1.2, label="Brightness")
            photo_out = gr.Image(label="Enhanced photo")
            gr.Button("Enhance").click(enhance_ticket_photo, [photo_in, brightness], photo_out)

        with gr.Tab("Support Chat"):
            gr.ChatInterface(fn=pyrail_bot)

demo.queue(default_concurrency_limit=5)
demo.launch()
```

### Logic Behind the Code

- Each tab's logic lives in its own module under `logic/` and is **imported**, not redefined — keeping `app.py` focused purely on layout/wiring, the Gradio equivalent of separating "data loaders" from "pages" in the Streamlit multipage course (Streamlit course, Module 06).
- `gr.ChatInterface` can be **embedded inside a `gr.Tab`** just like any other component-producing call — it doesn't need to be the only thing in the app; this is a natural extension of the "Interface is just a convenience wrapper around Blocks" idea from Module 03.
- `demo.queue(default_concurrency_limit=5)` enables Gradio's **queueing system** — without it, concurrent users calling a slow function (like image enhancement) can overload the server since each triggers a blocking call; queueing serializes/limits concurrent executions so the app degrades gracefully (users wait in a visible queue) instead of crashing or hanging under load.

---

## Deployment Option 1: Hugging Face Spaces (Native Home for Gradio)

Gradio is developed by Hugging Face, and **Spaces** is purpose-built for hosting Gradio apps for free.

1. Create a new Space at huggingface.co/new-space, choosing **Gradio** as the SDK.
2. Push your project (Spaces uses Git):
   ```bash
   git remote add space https://huggingface.co/spaces/<your-username>/pyrail
   git push space main
   ```
3. Spaces automatically detects `app.py` and `requirements.txt`, installs dependencies, and runs `demo.launch()` for you.
4. For secrets (API keys), use the Space's **Settings → Variables and secrets** — read them in code via `os.environ["KEY_NAME"]`, exactly like Streamlit's `st.secrets` conceptually, just sourced from environment variables instead of a TOML file.

**Logic**: Spaces exists specifically because Gradio apps are commonly ML/AI demos — Spaces offers free CPU hosting (and paid GPU tiers) tailored to that workload, plus built-in community discoverability, which general-purpose PaaS platforms don't offer out of the box.

---

## Deployment Option 2: Docker

`Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "app.py"]
```

```bash
docker build -t pyrail-gradio .
docker run -p 7860:7860 pyrail-gradio
```

### Logic Behind the Code

- `ENV GRADIO_SERVER_NAME="0.0.0.0"` is the Gradio equivalent of Streamlit's `--server.address=0.0.0.0` (Streamlit course, Module 08) — without it, Gradio binds to `localhost` inside the container by default, making it unreachable from outside.
- Docker is the right choice when you need infrastructure Spaces doesn't offer (a specific cloud VPC, integration with an existing internal auth system, a non-Hugging-Face cloud provider).

---

## Production Checklist

- [ ] `requirements.txt` pins reasonable version ranges (`gradio>=4.0,<5.0`)
- [ ] `demo.queue(...)` enabled for any app with slow functions (media processing, LLM calls, external APIs)
- [ ] `auth=` added for any internal/admin-only tab or app
- [ ] Secrets loaded from environment variables / platform secrets manager, never hardcoded
- [ ] Tested locally with `share=False` (default) before enabling `share=True` or deploying, to confirm no accidental public exposure during development
- [ ] Confirmed `GRADIO_SERVER_NAME=0.0.0.0` (or Docker/Spaces equivalent) is set for any containerized deployment

---

## Try It Yourself

1. Assemble the full PyRail Gradio app from Modules 02–07 into the structure shown above and confirm every tab works end-to-end.
2. Add `auth=` to the whole `demo.launch()` call and confirm the entire app (all tabs) is now gated behind login.
3. Deploy to Hugging Face Spaces and share the public URL — then check the Space's build logs to see exactly how your `requirements.txt` was installed, building intuition for debugging real deployments.

---

**Congratulations** — you've gone from "Hello, Gradio" to a fully deployed, multi-tab, themed, queued, authenticated production app, including image processing and a streaming chatbot. From here, the best next step is swapping the rule-based `pyrail_bot` for a real LLM API call, using the streaming pattern from Module 06.
