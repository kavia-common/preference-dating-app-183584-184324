from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    DATABASE_URL: Optional[str] = None

    PGHOST: str = "localhost"
    PGPORT: int = 5001
    PGDATABASE: str = "myapp"
    PGUSER: str = "appuser"
    PGPASSWORD: str = "dbuser123"

    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    CORS_ORIGINS: Optional[str] = None  # comma-separated list

    # PUBLIC_INTERFACE
    def build_db_url(self) -> str:
        """Build SQLAlchemy database URL from DATABASE_URL or the discrete PG variables."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+psycopg2://{self.PGUSER}:{self.PGPASSWORD}@{self.PGHOST}:{self.PGPORT}/{self.PGDATABASE}"


settings = Settings()  # Reads from environment and .env if present
