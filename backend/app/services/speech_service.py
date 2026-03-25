from io import BytesIO

from openai import OpenAI

from app.core.config import settings


class SpeechService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key)

    def transcribe_audio(self, filename: str, audio_bytes: bytes) -> str:
        file_like = BytesIO(audio_bytes)
        file_like.name = filename
        transcript = self.client.audio.transcriptions.create(model="whisper-1", file=file_like)
        return transcript.text
