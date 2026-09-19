from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, event

from app.core.dependency import get_database_url


BASE_DIR = Path(__file__).resolve().parents[2]


def resolve_database_url(raw_url_db: str) -> tuple[str, dict[str, Any]]:

    if raw_url_db.startswith("sqlite:///"):
        relative_path = raw_url_db.replace("sqlite:///", "")
        db_path = Path(BASE_DIR).joinpath(relative_path)

        db_path.parent.mkdir(parents=True, exist_ok=True)

        db_url = f"sqlite:///{db_path.as_posix()}"
        connect_args = {"check_same_thread": False}
    else:
        db_url = raw_url_db
        connect_args = {}

    return db_url, connect_args


def get_database_engine(raw_db_url: str | None):
    """
        Create a SQLAlchemy engine based on application configuration.

        Handles SQLite-specific behavior such as resolving relative paths
        and ensuring the database directory exists.
    """

    if raw_db_url is None:
        raw_db_url = get_database_url()

    db_url, connect_args = resolve_database_url(raw_db_url)

    engine = create_engine(
        db_url,
        connect_args=connect_args
    )

    if engine.dialect.name == "sqlite":

        @event.listens_for(engine, "connect")
        def enable_foreign_keys(dbapi_connection, connection_record):
            autocommit = dbapi_connection.autocommit
            dbapi_connection.autocommit = True

            try:
                cursor = dbapi_connection.cursor()
                try:
                    cursor.execute("PRAGMA foreign_keys=ON")
                finally:
                    cursor.close()
            finally:
                dbapi_connection.autocommit = autocommit

    return engine
