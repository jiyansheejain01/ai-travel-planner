"""
Itinerary Day service.

Contains itinerary day business logic.
"""

from uuid import UUID

from app.core.exceptions.itinerary_day import (
    ItineraryDayNotFoundException,
)
from app.core.exceptions.trip import TripNotFoundException
from app.data.database.models.itinerary_day import ItineraryDay
from app.data.repositories.itinerary_day_repository import (
    ItineraryDayRepository,
)
from app.data.repositories.trip_repository import TripRepository
from app.schemas.itinerary_day import (
    ItineraryDayCreateRequest,
    ItineraryDayUpdateRequest,
)


class ItineraryDayService:
    """
    Itinerary Day business logic.
    """

    def __init__(
        self,
        repository: ItineraryDayRepository,
        trip_repository: TripRepository,
    ) -> None:
        self.repository = repository
        self.trip_repository = trip_repository

    def create_day(
        self,
        trip_id: UUID,
        user_id: UUID,
        request: ItineraryDayCreateRequest,
    ) -> ItineraryDay:
        """
        Create a new itinerary day.
        """

        trip = self.trip_repository.get_by_id_and_user(
            trip_id,
            user_id,
        )

        if trip is None:
            raise TripNotFoundException()

        day = ItineraryDay(
            itinerary_id=trip.itinerary.id,
            day_number=request.day_number,
            date=request.date,
            summary=request.summary,
        )

        return self.repository.create(day)

    def list_days(
    self,
    trip_id: UUID,
    user_id: UUID,
) -> list[ItineraryDay]:

        trip = self.trip_repository.get_by_id_and_user(
            trip_id,
            user_id,
        )

        print("Trip:", trip)

        if trip is None:
            raise TripNotFoundException()

        print("Itinerary:", trip.itinerary)
        print("Itinerary ID:", trip.itinerary.id)

        days = self.repository.get_by_itinerary(
            trip.itinerary.id,
        )

        print("Days:", days)

        return days

    def get_day(
        self,
        trip_id: UUID,
        user_id: UUID,
        day_id: UUID,
    ) -> ItineraryDay:
        """
        Retrieve a single itinerary day.
        """

        trip = self.trip_repository.get_by_id_and_user(
            trip_id,
            user_id,
        )

        if trip is None:
            raise TripNotFoundException()

        day = self.repository.get_by_id_and_itinerary(
            day_id,
            trip.itinerary.id,
        )

        if day is None:
            raise ItineraryDayNotFoundException()

        return day

    def update_day(
        self,
        trip_id: UUID,
        user_id: UUID,
        day_id: UUID,
        request: ItineraryDayUpdateRequest,
    ) -> ItineraryDay:
        """
        Update an itinerary day.
        """

        trip = self.trip_repository.get_by_id_and_user(
            trip_id,
            user_id,
        )

        if trip is None:
            raise TripNotFoundException()

        day = self.repository.get_by_id_and_itinerary(
            day_id,
            trip.itinerary.id,
        )

        if day is None:
            raise ItineraryDayNotFoundException()

        update_data = request.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(day, field, value)

        return self.repository.update(day)

    def delete_day(
        self,
        trip_id: UUID,
        user_id: UUID,
        day_id: UUID,
    ) -> None:
        """
        Delete an itinerary day.
        """

        trip = self.trip_repository.get_by_id_and_user(
            trip_id,
            user_id,
        )

        if trip is None:
            raise TripNotFoundException()

        day = self.repository.get_by_id_and_itinerary(
            day_id,
            trip.itinerary.id,
        )

        if day is None:
            raise ItineraryDayNotFoundException()

        self.repository.delete(day)