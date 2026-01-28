from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    APP_NAME: str = "PredictaX"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "PredictaX"
    APP_DEBUG: bool = False
    APP_ENVIRONMENT: str = "development"

    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


@lru_cache()
def get_settings() -> Settings:
    return Settings()
