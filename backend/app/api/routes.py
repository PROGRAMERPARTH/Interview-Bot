from bson import ObjectId
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.api.deps import feedback_service, question_service, speech_service
from app.core.config import settings
from app.db.mongo import get_db
from app.models.interview import COLLECTION_NAME
from app.schemas.interview import (
    FinalReportResponse,
    InterviewStateResponse,
    StartInterviewRequest,
    StartInterviewResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
)
from app.services.report_service import build_final_report

router = APIRouter(prefix="/api/v1")


@router.post("/interviews", response_model=StartInterviewResponse)
def start_interview(payload: StartInterviewRequest):
    db = get_db()
    count = payload.question_count or settings.default_question_count

    first_question = question_service.generate_question(payload.role, payload.difficulty, asked_topics=[])

    interview = {
        "role": payload.role,
        "difficulty": payload.difficulty,
        "mode": payload.mode,
        "question_count": count,
        "questions": [first_question.model_dump()],
        "answers": [],
        "completed": False,
    }
    result = db[COLLECTION_NAME].insert_one(interview)

    return StartInterviewResponse(
        interview_id=str(result.inserted_id),
        current_question_index=0,
        total_questions=count,
        question=first_question,
    )


@router.get("/interviews/{interview_id}", response_model=InterviewStateResponse)
def get_interview(interview_id: str):
    db = get_db()
    interview = db[COLLECTION_NAME].find_one({"_id": ObjectId(interview_id)})
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    return InterviewStateResponse(
        interview_id=interview_id,
        role=interview["role"],
        difficulty=interview["difficulty"],
        mode=interview["mode"],
        current_question_index=len(interview.get("answers", [])),
        total_questions=interview["question_count"],
        completed=interview["completed"],
    )


def _submit_answer(interview_id: str, answer_text: str) -> SubmitAnswerResponse:
    db = get_db()
    interview = db[COLLECTION_NAME].find_one({"_id": ObjectId(interview_id)})
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    answered = len(interview["answers"])
    if answered >= interview["question_count"]:
        raise HTTPException(status_code=400, detail="Interview already completed")

    question = interview["questions"][answered]
    feedback = feedback_service.evaluate_answer(
        question=question["question"],
        ideal_answer=question["ideal_answer"],
        keywords=question["keywords"],
        answer=answer_text,
    )

    answer_payload = {
        "question_index": answered,
        "answer_text": answer_text,
        "feedback": feedback.model_dump(),
    }
    interview["answers"].append(answer_payload)

    completed = len(interview["answers"]) >= interview["question_count"]
    next_question = None

    if not completed:
        asked_topics = [q["topic"] for q in interview["questions"]]
        weak_topics = feedback.weaknesses[:2]
        next_question = question_service.generate_question(
            role=interview["role"],
            difficulty=interview["difficulty"],
            asked_topics=asked_topics,
            weak_topics=weak_topics,
        )
        interview["questions"].append(next_question.model_dump())

    interview["completed"] = completed
    db[COLLECTION_NAME].replace_one({"_id": ObjectId(interview_id)}, interview)

    return SubmitAnswerResponse(feedback=feedback, next_question=next_question, completed=completed)


@router.post("/interviews/{interview_id}/answer", response_model=SubmitAnswerResponse)
def submit_answer(interview_id: str, payload: SubmitAnswerRequest):
    return _submit_answer(interview_id, payload.answer)


@router.post("/interviews/{interview_id}/answer/voice", response_model=SubmitAnswerResponse)
async def submit_voice_answer(interview_id: str, audio: UploadFile = File(...)):
    content = await audio.read()
    transcript = speech_service.transcribe_audio(audio.filename, content)
    return _submit_answer(interview_id, transcript)


@router.get("/interviews/{interview_id}/report", response_model=FinalReportResponse)
def get_report(interview_id: str):
    db = get_db()
    interview = db[COLLECTION_NAME].find_one({"_id": ObjectId(interview_id)})
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return build_final_report(interview)
