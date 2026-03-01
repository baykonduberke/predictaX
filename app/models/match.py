import enum
from datetime import date, datetime, time
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, Integer, String, Time, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.prediction import Prediction


class MatchResult(str, enum.Enum):
    HOME = "H"
    AWAY = "A"
    DRAW = "D"


class Match(Base):
    """
    Futbol maçı.
    CSV'deki her satır bu tabloya INSERT edilecek.
    """

    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Lig ve Tarih
    division_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("divisions.id"), nullable=False
    )
    match_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    match_time: Mapped[time | None] = mapped_column(Time, nullable=True)

    # Takımlar
    home_team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.id"), nullable=False
    )
    away_team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.id"), nullable=False
    )

    # Maç Öncesi Verileri (Model INPUT)
    home_team_elo: Mapped[float | None] = mapped_column(Float, nullable=True)
    away_team_elo: Mapped[float | None] = mapped_column(Float, nullable=True)
    form3_home: Mapped[int | None] = mapped_column(Integer, nullable=True)
    form3_away: Mapped[int | None] = mapped_column(Integer, nullable=True)
    form5_home: Mapped[int | None] = mapped_column(Integer, nullable=True)
    form5_away: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Full-time sonuçlar (TARGET)
    ft_home: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ft_away: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ft_result: Mapped[MatchResult | None] = mapped_column(
        Enum(MatchResult), nullable=True
    )

    # Half-time sonuçlar
    ht_home: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ht_away: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ht_result: Mapped[MatchResult | None] = mapped_column(
        Enum(MatchResult), nullable=True
    )

    # İstatistikler (CSV)
    home_shots: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_shots: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_shots_target: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_shots_target: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_corners: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_corners: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_fouls: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_fouls: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_yellow: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_yellow: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_red: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_red: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Ek istatistikler (API)
    home_possession: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_possession: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_xg: Mapped[float | None] = mapped_column(Float, nullable=True)
    away_xg: Mapped[float | None] = mapped_column(Float, nullable=True)
    home_offsides: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_offsides: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_saves: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_saves: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Bahis oranları
    odd_home: Mapped[float | None] = mapped_column(Float, nullable=True)
    odd_draw: Mapped[float | None] = mapped_column(Float, nullable=True)
    odd_away: Mapped[float | None] = mapped_column(Float, nullable=True)
    odd_over25: Mapped[float | None] = mapped_column(Float, nullable=True)
    odd_under25: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Cluster verileri
    c_htb: Mapped[float | None] = mapped_column(Float, nullable=True)
    c_phb: Mapped[float | None] = mapped_column(Float, nullable=True)
    c_vhd: Mapped[float | None] = mapped_column(Float, nullable=True)
    c_vad: Mapped[float | None] = mapped_column(Float, nullable=True)
    c_lth: Mapped[float | None] = mapped_column(Float, nullable=True)
    c_lta: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Meta
    source: Mapped[str] = mapped_column(String(20), default="csv")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # İlişkiler
    division = relationship("Division", back_populates="matches")
    home_team = relationship(
        "Team", foreign_keys=[home_team_id], back_populates="home_matches"
    )
    away_team = relationship(
        "Team", foreign_keys=[away_team_id], back_populates="away_matches"
    )
    predictions: Mapped[list["Prediction"]] = relationship(
        "Prediction", back_populates="match"
    )

    # Helper properties
    @property
    def total_goals(self) -> int | None:
        if self.ft_home is not None and self.ft_away is not None:
            return self.ft_home + self.ft_away
        return None

    @property
    def total_corners(self) -> int | None:
        if self.home_corners is not None and self.away_corners is not None:
            return self.home_corners + self.away_corners
        return None

    @property
    def elo_diff(self) -> float | None:
        if self.home_team_elo is not None and self.away_team_elo is not None:
            return self.home_team_elo - self.away_team_elo
        return None

    @property
    def is_over_25(self) -> bool | None:
        if self.total_goals is not None:
            return self.total_goals > 2.5
        return None
