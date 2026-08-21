# 12 — `APIRouter` & Scaling Your Project Structure

## Scenario

`main.py` now has task endpoints, auth endpoints, and will soon have user
management too — it's becoming one long file with everything mixed
together. Real FastAPI projects split endpoints by feature area, the same
motivation as splitting `models.py` / `train_service.py` /
`booking_service.py` in the Railway Booking course.

## Logic: `APIRouter` — a mini FastAPI app you plug into the main one

```python
# routers/tasks.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from security import get_current_user
from schemas import TaskCreate, TaskOut
import crud

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskOut, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db),
                 current_user=Depends(get_current_user)):
    return crud.create_task(db, task, owner_id=current_user.id)


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

```python
# routers/auth.py

from fastapi import APIRouter, Depends
router = APIRouter(tags=["auth"])

@router.post("/login")
def login(...):
    ...

@router.post("/register")
def register(...):
    ...
```

```python
# main.py — now very small

from fastapi import FastAPI
from database import Base, engine
import models
from routers import tasks, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

app.include_router(tasks.router)
app.include_router(auth.router)
```

### Recommended project layout at this scale

```
taskflow/
├── main.py               # creates the app, includes routers
├── database.py            # engine, SessionLocal, get_db
├── models.py               # SQLAlchemy ORM models
├── schemas.py               # Pydantic request/response models
├── security.py               # password hashing, JWT, get_current_user
├── crud.py                    # database operations
├── exceptions.py                # custom exception classes
├── routers/
│   ├── __init__.py
│   ├── tasks.py
│   └── auth.py
└── tests/
    └── test_tasks.py
```

### Key ideas here

- **`prefix="/tasks"`** means every route in this router is automatically
  prefixed — `@router.post("/")` becomes `POST /tasks/`,
  `@router.get("/{task_id}")` becomes `GET /tasks/{task_id}`. You never
  repeat `/tasks` in every route definition.
- **`tags=["tasks"]`** groups these endpoints together visually in `/docs`
  — purely a documentation/organization aid, but it makes a growing API
  much easier to navigate.
- **`app.include_router(...)` is how the pieces connect.** `main.py`
  becomes almost entirely *composition* — plugging routers together —
  rather than containing actual endpoint logic itself.
- **This structure is the direct FastAPI equivalent of the Railway Booking
  project's final layout** (`train_service.py`, `booking_service.py`,
  `main.py` as a thin controller). The underlying principle is identical
  across frameworks and languages: **group code by responsibility, keep
  the entry point thin.**
- **Shared dependencies (`get_db`, `get_current_user`) live in their own
  files** (`database.py`, `security.py`) so every router can import them
  without circular dependencies or duplication.

## Try it yourself

1. Split your current `main.py` into `routers/tasks.py` and
   `routers/auth.py` following the pattern above, and confirm the app
   still works identically (test through `/docs`).
2. Add a third router, `routers/users.py`, with a `GET /users/me` endpoint
   that returns the current authenticated user's profile.
3. **Challenge:** add a router-level dependency so *every* route inside
   `tasks.router` requires authentication automatically, instead of adding
   `current_user=Depends(get_current_user)` to each one individually.
   (Hint: `APIRouter(dependencies=[Depends(get_current_user)])`.)

**Next:** `13_testing_fastapi.md`
