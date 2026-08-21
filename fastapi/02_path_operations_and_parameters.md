# 02 — Path Operations & Parameters

## Scenario

TaskFlow needs endpoints like: "get task #5", "list all tasks, optionally
filtered by status, with pagination." These require reading data *out of
the URL* — both from the path itself and from query parameters.

## Logic: two ways data arrives in the URL

```
GET /tasks/5?include_archived=true
     └─┬──┘  └───────────┬───────────┘
   path param        query parameter
```

- **Path parameters** are part of the URL structure — they identify *which
  resource* (task `5`, specifically).
- **Query parameters** come after `?` — they're *optional modifiers* to a
  request (filter, sort, paginate).

### Path parameters

```python
from fastapi import FastAPI

app = FastAPI()

fake_tasks_db = {
    1: {"title": "Buy groceries", "done": False},
    2: {"title": "Write report", "done": True},
}


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return fake_tasks_db.get(task_id, {"error": "Task not found"})
```

Visit `/tasks/1` → works. Visit `/tasks/abc` → FastAPI **automatically
rejects it** with a 422 error, because `task_id: int` declared that this
parameter must be an integer. You didn't write any "is this a number?"
check — the type hint *is* the validation.

```json
// GET /tasks/abc
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "task_id"],
      "msg": "Input should be a valid integer, unable to parse string as an integer"
    }
  ]
}
```

### Query parameters

Any function parameter that **isn't** part of the path is treated as a
query parameter automatically:

```python
@app.get("/tasks")
def list_tasks(status: str | None = None, skip: int = 0, limit: int = 10):
    tasks = list(fake_tasks_db.items())

    if status == "done":
        tasks = [(i, t) for i, t in tasks if t["done"]]
    elif status == "pending":
        tasks = [(i, t) for i, t in tasks if not t["done"]]

    return tasks[skip: skip + limit]
```

- `GET /tasks` → all tasks, first 10
- `GET /tasks?status=done` → only completed tasks
- `GET /tasks?skip=10&limit=5` → pagination

### Key ideas here

- **Default values make a parameter optional.** `skip: int = 0` means "if
  the caller doesn't provide `skip`, use `0`." `status: str | None = None`
  means "optional, and if given, must be a string."
- **The order of path vs. query params in your function doesn't matter to
  FastAPI** — it matches by *name*. FastAPI looks at your path
  (`/tasks/{task_id}`), sees `task_id` is declared there, and treats any
  other parameter as a query param automatically. This is a deliberate
  design choice that avoids repetitive boilerplate.
- **Type coercion, not just validation.** `skip: int = 0` doesn't just
  check "is this an int" — a query string is always text (`"5"`), and
  FastAPI *converts* it to a real Python `int` before your function runs.
  Inside `list_tasks`, `skip` is genuinely an `int`, ready to use in
  arithmetic.
- **`str | None`** (Python 3.10+ union syntax, or `Optional[str]` on older
  versions) tells both FastAPI *and* anyone reading your code that this
  value might be absent — the type hint carries real meaning here, not
  just documentation.

## Try it yourself

1. Add `GET /tasks/{task_id}` and `GET /tasks` as shown, and test both
   through `/docs`.
2. Add a `sort: str = "asc"` query parameter to `list_tasks` that reverses
   the list when `sort == "desc"`.
3. **Challenge:** what happens right now if someone requests
   `/tasks/999` (a task ID that doesn't exist)? It currently returns
   `{"error": "Task not found"}` with a `200 OK` status — which is
   misleading (the request technically failed, but nothing in the HTTP
   status says so). We'll fix this properly in Module 08 using
   `HTTPException` — for now, just notice the problem.

**Next:** `03_pydantic_models_and_request_bodies.md`
