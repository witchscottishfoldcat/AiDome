from typing import Generator
from database import SessionLocal
from sqlalchemy.orm import Session


def get_db() -> Generator[Session, None, None]:
    """Dependency to provide database session to endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()