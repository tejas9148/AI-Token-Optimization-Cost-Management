from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.history import HistoryResponse
from app.services.history_service import HistoryService

router = APIRouter(prefix="", tags=["History"])


@router.get("/history", response_model=HistoryResponse)
def get_history(
    page: int = Query(default=1, ge=1, description="Page number starting from 1"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of records per page"),
    db: Session = Depends(get_db),
) -> HistoryResponse:
    """Return a paginated list of previous AI requests."""

    service = HistoryService(db=db)
    return service.get_history(page=page, page_size=page_size)
