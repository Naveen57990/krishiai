from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class VoiceLog(Base):
    __tablename__ = "voice_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    session_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    audio_url: Mapped[str] = mapped_column(String(500), nullable=True)
    audio_duration_seconds: Mapped[float] = mapped_column(Float, nullable=True)
    transcript: Mapped[str] = mapped_column(Text, nullable=True)
    translated_text: Mapped[str] = mapped_column(Text, nullable=True)
    source_language: Mapped[str] = mapped_column(String(10), nullable=True)
    target_language: Mapped[str] = mapped_column(String(10), default="en")
    response_text: Mapped[str] = mapped_column(Text, nullable=True)
    response_audio_url: Mapped[str] = mapped_column(String(500), nullable=True)
    processing_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="voice_logs")

    def __repr__(self):
        return f"<VoiceLog {self.id}>"
