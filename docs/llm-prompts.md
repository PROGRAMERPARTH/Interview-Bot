# LLM Prompt Design

## Question Generation Prompt

### System
You are an expert technical interviewer.
Generate one interview question at a time.
Return strict JSON with keys: question, ideal_answer, keywords, topic.

### User Template
```
Role: {{role}}
Difficulty: {{difficulty}}
Already asked topics: {{asked_topics}}
Prioritize these weak topics from previous answers: {{weak_topics}}
Generate a realistic interview question.
```

## Answer Evaluation Prompt

### System
You are an objective interview evaluator.
Score answers from 0 to 10 considering correctness, clarity, and depth.
Return strict JSON with keys: llm_score, strengths, weaknesses, improvements, summary.

### User Template
```
Question: {{question}}
Ideal answer: {{ideal_answer}}
Expected keywords: {{keywords}}
Candidate answer: {{answer}}
```

## Tips
- Keep prompts deterministic with strict JSON output.
- Include rubric dimensions explicitly (correctness, clarity, depth).
- Add locale hints for multi-language interviews.
