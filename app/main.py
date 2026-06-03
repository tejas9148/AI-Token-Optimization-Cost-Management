from fastapi import FastAPI

from app.config.settings import get_settings
from app.routes.ask import router as ask_router

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0")

# Register the AI gateway routes.
app.include_router(ask_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Simple health endpoint for uptime checks."""

    return {"status": "ok"}
