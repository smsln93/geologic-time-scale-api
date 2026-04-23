from fastapi import APIRouter

from .root import root_router
from .units.units import units_router
from .export.export import export_router


api_router = APIRouter()

api_router.include_router(root_router)
api_router.include_router(units_router)
api_router.include_router(export_router)
