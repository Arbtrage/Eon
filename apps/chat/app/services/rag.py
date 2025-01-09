from typing import List
import logging
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        self.embedding_service_url = settings.EMBEDDING_SERVICE_URL
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_relevant_context(self, user_id: str, query: str, k: int = 3) -> str:
        try:
            response = await self.client.post(
                f"{self.embedding_service_url}/api/retrieve/",
                json={"user_id": user_id, "text": query, "k": k},
            )
            response.raise_for_status()
            result = response.json()
            contexts = [item["text"] for item in result.get("results", [])]
            return "\n\n".join(contexts) 
        except Exception as e:
            logger.error("Error retrieving context", extra={"props": {"error": str(e)}})
            return "" 

    async def __del__(self):
        await self.client.aclose()
