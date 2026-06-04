from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.config.settings import Settings
from app.models.ai_request import AIRequest
from app.repositories.ai_request_repository import create_ai_request
from app.services.gemini_service import GeminiService
from app.utils.cost_utils import calculate_estimated_cost
from app.utils.token_utils import calculate_total_tokens


@dataclass(slots=True)
class AskService:
    """Coordinate Gemini generation, token accounting, cost calculation, and persistence."""

    settings: Settings
    db: Session

    def process_prompt(self, prompt: str) -> AIRequest:
        """Handle a user prompt end-to-end and persist the request record."""

        gemini_service = GeminiService(settings=self.settings)
        response_text = gemini_service.generate_response(prompt)

        input_tokens = gemini_service.count_tokens(prompt)
        output_tokens = gemini_service.count_tokens(response_text)
        total_tokens = calculate_total_tokens(input_tokens, output_tokens)
        estimated_cost = calculate_estimated_cost(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            input_cost_per_million_tokens=self.settings.input_cost_per_million_tokens,
            output_cost_per_million_tokens=self.settings.output_cost_per_million_tokens,
        )

        return create_ai_request(
            self.db,
            prompt=prompt,
            response=response_text,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            estimated_cost=estimated_cost,
        )
