"""
Itinerary Day routes.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.data.database.models.user import User
from app.data.repositories.itinerary_day_repository import (
    ItineraryDayRepository,
)
from app.data.repositories.trip_repository import (
    TripRepository,
)
from app.schemas.itinerary_day import (
    ItineraryDayCreateRequest,
    ItineraryDayResponse,
    ItineraryDayUpdateRequest,
)
from app.services.itinerary_day_service import ItineraryDayService

router = APIRouter(
    prefix="/trips/{trip_id}/days",
    tags=["Itinerary Days"],
)


@router.post(
    "",
    response_model=ItineraryDayResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_day(
    trip_id: UUID,
    request: ItineraryDayCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ItineraryDayResponse:
    """
    Create an itinerary day.
    """

    repository = ItineraryDayRepository(db)
    trip_repository = TripRepository(db)

    service = ItineraryDayService(
        repository,
        trip_repository,
    )

    day = service.create_day(
        trip_id=trip_id,
        user_id=current_user.id,
        request=request,
    )

    return ItineraryDayResponse.model_validate(day)


@router.get(
    "",
    response_model=list[ItineraryDayResponse],
)
def list_days(
    trip_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ItineraryDayResponse]:
    """
    List all itinerary days.
    """

    repository = ItineraryDayRepository(db)
    trip_repository = TripRepository(db)

    service = ItineraryDayService(
        repository,
        trip_repository,
    )

    days = service.list_days(
        trip_id,
        current_user.id,
    )

    return [
        ItineraryDayResponse.model_validate(day)
        for day in days
    ]


@router.get(
    "/{day_id}",
    response_model=ItineraryDayResponse,
)
def get_day(
    trip_id: UUID,
    day_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ItineraryDayResponse:
    """
    Retrieve an itinerary day.
    """

    repository = ItineraryDayRepository(db)
    trip_repository = TripRepository(db)

    service = ItineraryDayService(
        repository,
        trip_repository,
    )

    day = service.get_day(
        trip_id=trip_id,
        user_id=current_user.id,
        day_id=day_id,
    )

    return ItineraryDayResponse.model_validate(day)


@router.put(
    "/{day_id}",
    response_model=ItineraryDayResponse,
)
def update_day(
    trip_id: UUID,
    day_id: UUID,
    request: ItineraryDayUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ItineraryDayResponse:
    """
    Update an itinerary day.
    """

    repository = ItineraryDayRepository(db)
    trip_repository = TripRepository(db)

    service = ItineraryDayService(
        repository,
        trip_repository,
    )

    day = service.update_day(
        trip_id=trip_id,
        user_id=current_user.id,
        day_id=day_id,
        request=request,
    )

    return ItineraryDayResponse.model_validate(day)


@router.delete(
    "/{day_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_day(
    trip_id: UUID,
    day_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete an itinerary day.
    """

    repository = ItineraryDayRepository(db)
    trip_repository = TripRepository(db)

    service = ItineraryDayService(
        repository,
        trip_repository,
    )

    service.delete_day(
        trip_id=trip_id,
        user_id=current_user.id,
        day_id=day_id,
    )