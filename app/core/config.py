import os


class Settings:
    """Application settings."""

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./interview_app.db")

    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")


settings = Settings()
