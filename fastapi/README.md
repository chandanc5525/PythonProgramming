# ⚡ FastAPI — Beginner to Advanced, One Project at a Time

This folder is a step-by-step course that builds **TaskFlow API**, a task
management REST API, using FastAPI. Each `.md` file covers one concept: a
**scenario**, the **logic/reasoning** behind the approach, and **working
Python code**.

It's for learners who know core Python and basic web concepts (what an
HTTP request/response is) and want to go from **beginner → intermediate →
advanced** FastAPI by building something real.

## How to use this folder

1. Go through files **in numeric order** — later modules build on earlier
   code.
2. Run every example — FastAPI's interactive docs (`/docs`) make it easy to
   test each endpoint as you add it.
3. Each file ends with **"Try it yourself"** exercises.
4. `15_final_project_full_source_code.md` assembles everything into one
   runnable app.

## Roadmap

| # | File | Level | Concept Focus |
|---|------|-------|----------------|
| 01 | `01_introduction_and_setup.md` | Beginner | What FastAPI is, install, first app |
| 02 | `02_path_operations_and_parameters.md` | Beginner | Routes, path & query parameters |
| 03 | `03_pydantic_models_and_request_bodies.md` | Beginner | Request bodies, validation basics |
| 04 | `04_response_models_and_status_codes.md` | Beginner | Response shaping, status codes |
| 05 | `05_validation_with_query_path_body.md` | Beginner→Intermediate | `Query`, `Path`, `Field` constraints |
| 06 | `06_dependency_injection.md` | Intermediate | `Depends`, shared/reusable logic |
| 07 | `07_database_integration_sqlalchemy.md` | Intermediate | SQLAlchemy models, sessions, CRUD |
| 08 | `08_error_handling_and_exceptions.md` | Intermediate | `HTTPException`, custom handlers |
| 09 | `09_authentication_and_jwt.md` | Intermediate→Advanced | OAuth2, password hashing, JWT |
| 10 | `10_middleware_and_cors.md` | Intermediate | Middleware, CORS |
| 11 | `11_background_tasks_and_async.md` | Intermediate→Advanced | `async`/`await`, `BackgroundTasks` |
| 12 | `12_routers_and_project_structure.md` | Advanced | `APIRouter`, scaling the codebase |
| 13 | `13_testing_fastapi.md` | Advanced | `TestClient`, pytest |
| 14 | `14_file_uploads_and_static_files.md` | Advanced | `UploadFile`, serving static files |
| 15 | `15_final_project_full_source_code.md` | — | The complete assembled application |

## The scenario used throughout

You're building **TaskFlow API** — a backend for a task management app. It
needs to:

- Let users sign up and log in securely (JWT-based auth)
- Let authenticated users create, read, update, and delete their own tasks
- Store data in a real database (SQLite via SQLAlchemy)
- Validate all input and return clean, predictable error responses
- Support file attachments on tasks
- Be organized into multiple files/routers, not one giant `main.py`
- Have automated tests

Every module builds one piece of this.

## Prerequisites

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy pydantic[email] \
            python-jose[cryptography] passlib[bcrypt] python-multipart \
            pytest httpx
```

Python 3.9+ recommended.

Start with `01_introduction_and_setup.md`.
