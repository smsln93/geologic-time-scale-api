from fastapi import Header, HTTPException

from app.core.config import app_configuration

def verify_api_key(api_key: str = Header(None)) -> None:
    if app_configuration.api_key is None:
        return

    if api_key != app_configuration.api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
