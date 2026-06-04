from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.repositories.ai_request_repository import get_ai_request_analytics
from app.schemas.analytics import AnalyticsResponse


@dataclass(slots=True)
class AnalyticsService:
    """Provide aggregated token and cost analytics."""

    db: Session

    def get_analytics(self) -> AnalyticsResponse:
        """Return total usage metrics across all AI requests."""

        return AnalyticsResponse(**get_ai_request_analytics(self.db))
