from fastapi import Depends

from app.core.config import Config


def get_config() -> Config:
    return Config()


def get_database_url(config: Config = Depends(get_config)) -> str:
    if not config.database_url:
        raise RuntimeError("Database URL not set")

    return config.database_url
