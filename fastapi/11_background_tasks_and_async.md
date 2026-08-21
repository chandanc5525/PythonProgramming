# 11 — `async`/`await` & Background Tasks

## Scenario

Two related but different problems: (1) when a task is created, TaskFlow
should send a confirmation email — but the client shouldn't have to *wait*
for the email to send before getting a response. (2) Some of TaskFlow's
future endpoints will call slow external services (a weather API for a
"due today" reminder, say) — done wrong, this could make the *entire
server* slow down for all users, not just the one making that request.

## Logic: `async def` and why it matters

```python
@app.get("/slow-sync")
def slow_sync_endpoint():
    time.sleep(5)   # blocks the ENTIRE server for 5 seconds
    return {"done": True}


@app.get("/slow-async")
async def slow_async_endpoint():
    await asyncio.sleep(5)   # only pauses THIS request; server handles others meanwhile
    return {"done": True}
```

FastAPI can run both `def` and `async def` endpoints. The difference
matters under load:

- A regular `def` endpoint that does something slow **blocks the worker
  thread handling it** — while `time.sleep(5)` runs, that worker can't
  serve other requests (FastAPI runs sync `def` endpoints in a thread
  pool, so it's not a total server freeze, but it does consume a limited
  thread pool slot).
- An `async def` endpoint that properly `await`s a slow operation lets the
  event loop serve *other* requests during that wait — genuinely
  non-blocking, and far more efficient at scale.

**The rule that matters in practice:** if you use `async def`, everything
slow inside it must also be awaitable (`await some_async_db_call()`,
`await httpx_client.get(...)`). Calling a *blocking* function like
`time.sleep()` or a non-async database driver inside an `async def`
endpoint defeats the purpose and can actually make things worse — it
blocks the entire event loop, not just one worker thread. When in doubt
with blocking libraries, a plain `def` endpoint (which FastAPI runs in a
thread pool automatically) is often the safer, simpler choice.

## Logic: `BackgroundTasks` for "fire and forget" work

For the confirmation-email scenario, we don't need concurrency — we need
the response to go out *immediately*, with the email sent afterward.

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()


def send_confirmation_email(email: str, task_title: str):
    # Simulate sending an email (replace with real email logic)
    print(f"Sending email to {email}: your task '{task_title}' was created")


@app.post("/tasks")
def create_task(task: TaskCreate, background_tasks: BackgroundTasks,
                 current_user=Depends(get_current_user)):
    new_task = crud.create_task(db, task)
    background_tasks.add_task(send_confirmation_email, current_user.email, task.title)
    return new_task   # response sent to client immediately; email sends after
```

- `background_tasks.add_task(function, *args)` schedules `function` to run
  **after** the response has already been sent to the client.
- The client sees the task created instantly — the email delay is invisible
  to them.

### When `BackgroundTasks` is *not* enough

`BackgroundTasks` runs in the same process as your API — fine for quick,
non-critical work (sending a log entry, a notification). For anything that
must survive a server restart, retry on failure, or run heavy/long
processing, a dedicated task queue (like **Celery** or **RQ**, backed by
Redis) is the right tool — that's beyond this course's scope, but good to
know the boundary: `BackgroundTasks` is for lightweight, best-effort,
in-process work only.

### Key ideas here

- **`async def` is about concurrency (handling many requests
  efficiently), not about "running in the background."** These are
  different concepts that beginners often conflate — `async` doesn't delay
  work past the response; it lets the *server* stay responsive to other
  requests while waiting on I/O.
- **`BackgroundTasks` is about deferring work past the response** — the
  opposite concern from `async`. You can combine both: an `async def`
  endpoint using `BackgroundTasks` for genuinely fire-and-forget work.
- **Never `await` inside a background task function unless the function
  itself is `async def`** — `background_tasks.add_task` supports both sync
  and async functions; just match the function's definition to how it's
  actually written.

## Try it yourself

1. Add `send_confirmation_email` as a background task to `create_task`,
   and confirm (via printed output) that it runs *after* the response is
   returned.
2. Write an `async def` endpoint that uses `await asyncio.sleep(2)` and
   test that other requests aren't blocked while it's "sleeping" (try
   hitting a different endpoint from another browser tab while it runs).
3. **Challenge:** research (or just reason through) why calling a
   synchronous, blocking database driver inside an `async def` endpoint
   would be a problem, even though the code "runs."

**Next:** `12_routers_and_project_structure.md`
