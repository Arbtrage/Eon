from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import TextRequest, SearchResponse, SearchResult
from app.services.embedding_service import EmbeddingService
from app.db.milvus import MilvusDB
from typing import Optional

router = APIRouter()


@router.post(
    "/retrieve/",
    response_model=SearchResponse,
    summary="Retrieve Similar Text",
    description="Retrieves similar text chunks using vector similarity in Milvus for a specific user",
)
async def retrieve_embeddings(
    data: TextRequest,
    limit: Optional[int] = 5,
    score_threshold: Optional[float] = 0.3,
    embedding_service: EmbeddingService = Depends(),
    db: MilvusDB = Depends(),
):
    try:
        print(f"🔍 Creating query embedding for text: {data.text[:100]}...")
        query_embedding = embedding_service.create_query_embedding(data.text)

        print(f"🔎 Searching for similar texts for user {data.user_id}...")
        similar_docs = db.search_similar(
            user_id=data.user_id,
            query_embedding=query_embedding,
            limit=limit,
            score_threshold=score_threshold,
        )

        results = [
            SearchResult(text=doc["text"], similarity=doc["score"])
            for doc in similar_docs
        ]

        print(f"✅ Found {len(results)} similar documents")
        return SearchResponse(results=results)

    except Exception as e:
        print(f"❌ Error during search: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error searching embeddings: {str(e)}"
        )
