from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class EloHistory(Base):
    """
    Takımların ELO puanı geçmişi.
    
    ClubElo ayda 2 kez (1. ve 15. gün) snapshot alıyor.
    Bu snapshot'ları burada saklıyoruz.
    
    Örnek:
    ┌────┬─────────┬────────────┬─────────┐
    │ id │ team_id │ date       │ elo     │
    ├────┼─────────┼────────────┼─────────┤
    │ 1  │ 1       │ 2024-01-01 │ 1820.5  │
    │ 2  │ 1       │ 2024-01-15 │ 1835.2  │
    │ 3  │ 1       │ 2024-02-01 │ 1842.5  │
    └────┴─────────┴────────────┴─────────┘
    """
    __tablename__ = "elo_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("teams.id"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    elo: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # İlişki
    team = relationship("Team", back_populates="elo_history")

