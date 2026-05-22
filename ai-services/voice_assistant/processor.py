import os
import tempfile
from typing import Optional, Tuple
from pathlib import Path


class VoiceProcessor:
    def __init__(self):
        self.whisper_model = None
        self._load_models()

    def _load_models(self):
        try:
            import whisper
            self.whisper_model = whisper.load_model("small")
            print("Whisper model loaded")
        except ImportError:
            print("Whisper not available, using API-based STT")
        except Exception as e:
            print(f"Whisper loading failed: {e}")

    def transcribe(self, audio_path: str, language: Optional[str] = None) -> str:
        if self.whisper_model:
            try:
                result = self.whisper_model.transcribe(
                    audio_path,
                    language=language if language and language != "auto" else None,
                    task="transcribe",
                )
                return result["text"].strip()
            except Exception as e:
                print(f"Whisper transcription failed: {e}")

        return self._api_transcribe(audio_path, language)

    def _api_transcribe(self, audio_path: str, language: Optional[str] = None) -> str:
        try:
            import openai
            from app.core.config import settings
            openai.api_key = settings.OPENAI_API_KEY
            with open(audio_path, "rb") as f:
                result = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    language=language if language and language != "auto" else None,
                )
            return result.text
        except Exception as e:
            print(f"API transcription failed: {e}")
            return ""

    def transcribe_with_diarization(self, audio_path: str) -> list:
        text = self.transcribe(audio_path)
        return [{"speaker": "farmer", "text": text, "timestamp": 0.0}]

    def get_audio_duration(self, audio_path: str) -> float:
        try:
            import soundfile as sf
            data, sr = sf.read(audio_path)
            return len(data) / sr
        except ImportError:
            return 0.0
        except Exception:
            return 0.0

    def convert_to_wav(self, input_path: str, output_path: Optional[str] = None) -> str:
        if output_path is None:
            output_path = input_path.rsplit(".", 1)[0] + ".wav"

        if input_path.endswith(".wav"):
            return input_path

        try:
            import soundfile as sf
            import numpy as np
            from pydub import AudioSegment

            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format="wav")
            return output_path
        except ImportError:
            from shutil import copyfile
            copyfile(input_path, output_path)
            return output_path
        except Exception as e:
            print(f"Conversion failed: {e}")
            return input_path


class TTSEngine:
    def __init__(self):
        pass

    def synthesize(self, text: str, language: str = "en", gender: str = "female", output_path: str = "output.mp3") -> str:
        try:
            import openai
            from app.core.config import settings
            openai.api_key = settings.OPENAI_API_KEY
            voice = "nova" if gender == "female" else "onyx"

            response = openai.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
            )
            response.stream_to_file(output_path)
            return output_path
        except Exception as e:
            print(f"TTS failed: {e}")
            return self._fallback_tts(text, output_path)

    def _fallback_tts(self, text: str, output_path: str) -> str:
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang="en", slow=False)
            tts.save(output_path)
            return output_path
        except Exception:
            with open(output_path, "wb") as f:
                f.write(b"")
            return output_path
