"""
Trip service.

Contains trip business logic.
"""
from uuid import UUID

from app.core.exceptions.trip import TripNotFoundException
from app.schemas.trip import TripUpdateRequest
from app.data.database.models.trip import Trip
from app.data.repositories.trip_repository import TripRepository
from app.schemas.trip import TripCreateRequest
from uuid import UUID
from app.core.exceptions.trip import TripNotFoundException

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
    
    def get_trip(
    self,
    trip_id: UUID,
    user_id: UUID,
) -> Trip:
        """
        Retrieve a single trip belonging to a user.
        """

        trip = self.repository.get_by_id_and_user(
            trip_id,
            user_id,
        )

        if trip is None:
            raise TripNotFoundException()

        return trip
    
    def update_trip(
    self,
    trip_id: UUID,
    user_id: UUID,
    request: TripUpdateRequest,
) -> Trip:
        """
        Update an existing trip.
        """

        trip = self.repository.get_by_id_and_user(
            trip_id,
            user_id,
        )

        if trip is None:
            raise TripNotFoundException()

        update_data = request.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(trip, field, value)

        return self.repository.update(trip)
    
    def delete_trip(
    self,
    trip_id: UUID,
    user_id: UUID,
) -> None:
        """
        Delete a trip.
        """

        trip = self.repository.get_by_id_and_user(
            trip_id,
            user_id,
        )

        if trip is None:
            raise TripNotFoundException()

        self.repository.delete(trip)