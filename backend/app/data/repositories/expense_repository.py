"""
Expense repository.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.database.models.expense import Expense
from app.data.database.models.trip import Trip

from .base_repository import BaseRepository


class ExpenseRepository(BaseRepository[Expense]):
    """
    Repository for Expense operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(
            db=db,
            model=Expense,
        )

    def get_by_id(
        self,
        expense_id: UUID,
    ) -> Expense | None:
        """
        Retrieve an expense by ID.
        """

        stmt = (
            select(self.model)
            .where(self.model.id == expense_id)
        )

        return self.db.scalar(stmt)

    def get_by_trip_id(
        self,
        trip_id: UUID,
    ) -> list[Expense]:
        """
        Retrieve all expenses for a trip.
        """

        stmt = (
            select(Expense)
            .where(
                Expense.trip_id == trip_id,
            )
            .order_by(
                Expense.expense_date.desc(),
            )
        )

        return list(self.db.scalars(stmt).all())

    def get_by_id_and_user(
        self,
        expense_id: UUID,
        user_id: UUID,
    ) -> Expense | None:
        """
        Retrieve an expense only if it belongs
        to the specified user.
        """

        stmt = (
            select(Expense)
            .join(Expense.trip)
            .where(
                Expense.id == expense_id,
                Trip.user_id == user_id,
            )
        )

        return self.db.scalar(stmt)

    def update(
        self,
        expense: Expense,
    ) -> Expense:
        """
        Update an expense.
        """

        self.db.commit()
        self.db.refresh(expense)

        return expense

    def delete(
        self,
        expense: Expense,
    ) -> None:
        """
        Delete an expense.
        """

        self.db.delete(expense)
        self.db.commit()