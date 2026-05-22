from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class YieldPrediction(Base):
    __tablename__ = "yield_predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    crop_name: Mapped[str] = mapped_column(String(255), nullable=False)
    area_hectares: Mapped[float] = mapped_column(Float, nullable=False)
    predicted_yield_kg: Mapped[float] = mapped_column(Float, nullable=True)
    predicted_yield_per_hectare: Mapped[float] = mapped_column(Float, nullable=True)
    confidence_interval_lower: Mapped[float] = mapped_column(Float, nullable=True)
    confidence_interval_upper: Mapped[float] = mapped_column(Float, nullable=True)
    soil_type: Mapped[str] = mapped_column(String(100), nullable=True)
    ph_level: Mapped[float] = mapped_column(Float, nullable=True)
    rainfall_mm: Mapped[float] = mapped_column(Float, nullable=True)
    temperature: Mapped[float] = mapped_column(Float, nullable=True)
    fertilizer_usage: Mapped[str] = mapped_column(String(255), nullable=True)
    irrigation_method: Mapped[str] = mapped_column(String(100), nullable=True)
    seed_variety: Mapped[str] = mapped_column(String(255), nullable=True)
    planting_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    harvest_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    historical_yield: Mapped[float] = mapped_column(Float, nullable=True)
    weather_impact_score: Mapped[float] = mapped_column(Float, nullable=True)
    model_used: Mapped[str] = mapped_column(String(100), nullable=True)
    model_version: Mapped[str] = mapped_column(String(50), nullable=True)
    features_used: Mapped[dict] = mapped_column(JSON, nullable=True)
    recommendations: Mapped[dict] = mapped_column(JSON, nullable=True)
    actual_yield_kg: Mapped[float] = mapped_column(Float, nullable=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="yield_predictions")

    def __repr__(self):
        return f"<YieldPrediction {self.crop_name}: {self.predicted_yield_kg}kg>"
