from __future__ import annotations

import re
from decimal import Decimal, ROUND_HALF_UP


_VERBOSE_PHRASES: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bin order to\b", re.IGNORECASE), "to"),
    (re.compile(r"\bdue to the fact that\b", re.IGNORECASE), "because"),
    (re.compile(r"\bat this point in time\b", re.IGNORECASE), "now"),
    (re.compile(r"\bin the event that\b", re.IGNORECASE), "if"),
    (re.compile(r"\bfor the purpose of\b", re.IGNORECASE), "for"),
    (re.compile(r"\bthe fact that\b", re.IGNORECASE), ""),
    (re.compile(r"\bmake sure to\b", re.IGNORECASE), "ensure"),
    (re.compile(r"\bit is important to\b", re.IGNORECASE), ""),
    (re.compile(r"\bplease note that\b", re.IGNORECASE), ""),
    (re.compile(r"\bi would like you to\b", re.IGNORECASE), ""),
    (re.compile(r"\bif possible\b", re.IGNORECASE), ""),
    (re.compile(r"\bin simple and easy-to-understand terms\b", re.IGNORECASE), "simply"),
    (re.compile(r"\bin a very simple and easy-to-understand way\b", re.IGNORECASE), "simply"),
    (re.compile(r"\bso that i can\b", re.IGNORECASE), "so I can"),
    (re.compile(r"\bvery clearly\b", re.IGNORECASE), "clearly"),
    (re.compile(r"\bpractical examples\b", re.IGNORECASE), "examples"),
    (re.compile(r"\breal-world applications\b", re.IGNORECASE), "real-world uses"),
    (re.compile(r"\bcan you please\b", re.IGNORECASE), ""),
    (re.compile(r"\bcould you please\b", re.IGNORECASE), ""),
    (re.compile(r"\bplease help me\b", re.IGNORECASE), ""),
    (re.compile(r"\bplease explain\b", re.IGNORECASE), "explain"),
)


_FILLER_PREFIXES: tuple[re.Pattern[str], ...] = (
    re.compile(r"^\s*please\s+", re.IGNORECASE),
    re.compile(r"^\s*kindly\s+", re.IGNORECASE),
    re.compile(r"^\s*could you please\s+", re.IGNORECASE),
    re.compile(r"^\s*can you please\s+", re.IGNORECASE),
    re.compile(r"^\s*i would like you to\s+", re.IGNORECASE),
    re.compile(r"^\s*if possible[, ]+", re.IGNORECASE),
)


def _normalize_sentence(sentence: str) -> str:
    return re.sub(r"\s+", " ", sentence).strip().lower()


def optimize_prompt(prompt: str) -> str:
    """Return a conservative, meaning-preserving prompt optimization."""

    text = re.sub(r"\s+", " ", prompt).strip()
    if not text:
        return text

    original_text = text

    for pattern in _FILLER_PREFIXES:
        text = pattern.sub("", text)

    for pattern, replacement in _VERBOSE_PHRASES:
        text = pattern.sub(replacement, text)

    text = re.sub(r"\b(please|kindly)\b[, ]*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(?:very )?(?:clearly|simply|briefly)\b", lambda match: match.group(0).lower(), text, flags=re.IGNORECASE)
    text = re.sub(r"\s+,", ",", text)
    text = re.sub(r",\s*,+", ",", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)

    sentences = re.split(r"(?<=[.!?])\s+", text)
    deduplicated_sentences: list[str] = []
    seen_sentences: set[str] = set()

    for sentence in sentences:
        normalized_sentence = _normalize_sentence(sentence)
        if not normalized_sentence:
            continue
        if normalized_sentence in seen_sentences:
            continue
        seen_sentences.add(normalized_sentence)
        deduplicated_sentences.append(sentence.strip())

    optimized_text = " ".join(deduplicated_sentences).strip()
    optimized_text = re.sub(r"\s+([,.;:!?])", r"\1", optimized_text)
    optimized_text = re.sub(r"\s+", " ", optimized_text).strip()

    if len(optimized_text) >= len(original_text):
        return original_text

    return optimized_text or text


def calculate_token_savings(original_tokens: int, optimized_tokens: int) -> tuple[int, Decimal]:
    """Return token savings and savings percentage for an optimization pass."""

    savings = max(original_tokens - optimized_tokens, 0)
    if original_tokens <= 0:
        return savings, Decimal("0.00")

    savings_percentage = (
        Decimal(savings) / Decimal(original_tokens) * Decimal("100")
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return savings, savings_percentage