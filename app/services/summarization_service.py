from dataclasses import dataclass

from app.config.settings import Settings
from app.services.gemini_service import GeminiService


@dataclass(slots=True)
class SummarizationService:
    """Generate compact conversation summaries with Gemini."""

    settings: Settings

    def summarize(self, *, existing_summary: str | None, messages_text: str) -> str:
        """Return a concise summary of earlier conversation context."""

        gemini_service = GeminiService(settings=self.settings)
        prompt_parts = [
            "You compress AI chat history into a short context summary for future turns.",
            "Preserve key facts, user goals, project-related context, decisions, constraints, preferences, and unresolved questions.",
            "Remove greetings, repetition, filler, and low-signal details.",
            "Write in plain text with concise bullets or compact paragraphs.",
        ]

        if existing_summary:
            prompt_parts.append("Existing summary:\n" + existing_summary.strip())

        prompt_parts.append("Conversation messages to summarize:\n" + messages_text.strip())
        prompt_parts.append("Return only the updated summary.")
        prompt = "\n\n".join(prompt_parts)

        return gemini_service.generate_response(prompt).strip()