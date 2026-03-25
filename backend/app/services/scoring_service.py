
def blended_score(llm_score: float, coverage_score: float, clarity_score: float) -> float:
    score = (0.5 * llm_score) + (0.3 * (coverage_score * 10)) + (0.2 * clarity_score)
    return round(min(max(score, 0), 10), 2)
