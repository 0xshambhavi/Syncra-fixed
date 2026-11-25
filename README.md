# README.md

## Repository Overview
This monorepo contains two main applications:
- **backend** – FastAPI service exposing a health endpoint.
- **frontend** – Vite + React + TypeScript + Tailwind UI that calls the backend health endpoint.

---
### Windows (PowerShell) commands
```powershell
# Clone the repo (if you haven't already)
git clone https://github.com/0xshambhavi/Syncra-fixed.git
cd Syncra-fixed

# ---------- Backend ----------
# Create a virtual environment
python -m venv venv
# Activate it
.\venv\Scripts\Activate.ps1
# Install dependencies
pip install -r backend\requirements.txt
# Run the server
cd backend
uvicorn app.main:app --reload
```
Open your browser to `http://localhost:8000/docs` to see the OpenAPI UI, or `http://localhost:8000/api/v1/health` to test the health endpoint.

```powershell
# ---------- Frontend ----------
cd ..\frontend
# Install Node dependencies
npm install
# Run the dev server (default http://localhost:5173)
npm run dev
# Build for production
npm run build
# Lint the code
npm run lint
```
The frontend reads the backend URL from the environment variable `VITE_API_URL`. Create a `.env` file (or copy `.env.example`) with:
```
VITE_API_URL=http://localhost:8000
```
---
### macOS / Linux (bash) equivalents
```bash
# Clone the repo
git clone https://github.com/0xshambhavi/Syncra-fixed.git
cd Syncra-fixed

# ---------- Backend ----------
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
cd backend
uvicorn app.main:app --reload
```
Open `http://localhost:8000/docs` or `http://localhost:8000/api/v1/health`.

```bash
# ---------- Frontend ----------
cd ../frontend
npm install
npm run dev
npm run build
npm run lint
```
Create a `.env` file (or copy `.env.example`) with:
```
VITE_API_URL=http://localhost:8000
```
---
## Project structure
```
/README.md                # This file
/.gitignore               # Ignored files
/.env.example             # Example env vars
/DECISIONS.md            # Design decisions log
/frontend/                # Vite React TS app
/backend/                 # FastAPI service
/docs/                    # Documentation (optional)
```
---
## Notes
- All commands are intended for **PowerShell 5.1** on Windows. Use the macOS/Linux block if you are on those platforms.
- The backend runs on port `8000`; the frontend on `5173`.
- The frontend expects the backend URL in `VITE_API_URL`.
