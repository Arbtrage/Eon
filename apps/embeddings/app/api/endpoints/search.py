from fastapi import APIRouter, Depends
from app.models.schemas import TextRequest, SearchResponse, SearchResult
from app.services.embedding_service import EmbeddingService
from app.db.milvus import MilvusDB

router = APIRouter()


@router.post(
    "/search/",
    response_model=SearchResponse,
    summary="Search Similar Text",
    description="Searches for similar text chunks using vector similarity in Milvus",
)
async def search_embeddings(
    data: TextRequest,
    embedding_service: EmbeddingService = Depends(),
    db: MilvusDB = Depends(),
):
    # Create query embedding
    query_embedding = embedding_service.create_query_embedding(data.text)

    # Search in Milvus
    collection = db.get_collection()
    collection.load()

    search_param = {
        "data": [query_embedding],
        "anns_field": "embedding",
        "param": {"nprobe": 10},
        "limit": 5,
        "output_fields": ["text"],
    }

    search_results = collection.search(**search_param)

    # Format results
    results = []
    for hits in search_results:
        for hit in hits:
            results.append(
                SearchResult(text=hit.entity.get("text"), similarity=hit.distance)
            )

    collection.release()

    return SearchResponse(results=results)
