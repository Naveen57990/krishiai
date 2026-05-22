from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.disease import DiseaseReportResponse, DiseaseDetectionResult
from app.services.disease_service import DiseaseService
from app.models.user import User

router = APIRouter()


@router.post("/detect", response_model=DiseaseReportResponse, status_code=status.HTTP_201_CREATED)
async def detect_disease(
    file: UploadFile = File(...),
    crop_name: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    lat: Optional[float] = Form(None),
    lng: Optional[float] = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = DiseaseService(db)
    report = await service.detect_disease(
        farmer_id=current_user.id,
        file=file,
        crop_name=crop_name,
        notes=notes,
        lat=lat,
        lng=lng,
    )
    return report


@router.get("/reports", response_model=list[DiseaseReportResponse])
async def get_disease_reports(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = DiseaseService(db)
    return await service.get_reports(current_user.id, skip, limit)


@router.get("/reports/{report_id}", response_model=DiseaseReportResponse)
async def get_disease_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = DiseaseService(db)
    return await service.get_report_by_id(report_id, current_user.id)


@router.put("/reports/{report_id}", response_model=DiseaseReportResponse)
async def update_disease_report(
    report_id: int,
    is_resolved: Optional[bool] = None,
    notes: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = DiseaseService(db)
    kwargs = {}
    if is_resolved is not None:
        kwargs["is_resolved"] = is_resolved
    if notes is not None:
        kwargs["notes"] = notes
    return await service.update_report(report_id, current_user.id, **kwargs)


@router.delete("/reports/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_disease_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = DiseaseService(db)
    await service.delete_report(report_id, current_user.id)
