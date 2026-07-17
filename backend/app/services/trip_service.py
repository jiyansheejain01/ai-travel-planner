"""
Trip service.

Contains trip business logic.
"""
from uuid import UUID

from app.core.exceptions.trip import TripNotFoundException
from app.schemas.trip import TripUpdateRequest
from app.data.database.models.trip import Trip
from app.data.database.models.itinerary import Itinerary
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
        user_id: UUID,
        request: TripCreateRequest,
    ) -> Trip:
        """
        Create a new trip.
        """
        if request.start_date > request.end_date:
            raise ValueError("Start date cannot be after end date.")
        if request.budget <= 0:
            raise ValueError("Budget must be greater than zero.")
        trip = Trip(
            user_id=user_id,
            title=request.title,
            primary_destination=request.primary_destination,
            start_date=request.start_date,
            end_date=request.end_date,
            budget=request.budget,
            currency=request.currency,
        )

        trip = self.repository.create(trip)

        trip.itinerary = Itinerary(
            trip_id=trip.id,
        )

        self.repository.db.add(trip.itinerary)
        self.repository.db.commit()
        self.repository.db.refresh(trip.itinerary)

        return trip

    def list_trips(
        self,
        user_id: UUID,
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
        new_start_date = update_data.get("start_date", trip.start_date)
        new_end_date = update_data.get("end_date", trip.end_date)

        if new_start_date > new_end_date:
            raise ValueError("Start date cannot be after end date.")
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