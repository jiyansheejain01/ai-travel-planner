"""
Dashboard repository.
"""

from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.data.database.models.activity import Activity
from app.data.database.models.budget import Budget
from app.data.database.models.expense import Expense
from app.data.database.models.itinerary import Itinerary
from app.data.database.models.itinerary_day import ItineraryDay
from app.data.database.models.trip import Trip

from .base_repository import BaseRepository


class DashboardRepository(BaseRepository[Trip]):
    """
    Repository for Dashboard operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(
            db=db,
            model=Trip,
        )

    def get_trip(
        self,
        trip_id: UUID,
    ) -> Trip | None:
        """
        Retrieve a trip by ID.
        """

        stmt = (
            select(Trip)
            .where(
                Trip.id == trip_id,
            )
        )

        return self.db.scalar(stmt)

    def get_budget(
        self,
        trip_id: UUID,
    ) -> Budget | None:
        """
        Retrieve a budget for a trip.
        """

        stmt = (
            select(Budget)
            .where(
                Budget.trip_id == trip_id,
            )
        )

        return self.db.scalar(stmt)

    def get_total_expenses(
        self,
        trip_id: UUID,
    ) -> tuple[int, Decimal]:
        """
        Retrieve total expense count and amount.
        """

        stmt = (
            select(
                func.count(Expense.id),
                func.coalesce(
                    func.sum(Expense.amount),
                    0,
                ),
            )
            .where(
                Expense.trip_id == trip_id,
            )
        )

        return self.db.execute(stmt).one()

    def get_expenses_by_category(
        self,
        trip_id: UUID,
    ):
        """
        Retrieve expense totals grouped by category.
        """

        stmt = (
            select(
                Expense.category,
                func.coalesce(
                    func.sum(Expense.amount),
                    0,
                ),
            )
            .where(
                Expense.trip_id == trip_id,
            )
            .group_by(
                Expense.category,
            )
        )

        return self.db.execute(stmt).all()

    def get_total_days(
        self,
        trip_id: UUID,
    ) -> int:
        """
        Retrieve total itinerary days.
        """

        stmt = (
            select(
                func.count(ItineraryDay.id),
            )
            .join(
                Itinerary,
                Itinerary.id == ItineraryDay.itinerary_id,
            )
            .where(
                Itinerary.trip_id == trip_id,
            )
        )

        return self.db.scalar(stmt) or 0

    def get_total_activities(
        self,
        trip_id: UUID,
    ) -> int:
        """
        Retrieve total activities.
        """

        stmt = (
            select(
                func.count(Activity.id),
            )
            .join(
                ItineraryDay,
                Activity.itinerary_day_id == ItineraryDay.id,
            )
            .join(
                Itinerary,
                ItineraryDay.itinerary_id == Itinerary.id,
            )
            .where(
                Itinerary.trip_id == trip_id,
            )
        )

        return self.db.scalar(stmt) or 0