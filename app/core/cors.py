from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings


def get_cors_origins(settings: Settings) -> list[str]:
    """
    Environment'a göre CORS origins döndür.
    Config'den (.env'den) okur.
    """
    if settings.APP_ENVIRONMENT == "development":
        return settings.CORS_ORIGINS if settings.CORS_ORIGINS else []
    elif settings.APP_ENVIRONMENT == "production":
        if not settings.CORS_ORIGINS:
            raise ValueError("CORS_ORIGINS must be set in production!")
        return settings.CORS_ORIGINS
    else:
        return []


def setup_cors(app: FastAPI, settings: Settings) -> None:
    """CORS middleware'i yapılandır ve ekle."""
    origins = get_cors_origins(settings)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
        expose_headers=settings.CORS_EXPOSE_HEADERS,
        max_age=settings.CORS_MAX_AGE,
    )
