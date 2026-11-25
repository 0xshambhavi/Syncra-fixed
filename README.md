# Syncra

A campus events platform for students, club presidents and faculty.

## Run locally

**Requirements:** Python 3.10+ and Node.js 20+.

### 1. Start the backend

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8000
```

Backend health: http://localhost:8000/health  
Interactive API docs: http://localhost:8000/docs

### 2. Start the frontend (in a second terminal)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

### Demo accounts

All three demo accounts use the password `syncra123`:

- `student@example.edu`
- `president@example.edu`
- `faculty@example.edu`

You can also create an account from the sign-up page. The local demo stores data in memory; restarting the backend resets new accounts, registrations, notifications and created events. The two sample events are loaded at startup.

## Important demo limitations

This is a runnable local prototype, not a production deployment. Authentication tokens and application data are held in memory, passwords are not persisted securely, and no real email verification, Supabase database, payment processing or realtime service is configured. Do not use real personal information or deploy this demo as-is. Configure persistent storage, password hashing, rate limiting, verified identity and database access policies before production.
