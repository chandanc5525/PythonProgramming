# 09 — Authentication with OAuth2 & JWT

## Scenario

Right now, *anyone* can create, view, or delete *any* task — there's no
concept of "who's asking." TaskFlow needs users to sign up, log in, and
have their tasks scoped to their own account only.

## Logic: the pieces of token-based authentication

1. **Password hashing** — never store plain-text passwords.
2. **Login endpoint** — verify credentials, issue a **JWT** (JSON Web
   Token) — a signed, tamper-proof string the client stores and sends back
   with future requests.
3. **A dependency** that reads the token from each request, verifies it,
   and looks up the current user — reusable across every protected
   endpoint (this is exactly the `get_current_user` preview from
   Module 06).

### Password hashing

```python
# security.py

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

Never store `password` directly — always store `hash_password(password)`.
`verify_password` re-hashes the login attempt and compares, rather than
ever decrypting the stored hash (bcrypt hashing is one-way by design).

### Creating and verifying JWTs

```python
# security.py (continued)

from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "change-this-to-a-real-secret-loaded-from-an-env-variable"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
```

A JWT is a **signed** string — the server can verify it hasn't been
tampered with (using `SECRET_KEY`), and it carries an expiry (`exp`) baked
in. **`SECRET_KEY` must never be hardcoded like this in real code** — load
it from an environment variable, and never commit it to version control.

### The login endpoint

```python
# main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from security import verify_password, create_access_token
import crud

app = FastAPI()


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

`OAuth2PasswordRequestForm` is a FastAPI-provided dependency that expects
standard form fields (`username`, `password`) — the conventional shape for
a login request under the OAuth2 spec, which is why `/docs` shows a proper
login form (and a padlock icon) for this endpoint automatically.

### Protecting endpoints with a reusable dependency

```python
# security.py (continued)

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = payload.get("sub")
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

```python
# main.py

from security import get_current_user

@app.get("/tasks/mine", response_model=list[TaskOut])
def my_tasks(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.list_tasks_for_user(db, current_user.id)
```

Any endpoint that adds `current_user=Depends(get_current_user)` is
instantly protected — FastAPI runs the whole chain
(`oauth2_scheme` → `get_current_user`) before your function body executes,
and rejects unauthenticated requests with `401` automatically.

### Key ideas here

- **`401 Unauthorized`** = "I don't know who you are" (missing/invalid
  token). **`403 Forbidden`** = "I know who you are, but you're not
  allowed to do this" (e.g., trying to delete someone *else's* task).
  Using the right one matters for clients reacting to failures correctly.
- **The dependency chain is the whole point of Module 06.** Auth isn't a
  special FastAPI feature bolted on — it's the exact same `Depends`
  mechanism, just composed: `get_current_user` depends on `oauth2_scheme`
  and `get_db`.
- **Never compare passwords with `==`.** Password verification must go
  through a hashing library's `verify` function (`pwd_context.verify`),
  which is designed to resist timing attacks — a plain string comparison
  is not.

## Try it yourself

1. Add a `UserModel` (Module 07's challenge), `hash_password` at
   registration, and the `/login` endpoint above.
2. Protect `POST /tasks` with `current_user=Depends(get_current_user)` and
   confirm `/docs` now requires a token (click "Authorize").
3. **Challenge:** update `crud.get_task` usage so a user can only fetch
   *their own* tasks — return `403` (not `404`) if the task exists but
   belongs to someone else, to avoid leaking whether the task ID exists at
   all.

**Next:** `10_middleware_and_cors.md`
