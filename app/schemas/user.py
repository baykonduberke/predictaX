from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr, Field, model_validator


# Auth Schemas
class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(
        ...,
        min_length=8,
        max_length=255,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        description="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character",
    )
    first_name: str = Field(
        ..., min_length=2, max_length=255, description="User first name"
    )
    last_name: str = Field(
        ..., min_length=2, max_length=255, description="User last name"
    )


# User Update Schemas
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="User email")
    first_name: Optional[str] = Field(
        None, min_length=2, max_length=255, description="User first name"
    )
    last_name: Optional[str] = Field(
        None, min_length=2, max_length=255, description="User last name"
    )


class AdminUserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="User email")
    first_name: Optional[str] = Field(
        None, min_length=2, max_length=255, description="User first name"
    )
    last_name: Optional[str] = Field(
        None, min_length=2, max_length=255, description="User last name"
    )
    is_active: Optional[bool] = Field(None, description="User is active")
    is_superuser: Optional[bool] = Field(None, description="User is superuser")
    is_verified: Optional[bool] = Field(None, description="User is verified")


# User Response Schemas
class UserOut(BaseModel):
    id: int = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email")
    first_name: str = Field(
        ..., min_length=2, max_length=255, description="User first name"
    )
    last_name: str = Field(
        ..., min_length=2, max_length=255, description="User last name"
    )
    created_at: datetime = Field(..., description="User created at")
    updated_at: datetime = Field(..., description="User updated at")
    is_active: bool = Field(..., description="User is active")
    is_superuser: bool = Field(..., description="User is superuser")
    is_verified: bool = Field(..., description="User is verified")
    is_deleted: bool = Field(..., description="User is deleted")
    is_deleted_at: Optional[datetime] = Field(None, description="User deleted at")

    class Config:
        from_attributes = True


class UserPublic(BaseModel):
    id: int = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email")
    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User last name")
    is_verified: bool = Field(..., description="User is verified")
    created_at: datetime = Field(..., description="User created at")

    class Config:
        from_attributes = True


class UserSummary(BaseModel):
    id: int = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email")
    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User last name")
    is_active: bool = Field(..., description="User is active")

    class Config:
        from_attributes = True


class UserList(BaseModel):
    users: List[UserOut] = Field(..., description="Users list")
    total: int = Field(..., description="Total users")
    page: int = Field(..., description="Page number")
    page_size: int = Field(..., description="Page size")
    total_pages: int = Field(..., description="Total pages")
    has_next: bool = Field(..., description="Has next page")
    has_previous: bool = Field(..., description="Has previous page")


# Token Schemas
class Token(BaseModel):
    access_token: str = Field(..., description="Access token")
    refresh_token: Optional[str] = Field(None, description="Refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Expires in seconds")


class TokenRefresh(BaseModel):
    refresh_token: str = Field(..., description="Refresh token")


class TokenPayload(BaseModel):
    sub: str = Field(..., description="Subject (user id)")
    exp: int = Field(..., description="Expiration time")
    iat: int = Field(..., description="Issued at")
    type: str = Field(..., description="Token type (access/refresh)")


# Password Schemas
class PasswordChange(BaseModel):
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=255,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        description="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character",
    )
    confirm_password: str = Field(
        ...,
        min_length=8,
        max_length=255,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        description="Password confirmation",
    )

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("New password and confirmation password do not match")
        if self.current_password == self.new_password:
            raise ValueError("New password must be different from current password")
        return self


class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., description="User email")


class PasswordReset(BaseModel):
    token: str = Field(..., description="Token")
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=255,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        description="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character",
    )
    confirm_password: str = Field(
        ...,
        min_length=8,
        max_length=255,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        description="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character",
    )

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("New password and confirmation password do not match")
        return self


# Email Verification Schemas
class EmailVerificationRequest(BaseModel):
    email: EmailStr = Field(..., description="User email to verify")


class EmailVerificationConfirm(BaseModel):
    token: str = Field(..., description="Email verification token")


# General Response Schema
class MessageResponse(BaseModel):
    message: str = Field(..., description="Response message")
    success: bool = Field(default=True, description="Operation success status")
    data: Optional[Any] = Field(None, description="Additional response data")
