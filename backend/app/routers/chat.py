from __future__ import annotations

from fastapi import APIRouter, HTTPException
from app.schemas import ChatMessageRequest, ChatResponse
from app.services.ai_service import AIService

router = APIRouter(prefix="/api", tags=["chat"])
ai_service = AIService()


@router.post("/v1/chat", response_model=ChatResponse)
def chat_with_assistant_v1(payload: ChatMessageRequest):
    if not payload.message or not payload.message.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    user_query = payload.message.strip()

    # Direct Gemini AI call
    answer = ai_service.generate_chat_response(
        question=user_query,
        retrieved_context=[],
        prior_message_count=0
    )

    return ChatResponse(
        answer=answer,
        conversation_id=payload.conversation_id or 0,
        source_documents=[]
    )


@router.post("/chat", response_model=ChatResponse)
def chat_with_assistant(payload: ChatMessageRequest):
    return chat_with_assistant_v1(payload)