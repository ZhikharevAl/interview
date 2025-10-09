from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    DATABASE_URL: str = Field(
        default="sqlite:///./interview_app.db", description="Database connection URL"
    )
    DEBUG: bool = Field(default=False, description="Debug mode")
    SECRET_KEY: str = Field(
        default="your-secret-key-here", description="Secret key for authentication"
    )
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FILE: str = Field(default="logs/app.log", description="Log file path")
    APP_NAME: str = Field(default="Interview Prep App", description="Application name")
    APP_VERSION: str = Field(default="0.1.0", description="Application version")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()
