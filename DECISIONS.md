# DECISIONS.md

## Phase 0 – Walking Skeleton

- **Windows PowerShell** is the primary development shell; all commands in README are PowerShell‑compatible. A Bash block is provided for macOS/Linux users.
- Backend runs from the `backend` folder with `uvicorn app.main:app --reload`; therefore `backend/app/__init__.py` is required.
- Tests are placed under `backend/tests/` and are discoverable by `pytest -q` when run from the `backend` directory.
- The frontend expects the backend URL in the environment variable `VITE_API_URL`. A `.env.example` is provided; the actual `.env` is ignored by `.gitignore`.
- Versions are pinned in `requirements.txt` and `package.json` to guarantee reproducible installs.
- If the GitHub CLI (`gh`) is unavailable, the PR URL will be printed for manual creation.
