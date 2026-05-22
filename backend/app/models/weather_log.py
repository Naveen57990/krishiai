from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class WeatherLog(Base):
    __tablename__ = "weather_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    location: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    temperature: Mapped[float] = mapped_column(Float, nullable=True)
    feels_like: Mapped[float] = mapped_column(Float, nullable=True)
    temp_min: Mapped[float] = mapped_column(Float, nullable=True)
    temp_max: Mapped[float] = mapped_column(Float, nullable=True)
    humidity: Mapped[float] = mapped_column(Float, nullable=True)
    pressure: Mapped[float] = mapped_column(Float, nullable=True)
    wind_speed: Mapped[float] = mapped_column(Float, nullable=True)
    wind_direction: Mapped[float] = mapped_column(Float, nullable=True)
    weather_condition: Mapped[str] = mapped_column(String(100), nullable=True)
    weather_description: Mapped[str] = mapped_column(String(255), nullable=True)
    weather_icon: Mapped[str] = mapped_column(String(50), nullable=True)
    rainfall_mm: Mapped[float] = mapped_column(Float, nullable=True)
    cloud_cover: Mapped[float] = mapped_column(Float, nullable=True)
    uv_index: Mapped[float] = mapped_column(Float, nullable=True)
    visibility: Mapped[float] = mapped_column(Float, nullable=True)
    forecast: Mapped[dict] = mapped_column(JSON, nullable=True)
    raw_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<WeatherLog {self.location}: {self.temperature}°C>"
