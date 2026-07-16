"""
Trip service.

Contains trip business logic.
"""

from app.data.database.models.trip import Trip
from app.data.repositories.trip_repository import TripRepository
from app.schemas.trip import TripCreateRequest


class TripService:
    """
    Trip business logic.
    """

    def __init__(
        self,
        repository: TripRepository,
    ) -> None:
        self.repository = repository

    def create_trip(
        self,
        user_id,
        request: TripCreateRequest,
    ) -> Trip:
        """
        Create a new trip.
        """

        trip = Trip(
            user_id=user_id,
            title=request.title,
            primary_destination=request.primary_destination,
            start_date=request.start_date,
            end_date=request.end_date,
            budget=request.budget,
            currency=request.currency,
        )

        return self.repository.create(trip)

    def list_trips(
        self,
        user_id,
    ) -> list[Trip]:
        """
        Retrieve all trips for a user.
        """

        return self.repository.get_by_user(user_id)