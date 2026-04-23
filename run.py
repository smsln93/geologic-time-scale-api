import uvicorn

from app.database.engine import engine
from app.database.session import create_session_local


SessionLocal = create_session_local(engine)


if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
