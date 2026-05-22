import enum
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Boolean, DateTime, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class UserRole(str, enum.Enum):
    FARMER = "farmer"
    ADMIN = "admin"
    EXTENSION_OFFICER = "extension_officer"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.FARMER, nullable=False)
    preferred_language: Mapped[str] = mapped_column(String(10), default="en")
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    farm_size: Mapped[float] = mapped_column(nullable=True)
    soil_type: Mapped[str] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    profile_image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    disease_reports = relationship("DiseaseReport", back_populates="farmer", lazy="selectin")
    chatbot_histories = relationship("ChatbotHistory", back_populates="user", lazy="selectin")
    recommendations = relationship("Recommendation", back_populates="user", lazy="selectin")
    yield_predictions = relationship("YieldPrediction", back_populates="user", lazy="selectin")
    voice_logs = relationship("VoiceLog", back_populates="user", lazy="selectin")
    memories = relationship("FarmerMemory", back_populates="user", lazy="selectin")

    def __repr__(self):
        return f"<User {self.email}>"
