from app.core.config import Config


def get_config(require_api: bool = True) -> Config:
    return Config(require_api=require_api)


def get_database_url() -> str:
    config = get_config(require_api=False)
    return config.database_url
