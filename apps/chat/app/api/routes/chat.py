from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.api.models.chat import ChatInput
from app.services.llm import LLMService
from app.services.rag import RAGService
import logging
import json
from typing import AsyncIterator

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"])
llm_service = LLMService()
rag_service = RAGService()


async def process_request(user_input: str) -> AsyncIterator[str]:
    try:
        yield f"data: {json.dumps({'text': 'Starting request processing...', 'type': 'system'})}\n\n"

        yield f"data: {json.dumps({'text': 'Retrieving relevant context...', 'type': 'system'})}\n\n"
        # context = await rag_service.get_relevant_context(user_input)
        context = "AI"

        async for chunk in llm_service.generate_stream(user_input, context):
            yield chunk

        # Step 4: Execute agent tasks
        # yield f"data: {json.dumps({'text': '\nExecuting agent tasks...', 'type': 'system'})}\n\n"
        # async for chunk in agent_manager.process_task(user_input):
        #     yield chunk

    except Exception as e:
        logger.error("Error in request processing", extra={"props": {"error": str(e)}})
        yield f"data: {json.dumps({'text': f'Error: {str(e)}', 'type': 'error'})}\n\n"


@router.post(
    "/chat",
    response_class=StreamingResponse,
    summary="Chat Endpoint",
    description="Streams a chat response using RAG and agents",
)
async def chat_endpoint(chat_input: ChatInput):
    return StreamingResponse(
        process_request(chat_input.input), media_type="text/event-stream"
    )
