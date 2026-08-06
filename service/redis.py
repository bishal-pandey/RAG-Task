import json
from typing import Any, Dict, List
import redis


class MemoryService:

    def __init__(self, redis_url= "redis://localhost:6379/0", ttl: int = 3600):
        self.client = redis.from_url(redis_url, decode_responses=True)
        self.ttl = ttl

    def _get_key(self, session_id: str) -> str:
        return f"chat_session:{session_id}"

    def get_messages(self, session_id):
        """
        Retrieves the ordered message history for OpenAI chat completions."""
        
        raw_data = self.client.get(self._get_key(session_id))
        if not raw_data:
            return []
        try:
            return json.loads(raw_data)
        except json.JSONDecodeError:
            return []

    def add_turn(self, session_id: str, user_msg: str, ai_msg: str) :

        messages = self.get_messages(session_id)
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": ai_msg})

        key = self._get_key(session_id)
        self.client.set(key, json.dumps(messages), ex=self.ttl)