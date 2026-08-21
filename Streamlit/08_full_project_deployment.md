# 08 — Capstone: Assembling & Deploying PyRail Dashboards

## 🎯 What You'll Learn
- Pulling every previous module together into one coherent app
- Managing secrets safely
- Deployment options: Streamlit Community Cloud, Docker, and a bare server
- Production checklist

---

## 📌 The Scenario

You now have everything: layout, widgets, data display, session state, forms, caching, file I/O, multipage navigation, fragments, and theming. This module assembles those pieces into the final **PyRail Dashboards** app and ships it to the internet.

---

## 📁 Final Project Structure

```
pyrail_dashboards/
├── .streamlit/
│   ├── config.toml          # theme (Module 07)
│   └── secrets.toml         # NEVER commit this file
├── shared/
│   ├── __init__.py
│   └── data_loader.py       # cached data functions (Module 05)
├── pages/
│   ├── bookings.py
│   ├── revenue.py
│   └── admin_settings.py
├── data/
│   └── bookings_history.csv
├── app.py                   # entry point + navigation (Module 06)
├── requirements.txt
└── README.md
```

---

## 💻 `shared/data_loader.py`

```python
import streamlit as st
import pandas as pd

@st.cache_data
def load_bookings(path: str = "data/bookings_history.csv") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["travel_date"])
    df["status"] = df["status"].astype("category")
    return df

@st.cache_data(ttl=600)
def route_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("route", as_index=False)
          .agg(total_fare=("fare", "sum"), bookings=("ticket_id", "count"))
          .sort_values("total_fare", ascending=False)
    )
```

### 🔍 Logic Behind the Code

- Splitting **raw load** (`load_bookings`) from **derived computation** (`route_summary`) into two separately-cached functions means changing a filter that only affects the summary doesn't force re-reading the CSV from disk — each cache invalidates independently based on its own arguments.

---

## 💻 `app.py` — Entry Point

```python
import streamlit as st

st.set_page_config(page_title="PyRail Dashboards", page_icon="🚆", layout="wide")

bookings_page = st.Page("pages/bookings.py", title="Bookings", icon="🎫", default=True)
revenue_page  = st.Page("pages/revenue.py", title="Revenue", icon="💰")
admin_page    = st.Page("pages/admin_settings.py", title="Admin Settings", icon="⚙️")

nav = st.navigation({
    "Operations": [bookings_page, revenue_page],
    "System": [admin_page],
})
nav.run()
```

---

## 💻 `pages/admin_settings.py` — Using Secrets

```python
import streamlit as st

st.title("⚙️ Admin Settings")

st.subheader("Live Currency API")
api_key = st.secrets.get("fx_api_key", "")
if api_key:
    st.success("FX API key loaded from secrets.")
else:
    st.warning("No FX API key configured. Add it to .streamlit/secrets.toml")

st.subheader("Danger Zone")
if st.button("Clear all cached data"):
    st.cache_data.clear()
    st.success("Cache cleared.")
```

`.streamlit/secrets.toml` (git-ignored):

```toml
fx_api_key = "your-real-api-key-here"
db_password = "super-secret-password"
```

### 🔍 Logic Behind the Code

- `st.secrets` reads key/value pairs from `.streamlit/secrets.toml` **locally**, or from the secrets manager built into Streamlit Community Cloud when deployed there — same code, different source, so you never hardcode credentials into a `.py` file that might get committed to Git.
- `st.cache_data.clear()` (no function reference) clears **every** `@st.cache_data`-backed cache in the whole app, useful as a blunt "reset everything" admin action, as opposed to `some_function.clear()` which only clears that one function's cache (Module 05).
- Always add `secrets.toml` to `.gitignore` — this is the single most common security mistake beginners make with Streamlit.

---

## 🚀 Deployment Option 1: Streamlit Community Cloud (Easiest)

1. Push your project to a public (or connected private) GitHub repo — including `requirements.txt`, excluding `secrets.toml`.
2. Go to [share.streamlit.io](https://share.streamlit.io), connect your GitHub account, and pick the repo + `app.py` as the entry point.
3. In the app's dashboard, open **Settings → Secrets** and paste the *contents* of your local `secrets.toml` — Community Cloud injects these into `st.secrets` at runtime.
4. Click Deploy. Every subsequent push to your chosen branch auto-redeploys.

**Logic**: Community Cloud is essentially a managed container runner that watches your GitHub repo — it installs `requirements.txt`, runs `streamlit run app.py`, and handles HTTPS/routing for you. It's free for public apps and the fastest path from "code" to "URL."

---

## 🚀 Deployment Option 2: Docker (Portable, Any Cloud)

`Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t pyrail-dashboards .
docker run -p 8501:8501 --env-file .env pyrail-dashboards
```

### 🔍 Logic Behind the Code

- `--server.address=0.0.0.0` is essential inside a container — Streamlit's default (`localhost`) would only accept connections from *inside* the container itself, making the app unreachable from outside. Binding to `0.0.0.0` means "accept connections from any network interface."
- The `HEALTHCHECK` hits Streamlit's built-in `/_stcore/health` endpoint, which cloud orchestrators (Kubernetes, ECS, etc.) use to know if the container is alive and should keep receiving traffic.
- Docker is the right choice when you need a specific cloud provider (AWS/GCP/Azure), specific compute (GPU for an ML-backed app), or infrastructure the free Community Cloud tier can't offer.

---

## ✅ Production Checklist

- [ ] `requirements.txt` pins reasonable version ranges (`streamlit>=1.30,<2.0`)
- [ ] No secrets committed to Git — verify `.gitignore` includes `secrets.toml` and `.env`
- [ ] Expensive functions wrapped in `@st.cache_data` / `@st.cache_resource`
- [ ] `st.set_page_config` set once, at the very top of `app.py`
- [ ] Sensitive admin actions (like "clear cache" or "delete data") gated behind a password check using `st.secrets`
- [ ] Tested with `streamlit run app.py` locally using the *same* `requirements.txt` you'll deploy with (a fresh venv catches missing dependencies early)

---

## 📝 Try It Yourself

1. Assemble the full PyRail Dashboards project from Modules 02–07 into this final structure and confirm every page loads.
2. Add a simple password gate to the Admin Settings page using `st.text_input(type="password")` compared against `st.secrets["admin_password"]`.
3. Deploy your finished app to Streamlit Community Cloud and share the live URL — then intentionally break `requirements.txt` (remove a needed package) and observe how the deployment logs report the failure, to build intuition for debugging real deployments.

---

🎉 **Congratulations** — you've gone from "Hello, Streamlit" to a fully deployed, multi-page, cached, themed, secrets-aware production app. From here, the best next step is rebuilding one of your own real datasets as a dashboard using this same structure.
