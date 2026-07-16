---
name: run_localhost
description: Start the contact_app locally — bring up the PostgreSQL Docker container, launch the FastAPI server with uvicorn, and open http://localhost:8000 in the browser. Use when the user asks to run, start, or open the app/server/localhost.
---

# Run contact_app on localhost

Follow these steps in order. Skip a step if its check shows it is already done.

## 1. Start the database (PostgreSQL in Docker)

The app expects PostgreSQL at `localhost:5432`, database `contactdb`, user/password `postgres`/`postgres` (see `database.py`; can be overridden with the `DATABASE_URL` env var).

Check whether the container is running:

```powershell
docker ps --filter "name=pg-lab" --format "{{.Names}} {{.Status}}"
```

- If it shows `pg-lab Up ...` → database is ready, go to step 2.
- If nothing is shown, start the existing container:

```powershell
docker start pg-lab
```

- If `docker start` fails because the container doesn't exist, create it:

```powershell
docker run -d --name pg-lab -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=contactdb -p 5432:5432 postgres:16
```

Tables are created automatically on app startup (`Base.metadata.create_all` in `main.py`) — no migration step needed.

## 2. Start the FastAPI server

Check whether port 8000 is already in use (server may already be running):

```powershell
Test-NetConnection -ComputerName localhost -Port 8000 -InformationLevel Quiet -WarningAction SilentlyContinue
```

- If `True` → server is already running, go to step 3.
- If `False`, start uvicorn **in the background** (use `run_in_background: true`) with the project venv's Python:

```powershell
& "C:\big21\vibe-coding\project\contact_app\.venv\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Then poll port 8000 until it responds (up to ~20 s):

```powershell
$deadline = (Get-Date).AddSeconds(20); do { $ok = Test-NetConnection -ComputerName localhost -Port 8000 -InformationLevel Quiet -WarningAction SilentlyContinue; if (-not $ok) { Start-Sleep -Milliseconds 500 } } until ($ok -or (Get-Date) -gt $deadline); $ok
```

If the server fails to start, read the background task's output file — a `psycopg` connection error means the database (step 1) isn't up.

## 3. Open in the browser

```powershell
Start-Process "http://localhost:8000"
```

## Notes

- API docs are at http://localhost:8000/docs (FastAPI Swagger UI).
- A `401 Unauthorized` on `GET /auth/me` in the server log is normal before login.
- A `ConnectionResetError: [WinError 10054]` traceback in the log is a harmless Windows/asyncio quirk from the browser aborting the background-video stream — ignore it.
- To stop the server, stop the background uvicorn task (or kill the process listening on port 8000).
