"""
Budget repository.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.database.models.budget import Budget
from app.data.database.models.trip import Trip

from .base_repository import BaseRepository


class BudgetRepository(BaseRepository[Budget]):
    """
    Repository for Budget operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(
            db=db,
            model=Budget,
        )

    def get_by_id(
        self,
        budget_id: UUID,
    ) -> Budget | None:
        """
        Retrieve a budget by ID.
        """

        stmt = (
            select(self.model)
            .where(self.model.id == budget_id)
        )

        return self.db.scalar(stmt)

    def get_by_trip_id(
        self,
        trip_id: UUID,
    ) -> Budget | None:
        """
        Retrieve the budget for a trip.
        """

        stmt = (
            select(Budget)
            .where(
                Budget.trip_id == trip_id,
            )
        )

        return self.db.scalar(stmt)

    def get_by_id_and_user(
        self,
        budget_id: UUID,
        user_id: UUID,
    ) -> Budget | None:
        """
        Retrieve a budget only if it belongs
        to the specified user.
        """

        stmt = (
            select(Budget)
            .join(Budget.trip)
            .where(
                Budget.id == budget_id,
                Trip.user_id == user_id,
            )
        )

        return self.db.scalar(stmt)

    def update(
        self,
        budget: Budget,
    ) -> Budget:
        """
        Update a budget.
        """

        self.db.commit()
        self.db.refresh(budget)

        return budget

    def delete(
        self,
        budget: Budget,
    ) -> None:
        """
        Delete a budget.
        """

        self.db.delete(budget)
        self.db.commit()