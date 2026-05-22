from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.repositories.base_repository import BaseRepository
from app.models.disease_report import DiseaseReport


class DiseaseReportRepository(BaseRepository[DiseaseReport]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, DiseaseReport)

    async def get_by_farmer_id(self, farmer_id: int, skip: int = 0, limit: int = 20) -> List[DiseaseReport]:
        stmt = select(DiseaseReport).where(DiseaseReport.farmer_id == farmer_id).order_by(desc(DiseaseReport.created_at)).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_unresolved_reports(self, farmer_id: int) -> List[DiseaseReport]:
        stmt = select(DiseaseReport).where(DiseaseReport.farmer_id == farmer_id, DiseaseReport.is_resolved == False)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
