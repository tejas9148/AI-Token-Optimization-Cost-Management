from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.repositories.ai_request_repository import count_ai_requests, list_ai_requests
from app.schemas.history import HistoryResponse


@dataclass(slots=True)
class HistoryService:
    """Provide paginated access to stored AI request history."""

    db: Session

    def get_history(self, *, page: int, page_size: int) -> HistoryResponse:
        """Return history records and pagination metadata."""

        offset = (page - 1) * page_size
        total_items = count_ai_requests(self.db)
        items = list_ai_requests(self.db, offset=offset, limit=page_size)
        total_pages = (total_items + page_size - 1) // page_size if total_items else 0

        return HistoryResponse(
            items=items,
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
        )
