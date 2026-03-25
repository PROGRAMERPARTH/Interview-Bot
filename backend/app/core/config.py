from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Interviewer Bot API"
    app_env: str = "dev"
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "interview_bot"
    default_question_count: int = 5

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
