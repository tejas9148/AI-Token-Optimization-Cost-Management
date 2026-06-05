from fastapi import APIRouter

from app.config.settings import get_settings
from app.services.cache_service import CacheService

router = APIRouter(prefix="", tags=["Health"])


@router.get("/health/cache")
def cache_health_check() -> dict[str, str | bool]:
    """Report whether the Redis cache backend is reachable."""

    settings = get_settings()
    cache_service = CacheService(settings=settings)
    cache_available = cache_service.is_available()

    return {
        "status": "ok" if cache_available else "degraded",
        "cache_available": cache_available,
    }