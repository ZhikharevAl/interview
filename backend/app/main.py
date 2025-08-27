from app.api.v1.api import api_router
from app.core.config import settings
from app.db.database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Interview Prep App", debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Welcome to Interview Prep App!"}


app.include_router(api_router, prefix="/api/v1")
