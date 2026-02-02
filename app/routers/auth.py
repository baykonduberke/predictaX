from fastapi import APIRouter, Depends, status

from app.core.config import get_settings
from app.core.dependencies import get_user_repository
from app.core.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    InvalidTokenError,
    UnverifiedUserError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    verify_token,
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import (
    Token,
    TokenRefresh,
    UserCreate,
    UserLogin,
    UserOut,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
settings = get_settings()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(
    user: UserCreate,
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserOut:
    """Register a new user."""
    existing_user = await user_repo.get_by_email(user.email)
    if existing_user:
        raise UserAlreadyExistsError()

    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        password=hashed_password,
        is_active=True,
        is_superuser=False,
        is_verified=True,
    )
    return await user_repo.create(new_user)


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    user: UserLogin,
    user_repo: UserRepository = Depends(get_user_repository),
) -> Token:
    """Login a user."""
    existing_user = await user_repo.get_by_email(user.email)
    if not existing_user:
        raise InvalidCredentialsError()
    if not verify_password(user.password, existing_user.password):
        raise InvalidCredentialsError()
    if not existing_user.is_active:
        raise InactiveUserError()
    if not existing_user.is_verified:
        raise UnverifiedUserError()

    # Create tokens
    access_token = create_access_token(data={"sub": str(existing_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(existing_user.id)})
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        access_token_expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        refresh_token_expires_in=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/refresh", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh(
    token_data: TokenRefresh,
    user_repo: UserRepository = Depends(get_user_repository),
) -> Token:
    """Refresh tokens using a refresh token."""
    payload = verify_token(token_data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise InvalidTokenError("Invalid refresh token")

    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenError("Invalid token payload")

    user = await user_repo.get_by_id(int(user_id))
    if not user:
        raise UserNotFoundError("User no longer exists")
    if not user.is_active:
        raise InactiveUserError()
    if not user.is_verified:
        raise UnverifiedUserError()

    access_token = create_access_token(data={"sub": user_id})
    refresh_token = create_refresh_token(data={"sub": user_id})
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        access_token_expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        refresh_token_expires_in=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
    )
