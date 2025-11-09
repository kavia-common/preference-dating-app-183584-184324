from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import profiles, categories

app = FastAPI(
    title="MatchFilter Dating API",
    description="REST API for profiles and filtering by height/weight categories.",
    version="0.1.0",
    openapi_tags=[
        {"name": "Profiles", "description": "Profile CRUD and listing endpoints"},
        {"name": "Categories", "description": "Height/Weight preset category endpoints"},
    ],
)

origins = []
if settings.CORS_ORIGINS:
    origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]

if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(profiles.router)
app.include_router(categories.router)

# PUBLIC_INTERFACE
@app.get("/", tags=["Categories"])
def health():
    """Simple health endpoint."""
    return {"status": "ok"}
