from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from datetime import datetime
from app.backend.api.v1.api import api_router
from app.backend.core.config import settings
from app.backend.schemas.common import HealthResponse

app = FastAPI(
    title="Scene API",
    description="Production-ready social app for Pakistan",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health():
    """Health check endpoint."""
    return HealthResponse(status="ok", timestamp=datetime.utcnow(), version="0.1.0")


app.include_router(api_router, prefix="/api/v1")