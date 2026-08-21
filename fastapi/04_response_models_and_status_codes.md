# 04 — Response Models & Status Codes

## Scenario

`create_task` (Module 03) currently just echoes back whatever was sent. In
reality, a created task needs a **server-generated ID**, and — importantly
— if we later add a `password` or `internal_notes` field to a model, we
must make sure it's never accidentally exposed in a response. We need
control over exactly what shape goes *out*, separate from what comes *in*.

## Logic: input shape and output shape are often different

A very common intermediate-level pattern: **separate Pydantic models for
input vs. output**, even when they look similar.

```python
# schemas.py

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    priority: str = "medium"


class TaskOut(BaseModel):
    id: int
    title: str
    priority: str
    done: bool
```

```python
# main.py

from fastapi import FastAPI, status
from schemas import TaskCreate, TaskOut

app = FastAPI()

fake_tasks_db: dict[int, dict] = {}
next_id = 1


@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    global next_id
    new_task = {"id": next_id, "title": task.title,
                "priority": task.priority, "done": False}
    fake_tasks_db[next_id] = new_task
    next_id += 1
    return new_task
```

### What `response_model` actually does

`response_model=TaskOut` tells FastAPI: *"whatever this function returns,
validate and filter it through `TaskOut` before sending it to the
client."* Two consequences:

1. **Extra fields get stripped.** If `new_task` accidentally contained a
   field not in `TaskOut` (say, an internal `created_by_ip`), it would
   silently be excluded from the response — a real security/privacy
   safeguard, not just a formatting nicety.
2. **The `/docs` page shows exactly what a successful response looks
   like** — the same automatic documentation benefit as request models.

### Status codes: say what actually happened

```python
status.HTTP_201_CREATED   # 201 — "a new resource was created"
status.HTTP_200_OK        # 200 — default for GET/successful requests
status.HTTP_204_NO_CONTENT # 204 — success, nothing to return (e.g. after delete)
status.HTTP_404_NOT_FOUND  # 404 — resource doesn't exist (Module 08)
```

Using `fastapi.status` constants (`status.HTTP_201_CREATED`) instead of
the raw number `201` is preferred — it's self-documenting and your editor
can autocomplete/verify it's a real status code.

```python
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    fake_tasks_db.pop(task_id, None)
    return None
```

### Key ideas here

- **Correct status codes are part of your API's contract**, not a cosmetic
  detail. Client applications (and other developers) rely on status codes
  to decide how to react — `201` vs `200` vs `404` carry real meaning that
  well-behaved clients branch on.
- **`response_model` is a filter, not just documentation.** This is easy to
  underestimate as a beginner — it's an active security boundary between
  your internal data and what leaves your API.
- **Returning a plain dict is fine** even with `response_model` set —
  FastAPI converts and validates it against `TaskOut` regardless of
  whether you return a dict or a `TaskOut` instance directly.

## Try it yourself

1. Add `response_model=TaskOut` and `status_code=201` to `create_task` as
   shown, and confirm `/docs` now shows the exact response shape.
2. Add a field to the dict returned by `create_task` that *isn't* in
   `TaskOut` (e.g. `"secret": "shh"`) and confirm it disappears from the
   actual HTTP response even though your Python code returned it.
3. **Challenge:** add `GET /tasks/{task_id}` with `response_model=TaskOut`
   and `status_code=200` (the default, but write it explicitly once to
   understand it).

**Next:** `05_validation_with_query_path_body.md`
