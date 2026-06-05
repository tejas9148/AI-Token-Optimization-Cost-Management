from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256

from redis import Redis
from redis.exceptions import RedisError

from app.config.settings import Settings


class CacheServiceError(Exception):
    """Base exception for cache service failures."""


class CacheUnavailableError(CacheServiceError):
    """Raised when Redis cannot be reached or used safely."""


@dataclass(slots=True)
class CacheService:
    """Redis-backed cache for prompt to response lookups."""

    settings: Settings
    _client: Redis | None = field(default=None, init=False, repr=False)

    def _get_client(self) -> Redis | None:
        if not self.settings.redis_url.strip():
            return None

        if self._client is None:
            self._client = Redis.from_url(self.settings.redis_url, decode_responses=True)

        return self._client

    def _build_cache_key(self, prompt: str) -> str:
        normalized_prompt = " ".join(prompt.strip().split())
        prompt_hash = sha256(normalized_prompt.encode("utf-8")).hexdigest()
        return f"tokenwise:prompt-response:{self.settings.gemini_model}:{prompt_hash}"

    def get_cached_response(self, prompt: str) -> str | None:
        client = self._get_client()
        if client is None:
            return None

        try:
            cached_response = client.get(self._build_cache_key(prompt))
        except RedisError as exc:  # pragma: no cover - defensive upstream mapping
            raise CacheUnavailableError("Redis is unavailable.") from exc

        if cached_response is None:
            return None

        return cached_response

    def store_response(self, prompt: str, response: str) -> None:
        client = self._get_client()
        if client is None:
            return

        try:
            client.setex(
                self._build_cache_key(prompt),
                self.settings.cache_ttl_seconds,
                response,
            )
        except RedisError as exc:  # pragma: no cover - defensive upstream mapping
            raise CacheUnavailableError("Redis is unavailable.") from exc

    def is_available(self) -> bool:
        client = self._get_client()
        if client is None:
            return False

        try:
            return bool(client.ping())
        except RedisError:
            return False