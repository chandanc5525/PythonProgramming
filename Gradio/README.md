# Gradio Course — Beginner to Advanced

Part of the [PythonProgramming](https://github.com/chandanc5525/PythonProgramming) repository.

A step-by-step, hands-on course for building interactive Python UIs and AI/ML demos with **Gradio**. Every module follows the same format: a real-world **scenario**, the **logic** behind the solution, **working code**, and **"Try it yourself"** exercises.

The course reuses the same running example as the companion Streamlit course — **PyRail**, a fictional railway booking service — so you can see how the two frameworks approach identical problems differently (Gradio's function-in/function-out, event-driven model vs. Streamlit's script-rerun model).

---

## Roadmap

| # | File | Level | Concept Focus |
|---|------|-------|----------------|
| 01 | [`01_introduction_and_setup.md`](./01_introduction_and_setup.md) | Beginner | What Gradio is, the function-wrapping model, installation, `share=True` |
| 02 | [`02_basic_interfaces_inputs_outputs.md`](./02_basic_interfaces_inputs_outputs.md) | Beginner | Core components, multiple inputs/outputs, live mode, examples, flagging |
| 03 | [`03_components_and_layouts_blocks.md`](./03_components_and_layouts_blocks.md) | Beginner–Intermediate | `gr.Blocks`, rows/columns/tabs, explicit event wiring |
| 04 | [`04_events_state_and_interactivity.md`](./04_events_state_and_interactivity.md) | Intermediate | Event vocabulary, `gr.State`, `gr.update`, chaining with `.then()` |
| 05 | [`05_file_media_handling.md`](./05_file_media_handling.md) | Intermediate | Images, files, audio, video — upload and download |
| 06 | [`06_chatbot_and_streaming.md`](./06_chatbot_and_streaming.md) | Intermediate–Advanced | `gr.ChatInterface`, message history, streaming with generators |
| 07 | [`07_custom_theming_and_auth.md`](./07_custom_theming_and_auth.md) | Advanced | Themes, custom CSS, `auth=`, custom components primer |
| 08 | [`08_full_project_deployment.md`](./08_full_project_deployment.md) | Advanced | Assembling the full app, queueing, Hugging Face Spaces & Docker deployment |

---

## How to Use This Folder

1. Work through the files **in numeric order** — each module builds on the app from the previous one.
2. Type the code yourself rather than copy-pasting.
3. Complete every **"Try it yourself"** section before moving on.
4. By Module 08 you'll have a deployed, multi-tab, themed, authenticated Gradio application with a streaming chatbot.

## Prerequisites

- Python 3.9+
- Comfort with basic Python (functions, generators, dicts)
- `pip install gradio numpy pillow pandas`
