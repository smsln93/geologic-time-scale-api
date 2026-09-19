from fastapi import Header, HTTPException, Depends

from app.core.dependency import get_config
from app.core.config import Config

def verify_api_key(x_api_key: str = Header(None),
                   config: Config = Depends(get_config)) -> None:

    if not config.api_key:
        raise HTTPException(status_code=503, detail="API key is not configured")

    if x_api_key is None:
        raise HTTPException(status_code=401, detail="API key is missing")

    if x_api_key != config.api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
