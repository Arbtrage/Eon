from pydantic import BaseModel


class ChatInput(BaseModel):
    chat_id: str
    input: str
