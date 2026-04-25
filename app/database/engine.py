from pathlib import Path
from typing import Optional, Tuple, Any

from sqlalchemy import create_engine

from app.core.dependency import get_database_url


BASE_DIR = Path(__file__).resolve().parents[2]


def resolve_database_url(raw_url_db: str) -> Tuple[str, dict[str, Any]]:

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


def get_database_engine(raw_db_url: Optional[str] = None):
    """
        Create a SQLAlchemy engine based on application configuration.

        Handles SQLite-specific behavior such as resolving relative paths
        and ensuring the database directory exists.
    """

    if raw_db_url is None:
        raw_db_url = get_database_url()

    db_url, connect_args = resolve_database_url(raw_db_url)

    return create_engine(
        db_url,
        connect_args=connect_args
    )
