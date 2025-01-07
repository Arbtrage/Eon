from pydantic import BaseModel, Field


class ChatInput(BaseModel):
    input: str = Field(..., description="The user's question or prompt")

    class Config:
        json_schema_extra = {
            "example": {"input": "Tell me about artificial intelligence"}
        }


class ErrorResponse(BaseModel):
    error: str
