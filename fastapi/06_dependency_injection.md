# 06 — Dependency Injection with `Depends`

## Scenario

Multiple TaskFlow endpoints need the same things repeated: a database
session, the currently logged-in user, and shared pagination parameters.
Copy-pasting this setup into every function is error-prone and hard to
change later. FastAPI's `Depends` mechanism solves exactly this.

## Logic: a dependency is just a function FastAPI calls for you

```python
from fastapi import FastAPI, Depends

app = FastAPI()


def get_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


@app.get("/tasks")
def list_tasks(pagination: dict = Depends(get_pagination)):
    return {"pagination": pagination, "tasks": []}
```

What happens: before running `list_tasks`, FastAPI calls
`get_pagination(...)` itself — reading `skip`/`limit` from the query
string exactly as it would for a normal path operation — and passes the
**result** into `list_tasks` as `pagination`. The dependency function
looks and behaves just like a path operation function, which is what makes
this pattern easy to pick up once Module 02/05 make sense.

### Why this matters: reuse across many endpoints

```python
@app.get("/tasks")
def list_tasks(pagination: dict = Depends(get_pagination)):
    ...

@app.get("/users")
def list_users(pagination: dict = Depends(get_pagination)):
    ...
```

Both endpoints share identical pagination validation and parsing — defined
**once**. If the pagination rules change (say, `limit` should default to
20), you change `get_pagination` in one place.

### The pattern that matters most: database sessions

This is the single most common use of `Depends` in real FastAPI apps —
previewing it here so it's familiar in Module 07:

```python
def get_db():
    db = SessionLocal()   # open a database session
    try:
        yield db           # hand it to the endpoint
    finally:
        db.close()          # always close it, even if the endpoint raised an error


@app.get("/tasks")
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()
```

- **`yield` instead of `return`** makes this a dependency *with cleanup*.
  Code before `yield` runs before the endpoint; code after `yield` (in
  `finally`) runs after the endpoint finishes — success or failure. This
  guarantees the database connection is always released, exactly like
  `with open(...)` guarantees a file gets closed (a pattern you may
  recognize from the Railway Booking course's persistence module).
- **Every endpoint gets its own fresh, isolated session** — FastAPI calls
  `get_db()` again for each incoming request.

### Dependencies can depend on other dependencies

```python
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # decode token, look up user in db (full version in Module 09)
    ...
    return user


@app.get("/tasks/mine")
def my_tasks(user=Depends(get_current_user)):
    return {"owner": user.username, "tasks": []}
```

`get_current_user` itself depends on `get_db` and a token dependency —
FastAPI resolves this whole chain automatically. This is how
authentication (Module 09) plugs into any endpoint that needs to know
"who's asking" with a single `Depends(get_current_user)`.

### Key ideas here

- **Dependency injection means: your function declares what it *needs*,
  and something else (FastAPI) is responsible for *providing* it.** Your
  endpoint function doesn't know or care how `db` was created — it just
  receives a ready-to-use session.
- **This is the FastAPI equivalent of the "service layer" idea** from the
  Railway Booking course — pulling shared, reusable logic out of individual
  functions into one place, called from many endpoints.
- **Dependencies are testable in isolation** — since `get_pagination` is
  just a normal function, you can call it directly in a unit test without
  spinning up a whole FastAPI app (Module 13 builds on this).

## Try it yourself

1. Write `get_pagination` as shown, and use it in two different endpoints.
2. Write a dependency `get_query_token(x_token: str = Header())` that reads
   a custom header (needs `from fastapi import Header`) and returns it.
3. **Challenge:** write a dependency that raises an `HTTPException` (a
   sneak peek at Module 08) if a query parameter `admin=true` is *not*
   present — simulating a very simple access check.

**Next:** `07_database_integration_sqlalchemy.md`
