from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_optional_user
from app.schemas.chatbot import ChatbotMessage, ChatbotResponse, ConversationHistory
from app.services.chatbot_service import ChatbotService
from app.models.user import User

router = APIRouter()


@router.post("/chat", response_model=ChatbotResponse)
async def chat(
    request: ChatbotMessage,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ChatbotService(db)
    result = await service.process_message(
        user_id=current_user.id,
        message=request.message,
        session_id=request.session_id,
        language=request.language,
        include_weather=request.include_weather,
        location=request.location,
    )
    return result


@router.post("/anonymous", response_model=ChatbotResponse)
async def anonymous_chat(
    request: ChatbotMessage,
    db: AsyncSession = Depends(get_db),
):
    service = ChatbotService(db)
    result = await service.process_message(
        user_id=0,
        message=request.message,
        session_id=request.session_id,
        language=request.language,
        include_weather=request.include_weather,
        location=request.location,
    )
    return result


@router.get("/history/{session_id}")
async def get_chat_history(
    session_id: str,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ChatbotService(db)
    messages = await service.get_conversation_history(current_user.id, session_id, skip, limit)
    return {
        "session_id": session_id,
        "messages": messages,
        "total_count": len(messages),
    }


@router.get("/sessions")
async def get_chat_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ChatbotService(db)
    return await service.get_sessions(current_user.id)
