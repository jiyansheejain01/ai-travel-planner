"""
Itinerary Day repository.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.database.models.itinerary_day import ItineraryDay

from .base_repository import BaseRepository


class ItineraryDayRepository(BaseRepository[ItineraryDay]):
    """
    Repository for Itinerary Day operations.
    """

    def __init__(self, db: Session) -> None:
        super().__init__(
            db=db,
            model=ItineraryDay,
        )

    def get_by_id(
        self,
        day_id: UUID,
    ) -> ItineraryDay | None:
        """
        Retrieve an itinerary day by ID.
        """

        stmt = (
            select(self.model)
            .where(self.model.id == day_id)
        )

        return self.db.scalar(stmt)

    def get_by_itinerary(
        self,
        itinerary_id: UUID,
    ) -> list[ItineraryDay]:
        """
        Retrieve all days for an itinerary.
        """

        stmt = (
            select(ItineraryDay)
            .where(
                ItineraryDay.itinerary_id == itinerary_id,
            )
            .order_by(ItineraryDay.day_number)
        )

        return list(
            self.db.scalars(stmt).all()
        )

    def get_by_id_and_itinerary(
        self,
        day_id: UUID,
        itinerary_id: UUID,
    ) -> ItineraryDay | None:
        """
        Retrieve an itinerary day only if it belongs to
        the specified itinerary.
        """

        stmt = (
            select(ItineraryDay)
            .where(
                ItineraryDay.id == day_id,
                ItineraryDay.itinerary_id == itinerary_id,
            )
        )

        return self.db.scalar(stmt)

    def update(
        self,
        day: ItineraryDay,
    ) -> ItineraryDay:
        """
        Update an itinerary day.
        """

        self.db.commit()
        self.db.refresh(day)

        return day

    def delete(
        self,
        day: ItineraryDay,
    ) -> None:
        """
        Delete an itinerary day.
        """

        self.db.delete(day)
        self.db.commit()