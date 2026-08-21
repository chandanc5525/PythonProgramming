# 05 — Deeper Validation: `Query`, `Path`, `Field`

## Scenario

Plain type hints (`skip: int = 0`) validate *type*, but not *range* or
*format*. TaskFlow needs stronger rules: `limit` must be between 1 and 100
(so a client can't request a million rows at once), `task_id` must be a
positive integer, and a task `title` must be non-empty and under 100
characters.

## Logic: `Query`, `Path`, and `Field` add constraints beyond type

These are special default values that carry extra validation metadata.

### `Query` — constrain query parameters

```python
from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/tasks")
def list_tasks(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None, max_length=50),
):
    return {"skip": skip, "limit": limit, "search": search}
```

- `ge=0` → "greater than or equal to 0"
- `le=100` → "less than or equal to 100"
- `max_length=50` → caps string length

`GET /tasks?limit=500` now automatically returns a 422 error — no manual
`if limit > 100: raise ...` needed.

### `Path` — constrain path parameters

```python
from fastapi import Path


@app.get("/tasks/{task_id}")
def get_task(task_id: int = Path(..., gt=0)):
    return {"task_id": task_id}
```

`...` (Python's `Ellipsis`) as the first argument to `Path` means **this
parameter is required, with no default** — `Path` needs an explicit way to
say "required" since simply omitting a default isn't possible when you're
also passing keyword constraints like `gt=0`.

`GET /tasks/-1` or `/tasks/0` → rejected automatically (`gt=0` means
strictly greater than zero).

### `Field` — constrain fields inside a Pydantic model

```python
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
```

- `min_length` / `max_length` bound string length.
- `pattern` restricts `priority` to *only* `"low"`, `"medium"`, or
  `"high"` using a regular expression — anything else is rejected before
  your function even runs.

### Key ideas here

- **`Query`, `Path`, and `Field` all express the same idea in three
  different locations**: query parameters, path parameters, and model
  fields respectively. Once you recognize the pattern
  (`ge`/`le`/`gt`/`lt` for numbers, `min_length`/`max_length`/`pattern` for
  strings), it transfers across all three.
- **Validation at the edge, not scattered inside your logic.** Every
  constraint declared this way is enforced *before* your function body
  runs — meaning your actual business logic (Modules 06–09) never has to
  re-check "is this a positive number" defensively. This keeps your core
  logic focused on what it actually does, trusting that input already
  meets its contract by the time it arrives.
- **`Enum` is often a better choice than `pattern` for a fixed set of
  values** (recall Module 07 of the Railway project — same idea applies
  here):

  ```python
  from enum import Enum

  class Priority(str, Enum):
      LOW = "low"
      MEDIUM = "medium"
      HIGH = "high"

  class TaskCreate(BaseModel):
      title: str = Field(..., min_length=1, max_length=100)
      priority: Priority = Priority.MEDIUM
  ```

  This is arguably clearer than a regex, and `/docs` will render `priority`
  as a dropdown of exactly those three choices — a nice payoff for using
  the right tool.

## Try it yourself

1. Apply `Query`/`Path` constraints to your `list_tasks` and `get_task`
   endpoints from Module 02, and confirm invalid values (like
   `limit=1000`) get rejected.
2. Convert `TaskCreate.priority` to use the `Priority` Enum shown above,
   and check how `/docs` renders it differently.
3. **Challenge:** add a `Field` constraint ensuring `due_date` (if
   provided) matches a `YYYY-MM-DD` pattern using a regex.

**Next:** `06_dependency_injection.md`
