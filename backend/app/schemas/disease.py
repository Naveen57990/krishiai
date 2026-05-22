from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DiseaseReportRequest(BaseModel):
    crop_name: Optional[str] = None
    notes: Optional[str] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None


class DiseaseReportResponse(BaseModel):
    id: int
    farmer_id: int
    crop_name: Optional[str] = None
    disease_name: Optional[str] = None
    confidence_score: Optional[float] = None
    image_url: Optional[str] = None
    treatment_recommended: Optional[str] = None
    organic_treatment: Optional[str] = None
    chemical_treatment: Optional[str] = None
    severity: Optional[str] = None
    is_resolved: bool
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DiseaseDetectionResult(BaseModel):
    disease_name: str
    disease_name_te: Optional[str] = None
    disease_name_hi: Optional[str] = None
    confidence_score: float
    severity: str
    description: Optional[str] = None
    symptoms: Optional[dict] = None
    causes: Optional[str] = None
    treatment: Optional[str] = None
    treatment_te: Optional[str] = None
    treatment_hi: Optional[str] = None
    organic_treatment: Optional[str] = None
    chemical_treatment: Optional[str] = None
    prevention: Optional[str] = None
