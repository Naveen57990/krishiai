from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.yield_prediction import YieldPredictionRequest, YieldPredictionResponse
from app.services.yield_service import YieldPredictionService
from app.models.user import User

router = APIRouter()


@router.post("/predict", response_model=YieldPredictionResponse, status_code=status.HTTP_201_CREATED)
async def predict_yield(
    request: YieldPredictionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = YieldPredictionService(db)
    result = await service.predict_yield(
        user_id=current_user.id,
        crop_name=request.crop_name,
        area_hectares=request.area_hectares,
        soil_type=request.soil_type,
        ph_level=request.ph_level,
        rainfall_mm=request.rainfall_mm,
        temperature=request.temperature,
        fertilizer_usage=request.fertilizer_usage,
        irrigation_method=request.irrigation_method,
        seed_variety=request.seed_variety,
        historical_yield=request.historical_yield,
    )
    return result


@router.get("/history", response_model=list[YieldPredictionResponse])
async def get_prediction_history(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = YieldPredictionService(db)
    return await service.get_history(current_user.id, skip, limit)


@router.get("/{prediction_id}", response_model=YieldPredictionResponse)
async def get_prediction(
    prediction_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = YieldPredictionService(db)
    return await service.get_by_id(prediction_id, current_user.id)
