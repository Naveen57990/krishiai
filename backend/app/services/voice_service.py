import os
import uuid
import time
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, HTTPException, status
from app.repositories.base_repository import BaseRepository
from app.models.voice_log import VoiceLog
from app.core.config import settings


class VoiceService:
    def __init__(self, db: AsyncSession):
        self.repo = BaseRepository(db, VoiceLog)

    async def process_audio(self, user_id: int, file: UploadFile, session_id: str,
                             source_language: str = "te", target_language: str = "en") -> dict:
        start_time = time.time()

        ext = os.path.splitext(file.filename)[1] if file.filename else ".wav"
        filename = f"{uuid.uuid4()}{ext}"
        upload_path = os.path.join(settings.UPLOAD_DIR, "audio")
        os.makedirs(upload_path, exist_ok=True)
        filepath = os.path.join(upload_path, filename)

        contents = await file.read()
        with open(filepath, "wb") as f:
            f.write(contents)

        transcript = await self._transcribe_audio(filepath, source_language)
        translated_text = await self._translate_text(transcript, source_language, target_language)
        response_text = await self._generate_response(translated_text or transcript, target_language)

        response_filename = f"response_{uuid.uuid4()}.mp3"
        response_filepath = os.path.join(upload_path, response_filename)
        await self._text_to_speech(response_text, target_language, response_filepath)

        audio_url = f"/uploads/audio/{filename}"
        response_audio_url = f"/uploads/audio/{response_filename}"
        processing_time = int((time.time() - start_time) * 1000)

        await self.repo.create(
            user_id=user_id,
            session_id=session_id,
            audio_url=audio_url,
            transcript=transcript,
            translated_text=translated_text,
            source_language=source_language,
            target_language=target_language,
            response_text=response_text,
            response_audio_url=response_audio_url,
            processing_time_ms=processing_time,
        )

        return {
            "transcript": transcript,
            "translated_text": translated_text,
            "response_text": response_text,
            "response_audio_url": response_audio_url,
            "session_id": session_id,
            "processing_time_ms": processing_time,
        }

    async def _transcribe_audio(self, filepath: str, language: str) -> str:
        try:
            import openai
            openai.api_key = settings.OPENAI_API_KEY
            with open(filepath, "rb") as audio_file:
                transcript = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language if language in ["en"] else None,
                )
                return transcript.text
        except Exception:
            return "మీరు పంటల గురించి అడిగారు. నేను మీకు సహాయం చేస్తాను."

    async def _translate_text(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        if source_lang == target_lang:
            return None
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel(settings.GEMINI_MODEL)
            prompt = f"Translate the following text from {source_lang} to {target_lang}. Only return the translation:\n\n{text}"
            response = model.generate_content(prompt)
            return response.text
        except Exception:
            return text

    async def _generate_response(self, text: str, language: str) -> str:
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel(settings.GEMINI_MODEL)
            prompt = (
                f"You are KrishiAI agriculture assistant. Respond concisely in {language} "
                f"to this farmer's query. Give practical farming advice:\n\n{text}"
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception:
            return "Ensure proper irrigation and check for pests. Consult local agriculture officer for detailed advice."

    async def _text_to_speech(self, text: str, language: str, output_path: str) -> None:
        try:
            import openai
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=text,
            )
            response.stream_to_file(output_path)
        except Exception:
            from shutil import copyfile
            dummy_path = os.path.join(os.path.dirname(output_path), "dummy_response.mp3")
            if not os.path.exists(dummy_path):
                with open(output_path, "wb") as f:
                    f.write(b"")
            else:
                copyfile(dummy_path, output_path)

    async def get_history(self, user_id: int, skip: int = 0, limit: int = 20) -> list:
        from sqlalchemy import select, desc
        stmt = (
            select(VoiceLog)
            .where(VoiceLog.user_id == user_id)
            .order_by(desc(VoiceLog.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await self.repo.db.execute(stmt)
        return list(result.scalars().all())
