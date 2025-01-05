from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Text Embedding and Search API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "An API for chunking text, creating embeddings, and performing semantic search using Milvus"
    )

    # Milvus settings
    MILVUS_HOST: str = "127.0.0.1"
    MILVUS_PORT: str = "19530"
    COLLECTION_NAME: str = "readme_embeddings"

    # Google API settings
    GOOGLE_API_KEY: str
    GEMINI_EMBEDDING_MODEL: str = "models/embedding-001"
    GEMINI_CHAT_MODEL: str = "gemini-pro"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings():
    return Settings()
