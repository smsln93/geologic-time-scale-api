from typing import Optional

from sqlalchemy.orm import sessionmaker

from app.database.engine import get_database_engine


def create_session_local(db_url: Optional[str] = None):
    engine = get_database_engine(db_url)

    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )


def get_db():
    SessionLocal = create_session_local()

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
