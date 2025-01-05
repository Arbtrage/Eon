from pydantic import BaseModel, Field
from typing import List, Optional


class TextRequest(BaseModel):
    text: str = Field(..., description="Text to be processed or searched")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "This is a sample text that needs to be processed or searched."
            }
        }


class SearchResult(BaseModel):
    text: str
    similarity: float


class SearchResponse(BaseModel):
    results: List[SearchResult]


class EmbeddingResponse(BaseModel):
    message: str
    chunk_count: int
