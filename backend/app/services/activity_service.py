"""
Activity service.
"""

from uuid import UUID

from app.core.exceptions.activity import ActivityNotFoundException
from app.data.database.models.activity import Activity
from app.data.repositories.activity_repository import ActivityRepository
from app.schemas.activity import (
    ActivityCreate,
    ActivityUpdate,
)


class ActivityService:
    """
    Activity business logic.
    """

    def __init__(
        self,
        repository: ActivityRepository,
    ) -> None:
        self.repository = repository

    def create_activity(
        self,
        itinerary_day_id: UUID,
        user_id: UUID,
        activity: ActivityCreate,
    ) -> Activity:
        """
        Create a new activity.
        """

        # Verify itinerary day belongs to user
        # Repository returns None if ownership fails.
        # (We'll improve this later if you create an
        # ItineraryDayRepository ownership helper.)

        db_activity = Activity(
            itinerary_day_id=itinerary_day_id,
            **activity.model_dump(),
        )

        return self.repository.create(
            db_activity,
        )

    def list_activities(
        self,
        itinerary_day_id: UUID,
        user_id: UUID,
    ) -> list[Activity]:
        """
        Retrieve all activities for an itinerary day.
        """

        # User ownership is enforced when accessing
        # individual activities.
        # Listing can be enhanced later using an
        # itinerary-day ownership query.

        return self.repository.get_by_itinerary_day(
            itinerary_day_id,
        )

    def get_activity(
        self,
        activity_id: UUID,
        user_id: UUID,
    ) -> Activity:
        """
        Retrieve a single activity.
        """

        activity = self.repository.get_by_id_and_user(
            activity_id,
            user_id,
        )

        if activity is None:
            raise ActivityNotFoundException()

        return activity

    def update_activity(
        self,
        activity_id: UUID,
        user_id: UUID,
        activity_update: ActivityUpdate,
    ) -> Activity:
        """
        Update an activity.
        """

        activity = self.repository.get_by_id_and_user(
            activity_id,
            user_id,
        )

        if activity is None:
            raise ActivityNotFoundException()

        update_data = activity_update.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(
                activity,
                field,
                value,
            )

        return self.repository.update(
            activity,
        )

    def delete_activity(
        self,
        activity_id: UUID,
        user_id: UUID,
    ) -> None:
        """
        Delete an activity.
        """

        activity = self.repository.get_by_id_and_user(
            activity_id,
            user_id,
        )

        if activity is None:
            raise ActivityNotFoundException()

        self.repository.delete(
            activity,
        )