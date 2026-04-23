from sqlalchemy.orm import sessionmaker


def create_session_local(engine):
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )


def get_db(session_local):
    def _get_db():
        db = session_local()
        try:
            yield db
        finally:
            db.close()
    return _get_db
