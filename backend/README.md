# Backend (FastAPI)

## Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Environment variables
Create `.env`:

```bash
APP_NAME=AI Interviewer Bot API
APP_ENV=dev
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=interview_bot
DEFAULT_QUESTION_COUNT=5
```
