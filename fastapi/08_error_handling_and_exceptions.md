# 08 — Error Handling & Custom Exceptions

## Scenario

Remember the problem flagged in Module 02: requesting a task that doesn't
exist currently returns a `200 OK` with an error message buried in the
body — which is misleading. We need endpoints to return **proper HTTP
status codes** for failure cases, consistently, across the whole app.

## Logic: `HTTPException` for expected, per-request failures

```python
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud

app = FastAPI()


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task
```

`raise HTTPException(...)` immediately stops execution and sends back:

```json
// 404 Not Found
{ "detail": "Task 5 not found" }
```

This is the correct pattern for **expected** failures — "not found",
"not authorized", "already exists" — cases your code anticipates and
handles deliberately, one at a time, right where they occur.

## Logic: custom exception + global handler, for repeated patterns

If the *same* kind of error needs the same response shape in many places,
repeating `raise HTTPException(...)` everywhere gets repetitive and easy to
get slightly inconsistent. A custom exception + a global handler solves
this — a step up in reuse, similar in spirit to the Railway Booking
project's custom exceptions (`SeatUnavailableError`, etc.), but wired
directly into FastAPI's response system.

```python
# exceptions.py

class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id
```

```python
# main.py

from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import TaskNotFoundError

app = FastAPI()


@app.exception_handler(TaskNotFoundError)
def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Task {exc.task_id} not found",
                 "path": str(request.url)},
    )
```

Now, anywhere in your codebase — endpoints, CRUD functions, dependencies —
you can simply:

```python
def get_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise TaskNotFoundError(task_id)
    return task
```

FastAPI intercepts `TaskNotFoundError` globally and always formats it the
same way — one definition, consistent everywhere, and the response format
can change in a single place later.

### Validation errors (automatic, but customizable)

FastAPI already returns `422` automatically for invalid input (Modules
03–05). You can customize *that* format too:

```python
from fastapi.exceptions import RequestValidationError


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request data", "errors": exc.errors()},
    )
```

### Key ideas here

- **Use `HTTPException` directly for one-off, endpoint-specific errors.**
  Use a **custom exception + global handler** when the same error type
  needs consistent handling across many endpoints — this is the same
  "don't repeat yourself" reasoning behind pulling fare calculation into
  its own function in the Railway Booking project.
- **Exception handlers keep error-formatting logic out of your endpoints
  entirely.** An endpoint just says "this failed" (by raising); it never
  needs to know *how* that failure gets formatted into JSON.
- **Status codes should always match what actually happened**: `404` for
  missing resources, `400`/`422` for bad input, `401` for missing/invalid
  credentials, `403` for "authenticated, but not allowed" (Module 09 uses
  both).

## Try it yourself

1. Add `HTTPException` to `get_task_endpoint`, and confirm requesting a
   missing task now returns a real `404` (check the status code in
   `/docs`, not just the message).
2. Convert it to use the custom `TaskNotFoundError` + global handler
   pattern instead.
3. **Challenge:** add a `TaskAlreadyDoneError` for attempting to mark an
   already-completed task as done again, and register a handler that
   returns `400 Bad Request`.

**Next:** `09_authentication_and_jwt.md`
