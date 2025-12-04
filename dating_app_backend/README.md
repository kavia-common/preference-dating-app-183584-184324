# Dating App Backend (FastAPI)

This service exposes REST and WebSocket APIs for the Preference Dating App and connects to the PostgreSQL database container.

Run:
- Install: `pip install -r requirements.txt`
- Env: copy `.env.example` to `.env` and adjust as needed
- Start: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

OpenAPI docs: http://localhost:8000/docs

Environment variables (see .env.example):
- DATABASE_URL or discrete PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD
- FRONTEND_URL (CORS origin), default http://localhost:5173
- API_PORT default 8000

APIs:
- POST /auth/login
- POST /profiles
- GET /profiles/{user_id}
- PUT /profiles/{user_id}
- GET /profiles/discover
- POST /swipe
- GET /matches/{user_id}
- GET /messages/{match_id}
- POST /messages
- GET /filters/presets
- POST /filters/presets
- WS /ws/chat/{match_id}
- GET /websocket-docs
