# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (requires MongoDB at localhost:27017)
uvicorn main:app --reload

# Run with Docker (includes MongoDB)
docker-compose up

# Run all tests
pytest tests/ -v

# Run a single test
pytest tests/test_task.py::test_create_task -v

# Run tests with output
pytest tests/ -v -s
```

Tests require a running MongoDB instance — no mocking is used.

## Architecture

FastAPI + MongoDB + JWT auth. Layered: routes → services → database.

```
main.py
app/
  config/     — Settings (Pydantic BaseSettings from .env), DB connection, JWT/password utils, custom exceptions
  models/     — Pydantic schemas: Task (models.py), User (user.py)
  services/   — Business logic: crud.py (tasks), user.py (users), pdf.py (ReportLab PDF export)
  routes/
    router.py              — Aggregates all sub-routers
    endpoints/
      task_routes.py       — /tasks CRUD + PDF export
      auth/auth.py         — /auth register, login, profile
      admin/admin.py       — /admin user list + role change (admin role required)
```

**Request flow:** route handler → validates with Pydantic model → calls service → PyMongo → MongoDB.

**Auth flow:** `POST /auth/login` returns a JWT bearer token. All `/tasks` and `/admin` routes require `Authorization: Bearer <token>`. Token lifetime: 1440 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`).

**RBAC:** Two roles — `user` (default) and `admin`. Admin routes enforce role check in `app/routes/endpoints/admin/admin.py`. Role changes are done via `PUT /admin/users/{username}/role`.

## Environment Variables

```
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=taskflow
SECRET_KEY=your-secret-key-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=1440
APP_NAME=TaskFlow API
APP_VERSION=1.0.0
DEBUG=false
```

Copy `.env.example` → `.env` before running locally. Docker Compose injects `MONGO_URI=mongodb://mongo:27017` automatically.

## Key Design Notes

- Password hashing uses `bcrypt` directly (`app/config/security.py`).
- Tasks are scoped to the authenticated user via `user_id` field — all CRUD queries filter by `user_id`.
- `POST /auth/register` always creates `role="user"`. Admin creation is only possible via `PUT /admin/users/{username}/role` by an existing admin, or by calling `create_user()` service directly (e.g. in tests/seeds).
- List endpoints support pagination: `GET /tasks?skip=0&limit=20`, `GET /admin/users?skip=0&limit=20` (max limit: 100).
- MongoDB indexes: `users.username` (unique), `users.email` (unique), `tasks.user_id`. Created automatically on startup in `database.py:_create_indexes()`.
- MongoDB IDs are serialized as strings; `_id` is remapped to `id` in response models.
- `get_current_user` (returns username string from JWT) is used for all task endpoints — no extra DB lookup. `get_current_user_with_role` (fetches full user from DB) is used only where role data is needed (profile, admin).

## Remaining TODOs

- Refresh token support
