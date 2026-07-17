"""
Itinerary service.

Contains itinerary business logic.
"""

from uuid import UUID

from app.data.database.models.itinerary import Itinerary
from app.data.repositories.itinerary_repository import ItineraryRepository
from app.core.exceptions.trip import TripNotFoundException

class ItineraryService:
    """
    Itinerary business logic.
    """

    def __init__(
        self,
        repository: ItineraryRepository,
    ) -> None:
        self.repository = repository

    def create_itinerary(
        self,
        trip_id: UUID,
    ) -> Itinerary:
        """
        Create an itinerary for a trip.
        """

        itinerary = Itinerary(
            trip_id=trip_id,
        )

        return self.repository.create(itinerary)

    def get_itinerary(
    self,
    trip_id: UUID,
    user_id: UUID,
) -> Itinerary:
        """
        Retrieve the itinerary for a user's trip.
        """

        itinerary = self.repository.get_by_trip_and_user(
            trip_id,
            user_id,
        )

        if itinerary is None:
            raise TripNotFoundException()

        return itinerary