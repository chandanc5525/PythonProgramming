# 07 — Database Integration with SQLAlchemy

## Scenario

Every task has lived in a plain Python dict so far — gone the moment the
server restarts. TaskFlow needs real persistence. We'll use **SQLAlchemy**
(the standard Python SQL toolkit/ORM) with **SQLite** (a file-based
database needing no separate server — ideal for learning).

## Logic: three layers, kept separate on purpose

This mirrors a distinction that trips up a lot of learners, so it's worth
naming explicitly:

| Layer | Purpose | Lives in |
|---|---|---|
| **ORM model** | how data is stored in the database | `models.py` |
| **Pydantic schema** | how data looks in API requests/responses | `schemas.py` |
| **Path operation** | the actual endpoint logic | `main.py` / routers |

They often *look* similar (both might have `title`, `id`), but they solve
different problems — the ORM model is about the database; the Pydantic
schema is about the API contract. Conflating them works for tiny projects
but becomes limiting fast (e.g., you never want a database-only field like
`hashed_password` leaking into a Pydantic response — Module 04's
`response_model` filtering depends on this separation).

### Database setup

```python
# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./taskflow.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

`connect_args={"check_same_thread": False}` is an SQLite-specific setting
— it's needed because FastAPI may use a task from a different thread than
the one that created the connection. This is not needed for other
databases (PostgreSQL, MySQL).

### The ORM model

```python
# models.py

from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    priority = Column(String(20), default="medium")
    done = Column(Boolean, default=False)
```

Creating the tables (run once at startup):

```python
# main.py
from database import Base, engine
import models

Base.metadata.create_all(bind=engine)
```

### CRUD functions — keeping database logic out of endpoints

```python
# crud.py

from sqlalchemy.orm import Session
from models import TaskModel
from schemas import TaskCreate


def create_task(db: Session, task: TaskCreate) -> TaskModel:
    db_task = TaskModel(title=task.title, priority=task.priority)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)   # pulls back the auto-generated id
    return db_task


def get_task(db: Session, task_id: int) -> TaskModel | None:
    return db.query(TaskModel).filter(TaskModel.id == task_id).first()


def list_tasks(db: Session, skip: int = 0, limit: int = 10) -> list[TaskModel]:
    return db.query(TaskModel).offset(skip).limit(limit).all()
```

### Wiring it into an endpoint

```python
# main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import TaskCreate, TaskOut
import crud

app = FastAPI()


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task_endpoint(task: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)
```

Notice the endpoint itself is now very small: validate input (Pydantic,
automatic) → delegate to `crud.create_task` → FastAPI filters the response
through `TaskOut` (Module 04). Each layer does exactly one job.

### Key ideas here

- **`db.add()` stages a change; `db.commit()` writes it to disk;
  `db.refresh()` reloads the object from the database** (picking up
  values the database itself generated, like the auto-incrementing `id`).
  This three-step pattern is worth memorizing — it's the same shape for
  every create operation.
- **CRUD functions take a `db: Session` as their first argument** rather
  than creating their own session — the session is *injected* (Module 06),
  which makes these functions independently testable and keeps a single
  session per request, avoiding subtle bugs from mixing sessions.
- **`TaskModel | None` as `get_task`'s return type** — same "might not
  exist" signal used in the Railway Booking course's service classes.
  Deciding what to do when it's `None` (404 error) belongs in the endpoint,
  covered next in Module 08.

## Try it yourself

1. Set up `database.py`, `models.py`, and `crud.py` as shown, and wire up
   `POST /tasks` using a real SQLite database.
2. Confirm `taskflow.db` is created in your project folder after running
   the server and creating a task.
3. Add `crud.delete_task(db, task_id)` and `crud.update_task(db, task_id,
   updates)` functions, following the same pattern.
4. **Challenge:** add a second model, `UserModel`, with a foreign key
   `owner_id` on `TaskModel` linking each task to a user — you'll need
   this for Module 09.

**Next:** `08_error_handling_and_exceptions.md`
