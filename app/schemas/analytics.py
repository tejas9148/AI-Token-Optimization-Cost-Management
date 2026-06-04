from decimal import Decimal

from pydantic import BaseModel


class AnalyticsResponse(BaseModel):
    """Aggregated usage and cost metrics for all stored AI requests."""

    total_requests: int
    total_input_tokens: int
    total_output_tokens: int
    total_tokens: int
    total_estimated_cost: Decimal
