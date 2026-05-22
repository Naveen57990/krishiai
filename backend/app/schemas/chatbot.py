from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatbotMessage(BaseModel):
    message: str
    session_id: str
    language: str = "en"
    include_weather: bool = False
    location: Optional[str] = None


class ChatbotResponse(BaseModel):
    response: str
    session_id: str
    language: str
    sources: Optional[List[str]] = None
    weather_context: Optional[dict] = None
    processing_time_ms: Optional[int] = None


class ChatbotHistoryResponse(BaseModel):
    id: int
    message: str
    response: str
    language: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationHistory(BaseModel):
    session_id: str
    messages: List[ChatbotHistoryResponse]
    total_count: int
