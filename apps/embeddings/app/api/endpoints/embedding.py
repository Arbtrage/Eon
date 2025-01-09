from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.models.schemas import TextRequest, EmbeddingResponse
from app.services.embedding_service import EmbeddingService
from app.services.text_service import TextService
from app.db.milvus import MilvusDB
from unstructured.partition.md import partition_md
from langchain.document_loaders import UnstructuredFileLoader
import logging
import os

router = APIRouter()


@router.post(
    "/process-files/",
    response_model=EmbeddingResponse,
    summary="Process Documentation Files",
    description="Processes various document types (Markdown, PDF, etc.), chunks their content, creates embeddings, and stores them in Milvus",
)
async def process_files(
    user_id: str,
    text_service: TextService = Depends(),
    embedding_service: EmbeddingService = Depends(),
    db: MilvusDB = Depends(),
):
    try:
        file_paths = [
            "./data/data.md",
        ]
        combined_elements = []

        for file_path in file_paths:
            try:
                print(f"Processing file: {file_path}")
                file_ext = os.path.splitext(file_path)[1].lower()

                if file_ext == ".md":
                    elements = partition_md(filename=file_path)
                    combined_elements.extend([str(element) for element in elements])
                else:
                    loader = UnstructuredFileLoader(file_path)
                    elements = loader.load()
                    combined_elements.extend(
                        [str(doc.page_content) for doc in elements]
                    )

                print(f"Successfully processed file: {file_path}")
            except Exception as file_error:
                logging.error(f"Error processing file {file_path}: {str(file_error)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error processing file {file_path}: {str(file_error)}",
                )

        combined_text = "\n\n".join(combined_elements)
        print(f"Combined text length: {len(combined_text)}")

        print("Starting hybrid text processing")
        processed_chunks = text_service.process_text(combined_text)
        print(f"Created {len(processed_chunks)} chunks")
        embedded_chunks = embedding_service.create_embeddings(processed_chunks)
        db.insert_embeddings(
            user_id=user_id, texts=processed_chunks, embeddings=embedded_chunks
        )
        print("Successfully stored embeddings")

        return EmbeddingResponse(
            message="Successfully processed and stored files",
            chunk_count=len(processed_chunks),
        )
    except Exception as e:
        logging.error(f"Error in process_files: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")
