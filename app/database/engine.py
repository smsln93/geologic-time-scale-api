from pathlib import Path

from sqlalchemy import create_engine

from app.config.config import app_configuration

BASE_DIR = Path(__file__).resolve().parent.parent.parent
raw_url_db = app_configuration.database_url

if raw_url_db.startswith("sqlite:///"):
    relative_path = raw_url_db.replace("sqlite:///", "")
    db_path = Path(BASE_DIR).joinpath(relative_path)

    db_path.parent.mkdir(parents=True, exist_ok=True)

    DATABASE_URL = f"sqlite:///{db_path.as_posix()}"
    connect_args = {"check_same_thread": False}
else:
    DATABASE_URL = raw_url_db
    connect_args = {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)