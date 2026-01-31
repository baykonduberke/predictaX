from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import BaseAppException


async def app_exception_handler(request: Request, exc: BaseAppException) -> JSONResponse:
    """Handle all application exceptions."""
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
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "detail": None,
        },
    )

