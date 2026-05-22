from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.voice import VoiceResponse, TTSRequest
from app.services.voice_service import VoiceService
from app.models.user import User

router = APIRouter()


@router.post("/process", response_model=VoiceResponse)
async def process_voice(
    file: UploadFile = File(...),
    session_id: str = Form(...),
    source_language: str = Form("te"),
    target_language: str = Form("en"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = VoiceService(db)
    result = await service.process_audio(
        user_id=current_user.id,
        file=file,
        session_id=session_id,
        source_language=source_language,
        target_language=target_language,
    )
    return result


@router.post("/tts")
async def text_to_speech(
    request: TTSRequest,
    db: AsyncSession = Depends(get_db),
):
    import os
    import uuid
    from app.core.config import settings

    upload_path = os.path.join(settings.UPLOAD_DIR, "audio")
    os.makedirs(upload_path, exist_ok=True)
    filename = f"tts_{uuid.uuid4()}.mp3"
    filepath = os.path.join(upload_path, filename)

    service = VoiceService(db)
    await service._text_to_speech(request.text, request.language, filepath)

    return {"audio_url": f"/uploads/audio/{filename}"}


@router.get("/history")
async def get_voice_history(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = VoiceService(db)
    return await service.get_history(current_user.id, skip, limit)
