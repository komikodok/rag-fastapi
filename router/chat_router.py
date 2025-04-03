from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from llm.app import LLMApp
from models.message import Message

chat_router = APIRouter(prefix="/api")

@chat_router.post("/chat", summary="llm", tags=["LLM"])
def chat(message: Message):
    llm = LLMApp()
    try:
        result = llm.invoke(message)
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request"
        )
    return result