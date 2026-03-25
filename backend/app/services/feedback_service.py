from app.core.prompts import EVALUATION_SYSTEM_PROMPT
from app.schemas.interview import Feedback
from app.services.llm_client import LLMClient
from app.services.scoring_service import blended_score
from app.utils.text_utils import clarity_score, keyword_coverage


class FeedbackService:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def evaluate_answer(self, question: str, ideal_answer: str, keywords: list[str], answer: str) -> Feedback:
        coverage = keyword_coverage(answer, keywords)
        clarity = clarity_score(answer)

        prompt = f"""
Question: {question}
Ideal answer: {ideal_answer}
Expected keywords: {keywords}
Candidate answer: {answer}
        """.strip()
        llm_data = self.llm.json_chat(EVALUATION_SYSTEM_PROMPT, prompt)

        llm_score = float(llm_data.get("llm_score", 5.0))
        total = blended_score(llm_score, coverage, clarity)

        return Feedback(
            score=total,
            strengths=llm_data.get("strengths", []),
            weaknesses=llm_data.get("weaknesses", []),
            suggested_improvements=llm_data.get("improvements", []),
            keyword_coverage=coverage,
            clarity_score=clarity,
            summary=llm_data.get("summary", "Good start. Add more concrete examples."),
        )
