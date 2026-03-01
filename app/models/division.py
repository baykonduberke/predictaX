from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.match import Match


class Division(Base):
    """
    Lig bilgisi.

    Örnek:
    ┌────┬──────┬───────────────────────┬─────────┐
    │ id │ code │ name                  │ country │
    ├────┼──────┼───────────────────────┼─────────┤
    │ 1  │ E0   │ English Premier League│ ENG     │
    │ 2  │ SP1  │ La Liga               │ ESP     │
    │ 3  │ TR1  │ Süper Lig             │ TUR     │
    └────┴──────┴───────────────────────┴─────────┘
    """

    __tablename__ = "divisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(
        String(10), unique=True, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), index=True)
    name_api: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str | None] = mapped_column(String(3), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    matches: Mapped[list["Match"]] = relationship("Match", back_populates="division")
