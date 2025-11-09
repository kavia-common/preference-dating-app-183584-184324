# preference-dating-app-183584-184324

This repository contains:
- dating_app_database: PostgreSQL container and tools (running on port 5001)
- backend: FastAPI application connecting to the database, with Alembic migrations and seed scripts

## Quick Start

1) Ensure PostgreSQL is running (see dating_app_database/README.md). It runs on port 5001, DB=myapp, user=appuser by default.

2) Backend setup:
```
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env if necessary
alembic upgrade head
python -m app.seeds.seed_categories
uvicorn app.main:app --reload --port ${APP_PORT:-8000}
```

Open http://localhost:8000/docs for API docs.

## Environment Variables

The backend uses either DATABASE_URL or discrete PG variables:
- DATABASE_URL (e.g., postgresql+psycopg2://appuser:dbuser123@localhost:5001/myapp)
- PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD
- APP_PORT (default 8000)
- CORS_ORIGINS (optional)

A template is provided at backend/.env.example.

## Endpoints (Minimal)

- POST /profiles
- GET /profiles/{id}
- PUT /profiles/{id}
- DELETE /profiles/{id}
- GET /profiles?height_category_id=&weight_category_id=
- GET /categories/height
- GET /categories/weight

## Notes

- Do not run Node or any other process in the database container. The backend is separate.
- Future enhancements include authentication flow, swipe mechanics, and WebSocket chat.
