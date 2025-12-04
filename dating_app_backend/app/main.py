import os
from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, BigInteger, Integer, String, Text, Boolean, DateTime, JSON, ForeignKey, Index
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Mapped, mapped_column, Session
from pydantic_settings import BaseSettings

# PUBLIC_INTERFACE
class Settings(BaseSettings):
    """Application configuration loaded from environment variables or .env file."""
    # Database
    DATABASE_URL: Optional[str] = None
    POSTGRES_URL: Optional[str] = None
    PGHOST: str = "localhost"
    PGPORT: int = 5001
    PGDATABASE: str = "myapp"
    PGUSER: str = "appuser"
    PGPASSWORD: str = "dbuser123"

    # CORS / frontend
    FRONTEND_URL: str = "http://localhost:5173"

    # Server
    API_PORT: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

def _build_db_url() -> str:
    url = settings.DATABASE_URL or settings.POSTGRES_URL
    if url:
        return url
    # Build from discrete PG* variables
    return f"postgresql://{settings.PGUSER}:{settings.PGPASSWORD}@{settings.PGHOST}:{settings.PGPORT}/{settings.PGDATABASE}"

DATABASE_URL = _build_db_url()

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

# SQLAlchemy Models (aligned with existing DB schema from database_backup.sql where practical)
class AuthUser(Base):
    __tablename__ = "auth_user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True)
    email: Mapped[str] = mapped_column(String(254))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    date_joined: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class Profile(Base):
    __tablename__ = "core_profile"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    display_name: Mapped[str] = mapped_column(String(100))
    bio: Mapped[str] = mapped_column(Text)
    height_cm: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    weight_kg: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    photo_url: Mapped[str] = mapped_column(String(200))
    gender: Mapped[str] = mapped_column(String(32))
    interests: Mapped[dict] = mapped_column(JSON)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("auth_user.id"), unique=True)

    __table_args__ = (
        Index("idx_profile_height_cm", "height_cm"),
        Index("idx_profile_weight_kg", "weight_kg"),
        Index("idx_profile_gender", "gender"),
    )

class Match(Base):
    __tablename__ = "core_match"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    matched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    user_a_id: Mapped[int] = mapped_column(Integer, ForeignKey("auth_user.id"))
    user_b_id: Mapped[int] = mapped_column(Integer, ForeignKey("auth_user.id"))

    __table_args__ = (
        Index("idx_match_user_a", "user_a_id"),
        Index("idx_match_user_b", "user_b_id"),
    )

class Message(Base):
    __tablename__ = "core_message"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    content: Mapped[str] = mapped_column(Text)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    match_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("core_match.id"))
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("auth_user.id"))

    __table_args__ = (
        Index("idx_message_match_id", "match_id"),
        Index("idx_message_sender_id", "sender_id"),
    )

class FilterPreset(Base):
    __tablename__ = "core_filterpreset"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    name: Mapped[str] = mapped_column(String(100))
    min_height_cm: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    max_height_cm: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    min_weight_kg: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    max_weight_kg: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    genders: Mapped[list] = mapped_column(JSON, default=list)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    owner_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("auth_user.id"), nullable=True)

# Pydantic Models
class AuthRequest(BaseModel):
    email: str = Field(..., description="Email for mock sign-in")
    username: str = Field(..., description="Username to create for mock user if not exists")

class AuthResponse(BaseModel):
    user_id: int
    username: str
    email: str
    token: str

class ProfileCreate(BaseModel):
    display_name: str
    bio: str
    height_cm: Optional[int] = None
    weight_kg: Optional[int] = None
    photo_url: str
    gender: str
    interests: List[str] = Field(default_factory=list)
    user_id: int

