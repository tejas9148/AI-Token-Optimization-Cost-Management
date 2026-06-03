from fastapi import APIRouter, HTTPException, status

from app.config.settings import get_settings
from app.schemas.ask import AskRequest, AskResponse
from app.services.gemini_service import (
    GeminiApiError,
    GeminiNetworkError,
    GeminiQuotaError,
    GeminiService,
    InvalidGeminiApiKeyError,
)

router = APIRouter(prefix="", tags=["AI Gateway"])


@router.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest) -> AskResponse:
    """Accept a prompt, send it to Gemini, and return the generated response."""

    settings = get_settings()

    try:
        service = GeminiService(settings=settings)
        gemini_response = service.generate_response(payload.prompt)
        return AskResponse(success=True, prompt=payload.prompt, response=gemini_response)
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
