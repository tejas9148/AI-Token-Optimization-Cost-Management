from fastapi import FastAPI

from app.config.settings import get_settings
from app.routes.analytics import router as analytics_router
from app.routes.ask import router as ask_router
from app.routes.health import router as health_router
from app.routes.history import router as history_router

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0")

# Register the AI gateway routes.
app.include_router(ask_router)
app.include_router(history_router)
app.include_router(analytics_router)
app.include_router(health_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Simple health endpoint for uptime checks."""

    return {"status": "ok"}
