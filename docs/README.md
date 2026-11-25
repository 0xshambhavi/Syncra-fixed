# Syncra — Local setup and demo

Syncra is a React + Vite + TypeScript frontend backed by a FastAPI service. The repository currently includes a local in-memory demo backend so that the UI and API can be started without Supabase credentials.

## Start the application

From the repository root, open two terminals.

**Terminal 1 — API**

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8000
```

**Terminal 2 — web app**

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:5173. API docs are at http://localhost:8000/docs and the health check is http://localhost:8000/health.

## Demo logins

| Role | Email | Password |
|---|---|---|
| Student | student@example.edu | syncra123 |
| Club president | president@example.edu | syncra123 |
| Faculty | faculty@example.edu | syncra123 |

The sign-up screen also creates a local demo account. Role permissions are enforced by the API for event creation and budget review.

## Current API surface

- `POST /api/v1/auth/signup`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me`
- `GET /api/v1/public/events`, `GET /api/v1/events`, `POST /api/v1/events`
- `POST /api/v1/events/{event_id}/register`
- `GET /api/v1/notifications`, `POST /api/v1/notifications/{notification_id}/read`
- `POST /api/v1/budget/request`, `GET /api/v1/budget/requests`, `POST /api/v1/budget/decision/{event_id}`
- `GET /api/v1/venues`

## Demo scope and production work

Data is in memory and is cleared when the API process restarts. Supabase, durable database storage, email verification, production-grade password hashing, payment processing and realtime updates are not connected. Do not use real personal information or deploy this prototype as-is. Before production, implement secure credential storage, identity verification, persistent storage, authorization policies, rate limiting, secrets management and tests for every role-protected workflow.
