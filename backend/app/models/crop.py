from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Crop(Base):
    __tablename__ = "crops"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    name_te: Mapped[str] = mapped_column(String(255), nullable=True)
    name_hi: Mapped[str] = mapped_column(String(255), nullable=True)
    scientific_name: Mapped[str] = mapped_column(String(255), nullable=True)
    crop_type: Mapped[str] = mapped_column(String(100), nullable=True)
    season: Mapped[str] = mapped_column(String(100), nullable=True)
    soil_type: Mapped[str] = mapped_column(String(100), nullable=True)
    min_ph: Mapped[float] = mapped_column(Float, nullable=True)
    max_ph: Mapped[float] = mapped_column(Float, nullable=True)
    min_rainfall: Mapped[float] = mapped_column(Float, nullable=True)
    max_rainfall: Mapped[float] = mapped_column(Float, nullable=True)
    min_temperature: Mapped[float] = mapped_column(Float, nullable=True)
    max_temperature: Mapped[float] = mapped_column(Float, nullable=True)
    growing_period_days: Mapped[int] = mapped_column(Integer, nullable=True)
    water_requirement: Mapped[str] = mapped_column(String(100), nullable=True)
    nutrition_info: Mapped[dict] = mapped_column(JSON, nullable=True)
    common_pests: Mapped[dict] = mapped_column(JSON, nullable=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Crop {self.name}>"


class CropDisease(Base):
    __tablename__ = "crop_diseases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    crop_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disease_name: Mapped[str] = mapped_column(String(255), nullable=False)
    disease_name_te: Mapped[str] = mapped_column(String(255), nullable=True)
    disease_name_hi: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    symptoms: Mapped[dict] = mapped_column(JSON, nullable=True)
    causes: Mapped[str] = mapped_column(Text, nullable=True)
    treatment: Mapped[str] = mapped_column(Text, nullable=True)
    treatment_te: Mapped[str] = mapped_column(Text, nullable=True)
    treatment_hi: Mapped[str] = mapped_column(Text, nullable=True)
    prevention: Mapped[str] = mapped_column(Text, nullable=True)
    organic_treatment: Mapped[str] = mapped_column(Text, nullable=True)
    chemical_treatment: Mapped[str] = mapped_column(Text, nullable=True)
    severity: Mapped[str] = mapped_column(String(50), default="medium")
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    confidence_threshold: Mapped[float] = mapped_column(Float, default=0.5)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<CropDisease {self.disease_name}>"
