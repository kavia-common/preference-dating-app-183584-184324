from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create SQLAlchemy engine using env-driven URL
DATABASE_URL = settings.build_db_url()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# PUBLIC_INTERFACE
def get_db():
    """FastAPI dependency that yields a DB session, ensuring proper close."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
