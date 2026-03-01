from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class MLModel(Base):
    """
    Eğitilmiş ML model versiyonları.
    
    Her eğitimde yeni bir satır eklenir.
    is_active=True olan model üretimde kullanılır.
    
    Örnek:
    ┌────┬──────────────┬─────────┬──────────┬───────────┐
    │ id │ name         │ version │ accuracy │ is_active │
    ├────┼──────────────┼─────────┼──────────┼───────────┤
    │ 1  │ result_model │ v1.0.0  │ 0.52     │ False     │
    │ 2  │ result_model │ v1.1.0  │ 0.55     │ True      │
    │ 3  │ goals_model  │ v1.0.0  │ 0.68     │ True      │
    └────┴──────────────┴─────────┴──────────┴───────────┘
    """
    __tablename__ = "ml_models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Model tanımlayıcıları
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    version: Mapped[str] = mapped_column(String(20), nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)

    # Eğitim bilgileri
    trained_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    training_samples: Mapped[int | None] = mapped_column(Integer, nullable=True)
    feature_names: Mapped[list | None] = mapped_column(JSON, nullable=True)
    hyperparameters: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Performans metrikleri
    accuracy: Mapped[float | None] = mapped_column(Float, nullable=True)
    f1_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    auc_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    log_loss: Mapped[float | None] = mapped_column(Float, nullable=True)
    mae: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Durum
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

