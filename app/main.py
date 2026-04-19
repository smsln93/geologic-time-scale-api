from fastapi import FastAPI

from app.database.base import Base
from app.database.engine import engine
from app.database.session import SessionLocal
from app.seed.seed_db import seed_db
from app.api.router import api_router

from app.routers import root  # noqa
from app.routers import units  # noqa
from app.routers import export  # noqa

app = FastAPI(
    title="Geologic Time Scale API",
    docs_url="/geologic-time-scale-api/v1/docs",
    redoc_url="/geologic-time-scale-api/v1/redoc",
    openapi_url="/geologic-time-scale-api/v1/openapi.json"
)


@app.on_event("startup")
def startup_event():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()

app.include_router(api_router)
