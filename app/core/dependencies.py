from typing import AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidTokenError, UserNotFoundError
from app.core.security import verify_token
from app.db.database import async_session_maker
from app.models.user import User
from app.repositories.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository),
) -> User:
    payload = verify_token(token)
    if not payload or payload.get("type") != "access":
        raise InvalidTokenError("Invalid access token")

    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenError("Invalid token payload")

    user = await user_repo.get_by_id(int(user_id))
    if not user:
        raise UserNotFoundError()
    return user
