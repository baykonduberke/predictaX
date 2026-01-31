from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import async_session_maker


async def get_db() -> Generator[AsyncSession, None, None]:
    async with async_session_maker() as session:
        try:
            yield session
            session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
