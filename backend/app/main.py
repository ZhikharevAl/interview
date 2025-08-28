from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging_config import get_logger, setup_logging
from app.db.database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

setup_logging(settings.LOG_LEVEL, settings.LOG_FILE)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, Any]:
    """Application lifecycle management."""
    logger.info("Application startup initiated")

    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception:
        logger.exception("Error creating database tables")
        raise

    logger.info("Application startup completed")

    yield

    logger.info("Application shutdown initiated")

    logger.info("Application shutdown completed")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

logger.info("Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("CORS middleware configured")

static_dir = Path("static")
if static_dir.exists() and static_dir.is_dir():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    logger.info("Static files mounted from %s", static_dir)
else:
    logger.warning("Static directory %s not found", static_dir)


@app.get("/", response_model=None)
def read_root() -> FileResponse | dict[str, Any]:
    """Root endpoint - serve the main HTML file."""
    logger.info("Root endpoint accessed")
    static_file = Path("static/index.html")

    if static_file.exists():
        logger.debug("Serving static file: %s", static_file)
        return FileResponse(str(static_file))

    logger.debug("Static file not found, returning JSON response")
    return {
        "message": f"Welcome to {settings.APP_NAME}!",
        "static_available": static_dir.exists(),
    }


@app.get("/health")
def health_check() -> dict[str, Any]:
    """Health check endpoint."""
    logger.info("Health check requested")

    masked_db_url = str(settings.DATABASE_URL)
    if "@" in masked_db_url:
        masked_db_url = masked_db_url.replace(masked_db_url.split("@")[0].split("://")[1], "***")

    return {
        "status": "healthy",
        "database_url": masked_db_url,
        "debug": settings.DEBUG,
        "version": settings.APP_VERSION,
    }


app.include_router(api_router, prefix="/api/v1")
logger.info("API router included with prefix /api/v1")
