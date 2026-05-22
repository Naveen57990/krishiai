from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class YieldPredictionRequest(BaseModel):
    crop_name: str
    area_hectares: float
    soil_type: str
    ph_level: Optional[float] = None
    rainfall_mm: Optional[float] = None
    temperature: Optional[float] = None
    fertilizer_usage: Optional[str] = None
    irrigation_method: Optional[str] = None
    seed_variety: Optional[str] = None
    planting_date: Optional[datetime] = None
    historical_yield: Optional[float] = None


class YieldPredictionResponse(BaseModel):
    id: int
    crop_name: str
    area_hectares: float
    predicted_yield_kg: Optional[float] = None
    predicted_yield_per_hectare: Optional[float] = None
    confidence_interval_lower: Optional[float] = None
    confidence_interval_upper: Optional[float] = None
    weather_impact_score: Optional[float] = None
    recommendations: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True
