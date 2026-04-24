from sqlalchemy.orm import sessionmaker

from app.database.engine import get_database_engine


def create_session_local():
    engine = get_database_engine()

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
