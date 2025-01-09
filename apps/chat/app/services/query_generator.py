from app.services.llm import LLMService
from typing import List, Dict

class QueryGenerator:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    async def generate_optimized_query(
        self, current_input: str, chat_history: List[Dict]
    ) -> str:
        prompt = self._create_query_generation_prompt(current_input, chat_history)
        query = await self.llm_service.generate_query(prompt)
        return query

    def _create_query_generation_prompt(
        self, current_input: str, chat_history: List[Dict]
    ) -> str:
        return f"""Based on the following chat history and current input, generate an optimized search query:

Chat History:
{self._format_chat_history(chat_history)}

Current Input: {current_input}

Generate a concise search query that captures the essential information needs."""

    def _format_chat_history(self, history: List[Dict]) -> str:
        return "\n".join(
            [
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in history[-3:]
            ]
        )
