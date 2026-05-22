from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class WeatherRequest(BaseModel):
    location: str


class CurrentWeatherResponse(BaseModel):
    location: str
    temperature: float
    feels_like: float
    humidity: float
    wind_speed: float
    weather_condition: str
    weather_description: str
    weather_icon: str
    rainfall_mm: Optional[float] = None
    uv_index: Optional[float] = None
    visibility: Optional[float] = None
    recorded_at: datetime


class ForecastResponse(BaseModel):
    location: str
    forecast: List[dict]
    generated_at: datetime


class WeatherRecommendation(BaseModel):
    location: str
    current_weather: CurrentWeatherResponse
    farming_advice: str
    pesticide_advice: Optional[str] = None
    irrigation_advice: Optional[str] = None
    harvest_advice: Optional[str] = None
    alerts: Optional[List[str]] = None
