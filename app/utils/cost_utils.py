from decimal import Decimal, ROUND_HALF_UP


def calculate_estimated_cost(
    input_tokens: int,
    output_tokens: int,
    input_cost_per_million_tokens: float,
    output_cost_per_million_tokens: float,
) -> Decimal:
    """Calculate the estimated request cost using per-million token pricing."""

    input_cost = Decimal(input_tokens) / Decimal(1_000_000) * Decimal(str(input_cost_per_million_tokens))
    output_cost = Decimal(output_tokens) / Decimal(1_000_000) * Decimal(str(output_cost_per_million_tokens))
    total_cost = input_cost + output_cost
    return total_cost.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
