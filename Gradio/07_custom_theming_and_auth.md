# 07 — Theming, Custom CSS & Authentication

## What You'll Learn
- Applying and customizing built-in Gradio themes
- Injecting custom CSS for fine-grained control
- Password-protecting an app with `auth=`
- A primer on custom components (the Gradio equivalent of Streamlit's third-party components)

---

## The Scenario

PyRail's chatbot and booking desk need to match brand colors (deep red + white), and the internal-only "Admin Settings" demo must not be publicly accessible without a login — you can't ship an internal tool with `share=True` and no password.

---

## Built-In Themes

```python
import gradio as gr

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# PyRail Booking Desk")
    gr.Textbox(label="Passenger name")
    gr.Button("Book Now")

demo.launch()
```

### Logic Behind the Code

- `gr.themes` ships several presets — `Base`, `Default`, `Soft`, `Glass`, `Monochrome` — each a coordinated set of colors, spacing, and border-radius choices. Passing one to `gr.Blocks(theme=...)` re-skins every component on the page **without touching individual component code**, the same separation-of-concerns idea as Streamlit's `config.toml` (Streamlit course, Module 07): design lives separately from logic.

---

## Customizing a Theme with Brand Colors

```python
import gradio as gr

pyrail_theme = gr.themes.Soft(
    primary_hue="red",
    secondary_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
).set(
    button_primary_background_fill="#D62828",
    button_primary_background_fill_hover="#A81E1E",
)

with gr.Blocks(theme=pyrail_theme) as demo:
    gr.Markdown("# 🚆 PyRail Booking Desk")
    gr.Button("Book Now", variant="primary")

demo.launch()
```

### Logic Behind the Code

- `gr.themes.Soft(primary_hue="red", ...)` starts from a preset and overrides its **hue tokens** — Gradio themes are built on a token system (similar to design-system tokens in modern frontend frameworks), where `primary_hue` cascades through dozens of related colors (button backgrounds, focus rings, etc.) automatically.
- `.set(...)` allows overriding **individual CSS variables** by their specific name when the hue-level control isn't precise enough — e.g., forcing the exact hex `#D62828` for brand consistency, rather than accepting whatever shade Gradio's "red" hue defaults to.
- `gr.themes.GoogleFont("Inter")` pulls a Google Font directly, with the plain string as a fallback if the font fails to load — no separate `<link>` tag or manual CSS needed.

---

## Custom CSS for Full Control

```python
import gradio as gr

custom_css = """
#pyrail-header {
    background: linear-gradient(90deg, #D62828, #A81E1E);
    color: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
}
"""

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# PyRail Booking Desk", elem_id="pyrail-header")
    gr.Textbox(label="Passenger name")

demo.launch()
```

### Logic Behind the Code

- `elem_id="pyrail-header"` assigns an HTML `id` attribute to that specific component, which the `custom_css` string then targets exactly like normal web CSS — this is the escape hatch for anything themes/tokens can't express (gradients, custom shadows, precise spacing).
- Because Gradio renders real HTML/CSS under the hood, **any valid CSS works** — a learner who knows basic web CSS can transfer that knowledge directly, unlike Streamlit's theming, which is limited to the token set in `config.toml`.

---

## Authentication

```python
import gradio as gr

def admin_panel():
    return "Welcome to PyRail Admin — cache cleared, logs reviewed."

demo = gr.Interface(fn=lambda: admin_panel(), inputs=None, outputs=gr.Textbox())

demo.launch(auth=("admin", "pyrail-secure-2026"))
```

### Logic Behind the Code

- `auth=(username, password)` puts the **entire app** behind a browser-native HTTP Basic Auth prompt — nobody sees any part of the UI until they authenticate, which matters because `share=True` links are otherwise publicly reachable by anyone with the URL.
- For multiple users with different credentials, pass a **list of tuples** instead: `auth=[("admin", "pw1"), ("staff", "pw2")]`.
- For dynamic checking against a database, pass a **function** instead of a tuple: `auth=lambda username, password: check_db(username, password)` — Gradio calls it with the entered credentials and expects a boolean back.
- Just like Streamlit's `st.secrets` (Streamlit course, Module 08), **never hardcode real passwords directly in source code** committed to Git — load them from an environment variable instead: `auth=("admin", os.environ["PYRAIL_ADMIN_PW"])`.

---

## Primer: Custom Components

For needs beyond built-in components (a specialized map widget, a custom annotation tool), Gradio supports a **Custom Component** system (`gradio cc create`) that lets developers build new components in Svelte/React and publish them to PyPI for others to `pip install` and use exactly like any built-in component. As with Streamlit's custom components (Streamlit course, Module 07), the important takeaway for this course is: **using** a published custom component requires no frontend knowledge at all — it's just another `gr.SomeCustomComponent(...)` call, wired up with the same `.click()`/`.change()` patterns you already know.

---

## Try It Yourself

1. Build a themed version of the fare calculator from Module 03 using `gr.themes.Monochrome()`, then override its accent color to PyRail red using `.set(...)`.
2. Add `elem_id`s to your fare calculator's key outputs and write custom CSS to give the fare number a large, bold, colored appearance.
3. Add `auth=` to your Admin Settings-style demo, and confirm (by opening in an incognito window) that the app is genuinely inaccessible without the correct credentials.

**Next up:** `08_full_project_deployment.md` — assembling everything into one deployable PyRail Gradio app.
