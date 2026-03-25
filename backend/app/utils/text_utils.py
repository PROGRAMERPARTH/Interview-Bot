import re


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    return re.sub(r"\s+", " ", text)


def keyword_coverage(answer: str, keywords: list[str]) -> float:
    if not keywords:
        return 0.0
    normalized = normalize_text(answer)
    hits = sum(1 for keyword in keywords if normalize_text(keyword) in normalized)
    return round(hits / len(keywords), 2)


def clarity_score(answer: str) -> float:
    words = max(len(answer.split()), 1)
    if words < 10:
        return 4.0
    if words < 30:
        return 6.5
    if words < 80:
        return 8.0
    return 7.0
