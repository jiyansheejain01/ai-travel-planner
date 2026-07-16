from fastapi import FastAPI

from app.api.v1.routes.health import router as health_router
from app.core.config import settings
from app.core.logging import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.include_router(health_router)

logger.info("AI Travel Planner backend started successfully.")