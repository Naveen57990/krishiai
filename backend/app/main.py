from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from prometheus_fastapi_instrumentator import Instrumentator
from loguru import logger
import sys
import os

from app.core.config import settings
from app.core.database import init_db, close_db
from app.api.v1 import router as api_router
from app.middleware.error_handler import global_exception_handler, validation_exception_handler
from app.middleware.logging_middleware import logging_middleware
from app.middleware.rate_limit import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    await init_db()
    logger.info("Database initialized")
    try:
        from app.db.seed_data import seed_database
        await seed_database()
        logger.info("Seed data checked/applied")
    except Exception as e:
        logger.warning(f"Seed data skipped: {e}")
    yield
    await close_db()
    logger.info("Application shutdown")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Agriculture Assistant Platform",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.middleware("http")(logging_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, global_exception_handler)

app.include_router(api_router)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
uploads_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), settings.UPLOAD_DIR)
if os.path.exists(uploads_path) and settings.DEBUG:
    app.mount("/uploads", StaticFiles(directory=uploads_path), name="uploads")

if not settings.DEBUG:
    Instrumentator().instrument(app).expose(app)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
