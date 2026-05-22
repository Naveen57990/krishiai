from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base_repository import BaseRepository
from app.models.recommendation import Recommendation
from app.models.crop import Crop
from datetime import datetime, timezone
import numpy as np
from sqlalchemy import select


class RecommendationService:
    def __init__(self, db: AsyncSession):
        self.repo = BaseRepository(db, Recommendation)

    async def get_recommendations(self, user_id: int, soil_type: str, ph_level: float,
                                   rainfall_mm: float, temperature: float, season: str,
                                   location: Optional[str] = None,
                                   farm_size: Optional[float] = None) -> dict:
        from sqlalchemy import select
        stmt = select(Crop).where(Crop.soil_type == soil_type)
        if ph_level:
            stmt = stmt.where(Crop.min_ph <= ph_level, Crop.max_ph >= ph_level)
        if season:
            stmt = stmt.where(Crop.season.ilike(f"%{season}%"))

        result = await self.repo.db.execute(stmt)
        suitable_crops = list(result.scalars().all())

        suggestions = []
        for crop in suitable_crops:
            score = self._calculate_suitability(crop, ph_level, rainfall_mm, temperature, soil_type)
            if score > 0.3:
                suggestions.append({
                    "crop_name": crop.name,
                    "crop_name_te": crop.name_te,
                    "crop_name_hi": crop.name_hi,
                    "confidence_score": round(score, 3),
                    "suitability_score": round(score, 3),
                    "expected_yield_per_hectare": None,
                    "profitability_estimate": round(score * np.random.uniform(50000, 200000), 2),
                    "risk_score": round(1 - score, 3),
                    "risk_factors": self._get_risk_factors(crop, ph_level, rainfall_mm, temperature),
                    "farming_tips": {"water": crop.water_requirement, "days": crop.growing_period_days},
                    "growing_period_days": crop.growing_period_days,
                })

        suggestions.sort(key=lambda x: x["confidence_score"], reverse=True)

        if suggestions and user_id:
            top = suggestions[0]
            await self.repo.create(
                user_id=user_id,
                crop_name=top["crop_name"],
                crop_name_te=top.get("crop_name_te"),
                crop_name_hi=top.get("crop_name_hi"),
                confidence_score=top["confidence_score"],
                soil_type=soil_type,
                ph_level=ph_level,
                rainfall_mm=rainfall_mm,
                temperature=temperature,
                season=season,
                location=location,
                profitability_estimate=top["profitability_estimate"],
                risk_score=top["risk_score"],
            )

        return {
            "recommendations": suggestions[:5],
            "location": location,
            "season": season,
            "soil_type": soil_type,
            "ph_level": ph_level,
            "total_suggestions": len(suggestions),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _calculate_suitability(self, crop: Crop, ph: float, rainfall: float, temp: float, soil: str) -> float:
        scores = []
        if crop.min_ph and crop.max_ph:
            ph_score = 1 - abs(ph - (crop.min_ph + crop.max_ph) / 2) / (crop.max_ph - crop.min_ph + 0.1)
            scores.append(max(0, ph_score))
        if crop.min_rainfall and crop.max_rainfall:
            rf_score = 1 - abs(rainfall - (crop.min_rainfall + crop.max_rainfall) / 2) / (crop.max_rainfall - crop.min_rainfall + 1)
            scores.append(max(0, rf_score))
        if crop.min_temperature and crop.max_temperature:
            temp_score = 1 - abs(temp - (crop.min_temperature + crop.max_temperature) / 2) / (crop.max_temperature - crop.min_temperature + 0.1)
            scores.append(max(0, temp_score))
        if crop.soil_type and soil:
            soil_score = 1.0 if crop.soil_type.lower() == soil.lower() else 0.5
            scores.append(soil_score)
        return np.mean(scores) if scores else 0.5

    def _get_risk_factors(self, crop: Crop, ph: float, rainfall: float, temp: float) -> dict:
        risks = []
        if crop.min_ph and ph < crop.min_ph:
            risks.append("Soil pH is below optimal range")
        if crop.max_ph and ph > crop.max_ph:
            risks.append("Soil pH is above optimal range")
        if crop.min_rainfall and rainfall < crop.min_rainfall.min_rainfall:
            risks.append("Rainfall below optimal range, irrigation needed")
        if crop.max_rainfall and rainfall > crop.max_rainfall:
            risks.append("Excess rainfall risk, ensure drainage")
        if crop.min_temperature and temp < crop.min_temperature:
            risks.append("Temperature below optimal range")
        if crop.max_temperature and temp > crop.max_temperature:
            risks.append("Temperature above optimal range")
        return {"risks": risks, "overall_risk": len(risks) / 6 if risks else 0}

    async def get_history(self, user_id: int, skip: int = 0, limit: int = 20) -> list:
        from sqlalchemy import select, desc
        stmt = (
            select(Recommendation)
            .where(Recommendation.user_id == user_id)
            .order_by(desc(Recommendation.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await self.repo.db.execute(stmt)
        return list(result.scalars().all())
