from fastapi import APIRouter, Depends
from app.models.schemas import TextRequest, EmbeddingResponse
from app.services.embedding_service import EmbeddingService
from app.services.text_service import TextService
from app.db.milvus import MilvusDB

router = APIRouter()


@router.post(
    "/chunk-and-embed/",
    response_model=EmbeddingResponse,
    summary="Chunk and Embed Text",
    description="Takes input text, chunks it, creates embeddings, and stores them in Milvus",
)
async def chunk_and_embed(
    data: TextRequest,
    text_service: TextService = Depends(),
    embedding_service: EmbeddingService = Depends(),
    db: MilvusDB = Depends(),
):
    # Process text
    summarized_chunks = text_service.chunk_and_summarize(data.text)

    # Create embeddings
    embedded_chunks = embedding_service.create_embeddings(summarized_chunks)

    # Store in Milvus
    collection = db.create_collection()
    data_to_insert = [
        {"text": chunk, "embedding": embedding}
        for chunk, embedding in zip(summarized_chunks, embedded_chunks)
    ]
    collection.insert(data_to_insert)

    return EmbeddingResponse(
        message="Successfully processed and stored text",
        chunk_count=len(summarized_chunks),
    )
