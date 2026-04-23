from fastapi import FastAPI

from app.routers.router import api_router


from app.database.engine import engine
from app.database.session import create_session_local


SessionLocal = create_session_local(engine)


app = FastAPI(
    title="Geologic Time Scale API",
    docs_url="/geologic-time-scale-api/v1/docs",
    redoc_url="/geologic-time-scale-api/v1/redoc",
    openapi_url="/geologic-time-scale-api/v1/openapi.json"
)

app.include_router(api_router, prefix="/geologic-time-scale-api/v1")
