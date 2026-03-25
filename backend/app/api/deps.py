from app.services.feedback_service import FeedbackService
from app.services.llm_client import LLMClient
from app.services.question_service import QuestionService
from app.services.speech_service import SpeechService


llm_client = LLMClient()
question_service = QuestionService(llm_client)
feedback_service = FeedbackService(llm_client)
speech_service = SpeechService()
