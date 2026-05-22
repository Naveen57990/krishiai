from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base_repository import BaseRepository
from app.models.farmer_memory import FarmerMemory
from datetime import datetime, timezone


class MemoryService:
    def __init__(self, db: AsyncSession):
        self.repo = BaseRepository(db, FarmerMemory)

    async def store_memory(self, user_id: int, memory_type: str, key: str,
                            value: dict, context: Optional[str] = None,
                            importance: float = 0.5) -> FarmerMemory:
        from sqlalchemy import select
        stmt = select(FarmerMemory).where(
            FarmerMemory.user_id == user_id,
            FarmerMemory.memory_type == memory_type,
            FarmerMemory.key == key,
        )
        result = await self.repo.db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            updated = await self.repo.update_by_id(
                existing.id,
                value=value,
                context=context,
                importance_score=importance,
                access_count=existing.access_count + 1,
                last_accessed_at=datetime.now(timezone.utc),
            )
            return updated

        return await self.repo.create(
            user_id=user_id,
            memory_type=memory_type,
            key=key,
            value=value,
            context=context,
            importance_score=importance,
        )

    async def get_memory(self, user_id: int, memory_type: str, key: str) -> Optional[FarmerMemory]:
        from sqlalchemy import select
        stmt = select(FarmerMemory).where(
            FarmerMemory.user_id == user_id,
            FarmerMemory.memory_type == memory_type,
            FarmerMemory.key == key,
        )
        result = await self.repo.db.execute(stmt)
        memory = result.scalar_one_or_none()
        if memory:
            await self.repo.update_by_id(
                memory.id,
                access_count=memory.access_count + 1,
                last_accessed_at=datetime.now(timezone.utc),
            )
        return memory

    async def get_memories_by_type(self, user_id: int, memory_type: str) -> List[FarmerMemory]:
        from sqlalchemy import select, desc
        stmt = (
            select(FarmerMemory)
            .where(FarmerMemory.user_id == user_id, FarmerMemory.memory_type == memory_type)
            .order_by(desc(FarmerMemory.importance_score), desc(FarmerMemory.updated_at))
        )
        result = await self.repo.db.execute(stmt)
        return list(result.scalars().all())

    async def get_user_context(self, user_id: int) -> dict:
        memories = await self.get_memories_by_type(user_id, "disease")
        disease_history = [
            {
                "crop": m.value.get("crop_name"),
                "disease": m.value.get("disease_name"),
                "date": m.created_at.isoformat() if m.created_at else None,
                "resolved": m.value.get("resolved", False),
            }
            for m in memories
        ]

        crop_memories = await self.get_memories_by_type(user_id, "crop")
        crops_grown = [m.value.get("crop_name") for m in crop_memories]

        pref_memories = await self.get_memories_by_type(user_id, "preference")
        preferences = {m.key: m.value for m in pref_memories}

        return {
            "disease_history": disease_history,
            "crops_grown": crops_grown,
            "preferences": preferences,
        }

    async def store_disease_memory(self, user_id: int, crop_name: str,
                                    disease_name: str, resolved: bool = False) -> FarmerMemory:
        return await self.store_memory(
            user_id=user_id,
            memory_type="disease",
            key=f"disease_{disease_name}_{crop_name}",
            value={
                "crop_name": crop_name,
                "disease_name": disease_name,
                "resolved": resolved,
                "count": 1,
            },
            context=f"Farmer had {disease_name} in {crop_name}",
            importance=0.7,
        )

    async def delete_memory(self, memory_id: int, user_id: int) -> bool:
        memory = await self.repo.get_by_id(memory_id)
        if not memory or memory.user_id != user_id:
            return False
        return await self.repo.delete_by_id(memory_id)
