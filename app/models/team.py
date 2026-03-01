from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.elo_history import EloHistory
    from app.models.match import Match
    from app.models.team_stats import TeamStats


class Team(Base):
    """
    Futbol takımı.

    Örnek:
    ┌────┬───────────────┬─────────┬─────────────┐
    │ id │ name          │ country │ current_elo │
    ├────┼───────────────┼─────────┼─────────────┤
    │ 1  │ Galatasaray   │ TUR     │ 1842.5      │
    │ 2  │ Man United    │ ENG     │ 1756.2      │
    └────┴───────────────┴─────────┴─────────────┘
    """

    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    name_api: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str | None] = mapped_column(String(3), nullable=True)
    current_elo: Mapped[float | None] = mapped_column(Float, nullable=True)
    elo_updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # İlişkiler
    home_matches: Mapped[list["Match"]] = relationship(
        "Match",
        foreign_keys="[Match.home_team_id]",
        back_populates="home_team",
    )
    away_matches: Mapped[list["Match"]] = relationship(
        "Match",
        foreign_keys="[Match.away_team_id]",
        back_populates="away_team",
    )
    stats: Mapped["TeamStats | None"] = relationship(
        "TeamStats", back_populates="team", uselist=False
    )
    elo_history: Mapped[list["EloHistory"]] = relationship(
        "EloHistory", back_populates="team"
    )
