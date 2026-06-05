from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class AskRequest(BaseModel):
    """Request payload for the /ask endpoint."""

    prompt: str = Field(..., description="User prompt sent to Gemini")

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        """Reject empty prompts and normalize surrounding whitespace."""

        normalized = value.strip()
        if not normalized:
            raise ValueError("Prompt cannot be empty.")
        return normalized


class AskResponse(BaseModel):
    """Response payload returned by the /ask endpoint."""

    success: bool
    id: int
    prompt: str
    response: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost: Decimal
    cached: bool
    created_at: datetime
