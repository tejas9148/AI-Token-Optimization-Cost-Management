from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings
from app.routes.chat import router as chat_router
from app.routes.analytics import router as analytics_router
from app.routes.ask import router as ask_router
from app.routes.health import router as health_router
from app.routes.history import router as history_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ask_router)
app.include_router(chat_router)
app.include_router(history_router)
app.include_router(analytics_router)
app.include_router(health_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}