"""
Backend configuration for Phase II Full-Stack Web Application

Per @specs/002-phase2-webapp/plan.md and @specs/002-phase2-webapp/quickstart.md
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/todo_db"
    )

    # JWT Secret
    JWT_SECRET: str = os.getenv(
        "JWT_SECRET",
        "change-this-secret-in-production-use-a-strong-random-string"
    )

    # Application Configuration
    API_HOST: str = os.getenv("API_HOST", "http://localhost:8000")
    API_PREFIX: str = os.getenv("API_PREFIX", "/v1")

    # CORS Configuration
    CORS_ORIGINS: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000"
    )

    # Performance Configuration
    MAX_CONNECTION_POOL_SIZE: int = int(os.getenv("MAX_CONNECTION_POOL_SIZE", "10"))

    class Config:
        """Pydantic v2 config for compatibility"""
        env_file = ".env"
        extra = "ignore"

    @property
    def database_url(self) -> str:
        """Get database URL"""
        return self.DATABASE_URL

    @property
    def jwt_secret(self) -> str:
        """Get JWT secret"""
        return self.JWT_SECRET

# Database engine and session factory
engine: Optional[object] = None
SessionLocal: Optional[sessionmaker] = None


def get_engine():
    """Get database engine with connection pooling"""
    global engine
    if engine is None:
        settings = Settings()

        # SQLite needs different arguments than PostgreSQL
        if settings.database_url.startswith("sqlite"):
            engine = create_engine(
                settings.database_url,
                connect_args={"check_same_thread": False}
            )
        else:
            engine = create_engine(
                settings.database_url.replace("postgresql://", "postgresql+psycopg2://") if "postgresql" in settings.database_url else settings.database_url,
                pool_size=settings.MAX_CONNECTION_POOL_SIZE,
                echo=False
            )
    return engine


def get_session():
    """Dependency for providing a database session"""
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine(),
            class_=Session
        )

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
