from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    crop_name: Mapped[str] = mapped_column(String(255), nullable=False)
    crop_name_te: Mapped[str] = mapped_column(String(255), nullable=True)
    crop_name_hi: Mapped[str] = mapped_column(String(255), nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=True)
    soil_type: Mapped[str] = mapped_column(String(100), nullable=True)
    ph_level: Mapped[float] = mapped_column(Float, nullable=True)
    rainfall_mm: Mapped[float] = mapped_column(Float, nullable=True)
    temperature: Mapped[float] = mapped_column(Float, nullable=True)
    season: Mapped[str] = mapped_column(String(50), nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    profitability_estimate: Mapped[float] = mapped_column(Float, nullable=True)
    risk_score: Mapped[float] = mapped_column(Float, nullable=True)
    risk_factors: Mapped[dict] = mapped_column(JSON, nullable=True)
    farming_tips: Mapped[dict] = mapped_column(JSON, nullable=True)
    is_adopted: Mapped[bool] = mapped_column(default=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="recommendations")

    def __repr__(self):
        return f"<Recommendation {self.crop_name}>"
