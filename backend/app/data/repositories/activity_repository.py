"""
Activity repository.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.database.models.activity import Activity
from app.data.database.models.itinerary import Itinerary
from app.data.database.models.itinerary_day import ItineraryDay
from app.data.database.models.trip import Trip

from .base_repository import BaseRepository


class ActivityRepository(BaseRepository[Activity]):
    """
    Repository for Activity operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(
            db=db,
            model=Activity,
        )

    def get_by_id(
        self,
        activity_id: UUID,
    ) -> Activity | None:
        """
        Retrieve an activity by ID.
        """

        stmt = (
            select(self.model)
            .where(self.model.id == activity_id)
        )

        return self.db.scalar(stmt)

    def get_by_itinerary_day(
        self,
        itinerary_day_id: UUID,
    ) -> list[Activity]:
        """
        Retrieve all activities belonging to an itinerary day.
        """

        stmt = (
            select(Activity)
            .where(
                Activity.itinerary_day_id == itinerary_day_id,
            )
            .order_by(Activity.display_order)
        )

        return list(
            self.db.scalars(stmt).all()
        )

    def get_by_id_and_user(
        self,
        activity_id: UUID,
        user_id: UUID,
    ) -> Activity | None:
        """
        Retrieve an activity only if it belongs
        to the specified user.
        """

        stmt = (
            select(Activity)
            .join(Activity.itinerary_day)
            .join(ItineraryDay.itinerary)
            .join(Itinerary.trip)
            .where(
                Activity.id == activity_id,
                Trip.user_id == user_id,
            )
        )

        return self.db.scalar(stmt)

    def update(
        self,
        activity: Activity,
    ) -> Activity:
        """
        Update an activity.
        """

        self.db.commit()
        self.db.refresh(activity)

        return activity

    def delete(
        self,
        activity: Activity,
    ) -> None:
        """
        Delete an activity.
        """

        self.db.delete(activity)
        self.db.commit()