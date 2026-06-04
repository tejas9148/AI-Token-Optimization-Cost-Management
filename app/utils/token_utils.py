import re


def estimate_token_count(text: str) -> int:
    """Estimate token count from text using a lightweight heuristic fallback."""

    normalized_text = text.strip()
    if not normalized_text:
        return 0

    tokens = re.findall(r"\w+|[^\w\s]", normalized_text)
    return len(tokens)


def count_tokens(text: str) -> int:
    """Backward-compatible alias for the fallback estimator."""

    return estimate_token_count(text)


def calculate_total_tokens(input_tokens: int, output_tokens: int) -> int:
    """Return the total token count for a single request."""

    return input_tokens + output_tokens
