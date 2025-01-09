from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = ""
    PROJECT_NAME: str = "RAGing Service"

    # LLM Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    MODEL_NAME: str = "gpt-3.5-turbo"
    TEMPERATURE: float = 0.7

    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Embedding Service Settings
    EMBEDDING_SERVICE_URL: str = "http://localhost:8000"
    EMBEDDING_SERVICE_ENDPOINT: str = "/api/retrieve"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
