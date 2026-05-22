from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.weather import (
    WeatherRequest, CurrentWeatherResponse, ForecastResponse, WeatherRecommendation,
)
from app.services.weather_service import WeatherService

router = APIRouter()


@router.get("/current", response_model=CurrentWeatherResponse)
async def get_current_weather(
    location: str = Query(..., description="City or location name"),
):
    service = WeatherService()
    weather = await service.get_current_weather(location)
    return weather


@router.get("/forecast", response_model=ForecastResponse)
async def get_weather_forecast(
    location: str = Query(..., description="City or location name"),
    days: int = Query(5, ge=1, le=7),
):
    service = WeatherService()
    return await service.get_forecast(location, days)


@router.get("/farming-advice", response_model=WeatherRecommendation)
async def get_farming_advice(
    location: str = Query(..., description="City or location name"),
    db: AsyncSession = Depends(get_db),
):
    service = WeatherService(db)
    return await service.get_farming_recommendations(location)
