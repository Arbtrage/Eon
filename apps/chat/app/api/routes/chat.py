from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.api.models.chat import ChatInput
from app.services.llm import LLMService
from app.services.rag import RAGService
from app.services.redis_service import RedisService
from app.services.query_generator import QueryGenerator
import logging
import json
from typing import AsyncIterator

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"])
llm_service = LLMService()
rag_service = RAGService()
redis_service = RedisService()
query_generator = QueryGenerator(llm_service)


async def process_request(chat_id: str, user_input: str) -> AsyncIterator[str]:
    try:
        yield f"data: {json.dumps({'text': 'Starting request processing...', 'type': 'system'})}\n\n"

        chat_history = await redis_service.get_chat_history(chat_id)

        print(chat_history)

        yield f"data: {json.dumps({'text': 'Generating optimized query...', 'type': 'system'})}\n\n"
        optimized_query = await query_generator.generate_optimized_query(
            user_input, chat_history
        )

        yield f"data: {json.dumps({'text': 'Retrieving relevant context...', 'type': 'system'})}\n\n"
        context = await rag_service.get_relevant_context(
            "default_user", optimized_query
        )

        if not context:
            context = "No relevant context found"

        full_context = {
            "chat_history": chat_history,
            "current_input": user_input,
            "retrieved_context": context,
        }

        # Generate response
        response_text = ""
        async for chunk in llm_service.generate_stream(user_input, full_context):
            response_text += json.loads(chunk.split("data: ")[1])["text"]
            yield chunk

        # Store in Redis
        await redis_service.append_to_history(
            chat_id, {"role": "user", "content": user_input}
        )
        await redis_service.append_to_history(
            chat_id, {"role": "assistant", "content": response_text}
        )

    except Exception as e:
        logger.error("Error in request processing", extra={"props": {"error": str(e)}})
        yield f"data: {json.dumps({'text': f'Error: {str(e)}', 'type': 'error'})}\n\n"


@router.post(
    "/chat",
    response_class=StreamingResponse,
    summary="Chat Endpoint",
    description="Streams a chat response using RAG and agents with chat history",
)
async def chat_endpoint(chat_input: ChatInput):
    return StreamingResponse(
        process_request(chat_input.chat_id, chat_input.input),
        media_type="text/event-stream",
    )
