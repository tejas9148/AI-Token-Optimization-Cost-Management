from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.settings import get_settings
from app.db.database import get_db
from app.schemas.ask import AskRequest, AskResponse
from app.services.ask_service import AskService
from app.services.gemini_service import (
    GeminiApiError,
    GeminiNetworkError,
    GeminiQuotaError,
    InvalidGeminiApiKeyError,
)

router = APIRouter(prefix="", tags=["AI Gateway"])


@router.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest, db: Session = Depends(get_db)) -> AskResponse:
    """Accept a prompt, send it to Gemini, and return the generated response."""

    settings = get_settings()

    try:
        service = AskService(settings=settings, db=db)
        ai_request = service.process_prompt(payload.prompt)
        return AskResponse(
            success=True,
            id=ai_request.id,
            prompt=ai_request.prompt,
            original_prompt=ai_request.original_prompt,
            optimized_prompt=ai_request.optimized_prompt,
            response=ai_request.response,
            original_tokens=ai_request.original_input_tokens,
            optimized_tokens=ai_request.optimized_input_tokens,
            tokens_saved=ai_request.tokens_saved,
            savings_percentage=float(ai_request.savings_percentage),
            input_tokens=ai_request.input_tokens,
            output_tokens=ai_request.output_tokens,
            total_tokens=ai_request.total_tokens,
            estimated_cost=ai_request.estimated_cost,
            cached=ai_request.served_from_cache,
            created_at=ai_request.created_at,
        )
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
