"""
Itinerary routes.
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.data.database.models.user import User
from app.data.repositories.itinerary_repository import ItineraryRepository
from app.schemas.itinerary import ItineraryResponse
from app.services.itinerary_service import ItineraryService

router = APIRouter(
    prefix="/itineraries",
    tags=["Itineraries"],
)


@router.get(
    "/{trip_id}",
    response_model=ItineraryResponse,
)
def get_itinerary(
    trip_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ItineraryResponse:
    """
    Retrieve the itinerary for a trip.
    """

    repository = ItineraryRepository(db)
    service = ItineraryService(repository)

    itinerary = service.get_itinerary(
    trip_id=trip_id,
    user_id=current_user.id,
    )

    return ItineraryResponse.model_validate(itinerary)