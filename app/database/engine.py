from pathlib import Path

from sqlalchemy import create_engine

from app.core.dependency import get_config


BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_database_engine():
    """
        Create a SQLAlchemy engine based on application configuration.

        Handles SQLite-specific behavior such as resolving relative paths
        and ensuring the database directory exists.
    """
    config = get_config()
    raw_url_db = config.database_url

    if raw_url_db.startswith("sqlite:///"):
        relative_path = raw_url_db.replace("sqlite:///", "")
        db_path = Path(BASE_DIR).joinpath(relative_path)

        db_path.parent.mkdir(parents=True, exist_ok=True)

        db_url = f"sqlite:///{db_path.as_posix()}"
        connect_args = {"check_same_thread": False}
    else:
        db_url = raw_url_db
        connect_args = {}

    return create_engine(
        db_url,
        connect_args=connect_args
    )
