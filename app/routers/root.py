from typing import Dict

from app.api.router import api_router

@api_router.get(path="/",
                tags=["Root"],
                summary="API root endpoint",
                description="Returns basic information about the Geologic Time Scale API")
def root() -> Dict:
    return {"name": "Geologic Time Scale API",
            "docs": "/docs"}
