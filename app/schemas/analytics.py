from decimal import Decimal

from pydantic import BaseModel


class AnalyticsResponse(BaseModel):
    """Aggregated usage and cost metrics for all stored AI requests."""

    total_requests: int
    total_input_tokens: int
    total_output_tokens: int
    total_tokens: int
    total_estimated_cost: Decimal
    total_cache_hits: int
    total_cache_misses: int
    cache_hit_rate: float
    estimated_requests_saved: int
    total_tokens_saved: int
    average_tokens_saved_per_request: float
    average_savings_percentage: float
