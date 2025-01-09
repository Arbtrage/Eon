from redis import Redis
import json
from typing import List, Dict, Optional


class RedisService:
    def __init__(self):
        self.redis_client = Redis(host="127.0.0.1", port=6379, decode_responses=True)

    async def get_chat_history(self, chat_id: str) -> List[Dict]:
        history = self.redis_client.get(f"chat:{chat_id}")
        if not history:
            return []
        return json.loads(history)

    async def append_to_history(self, chat_id: str, message: Dict):
        key = f"chat:{chat_id}"
        history = self.redis_client.get(key)
        if history:
            messages = json.loads(history)
        else:
            messages = []
        messages.append(message)
        self.redis_client.set(key, json.dumps(messages))