class ProfileUpdate(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    height_cm: Optional[int] = None
    weight_kg: Optional[int] = None
    photo_url: Optional[str] = None
    gender: Optional[str] = None
    interests: Optional[List[str]] = None

class ProfileOut(BaseModel):
    id: int
    display_name: str
    bio: str
    height_cm: Optional[int]
    weight_kg: Optional[int]
    photo_url: str
    gender: str
    interests: List[str]
    user_id: int

class SwipeRequest(BaseModel):
    swiper_user_id: int = Field(..., description="User performing the swipe")
    target_user_id: int = Field(..., description="User being swiped on")
    direction: str = Field(..., description="'right' or 'left'")

class MatchOut(BaseModel):
    id: int
    user_a_id: int
    user_b_id: int
    matched_at: datetime
    is_active: bool

class MessageCreate(BaseModel):
    match_id: int
    sender_id: int
    content: str

class MessageOut(BaseModel):
    id: int
    match_id: int
    sender_id: int
    content: str
    sent_at: datetime
    is_read: bool

class FilterSettings(BaseModel):
    min_height_cm: Optional[int] = None
    max_height_cm: Optional[int] = None
    min_weight_kg: Optional[int] = None
    max_weight_kg: Optional[int] = None
    genders: List[str] = Field(default_factory=list)

class FilterPresetCreate(BaseModel):
    name: str
    is_public: bool = True
    owner_id: Optional[int] = None
    min_height_cm: Optional[int] = None
    max_height_cm: Optional[int] = None
    min_weight_kg: Optional[int] = None
    max_weight_kg: Optional[int] = None
    genders: List[str] = Field(default_factory=list)

# FastAPI app
app = FastAPI(
    title="Preference Dating App API",
    description="REST and WebSocket APIs for profiles, swipes/matches, chat messages, and filter settings.",
    version="0.1.0",
    openapi_tags=[
        {"name": "auth", "description": "Mock authentication endpoints"},
        {"name": "profiles", "description": "Manage user profiles"},
        {"name": "swipe", "description": "Swipe actions and match creation"},
        {"name": "matches", "description": "Retrieve user matches"},
        {"name": "messages", "description": "Send and list chat messages"},
        {"name": "filters", "description": "Filter settings and presets"},
        {"name": "websocket", "description": "Real-time chat over WebSocket"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# PUBLIC_INTERFACE
@app.post("/auth/login", response_model=AuthResponse, tags=["auth"], summary="Mock email/username login")
def login(payload: AuthRequest, db: Session = Depends(get_db)):
    """Mock authentication that creates a user row in auth_user if username doesn't exist and returns a fake token."""
    user = db.query(AuthUser).filter(AuthUser.username == payload.username).first()
    if not user:
        user = AuthUser(username=payload.username, email=payload.email, is_active=True, date_joined=datetime.utcnow())
        db.add(user)
        db.commit()
        db.refresh(user)
    token = f"mocktoken-{user.id}"
    return AuthResponse(user_id=user.id, username=user.username, email=user.email, token=token)

# PUBLIC_INTERFACE
@app.post("/profiles", response_model=ProfileOut, tags=["profiles"], summary="Create profile")
def create_profile(p: ProfileCreate, db: Session = Depends(get_db)):
    """Create a profile for a given user."""
    exists = db.query(Profile).filter(Profile.user_id == p.user_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Profile already exists for user")
    profile = Profile(
        display_name=p.display_name,
        bio=p.bio,
        height_cm=p.height_cm,
        weight_kg=p.weight_kg,
        photo_url=p.photo_url,
        gender=p.gender,
        interests={"tags": p.interests},
        user_id=p.user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return ProfileOut(
        id=profile.id,
        display_name=profile.display_name,
        bio=profile.bio,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        photo_url=profile.photo_url,
        gender=profile.gender,
        interests=profile.interests.get("tags", []),
        user_id=profile.user_id,
    )

# PUBLIC_INTERFACE
@app.get("/profiles/{user_id}", response_model=ProfileOut, tags=["profiles"], summary="Get profile by user_id")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    """Retrieve a profile by the owning auth_user ID."""
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProfileOut(
        id=profile.id,
        display_name=profile.display_name,
        bio=profile.bio,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        photo_url=profile.photo_url,
        gender=profile.gender,
        interests=profile.interests.get("tags", []),
        user_id=profile.user_id,
    )

# PUBLIC_INTERFACE
@app.put("/profiles/{user_id}", response_model=ProfileOut, tags=["profiles"], summary="Update profile by user_id")
def update_profile(user_id: int, patch: ProfileUpdate, db: Session = Depends(get_db)):
    """Update mutable fields in a profile."""
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    if patch.display_name is not None:
        profile.display_name = patch.display_name
    if patch.bio is not None:
        profile.bio = patch.bio
    if patch.height_cm is not None:
        profile.height_cm = patch.height_cm
    if patch.weight_kg is not None:
        profile.weight_kg = patch.weight_kg
    if patch.photo_url is not None:
        profile.photo_url = patch.photo_url
    if patch.gender is not None:
        profile.gender = patch.gender
    if patch.interests is not None:
        profile.interests = {"tags": patch.interests}
    profile.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(profile)
    return ProfileOut(
        id=profile.id,
        display_name=profile.display_name,
        bio=profile.bio,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        photo_url=profile.photo_url,
        gender=profile.gender,
        interests=profile.interests.get("tags", []),
        user_id=profile.user_id,
    )

# PUBLIC_INTERFACE
@app.get("/profiles/discover", response_model=List[ProfileOut], tags=["profiles"], summary="Discover profiles with filters")
def discover_profiles(
    min_height_cm: Optional[int] = Query(None),
    max_height_cm: Optional[int] = Query(None),
    min_weight_kg: Optional[int] = Query(None),
    max_weight_kg: Optional[int] = Query(None),
    genders: Optional[str] = Query(None, description="Comma-separated list, e.g., male,female,nonbinary"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Fetch profiles matching filter criteria and return up to limit results."""
    q = db.query(Profile)
    if min_height_cm is not None:
        q = q.filter(Profile.height_cm >= min_height_cm)
    if max_height_cm is not None:
        q = q.filter(Profile.height_cm <= max_height_cm)
    if min_weight_kg is not None:
        q = q.filter(Profile.weight_kg >= min_weight_kg)
    if max_weight_kg is not None:
        q = q.filter(Profile.weight_kg <= max_weight_kg)
    if genders:
        gs = [g.strip() for g in genders.split(",") if g.strip()]
        if gs:
            q = q.filter(Profile.gender.in_(gs))
    rows = q.order_by(Profile.updated_at.desc()).limit(limit).all()
    out: List[ProfileOut] = []
    for r in rows:
        out.append(ProfileOut(
            id=r.id,
            display_name=r.display_name,
            bio=r.bio,
            height_cm=r.height_cm,
            weight_kg=r.weight_kg,
            photo_url=r.photo_url,
            gender=r.gender,
            interests=r.interests.get("tags", []),
            user_id=r.user_id
        ))
    return out

# PUBLIC_INTERFACE
@app.post("/swipe", response_model=Optional[MatchOut], tags=["swipe"], summary="Swipe left/right and create match if mutual")
def swipe(payload: SwipeRequest, db: Session = Depends(get_db)):
    """Record a swipe. If right-swipe is mutual, create a match record. For MVP, treat any right-swipe as mutual for demo."""
    if payload.direction not in ("right", "left"):
        raise HTTPException(status_code=400, detail="direction must be 'right' or 'left'")
    if payload.direction == "left":
        return None
    # Create a simple match on right swipe (MVP mutuality simulation)
    a = min(payload.swiper_user_id, payload.target_user_id)
    b = max(payload.swiper_user_id, payload.target_user_id)
    # Check existing match
    existing = db.query(Match).filter(Match.user_a_id == a, Match.user_b_id == b).first()
    if existing:
        return MatchOut(id=existing.id, user_a_id=existing.user_a_id, user_b_id=existing.user_b_id, matched_at=existing.matched_at, is_active=existing.is_active)
    m = Match(user_a_id=a, user_b_id=b, matched_at=datetime.utcnow(), is_active=True, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(m)
    db.commit()
    db.refresh(m)
    return MatchOut(id=m.id, user_a_id=m.user_a_id, user_b_id=m.user_b_id, matched_at=m.matched_at, is_active=m.is_active)

# PUBLIC_INTERFACE
@app.get("/matches/{user_id}", response_model=List[MatchOut], tags=["matches"], summary="List user matches")
def list_matches(user_id: int, db: Session = Depends(get_db)):
    """List all matches involving a user."""
    ms = db.query(Match).filter((Match.user_a_id == user_id) | (Match.user_b_id == user_id)).order_by(Match.matched_at.desc()).all()
    return [MatchOut(id=m.id, user_a_id=m.user_a_id, user_b_id=m.user_b_id, matched_at=m.matched_at, is_active=m.is_active) for m in ms]

# PUBLIC_INTERFACE
@app.get("/messages/{match_id}", response_model=List[MessageOut], tags=["messages"], summary="List messages for a match")
def list_messages(match_id: int, db: Session = Depends(get_db)):
    """List messages for a match ordered by sent time ascending."""
    msgs = db.query(Message).filter(Message.match_id == match_id).order_by(Message.sent_at.asc()).limit(200).all()
    return [MessageOut(id=m.id, match_id=m.match_id, sender_id=m.sender_id, content=m.content, sent_at=m.sent_at, is_read=m.is_read) for m in msgs]

# PUBLIC_INTERFACE
@app.post("/messages", response_model=MessageOut, tags=["messages"], summary="Send a message")
def send_message(payload: MessageCreate, db: Session = Depends(get_db)):
    """Persist a message to the DB and broadcast over WebSocket (in-memory hub for MVP)."""
    # Ensure match exists
    match = db.query(Match).filter(Match.id == payload.match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    msg = Message(
        match_id=payload.match_id,
        sender_id=payload.sender_id,
        content=payload.content,
        sent_at=datetime.utcnow(),
        is_read=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    # Broadcast via WS hub
    WsHub.broadcast_to_match(str(payload.match_id), {
        "type": "message",
        "data": {
            "id": msg.id,
            "match_id": msg.match_id,
            "sender_id": msg.sender_id,
            "content": msg.content,
            "sent_at": msg.sent_at.isoformat(),
            "is_read": msg.is_read
        }
    })
    return MessageOut(id=msg.id, match_id=msg.match_id, sender_id=msg.sender_id, content=msg.content, sent_at=msg.sent_at, is_read=msg.is_read)

# PUBLIC_INTERFACE
@app.get("/filters/presets", response_model=List[FilterPresetCreate], tags=["filters"], summary="List preset filters")
def list_filter_presets(db: Session = Depends(get_db)):
    """List available filter presets (public and private)."""
    presets = db.query(FilterPreset).order_by(FilterPreset.updated_at.desc()).limit(100).all()
    out: List[FilterPresetCreate] = []
    for p in presets:
        out.append(FilterPresetCreate(
            name=p.name,
            is_public=p.is_public,
            owner_id=p.owner_id,
            min_height_cm=p.min_height_cm,
            max_height_cm=p.max_height_cm,
            min_weight_kg=p.min_weight_kg,
            max_weight_kg=p.max_weight_kg,
            genders=list(p.genders) if isinstance(p.genders, list) else []
        ))
    return out

# PUBLIC_INTERFACE
@app.post("/filters/presets", tags=["filters"], summary="Create a filter preset")
def create_filter_preset(preset: FilterPresetCreate, db: Session = Depends(get_db)):
    """Create a new filter preset."""
    p = FilterPreset(
        name=preset.name,
        is_public=preset.is_public,
        owner_id=preset.owner_id,
        min_height_cm=preset.min_height_cm,
        max_height_cm=preset.max_height_cm,
        min_weight_kg=preset.min_weight_kg,
        max_weight_kg=preset.max_weight_kg,
        genders=preset.genders,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(p)
    db.commit()
    return {"status": "ok"}

# Minimal in-memory WebSocket hub by match_id channel
class WsHub:
    channels = {}  # match_id -> set of WebSocket

    @classmethod
    def register(cls, match_id: str, ws: WebSocket):
        cls.channels.setdefault(match_id, set()).add(ws)

    @classmethod
    def unregister(cls, match_id: str, ws: WebSocket):
        try:
            cls.channels.get(match_id, set()).discard(ws)
        except KeyError:
            pass

    @classmethod
    def broadcast_to_match(cls, match_id: str, payload: dict):
        conns = cls.channels.get(match_id, set())
        to_remove = []
        for ws in conns:
            try:
                # FastAPI will handle JSON serialization
                import anyio
                anyio.from_thread.run(ws.send_json, payload)  # background safe call
            except Exception:
                to_remove.append(ws)
        for ws in to_remove:
            cls.unregister(match_id, ws)

# PUBLIC_INTERFACE
@app.websocket(
    "/ws/chat/{match_id}",
)
async def ws_chat(websocket: WebSocket, match_id: str):
    """
    WebSocket endpoint for real-time chat updates.
    Connect to /ws/chat/{match_id}. Messages sent by clients are echoed to all participants and saved via REST /messages.
    """
    await websocket.accept()
    WsHub.register(match_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Broadcast to others
            WsHub.broadcast_to_match(match_id, {"type": "client-event", "data": data})
    except WebSocketDisconnect:
        WsHub.unregister(match_id, websocket)

# PUBLIC_INTERFACE
@app.get("/websocket-docs", tags=["websocket"], summary="WebSocket usage help")
def websocket_docs():
    """Simple help for connecting to the chat WebSocket endpoint."""
    return {
        "websocket_endpoint": "/ws/chat/{match_id}",
        "usage": "Connect via ws://localhost:{API_PORT}/ws/chat/{match_id}. Server broadcasts new messages posted via REST /messages, and echoes client events for demo."
    }
