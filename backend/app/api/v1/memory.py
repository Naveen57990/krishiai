from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.services.memory_service import MemoryService
from app.models.user import User
from pydantic import BaseModel


class MemoryStoreRequest(BaseModel):
    memory_type: str
    key: str
    value: dict
    context: Optional[str] = None
    importance: float = 0.5


class MemoryResponse(BaseModel):
    id: int
    memory_type: str
    key: str
    value: dict
    context: Optional[str] = None
    importance_score: float
    access_count: int
    created_at: str

    class Config:
        from_attributes = True


router = APIRouter()


@router.post("/store", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
async def store_memory(
    request: MemoryStoreRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = MemoryService(db)
    memory = await service.store_memory(
        user_id=current_user.id,
        memory_type=request.memory_type,
        key=request.key,
        value=request.value,
        context=request.context,
        importance=request.importance,
    )
    return memory


@router.get("/{memory_type}/{key}", response_model=Optional[MemoryResponse])
async def get_memory(
    memory_type: str,
    key: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = MemoryService(db)
    memory = await service.get_memory(current_user.id, memory_type, key)
    return memory


@router.get("/type/{memory_type}", response_model=list[MemoryResponse])
async def get_memories_by_type(
    memory_type: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = MemoryService(db)
    return await service.get_memories_by_type(current_user.id, memory_type)


@router.get("/context")
async def get_user_context(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = MemoryService(db)
    return await service.get_user_context(current_user.id)


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory(
    memory_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = MemoryService(db)
    deleted = await service.delete_memory(memory_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found")
