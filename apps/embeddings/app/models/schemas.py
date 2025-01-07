from pydantic import BaseModel
from typing import List, Optional


class TextRequest(BaseModel):
    text: str
    user_id: str


class SearchResult(BaseModel):
    text: str
    similarity: float


class SearchResponse(BaseModel):
    results: List[SearchResult]


class EmbeddingResponse(BaseModel):
    message: str
    chunk_count: int
