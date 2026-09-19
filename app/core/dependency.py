from app.core.config import Config


def get_config() -> Config:
    return Config()


def get_database_url() -> str:
    config = get_config()

    if not config.database_url:
        raise RuntimeError("Database URL not set")

    return config.database_url
