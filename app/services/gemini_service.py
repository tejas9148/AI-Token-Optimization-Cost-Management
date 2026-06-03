from __future__ import annotations

from dataclasses import dataclass, field

from google import genai

from app.config.settings import Settings


class GeminiServiceError(Exception):
    """Base exception for Gemini service failures."""


class InvalidGeminiApiKeyError(GeminiServiceError):
    """Raised when the Gemini API key is missing or rejected."""


class GeminiNetworkError(GeminiServiceError):
    """Raised when the Gemini API cannot be reached reliably."""


class GeminiApiError(GeminiServiceError):
    """Raised when Gemini returns an application-level error."""


class GeminiQuotaError(GeminiServiceError):
    """Raised when Gemini quota or billing limits block the request."""


@dataclass(slots=True)
class GeminiService:
    """Dedicated service layer for all Gemini API communication."""

    settings: Settings
    _client: genai.Client = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Create a Gemini client using the configured API key."""

        if not self.settings.gemini_api_key.strip():
            raise InvalidGeminiApiKeyError("Gemini API key is missing.")

        self._client = genai.Client(api_key=self.settings.gemini_api_key)

    def generate_response(self, prompt: str) -> str:
        """Send a prompt to Gemini and return the generated text."""

        try:
            response = self._client.models.generate_content(
                model=self.settings.gemini_model,
                contents=prompt,
            )
            text = getattr(response, "text", None)
            if not text:
                raise GeminiApiError("Gemini returned an empty response.")
            return text.strip()
        except InvalidGeminiApiKeyError:
            raise
        except Exception as exc:  # pragma: no cover - defensive upstream mapping
            error_message = str(exc).lower()
            if "quota" in error_message or "resource_exhausted" in error_message or "429" in error_message:
                raise GeminiQuotaError(
                    "Gemini quota is exhausted or billing is not enabled for this project."
                ) from exc
            if "api key" in error_message or "unauthorized" in error_message or "401" in error_message:
                raise InvalidGeminiApiKeyError("Gemini API key was rejected.") from exc
            if "timeout" in error_message or "network" in error_message or "connection" in error_message:
                raise GeminiNetworkError("A network error occurred while calling Gemini.") from exc
            raise GeminiApiError("Gemini API returned an unexpected error.") from exc
