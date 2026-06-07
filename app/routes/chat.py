from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.config.settings import get_settings
from app.db.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse, ConversationDetailResponse, ConversationListResponse
from app.services.conversation_service import ConversationService
from app.services.gemini_service import (
    GeminiApiError,
    GeminiNetworkError,
    GeminiQuotaError,
    InvalidGeminiApiKeyError,
)

router = APIRouter(prefix="", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    """Handle a conversation turn with automatic context compression."""

    settings = get_settings()

    try:
        service = ConversationService(settings=settings, db=db)
        return service.chat(conversation_id=payload.conversation_id, user_message=payload.user_message)
    except InvalidGeminiApiKeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Gemini API key.",
        ) from exc
    except GeminiNetworkError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to reach Gemini. Please try again later.",
        ) from exc
    except GeminiQuotaError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Gemini quota is exhausted or billing is not enabled for this project.",
        ) from exc
    except GeminiApiError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Gemini API returned an error.",
        ) from exc


@router.get("/conversations", response_model=ConversationListResponse)
def get_conversations(
    page: int = Query(default=1, ge=1, description="Page number starting from 1"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of records per page"),
    db: Session = Depends(get_db),
) -> ConversationListResponse:
    """Return a paginated list of conversations."""

    service = ConversationService(settings=get_settings(), db=db)
    return service.get_conversations(page=page, page_size=page_size)


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
def get_conversation(conversation_id: str, db: Session = Depends(get_db)) -> ConversationDetailResponse:
    """Return a single conversation and its messages."""

    service = ConversationService(settings=get_settings(), db=db)
    conversation = service.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")
    return conversation