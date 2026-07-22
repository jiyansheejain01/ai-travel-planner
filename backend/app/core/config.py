from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration.

    Every configurable value in the project should live here.
    Values are automatically loaded from the .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ==========================
    # Application
    # ==========================
    APP_NAME: str = Field(default="AI Travel Planner")
    APP_VERSION: str = Field(default="1.0.0")
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)

    # ==========================
    # Server
    # ==========================
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)

    # ==========================
    # Database
    # ==========================
    DATABASE_URL: str

    # ==========================
    # Security
    # ==========================
    SECRET_KEY: str
    ALGORITHM: str = Field(default="HS256")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    # ==========================
    # LLM
    # ==========================
    AI_PROVIDER: str = Field(default="groq")

    GROQ_API_KEY: str = Field(default="")
    GROQ_MODEL: str = Field(default="llama-3.3-70b-versatile")
    ENVIRONMENT: str = "development"

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    The configuration is loaded only once during the application's lifetime.
    """
    return Settings()


settings = get_settings()