"""
Dashboard routes.
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user,
    get_db,
)
from app.data.database.models.user import User
from app.data.repositories.dashboard_repository import (
    DashboardRepository,
)
from app.data.repositories.trip_repository import (
    TripRepository,
)
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/trips/{trip_id}",
    response_model=DashboardResponse,
)
def get_dashboard(
    trip_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardResponse:
    """
    Retrieve dashboard for a trip.
    """

    dashboard_repository = DashboardRepository(db)
    trip_repository = TripRepository(db)

    service = DashboardService(
        dashboard_repository,
        trip_repository,
    )

    return service.get_dashboard(
        trip_id=trip_id,
        user_id=current_user.id,
    )