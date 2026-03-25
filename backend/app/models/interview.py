from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class InterviewSession:
    role: str
    difficulty: str
    mode: str
    question_count: int
    created_at: datetime = field(default_factory=datetime.utcnow)
    questions: list[dict[str, Any]] = field(default_factory=list)
    answers: list[dict[str, Any]] = field(default_factory=list)
    completed: bool = False


COLLECTION_NAME = "interviews"
