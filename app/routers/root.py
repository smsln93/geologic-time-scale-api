from typing import Dict

from fastapi import APIRouter

root_router = APIRouter(tags=["Root"])


@root_router.get(path="/",
                 summary="API root endpoint",
                 description="Returns basic information about the Geologic Time Scale API")
def root() -> Dict:
    return {"name": "Geologic Time Scale API",
            "docs": "/docs"}
