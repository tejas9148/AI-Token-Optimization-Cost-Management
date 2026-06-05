from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy import Integer, func

from app.models.ai_request import AIRequest


def create_ai_request(
    db: Session,
    *,
    prompt: str,
    response: str,
    input_tokens: int,
    output_tokens: int,
    total_tokens: int,
    estimated_cost,
    served_from_cache: bool,
) -> AIRequest:
    """Persist a Gemini request record and return the stored row."""

    ai_request = AIRequest(
        prompt=prompt,
        response=response,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        estimated_cost=estimated_cost,
        served_from_cache=served_from_cache,
    )
    db.add(ai_request)
    db.commit()
    db.refresh(ai_request)
    return ai_request


def list_ai_requests(db: Session, *, offset: int, limit: int) -> list[AIRequest]:
    """Return a paginated list of AI requests ordered by newest first."""

    return (
        db.query(AIRequest)
        .order_by(AIRequest.created_at.desc(), AIRequest.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def count_ai_requests(db: Session) -> int:
    """Return the total number of AI request records."""

    return db.query(AIRequest).count()


def get_ai_request_analytics(db: Session) -> dict[str, int | Decimal | float]:
    """Return aggregate usage and cost metrics for stored AI requests."""

    total_requests, total_input_tokens, total_output_tokens, total_tokens, total_estimated_cost, total_cache_hits = (
        db.query(
            func.count(AIRequest.id),
            func.coalesce(func.sum(AIRequest.input_tokens), 0),
            func.coalesce(func.sum(AIRequest.output_tokens), 0),
            func.coalesce(func.sum(AIRequest.total_tokens), 0),
            func.coalesce(func.sum(AIRequest.estimated_cost), 0),
            func.coalesce(func.sum(func.cast(AIRequest.served_from_cache, Integer)), 0),
        ).one()
    )

    total_requests_int = int(total_requests)
    total_cache_hits_int = int(total_cache_hits)
    total_cache_misses_int = total_requests_int - total_cache_hits_int
    cache_hit_rate = (total_cache_hits_int / total_requests_int) if total_requests_int else 0.0

    return {
        "total_requests": total_requests_int,
        "total_input_tokens": int(total_input_tokens),
        "total_output_tokens": int(total_output_tokens),
        "total_tokens": int(total_tokens),
        "total_estimated_cost": Decimal(str(total_estimated_cost)),
        "total_cache_hits": total_cache_hits_int,
        "total_cache_misses": total_cache_misses_int,
        "cache_hit_rate": cache_hit_rate,
        "estimated_requests_saved": total_cache_hits_int,
    }
