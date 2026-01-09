# Placeholder for SQLAlchemy session
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/notes_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db()-> Session:
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()