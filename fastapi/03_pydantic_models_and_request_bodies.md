# 03 — Pydantic Models & Request Bodies

## Scenario

To *create* a task, a client sends a JSON body:

```json
{ "title": "Buy groceries", "priority": "medium" }
```

We need a way to describe *the shape this data must have*, validate it
automatically, and get it into our function as a real Python object — not
a raw, unchecked dict.

## Logic: Pydantic models as the single source of truth for a shape

```python
# schemas.py

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    priority: str = "medium"
    done: bool = False
```

A `BaseModel` subclass declares fields the same way you'd declare
attributes on a dataclass — but Pydantic uses these declarations to
**validate incoming data at runtime**, not just document intent.

```python
# main.py

from fastapi import FastAPI
from schemas import TaskCreate

app = FastAPI()


@app.post("/tasks")
def create_task(task: TaskCreate):
    return {"received": task}
```

That's it — no manual JSON parsing, no manual `if "title" not in data`
checks. Here's what happens on a request:

```
POST /tasks
{"title": "Buy groceries"}
```

1. FastAPI reads the raw JSON body.
2. It hands that JSON to `TaskCreate` for validation.
3. `priority` and `done` weren't provided → their defaults (`"medium"`,
   `False`) are used.
4. `task` inside `create_task` is a **real `TaskCreate` instance** —
   `task.title`, `task.priority` work exactly like attribute access on any
   Python object.

If the body is missing `title` entirely (which has no default, so it's
required):

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "title"],
      "msg": "Field required"
    }
  ]
}
```

FastAPI returns this automatically, as a `422 Unprocessable Entity` — your
function body never even runs on invalid input.

### Nested and list fields work the same way

```python
class TaskCreate(BaseModel):
    title: str
    priority: str = "medium"
    tags: list[str] = []


class TaskBatchCreate(BaseModel):
    tasks: list[TaskCreate]
```

Pydantic validates nested structures recursively — a `TaskBatchCreate`
automatically validates every item inside `tasks` against `TaskCreate`'s
rules, with no extra code from you.

### Key ideas here

- **A Pydantic model is a *contract*.** It says "this is exactly the shape
  of data I accept" — and that contract is enforced automatically on every
  request, consistently, instead of scattered manual `if` checks across
  your endpoints.
- **Defaults vs. required fields**: a field with `= something` is
  optional; a field with no default (`title: str`) is required. This one
  line of code does double duty as both validation rule *and*
  documentation.
- **This is also why `/docs` (Module 01) gets richer as you add models** —
  FastAPI reads `TaskCreate`'s fields and shows exactly what a valid
  request body looks like, with types, defaults, and which fields are
  required, generated straight from your Python class.
- **Separating schemas into their own file** (`schemas.py`) rather than
  mixing them into `main.py` is a habit worth starting early — it scales
  cleanly as you add more models (Module 12 formalizes this into a full
  project structure).

## Try it yourself

1. Create `schemas.py` with `TaskCreate` as shown, wire up
   `POST /tasks` in `main.py`, and test it via `/docs`.
2. Send a request missing `title` and observe the automatic 422 error.
3. Add a `due_date: str | None = None` field to `TaskCreate`.
4. **Challenge:** Pydantic can validate more than just "is this a string" —
   look up `EmailStr` (needs `pip install pydantic[email]`) and imagine
   where you'd use it later (hint: Module 09, user registration).

**Next:** `04_response_models_and_status_codes.md`
