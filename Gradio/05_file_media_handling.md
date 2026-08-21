# 05 — File, Image, Audio & Video Handling

## 🎯 What You'll Learn
- Image components for upload, processing, and display
- File upload/download for arbitrary documents
- Audio and video components — a quick tour, since Gradio was built with these as first-class citizens

---

## 📌 The Scenario

PyRail wants an "Upload your ticket photo" feature that lets a passenger snap a photo of a printed ticket, have it auto-cropped/enhanced, and get a downloadable cleaned-up PDF/image back. This kind of media-in, media-out workflow is exactly what Gradio was originally built for — it's a strong differentiator versus most other Python UI tools.

---

## 💻 Image In, Image Out

```python
import gradio as gr
import numpy as np
from PIL import Image, ImageEnhance

def enhance_ticket_photo(image: np.ndarray, brightness: float) -> np.ndarray:
    pil_img = Image.fromarray(image)
    enhancer = ImageEnhance.Brightness(pil_img)
    brightened = enhancer.enhance(brightness)
    return np.array(brightened)

demo = gr.Interface(
    fn=enhance_ticket_photo,
    inputs=[
        gr.Image(label="Upload ticket photo", type="numpy"),
        gr.Slider(0.5, 2.0, value=1.2, label="Brightness"),
    ],
    outputs=gr.Image(label="Enhanced photo"),
    title="🎫 Ticket Photo Enhancer",
)

demo.launch()
```

### 🔍 Logic Behind the Code

- `gr.Image(type="numpy")` tells Gradio to hand your function a **NumPy array** (height × width × channels) — the other common options are `type="pil"` (a `PIL.Image.Image` object) and `type="filepath"` (a string path to a temp file on disk). Choosing the right type avoids unnecessary conversions inside your function — e.g., if you're using OpenCV, you'd typically want `numpy`; if you're using PIL-based operations, `pil` avoids a manual `Image.fromarray` step.
- The function must **return the same kind of object** the output `gr.Image` expects to display — Gradio is fairly forgiving and auto-converts between NumPy/PIL in most cases, but staying consistent avoids subtle bugs.
- Uploading an image and dragging the slider (this uses `Interface`'s default submit-triggered mode) re-runs `enhance_ticket_photo` fresh each time — there's no accumulated state; each call starts from the originally uploaded image, not the previous output, since `image` is always the input component's current value.

---

## 💻 Sketch/Annotation Input

```python
import gradio as gr

def count_dark_pixels(image):
    import numpy as np
    arr = np.array(image.convert("L"))
    return int((arr < 128).sum())

demo = gr.Interface(
    fn=count_dark_pixels,
    inputs=gr.Image(type="pil", sources=["upload", "webcam"], label="Photo or webcam capture"),
    outputs=gr.Number(label="Dark pixel count"),
)
demo.launch()
```

- `sources=["upload", "webcam"]` lets the user **either** upload a file **or** capture directly from their webcam, right inside the same component — a common requirement for verification/scanning-style features (e.g., "scan your ID/ticket").

---

## 💻 Generic File Upload & Download

```python
import gradio as gr
import pandas as pd

def summarize_csv(file_obj):
    df = pd.read_csv(file_obj.name)
    summary = df.describe().to_string()

    output_path = "summary.txt"
    with open(output_path, "w") as f:
        f.write(summary)

    return summary, output_path

demo = gr.Interface(
    fn=summarize_csv,
    inputs=gr.File(label="Upload bookings CSV", file_types=[".csv"]),
    outputs=[gr.Textbox(label="Summary", lines=10), gr.File(label="Download summary")],
)

demo.launch()
```

### 🔍 Logic Behind the Code

- `gr.File` gives your function a **temp file object** with a `.name` attribute pointing to where Gradio saved the uploaded bytes on disk — unlike Gradio's image components, generic files are always given to you via a real filesystem path rather than an in-memory array, since arbitrary file types (CSV, PDF, ZIP) don't have a universal in-memory Python representation the way images do.
- Returning a **file path** (`output_path`) for a `gr.File` output tells Gradio "serve this file for download" — it automatically handles the download button and correct filename, similar in spirit to Streamlit's `st.download_button`, but here triggered by simply returning a path string rather than raw bytes.
- `file_types=[".csv"]` restricts what the browser's file picker will show/accept, exactly like Streamlit's `type=` argument on `st.file_uploader`.

---

## 💻 Audio & Video — Quick Tour

```python
import gradio as gr
import numpy as np

def speed_up_audio(audio):
    sample_rate, data = audio
    # crude "speed up" by dropping every other sample
    faster = data[::2]
    return (sample_rate, faster)

demo = gr.Interface(
    fn=speed_up_audio,
    inputs=gr.Audio(sources=["upload", "microphone"], label="Announcement audio"),
    outputs=gr.Audio(label="Sped-up announcement"),
)
demo.launch()
```

### 🔍 Logic Behind the Code

- `gr.Audio` hands your function a **tuple** `(sample_rate, numpy_array)` by default — the same "give me the data as a native Python/NumPy structure" philosophy as images, so you can process it with `numpy`/`scipy`/`librosa` directly without manual file parsing.
- `sources=["upload", "microphone"]` mirrors the image component's pattern — record live or upload a file, same component, same downstream function.
- `gr.Video` follows the same conventions (accepts a file path, can be combined with `gr.Image` for a thumbnail, etc.) — once you understand the Image/Audio pattern, Video is a natural extension and is covered only briefly here since it's used less frequently in typical business apps like PyRail's.

---

## 📝 Try It Yourself

1. Extend `enhance_ticket_photo` to also accept a `gr.Slider` for contrast, using `ImageEnhance.Contrast`, and chain both adjustments.
2. Build a "Route Map Uploader": accept an image of a route map, and use `gr.Image(type="filepath")` instead of `numpy` — inspect what your function receives and note the difference from the `numpy`/`pil` types.
3. Modify `summarize_csv` to also generate a bar chart image (using matplotlib, saved to a temp PNG path) as a *third* output, alongside the text summary and the downloadable file.

**Next up:** `06_chatbot_and_streaming.md` — building conversational interfaces and streaming outputs token-by-token.
