"""
Itinerary repository.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.database.models.itinerary import Itinerary
from app.data.database.models.trip import Trip

from .base_repository import BaseRepository


class ItineraryRepository(BaseRepository[Itinerary]):
    """
    Repository for itinerary operations.
    """

    def __init__(self, db: Session) -> None:
        super().__init__(
            db=db,
            model=Itinerary,
        )

    def get_by_trip_and_user(
        self,
        trip_id: UUID,
        user_id: UUID,
    ) -> Itinerary | None:
        """
        Retrieve an itinerary only if the trip belongs to the user.
        """

        stmt = (
            select(Itinerary)
            .join(Trip)
            .where(
                Itinerary.trip_id == trip_id,
                Trip.user_id == user_id,
            )
        )

        return self.db.scalar(stmt)