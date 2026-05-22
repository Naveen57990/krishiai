from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class DiseaseReport(Base):
    __tablename__ = "disease_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    farmer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    crop_id: Mapped[int] = mapped_column(Integer, nullable=True)
    crop_name: Mapped[str] = mapped_column(String(255), nullable=True)
    disease_name: Mapped[str] = mapped_column(String(255), nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    image_thumbnail_url: Mapped[str] = mapped_column(String(500), nullable=True)
    treatment_recommended: Mapped[str] = mapped_column(Text, nullable=True)
    organic_treatment: Mapped[str] = mapped_column(Text, nullable=True)
    chemical_treatment: Mapped[str] = mapped_column(Text, nullable=True)
    severity: Mapped[str] = mapped_column(String(50), nullable=True)
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    location_lat: Mapped[float] = mapped_column(Float, nullable=True)
    location_lng: Mapped[float] = mapped_column(Float, nullable=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    farmer = relationship("User", back_populates="disease_reports")

    def __repr__(self):
        return f"<DiseaseReport {self.id}: {self.disease_name}>"
