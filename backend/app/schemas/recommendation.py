from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CropRecommendationRequest(BaseModel):
    soil_type: str
    ph_level: float
    rainfall_mm: float
    temperature: float
    season: str
    location: Optional[str] = None
    farm_size_hectares: Optional[float] = None


class CropSuggestion(BaseModel):
    crop_name: str
    crop_name_te: Optional[str] = None
    crop_name_hi: Optional[str] = None
    confidence_score: float
    suitability_score: float
    expected_yield_per_hectare: Optional[float] = None
    profitability_estimate: Optional[float] = None
    risk_score: float
    risk_factors: Optional[dict] = None
    farming_tips: Optional[dict] = None
    growing_period_days: Optional[int] = None


class CropRecommendationResponse(BaseModel):
    recommendations: List[CropSuggestion]
    location: Optional[str] = None
    season: str
    soil_type: str
    ph_level: float
    total_suggestions: int
    generated_at: datetime


class RecommendationHistoryResponse(BaseModel):
    id: int
    crop_name: str
    confidence_score: Optional[float] = None
    profitability_estimate: Optional[float] = None
    risk_score: Optional[float] = None
    is_adopted: bool
    created_at: datetime

    class Config:
        from_attributes = True
