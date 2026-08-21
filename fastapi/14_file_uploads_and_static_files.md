# 14 — File Uploads & Static Files

## Scenario

TaskFlow users want to attach a file (a screenshot, a document) to a task.
We need an endpoint that accepts file uploads and a way to serve those
files back.

## Logic: `UploadFile` for receiving files

```bash
pip install python-multipart   # required for form/file uploads
```

```python
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_TYPES = {"image/png", "image/jpeg", "application/pdf"}
MAX_SIZE_MB = 5


@app.post("/tasks/{task_id}/attachment")
async def upload_attachment(task_id: int, file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400,
                             detail=f"File type {file.content_type} not allowed")

    contents = await file.read()
    if len(contents) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400,
                             detail=f"File exceeds {MAX_SIZE_MB}MB limit")

    file_path = UPLOAD_DIR / f"task_{task_id}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)

    return {"filename": file.filename, "size_bytes": len(contents),
            "content_type": file.content_type}
```

### Key ideas here

- **`UploadFile` vs. `bytes`**: FastAPI also supports
  `file: bytes = File(...)`, which loads the *entire* file into memory
  immediately. `UploadFile` is preferred for anything beyond tiny files —
  it's backed by a spooled temporary file, only fully loaded into memory
  if it exceeds a size threshold, so large uploads don't spike your
  server's memory usage.
- **`await file.read()`** — reading an `UploadFile` is an async operation
  (it may involve actual disk I/O for large files), so the endpoint must
  be `async def` and this call must be awaited (recall Module 11's
  reasoning about why blocking I/O inside `async def` is a problem —
  `UploadFile`'s methods are properly async-native, so this is safe).
- **Always validate `content_type` and size before trusting a file.** A
  client can claim any filename or extension it wants — checking
  `content_type` (with awareness that this is client-supplied and can be
  spoofed) and enforcing a size cap are baseline safeguards. Real
  production systems often go further (checking actual file *content*,
  virus scanning, storing files outside the web root).
- **Never trust `file.filename` directly for constructing a file path**
  without sanitizing it — a malicious filename like `../../etc/passwd`
  could attempt a path traversal attack. The example above prefixes with
  `task_{task_id}_`, but a real system should strip path separators from
  `file.filename` explicitly, or generate a new filename entirely (e.g., a
  UUID) rather than trusting client input for the path.

## Logic: serving files back with `StaticFiles`

```python
from fastapi.staticfiles import StaticFiles

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
```

Now any file in the `uploads/` folder is servable directly, e.g.
`GET /uploads/task_5_screenshot.png` returns the raw file. `app.mount`
hands off an entire URL prefix to a different, specialized ASGI
application (`StaticFiles`) rather than going through your regular path
operations — useful for serving assets efficiently without writing a
custom endpoint for every file.

**Caution:** mounting `uploads/` directly like this makes every file in it
publicly accessible to anyone with the URL, with no access control. For
TaskFlow (where attachments belong to a specific user's task), you'd
instead want a proper endpoint like
`GET /tasks/{task_id}/attachment` that checks `current_user` owns
`task_id` (Module 09) before returning the file — trading the convenience
of `StaticFiles` for actual access control.

## Try it yourself

1. Add the upload endpoint, and test it via `/docs` — note that `/docs`
   automatically renders a file-picker UI for `UploadFile` parameters.
2. Try uploading a file over the 5MB limit and a disallowed file type —
   confirm both are rejected with `400`.
3. **Challenge:** rewrite file retrieval as a proper endpoint
   (`GET /tasks/{task_id}/attachment`) that checks the requesting user
   owns the task before returning the file with `FileResponse`, instead of
   using an unrestricted `StaticFiles` mount.

**Next:** `15_final_project_full_source_code.md`
