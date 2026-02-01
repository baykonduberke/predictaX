import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import BaseAppException

logger = logging.getLogger(__name__)


async def app_exception_handler(
    request: Request, exc: BaseAppException
) -> JSONResponse:
    """Handle all application exceptions."""
    logger.warning(
        f"App error: {exc.message} | Path: {request.url.path} | Method: {request.method}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "detail": exc.detail,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.error(
        f"Unexpected error: {str(exc)} | Path: {request.url.path} | Method: {request.method}",
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "detail": None,
        },
    )
