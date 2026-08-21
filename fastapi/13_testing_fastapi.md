# 13 — Testing FastAPI with `TestClient`

## Scenario

TaskFlow now has real logic: auth, database operations, validation. Every
manual check through `/docs` takes time and doesn't scale as the app
grows. We need automated tests, the same motivation as Module 13 in the
Railway Booking course — but here we're testing **HTTP endpoints**, not
just plain Python functions.

## Logic: `TestClient` simulates real HTTP requests without a running server

```bash
pip install pytest httpx
```

```python
# tests/test_tasks.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_task_requires_auth():
    response = client.post("/tasks/", json={"title": "Buy milk"})
    assert response.status_code == 401


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

Run with:

```bash
pytest tests/ -v
```

`TestClient` wraps your actual FastAPI `app` and lets you call it exactly
like a real HTTP client would (`client.get`, `.post`, `.put`, `.delete`) —
no server process needs to be running.

## Logic: testing authenticated endpoints

```python
def get_auth_headers(client):
    client.post("/register", json={
        "username": "testuser", "password": "testpass123", "email": "test@example.com"
    })
    response = client.post("/login", data={"username": "testuser", "password": "testpass123"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_task_succeeds_when_authenticated():
    headers = get_auth_headers(client)
    response = client.post("/tasks/", json={"title": "Buy milk"}, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["done"] is False
```

Notice this test **exercises the real flow**: register → log in → get a
real JWT → use it in the `Authorization` header — exactly like a real
client would, rather than mocking the auth logic away.

## Logic: using a separate test database

Running tests against your real `taskflow.db` risks polluting real data,
and tests should be repeatable/isolated. **Override the `get_db`
dependency** during tests to point at a throwaway database:

```python
# tests/conftest.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)   # clean slate after every test


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
```

### Key ideas here

- **`app.dependency_overrides[get_db] = override_get_db`** is FastAPI's
  built-in mechanism for swapping a dependency during tests — this is the
  direct payoff of using `Depends` in the first place (Module 06):
  anything injected can be substituted, without changing a single line of
  your actual endpoint code.
- **`autouse=True` on the `setup_database` fixture** means it runs
  automatically before *every* test, without each test needing to request
  it explicitly — tests always start from a clean, empty database.
- **Test the behaviors that matter, not implementation details**: "an
  unauthenticated request is rejected," "a valid request returns the
  correct shape," "a task can't be fetched by a user who doesn't own it"
  (from Module 09's challenge) — these describe *what the API guarantees*,
  which is exactly what you want protected by tests as the codebase grows.
- **This mirrors the Railway Booking project's `setUp()` pattern** — fresh
  state before every test — just implemented through FastAPI's dependency
  override system instead of a plain class constructor.

## Try it yourself

1. Set up `conftest.py` with a test database as shown, and write
   `test_create_task_requires_auth` and
   `test_create_task_succeeds_when_authenticated`.
2. Add a test confirming a `404` is returned when fetching a task ID that
   doesn't exist.
3. **Challenge:** write a test proving that User A cannot fetch or delete
   User B's task (revisit Module 09's `403` challenge if you built it).

**Next:** `14_file_uploads_and_static_files.md`
