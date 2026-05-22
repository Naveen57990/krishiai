from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.recommendation import (
    CropRecommendationRequest, CropRecommendationResponse, RecommendationHistoryResponse,
)
from app.services.recommendation_service import RecommendationService
from app.models.user import User

router = APIRouter()


@router.post("/crop", response_model=CropRecommendationResponse)
async def recommend_crops(
    request: CropRecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = RecommendationService(db)
    result = await service.get_recommendations(
        user_id=current_user.id,
        soil_type=request.soil_type,
        ph_level=request.ph_level,
        rainfall_mm=request.rainfall_mm,
        temperature=request.temperature,
        season=request.season,
        location=request.location,
        farm_size=request.farm_size_hectares,
    )
    return result


@router.get("/history", response_model=list[RecommendationHistoryResponse])
async def get_recommendation_history(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = RecommendationService(db)
    return await service.get_history(current_user.id, skip, limit)
