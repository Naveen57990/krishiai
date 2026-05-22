import time
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base_repository import BaseRepository
from app.models.chatbot_history import ChatbotHistory
from app.core.config import settings


class ChatbotService:
    def __init__(self, db: AsyncSession):
        self.repo = BaseRepository(db, ChatbotHistory)

    async def process_message(self, user_id: int, message: str, session_id: str,
                               language: str = "en", include_weather: bool = False,
                               location: Optional[str] = None) -> dict:
        start_time = time.time()

        weather_context = None
        if include_weather and location:
            try:
                from app.services.weather_service import WeatherService
                ws = WeatherService()
                weather_context = await ws.get_current_weather(location)
            except Exception:
                pass

        response_text = await self._generate_response(message, language, weather_context, user_id)
        processing_time = int((time.time() - start_time) * 1000)

        history = await self.repo.create(
            user_id=user_id,
            session_id=session_id,
            message=message,
            response=response_text,
            language=language,
            processing_time_ms=processing_time,
        )

        return {
            "response": response_text,
            "session_id": session_id,
            "language": language,
            "weather_context": weather_context,
            "processing_time_ms": processing_time,
        }

    async def _generate_response(self, message: str, language: str,
                                  weather_context: Optional[dict] = None,
                                  user_id: Optional[int] = None) -> str:
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel(settings.GEMINI_MODEL)

            system_prompt = self._get_system_prompt(language, weather_context)
            full_prompt = f"{system_prompt}\n\nFarmer: {message}\n\nAssistant:"

            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            try:
                import openai
                openai.api_key = settings.OPENAI_API_KEY
                system_prompt = self._get_system_prompt(language, weather_context)
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message},
                    ],
                    max_tokens=500,
                )
                return response.choices[0].message.content
            except Exception:
                return self._get_fallback_response(message, language)

    def _get_system_prompt(self, language: str, weather_context: Optional[dict] = None) -> str:
        base_prompt = (
            "You are KrishiAI, an expert AI agriculture assistant for farmers in India. "
            "Provide practical, actionable advice about farming, crop management, pest control, "
            "irrigation, fertilization, and sustainable agriculture practices. "
            "Keep responses concise, practical, and easy to understand. "
            "Use simple language. Be specific with measurements and quantities when recommending treatments."
        )

        if language == "te":
            base_prompt += (
                " దయచేసి తెలుగులో సమాధానం ఇవ్వండి. వ్యవసాయ సంబంధిత సలహాలను సులభమైన భాషలో వివరించండి."
            )
        elif language == "hi":
            base_prompt += (
                " कृपया हिंदी में उत्तर दें। कृषि संबंधी सलाह सरल भाषा में समझाएं।"
            )

        if weather_context:
            base_prompt += (
                f"\n\nCurrent weather at farmer's location: "
                f"Temperature: {weather_context.get('temperature', 'N/A')}°C, "
                f"Humidity: {weather_context.get('humidity', 'N/A')}%, "
                f"Condition: {weather_context.get('weather_condition', 'N/A')}. "
                "Consider these weather conditions in your advice."
            )

        return base_prompt

    def _get_fallback_response(self, message: str, language: str) -> str:
        responses = {
            "en": "I understand you're asking about farming. For specific advice, please consult your local agricultural extension officer. In the meantime, ensure your crops are well-watered and check for pest signs regularly.",
            "te": "మీరు వ్యవసాయం గురించి అడుగుతున్నారని నేను అర్థం చేసుకున్నాను. నిర్దిష్ట సలహా కోసం, దయచేసి మీ స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి. ఇప్పుడు, మీ పంటలకు సరిగ్గా నీరు అందించండి మరియు తెగుళ్ళ సంకేతాల కోసం క్రమం తప్పకుండా తనిఖీ చేయండి.",
            "hi": "मैं समझता हूं कि आप खेती के बारे में पूछ रहे हैं। विशिष्ट सलाह के लिए, कृपया अपने स्थानीय कृषि अधिकारी से परामर्श करें। तब तक, सुनिश्चित करें कि आपकी फसलों को अच्छी तरह से पानी मिल रहा है और कीटों के संकेतों के लिए नियमित रूप से जांच करें।",
        }
        return responses.get(language, responses["en"])

    async def get_conversation_history(self, user_id: int, session_id: str, skip: int = 0, limit: int = 50) -> List[ChatbotHistory]:
        from sqlalchemy import select, desc
        from sqlalchemy.ext.asyncio import AsyncSession
        stmt = (
            select(ChatbotHistory)
            .where(ChatbotHistory.user_id == user_id, ChatbotHistory.session_id == session_id)
            .order_by(desc(ChatbotHistory.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await self.repo.db.execute(stmt)
        return list(result.scalars().all())

    async def get_sessions(self, user_id: int) -> list:
        from sqlalchemy import select, func
        stmt = (
            select(ChatbotHistory.session_id, func.count(), func.max(ChatbotHistory.created_at))
            .where(ChatbotHistory.user_id == user_id)
            .group_by(ChatbotHistory.session_id)
            .order_by(func.max(ChatbotHistory.created_at).desc())
        )
        result = await self.repo.db.execute(stmt)
        return [{"session_id": row[0], "message_count": row[1], "last_activity": row[2]} for row in result]
