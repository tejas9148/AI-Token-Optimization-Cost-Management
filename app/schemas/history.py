from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class HistoryItem(BaseModel):
    """Single request record returned in the history list."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    prompt: str
    response: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost: Decimal
    created_at: datetime


class HistoryResponse(BaseModel):
    """Paginated history response."""

    items: list[HistoryItem]
    page: int
    page_size: int
    total_items: int
    total_pages: int
