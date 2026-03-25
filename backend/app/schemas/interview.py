from typing import Literal

from pydantic import BaseModel, Field


Difficulty = Literal["Beginner", "Intermediate", "Advanced"]
Mode = Literal["text", "voice"]


class StartInterviewRequest(BaseModel):
    role: str = Field(..., examples=["Software Engineer"])
    difficulty: Difficulty
    mode: Mode
    question_count: int | None = Field(default=None, ge=1, le=20)


class GeneratedQuestion(BaseModel):
    question: str
    ideal_answer: str
    keywords: list[str]
    topic: str


class StartInterviewResponse(BaseModel):
    interview_id: str
    current_question_index: int
    total_questions: int
    question: GeneratedQuestion


class SubmitAnswerRequest(BaseModel):
    answer: str = Field(..., min_length=1)


class Feedback(BaseModel):
    score: float
    strengths: list[str]
    weaknesses: list[str]
    suggested_improvements: list[str]
    keyword_coverage: float
    clarity_score: float
    summary: str


class SubmitAnswerResponse(BaseModel):
    feedback: Feedback
    next_question: GeneratedQuestion | None
    completed: bool


class InterviewStateResponse(BaseModel):
    interview_id: str
    role: str
    difficulty: Difficulty
    mode: Mode
    current_question_index: int
    total_questions: int
    completed: bool


class FinalReportResponse(BaseModel):
    interview_id: str
    role: str
    difficulty: Difficulty
    total_questions: int
    average_score: float
    strengths: list[str]
    weaknesses: list[str]
    suggested_improvements: list[str]
    question_breakdown: list[dict]
