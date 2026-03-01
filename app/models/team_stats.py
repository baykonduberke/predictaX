from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class TeamStats(Base):
    """
    Takımın son 5 maçlık ortalamaları (Feature Store).
    
    XGBoost modeline feature sağlar.
    Her takım için TEK satır vardır.
    
    Örnek:
    ┌─────────┬────────────────────┬─────────────────┬──────────────┐
    │ team_id │ avg_goals_scored_5 │ avg_corners_5   │ current_form │
    ├─────────┼────────────────────┼─────────────────┼──────────────┤
    │ 1       │ 2.4                │ 6.2             │ 13           │
    │ 2       │ 1.2                │ 4.8             │ 7            │
    └─────────┴────────────────────┴─────────────────┴──────────────┘
    """
    __tablename__ = "team_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.id"), unique=True, nullable=False
    )

    # Gol istatistikleri
    avg_goals_scored_5: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_goals_conceded_5: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Şut istatistikleri
    avg_shots_5: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_shots_target_5: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Korner istatistikleri
    avg_corners_5: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_corners_conceded_5: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Form ve streak
    current_form: Mapped[int | None] = mapped_column(Integer, nullable=True)
    win_streak: Mapped[int] = mapped_column(Integer, default=0)
    scoring_streak: Mapped[int] = mapped_column(Integer, default=0)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # İlişki
    team = relationship("Team", back_populates="stats")

