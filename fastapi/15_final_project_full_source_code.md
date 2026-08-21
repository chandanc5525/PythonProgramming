# 15 — Final Project: The Complete TaskFlow API

## Scenario

You've built every concept across 14 modules. This file assembles a
working, simplified version of TaskFlow into the final project layout so
you can run the whole thing end-to-end. Create each file exactly as shown
in a `taskflow/` folder.

```
taskflow/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── security.py
├── crud.py
├── exceptions.py
└── routers/
    ├── __init__.py
    ├── auth.py
    └── tasks.py
```

Install dependencies:

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy "pydantic[email]" \
            "python-jose[cryptography]" "passlib[bcrypt]" python-multipart
```

---

### `database.py`

```python
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

---

### `models.py`

```python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    tasks = relationship("TaskModel", back_populates="owner")


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    priority = Column(String(20), default="medium")
    done = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserModel", back_populates="tasks")
```

---

### `schemas.py`

```python
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")


class TaskOut(BaseModel):
    id: int
    title: str
    priority: str
    done: bool

    class Config:
        from_attributes = True
```

`class Config: from_attributes = True` tells Pydantic it's allowed to read
data from an ORM object's *attributes* (`task.title`) rather than only
from a dict — necessary since `crud.py` returns SQLAlchemy model
instances, not dicts.

---

### `security.py`

```python
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext

from database import get_db
import crud

SECRET_KEY = "dev-only-secret-change-me"   # load from an env var in real deployments
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

---

### `crud.py`

```python
from sqlalchemy.orm import Session
from models import UserModel, TaskModel
from schemas import UserCreate, TaskCreate
from security import hash_password


def create_user(db: Session, user: UserCreate) -> UserModel:
    db_user = UserModel(username=user.username, email=user.email,
                         hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()


def create_task(db: Session, task: TaskCreate, owner_id: int) -> TaskModel:
    db_task = TaskModel(title=task.title, priority=task.priority, owner_id=owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int):
    return db.query(TaskModel).filter(TaskModel.id == task_id).first()


def list_tasks_for_user(db: Session, owner_id: int, skip: int = 0, limit: int = 10):
    return (db.query(TaskModel)
              .filter(TaskModel.owner_id == owner_id)
              .offset(skip).limit(limit).all())
```

---

### `exceptions.py`

```python
class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id


class NotTaskOwnerError(Exception):
    pass
```

---

### `routers/auth.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from schemas import UserCreate, UserOut
from security import verify_password, create_access_token
import crud

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    return crud.create_user(db, user)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
```

---

### `routers/tasks.py`

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas import TaskCreate, TaskOut
from security import get_current_user
from exceptions import TaskNotFoundError, NotTaskOwnerError
import crud

router = APIRouter(prefix="/tasks", tags=["tasks"],
                    dependencies=[Depends(get_current_user)])


@router.post("/", response_model=TaskOut, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db),
                 current_user=Depends(get_current_user)):
    return crud.create_task(db, task, owner_id=current_user.id)


@router.get("/", response_model=list[TaskOut])
def list_my_tasks(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100),
                   db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.list_tasks_for_user(db, current_user.id, skip, limit)


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db),
             current_user=Depends(get_current_user)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise TaskNotFoundError(task_id)
    if task.owner_id != current_user.id:
        raise NotTaskOwnerError()
    return task
```

---

### `main.py`

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
import models
from routers import auth, tasks
from exceptions import TaskNotFoundError, NotTaskOwnerError

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(TaskNotFoundError)
def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(status_code=404,
                         content={"detail": f"Task {exc.task_id} not found"})


@app.exception_handler(NotTaskOwnerError)
def not_owner_handler(request: Request, exc: NotTaskOwnerError):
    return JSONResponse(status_code=403,
                         content={"detail": "You do not own this task"})


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(tasks.router)
```

---

### `routers/__init__.py`

```python
# empty — makes routers/ a package
```

---

## Running the project

```bash
cd taskflow
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` and:

1. `POST /register` — create a user
2. `POST /login` — get a JWT (use the "Authorize" button in `/docs` to
   store it)
3. `POST /tasks/` — create a task (now requires auth, enforced at the
   router level)
4. `GET /tasks/` — list your own tasks

## Where to go from here

You've covered routing, validation, response shaping, dependency
injection, a real database, error handling, authentication, middleware,
async concerns, project structure, testing, and file uploads. Natural next
steps:

1. **Add the testing setup from Module 13** (`conftest.py` with an
   overridden test database) and write tests for every endpoint above.
2. **Add the attachment endpoints from Module 14**, scoped to task
   ownership.
3. **Add pagination metadata** to `GET /tasks/` (total count, next/prev
   links) instead of just a raw list.
4. **Add rate limiting** (e.g. with `slowapi`) to `/login` to prevent
   brute-force password guessing.
5. **Containerize it** with Docker, and deploy behind a production ASGI
   setup (`uvicorn` with multiple workers, behind Nginx or a managed
   platform) — replacing `--reload` and the hardcoded `SECRET_KEY` with
   production-appropriate configuration loaded from environment variables.

You've gone from a single `@app.get("/")` in Module 01 to a structured,
authenticated, tested, database-backed API — the same beginner → advanced
arc as the Railway Booking System course, applied to a real web framework.
