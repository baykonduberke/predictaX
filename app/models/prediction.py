from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Prediction(Base):
    """
    Model tahminleri kaydı.
    
    Her tahmin bir maç ve bir market için yapılır.
    
    Örnek:
    ┌────┬──────────┬─────────┬────────────┬─────────────┬────────────┐
    │ id │ match_id │ market  │ prediction │ probability │ is_correct │
    ├────┼──────────┼─────────┼────────────┼─────────────┼────────────┤
    │ 1  │ 1        │ result  │ H          │ 0.65        │ True       │
    │ 2  │ 1        │ over25  │ Over       │ 0.72        │ True       │
    │ 3  │ 1        │ corners │ NULL       │ NULL        │ NULL       │
    └────┴──────────┴─────────┴────────────┴─────────────┴────────────┘
    """
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_id: Mapped[int] = mapped_column(Integer, ForeignKey("matches.id"), index=True)

    # Tahmin bilgileri
    market: Mapped[str] = mapped_column(String(50), nullable=False)
    prediction: Mapped[str | None] = mapped_column(String(10), nullable=True)
    probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    prob_details: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    predicted_value: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Model bilgisi
    model_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    features_used: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Doğrulama (maç bittikten sonra)
    is_correct: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    actual_value: Mapped[str | None] = mapped_column(String(50), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # İlişki
    match = relationship("Match", back_populates="predictions")

