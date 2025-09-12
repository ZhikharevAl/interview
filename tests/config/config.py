from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    """
    Configuration for tests, managed via Pydantic.

    Pydantic automatically reads values from environment variables.
    If the variable is not found, the default value is used.
    """

    BASE_URL: str = "http://localhost:8080"

    TIMEOUT: int = 30000

    CATEGORIES_ENDPOINT: str = "/api/v1/categories"
    QUESTIONS_ENDPOINT: str = "/api/v1/questions"

    model_config = SettingsConfigDict(env_file=".env.test", extra="ignore")


settings = TestSettings()
