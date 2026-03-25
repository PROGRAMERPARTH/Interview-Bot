from app.core.prompts import QUESTION_SYSTEM_PROMPT
from app.schemas.interview import GeneratedQuestion
from app.services.llm_client import LLMClient


class QuestionService:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def generate_question(
        self,
        role: str,
        difficulty: str,
        asked_topics: list[str],
        weak_topics: list[str] | None = None,
    ) -> GeneratedQuestion:
        adaptive_hint = (
            f"Prioritize these weak topics from previous answers: {', '.join(weak_topics)}."
            if weak_topics
            else ""
        )
        prompt = f"""
Role: {role}
Difficulty: {difficulty}
Already asked topics: {asked_topics}
{adaptive_hint}
Generate a realistic interview question.
        """.strip()

        data = self.llm.json_chat(QUESTION_SYSTEM_PROMPT, prompt)
        return GeneratedQuestion(
            question=data.get("question", "Explain a challenging project you worked on."),
            ideal_answer=data.get("ideal_answer", "Structured, concrete and technical response."),
            keywords=data.get("keywords", ["problem", "solution", "impact"]),
            topic=data.get("topic", "general"),
        )
