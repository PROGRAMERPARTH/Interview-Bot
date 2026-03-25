from collections import Counter


def build_final_report(interview: dict) -> dict:
    answers = interview.get("answers", [])
    avg = round(sum(a["feedback"]["score"] for a in answers) / max(len(answers), 1), 2)

    strengths_counter = Counter(s for a in answers for s in a["feedback"].get("strengths", []))
    weak_counter = Counter(w for a in answers for w in a["feedback"].get("weaknesses", []))
    improve_counter = Counter(i for a in answers for i in a["feedback"].get("suggested_improvements", []))

    return {
        "interview_id": str(interview["_id"]),
        "role": interview["role"],
        "difficulty": interview["difficulty"],
        "total_questions": interview["question_count"],
        "average_score": avg,
        "strengths": [x for x, _ in strengths_counter.most_common(5)],
        "weaknesses": [x for x, _ in weak_counter.most_common(5)],
        "suggested_improvements": [x for x, _ in improve_counter.most_common(5)],
        "question_breakdown": answers,
    }
