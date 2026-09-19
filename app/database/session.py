from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from app.core.dependency import get_database_url
from app.database.engine import get_database_engine


@lru_cache(maxsize=None)
def create_session_local(db_url: str | None):
    engine = get_database_engine(db_url)

    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )


def get_db(db_url: str = Depends(get_database_url)):
    SessionLocal = create_session_local(db_url)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
