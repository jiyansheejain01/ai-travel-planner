"""
Trip routes.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.data.database.models.user import User
from app.data.repositories.trip_repository import TripRepository
from app.schemas.trip import (
    TripCreateRequest,
    TripResponse,
)
from app.services.trip_service import TripService

router = APIRouter(
    prefix="/trips",
    tags=["Trips"],
)


@router.post(
    "",
    response_model=TripResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_trip(
    request: TripCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TripResponse:
    """
    Create a new trip.
    """

    repository = TripRepository(db)
    service = TripService(repository)

    trip = service.create_trip(
        current_user.id,
        request,
    )

    return TripResponse.model_validate(trip)


@router.get(
    "",
    response_model=list[TripResponse],
)
def list_trips(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TripResponse]:
    """
    List all trips for the current user.
    """

    repository = TripRepository(db)
    service = TripService(repository)

    trips = service.list_trips(current_user.id)

    return [
        TripResponse.model_validate(trip)
        for trip in trips
    ]