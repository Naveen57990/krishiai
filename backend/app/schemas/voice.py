from pydantic import BaseModel
from typing import Optional


class VoiceRequest(BaseModel):
    session_id: str
    source_language: str = "te"
    target_language: str = "en"


class VoiceResponse(BaseModel):
    transcript: str
    translated_text: Optional[str] = None
    response_text: str
    response_audio_url: Optional[str] = None
    session_id: str
    processing_time_ms: Optional[int] = None


class TTSRequest(BaseModel):
    text: str
    language: str = "en"
    gender: str = "female"
