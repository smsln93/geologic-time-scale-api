from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from app.routers.router import api_router


app = FastAPI(
    title="Geologic Time Scale API",
    docs_url="/geologic-time-scale-api/v1/docs",
    redoc_url="/geologic-time-scale-api/v1/redoc",
    openapi_url="/geologic-time-scale-api/v1/openapi.json"
)

app.include_router(api_router, prefix="/geologic-time-scale-api/v1")
