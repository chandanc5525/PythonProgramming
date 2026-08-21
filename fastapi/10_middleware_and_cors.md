# 10 — Middleware & CORS

## Scenario

Two new needs: (1) TaskFlow's frontend runs on a different domain
(`http://localhost:3000`) than the API (`http://localhost:8000`) — browsers
block this by default unless the API explicitly allows it. (2) You want to
log how long every request takes, without adding timing code to every
single endpoint.

## Logic: middleware runs around every request

Middleware is code that runs **before and after every request**, no
matter which endpoint handles it — the same "shared behavior, defined
once" idea as dependencies (Module 06), but applied at the whole-app level
rather than per-endpoint.

### Custom middleware — request timing

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)          # runs the actual endpoint
    duration = time.time() - start_time
    response.headers["X-Process-Time"] = str(duration)
    return response
```

- `call_next(request)` is how the middleware hands control to the next
  step (another middleware, or the endpoint itself) and gets the response
  back.
- Code **before** `call_next` runs on the way in; code **after** runs on
  the way out — this "before/after" shape is the defining feature of
  middleware.
- Every single response from every endpoint now carries an
  `X-Process-Time` header — added in one place.

### CORS — Cross-Origin Resource Sharing

By default, a browser blocks JavaScript on `localhost:3000` from calling
an API on `localhost:8000` — this is a browser security feature, not a
FastAPI limitation. The API must explicitly say which origins are allowed.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://taskflow.example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

- `allow_origins` — **never use `["*"]` in production if
  `allow_credentials=True`** — that combination would let *any* website
  make authenticated requests to your API on a logged-in user's behalf,
  a real security risk. List specific trusted domains instead.
- `allow_methods=["*"]` / `allow_headers=["*"]` — permissive for
  development; in production, consider narrowing these to only what your
  frontend actually needs.

### Key ideas here

- **`CORSMiddleware` is built into FastAPI/Starlette** — you configure it,
  you don't write the CORS logic yourself. This is the most common
  middleware every real FastAPI project needs, so it's worth recognizing
  immediately.
- **Middleware order matters.** Middleware added later runs "closer" to
  your endpoint (added middlewares wrap around each other, like layers of
  an onion). If you add both custom timing middleware and `CORSMiddleware`,
  think about which should see the request first.
- **Middleware vs. dependencies — when to use which:**
  - Use a **dependency** (Module 06) when the behavior only applies to
    *some* endpoints, or needs to inject a value into the endpoint
    function (like `db` or `current_user`).
  - Use **middleware** when the behavior applies to *every* request
    uniformly and doesn't need to hand data into the endpoint function
    itself (like logging, timing, or CORS headers).

## Try it yourself

1. Add the timing middleware, make a few requests, and inspect the
   `X-Process-Time` response header in `/docs` or your browser's network
   tab.
2. Add `CORSMiddleware` allowing `http://localhost:3000`, and confirm (by
   reading the config, or testing with a simple frontend if you have one)
   that other origins would be rejected.
3. **Challenge:** write middleware that logs `request.method` and
   `request.url.path` to the console for every incoming request — a
   minimal request logger.

**Next:** `11_background_tasks_and_async.md`
