# MatchFilter Frontend (Vite + React)

A minimal frontend to exercise the FastAPI backend:
- List candidate profiles with simple swipe-like Accept/Reject (client-side only)
- Create/Update a profile
- Apply height/weight filters using categories endpoints

This is a lightweight developer UI intended to verify backend functionality quickly.

## Prerequisites

- Node.js 18+
- FastAPI backend running on http://localhost:8000 (or configure via .env)

Backend quick start (from repository root, summarized):
- See ../backend/README.md
- Ensure DB on port 5001 is running
- In backend/, create venv, install requirements, run alembic migrations, seed categories, start uvicorn

## Setup

From this folder:

```
cp .env.example .env
# Edit VITE_API_BASE_URL if backend is on a different host/port
npm install
```

## Run (do not start previews in CI)

Local dev:

```
npm run dev
```

Build:

```
npm run build
```

Preview (optional):

```
npm run preview
```

Open http://localhost:5173

## Environment

- VITE_API_BASE_URL (default http://localhost:8000)

Endpoints assumed (from backend):
- GET /profiles?height_category_id=&weight_category_id=
- POST /profiles
- GET /profiles/{id}
- PUT /profiles/{id}
- GET /categories/height
- GET /categories/weight

## Pages

- Candidates (/) — List profiles, apply filters (height/weight), Accept/Reject locally
- Profile (/profile) — Create a new profile (includes user_id)
- Profile Edit (/profile/:id) — Edit an existing profile

## Styling

- Ocean Professional theme: blue and amber accents
- Minimal CSS in src/styles.css

## Notes

- No authentication
- Accept/Reject is local state only (no server mutation)
- Ensure CORS is configured in backend if accessing from a different origin
