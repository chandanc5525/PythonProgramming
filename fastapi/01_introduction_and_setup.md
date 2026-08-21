# 01 — Introduction & Setup

## Scenario

You need to build a backend API for **TaskFlow**, a task management app.
Before picking a framework, it's worth understanding *why* FastAPI is a
strong choice for this.

## Logic: what FastAPI actually gives you

FastAPI is a Python web framework built on two foundations:

- **Starlette** — handles the actual HTTP layer (routing, requests,
  responses), and gives FastAPI native `async` support.
- **Pydantic** — handles data validation using plain Python type hints.

The core idea that makes FastAPI different from something like Flask: **you
describe your data shapes using regular Python type hints, and FastAPI
uses that to validate input, serialize output, and generate interactive
API documentation automatically** — without you writing separate
validation code or documentation by hand.

```python
def add(a: int, b: int) -> int:
    return a + b
```

In plain Python, type hints like `a: int` are just documentation — nothing
enforces them. FastAPI is built around the idea of taking hints like this
*seriously*: if a request sends `a="abc"`, FastAPI rejects it automatically
with a clear error, before your function body even runs.

## Installing and running your first app

```bash
pip install fastapi "uvicorn[standard]"
```

`uvicorn` is the **ASGI server** that actually runs your app and talks to
the network — FastAPI itself is just the framework; it needs a server to
execute.

```python
# main.py

from fastapi import FastAPI

app = FastAPI(title="TaskFlow API")


@app.get("/")
def read_root():
    return {"message": "Welcome to TaskFlow API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
```

Run it:

```bash
uvicorn main:app --reload
```

- `main:app` means: in the file `main.py`, find the object named `app`.
- `--reload` restarts the server automatically whenever you save a file —
  essential during development, remove it in production.

Visit:

- `http://127.0.0.1:8000/` → your JSON response
- `http://127.0.0.1:8000/docs` → **interactive API documentation**, auto
  generated from your code, where you can try each endpoint in the browser
- `http://127.0.0.1:8000/redoc` → an alternative documentation view

### Key ideas here

- **`@app.get("/")` is a decorator that registers a "path operation."** In
  FastAPI terminology, a "path operation" = an HTTP method (`GET`, `POST`,
  etc.) + a URL path, mapped to a Python function.
- **You return a plain Python dict, and FastAPI converts it to JSON**
  automatically — no manual `json.dumps()` needed.
- **The `/docs` page isn't something you write** — FastAPI generates it
  from your type hints and function signatures. This becomes far more
  powerful once we add Pydantic models (Module 03) and multiple parameters
  (Module 02) — the documentation grows in detail as your code does, for
  free.
- **This is why FastAPI is a good learning framework**: the feedback loop
  is immediate. Write a function with type hints → see it appear, fully
  documented and testable, in your browser.

## Try it yourself

1. Install FastAPI and Uvicorn, create `main.py` with the code above, and
   run it with `--reload`.
2. Open `/docs` and try the `GET /health` endpoint directly from the
   browser using the "Try it out" button.
3. Add a third endpoint, `GET /about`, returning a dict with `name` and
   `version` keys.
4. **Challenge:** what happens if you visit a path that doesn't exist, like
   `/nope`? Look at the JSON error response FastAPI returns automatically
   — note the status code too (we'll use this pattern deliberately in
   Module 08).

**Next:** `02_path_operations_and_parameters.md`
