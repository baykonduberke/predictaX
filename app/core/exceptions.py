from typing import Any, Optional


class BaseAppException(Exception):
    """Base exception for all application exceptions."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        detail: Optional[Any] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.message)


# Authentication Exceptions
class AuthenticationError(BaseAppException):
    """Authentication failed."""

    def __init__(
        self, message: str = "Authentication failed", detail: Optional[Any] = None
    ):
        super().__init__(message=message, status_code=401, detail=detail)


class InvalidCredentialsError(AuthenticationError):
    """Invalid email or password."""

    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message=message)


class InvalidTokenError(AuthenticationError):
    """Invalid or expired token."""

    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message=message)


class TokenExpiredError(AuthenticationError):
    """Token has expired."""

    def __init__(self, message: str = "Token has expired"):
        super().__init__(message=message)


# Authorization Exceptions
class AuthorizationError(BaseAppException):
    """Authorization failed."""

    def __init__(self, message: str = "Not authorized", detail: Optional[Any] = None):
        super().__init__(message=message, status_code=403, detail=detail)


class InactiveUserError(AuthorizationError):
    """User account is inactive."""

    def __init__(self, message: str = "User account is inactive"):
        super().__init__(message=message)


class UnverifiedUserError(AuthorizationError):
    """User account is not verified."""

    def __init__(self, message: str = "User account is not verified"):
        super().__init__(message=message)


class InsufficientPermissionsError(AuthorizationError):
    """User doesn't have required permissions."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message=message)


# Resource Exceptions
class NotFoundError(BaseAppException):
    """Resource not found."""

    def __init__(
        self, message: str = "Resource not found", detail: Optional[Any] = None
    ):
        super().__init__(message=message, status_code=404, detail=detail)


class UserNotFoundError(NotFoundError):
    """User not found."""

    def __init__(self, message: str = "User not found"):
        super().__init__(message=message)


# Conflict Exceptions
class ConflictError(BaseAppException):
    """Resource conflict."""

    def __init__(
        self, message: str = "Resource conflict", detail: Optional[Any] = None
    ):
        super().__init__(message=message, status_code=409, detail=detail)


class UserAlreadyExistsError(ConflictError):
    """User already exists."""

    def __init__(self, message: str = "User with this email already exists"):
        super().__init__(message=message)


# Validation Exceptions
class ValidationError(BaseAppException):
    """Validation error."""

    def __init__(self, message: str = "Validation error", detail: Optional[Any] = None):
        super().__init__(message=message, status_code=422, detail=detail)


class PasswordValidationError(ValidationError):
    """Password validation failed."""

    def __init__(self, message: str = "Password validation failed"):
        super().__init__(message=message)


# Database Exceptions
class DatabaseError(BaseAppException):
    """Database error."""

    def __init__(self, message: str = "Database error", detail: Optional[Any] = None):
        super().__init__(message=message, status_code=500, detail=detail)
