# Preference Dating App – Full Stack

Services:
- PostgreSQL (existing) at preference-dating-app-183584-184324/dating_app_database
- Backend (FastAPI) at preference-dating-app-183584-184324/dating_app_backend
- Frontend (React + Vite) at preference-dating-app-183584-184324/dating_app_frontend

Database:
- Start DB: run `dating_app_database/startup.sh`
- Connection: see `dating_app_database/db_connection.txt`
- Default: postgres://appuser:dbuser123@localhost:5001/myapp

Backend:
- cd dating_app_backend
- `pip install -r requirements.txt`
- copy .env.example to .env (ensure DATABASE_URL points to DB)
- (optional) seed: `python -m app.seed`
- run: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- docs: http://localhost:8000/docs

Frontend:
- cd dating_app_frontend
- `npm install`
- copy .env.example to .env (ensure VITE_API_BASE points to backend)
- `npm run dev` (http://localhost:5173)

Acceptance checklist:
- REST endpoints for profiles, swipes, matches, messages, filters available
- DB schema already exists in Postgres (from container); seed script adds demo data
- Frontend matches modern theme with blue/amber accents
- Env variables documented in .env.example
- Seed data available
