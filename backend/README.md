# MatchFilter Dating App Backend (FastAPI + SQLAlchemy)

This backend connects to the existing PostgreSQL container running on TCP port 5001 and provides REST APIs for profiles and candidate filtering by height and weight categories.

- Framework: FastAPI
- ORM: SQLAlchemy
- Migrations: Alembic
- DB: PostgreSQL (via env)
- Port: 8000 (default, configurable via .env)

## Run with preview DB (port 5001)

Use the existing preview PostgreSQL that is already running on localhost:5001.

1) Create your virtual environment and install deps:
```
cd preference-dating-app-183584-184324/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2) Create .env from template and keep defaults (pointing to preview DB on 5001):
```
cp .env.example .env
# edit only if your host/port differ; defaults are:
# DATABASE_URL=postgresql+psycopg2://appuser:dbuser123@localhost:5001/myapp
# or the discrete PG* variables shown below
```

3) Run Alembic migrations and seed preset categories:
```
alembic upgrade head
python -m app.seeds.seed_categories
```

4) Start the FastAPI app (0.0.0.0 for accessibility):
```
uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT:-8000}
```

Open http://localhost:8000/docs for Swagger UI.

### Example .env values

Single DATABASE_URL (recommended):
```
DATABASE_URL=postgresql+psycopg2://appuser:dbuser123@localhost:5001/myapp
APP_PORT=8000
```

Discrete PG* variables (used if DATABASE_URL is empty):
```
PGHOST=localhost
PGPORT=5001
PGDATABASE=myapp
PGUSER=appuser
PGPASSWORD=dbuser123
APP_PORT=8000
```

## Features in this scaffold

- Core domain tables:
  - users (basic auth details)
  - profiles (height_cm, weight_kg, bio, gender, photo URL, interests)
  - photos (additional photos per profile)
  - matches (bidirectional match record with user_a_id, user_b_id)
  - messages (chat messages linked to match)
  - height_categories (preset buckets)
  - weight_categories (preset buckets)
  - filter_settings (per-user filter settings, stored as category IDs)
  - sessions (simple token placeholder)

- REST endpoints (minimal):
  - POST /profiles
  - GET /profiles/{id}
  - PUT /profiles/{id}
  - DELETE /profiles/{id}
  - GET /profiles?height_category_id=&weight_category_id= (candidate filtering)
  - GET /categories/height
  - GET /categories/weight

- OpenAPI docs at /docs; OpenAPI JSON at /openapi.json

## Prerequisites

- Python 3.11+
- Running PostgreSQL (the provided database container on port 5001)
- Virtualenv recommended

## Environment

Copy .env.example to .env and set values:

```
cp .env.example .env
```

Required environment variables:

- DATABASE_URL or the discrete PG variables (PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE)
- APP_PORT (optional; defaults to 8000)

## Installation

From backend directory:

```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Database Migrations and Seed

Initialize database schema and seed preset categories:

```
alembic upgrade head
python -m app.seeds.seed_categories
```

This creates the required tables and seeds height/weight categories.

## Run the API

```
uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT:-8000}
```

API docs: http://localhost:8000/docs

## Notes

- This scaffold provides the minimal endpoints and models to start. Extend as needed for auth, real-time chat (websockets), and swipe mechanics.
- The DB connection is taken from env. Do not hard-code secrets.
- For testing with the existing DB container, ensure it is up and running (port 5001) as documented in dating_app_database/README.md.

## Project Structure

```
backend/
  .env.example
  requirements.txt
  alembic.ini
  alembic/
    env.py
    script.py.mako
    versions/
      20250101_000001_initial_schema.py
  app/
    __init__.py
    config.py
    db.py
    models.py
    schemas.py
    crud.py
    main.py
    routers/
      __init__.py
      profiles.py
      categories.py
    seeds/
      __init__.py
      seed_categories.py
```

## Candidate Filtering

Use GET /profiles with query params:
- height_category_id
- weight_category_id

Both optional; if supplied, candidates are filtered to profiles within the category ranges.

```
GET /profiles?height_category_id=2&weight_category_id=3
```

## Upcoming Enhancements (not included yet)

- Authentication flow (signup/login, password hashing, token issuance)
- Swipe endpoints and match creation logic
- WebSocket chat (FastAPI websockets) and message persistence
- Pagination and ordering for candidate lists
