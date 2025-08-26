from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Interview Prep App", debug=settings.DEBUG)


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Welcome to Interview Prep App!"}


app.include_router(api_router, prefix="/api/v1")
