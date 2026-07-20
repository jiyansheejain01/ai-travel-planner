from fastapi import FastAPI

from app.core.config import settings
from app.core.exceptions.handlers import register_exception_handlers
from app.core.logging import logger
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.trip import router as trip_router
from app.api.v1.routes.itinerary import router as itinerary_router
from app.api.v1.routes.itinerary_day import router as itinerary_day_router
from app.api.v1.routes.activity import router as activity_router
from app.api.v1.routes.budget import router as budget_router
from app.api.v1.routes.expense import router as expense_router
from app.api.v1.routes.dashboard import router as dashboard_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

register_exception_handlers(app)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(trip_router)
app.include_router(itinerary_router)
app.include_router(itinerary_day_router)
app.include_router(activity_router)
app.include_router(budget_router)
app.include_router(expense_router)
app.include_router(dashboard_router)

logger.info("AI Travel Planner backend started successfully.")