from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == int(user_id), ~User.is_deleted)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.email == email, ~User.is_deleted)
        )
        return result.scalar_one_or_none()

    async def get_by_id_included_deleted(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == int(user_id)))
        return result.scalar_one_or_none()

    async def get_by_email_included_deleted(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user: User) -> User:
        """Kullanıcı güncelle."""
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def soft_delete(self, user: User) -> User:
        """Kullanıcıyı soft delete yap."""
        user.is_deleted = True
        user.is_deleted_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_all(self) -> List[User]:
        result = await self.db.execute(select(User).where(~User.is_deleted))
        return result.scalars().all()

    async def get_all_included_deleted(self) -> List[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_all_with_pagination(self, skip: int, limit: int) -> List[User]:
        result = await self.db.execute(
            select(User)
            .where(~User.is_deleted)
            .order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_all_with_pagination_included_deleted(
        self, skip: int, limit: int
    ) -> List[User]:
        result = await self.db.execute(
            select(User).order_by(User.created_at.desc()).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.db.execute(
            select(func.count(User.id)).where(~User.is_deleted)
        )
        return result.scalar() or 0

    async def count_included_deleted(self) -> int:
        result = await self.db.execute(select(func.count(User.id)))
        return result.scalar() or 0
