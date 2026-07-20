"""
Expense service.

Contains expense business logic.
"""

from uuid import UUID

from app.core.exceptions.expense import ExpenseNotFoundException
from app.core.exceptions.trip import TripNotFoundException
from app.data.database.models.expense import Expense
from app.data.repositories.expense_repository import ExpenseRepository
from app.data.repositories.trip_repository import TripRepository
from app.schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
)


class ExpenseService:
    """
    Expense business logic.
    """

    def __init__(
        self,
        expense_repository: ExpenseRepository,
        trip_repository: TripRepository,
    ) -> None:
        self.expense_repository = expense_repository
        self.trip_repository = trip_repository

    def create_expense(
        self,
        trip_id: UUID,
        user_id: UUID,
        request: ExpenseCreate,
    ) -> Expense:
        """
        Create an expense for a trip.
        """

        trip = self.trip_repository.get_by_id_and_user(
            trip_id,
            user_id,
        )

        if trip is None:
            raise TripNotFoundException()

        expense = Expense(
            trip_id=trip_id,
            **request.model_dump(),
        )

        return self.expense_repository.create(
            expense,
        )

    def get_expenses(
        self,
        trip_id: UUID,
        user_id: UUID,
    ) -> list[Expense]:
        """
        Retrieve all expenses for a trip.
        """

        trip = self.trip_repository.get_by_id_and_user(
            trip_id,
            user_id,
        )

        if trip is None:
            raise TripNotFoundException()

        return self.expense_repository.get_by_trip_id(
            trip_id,
        )

    def get_expense(
        self,
        expense_id: UUID,
        user_id: UUID,
    ) -> Expense:
        """
        Retrieve an expense.
        """

        expense = self.expense_repository.get_by_id_and_user(
            expense_id,
            user_id,
        )

        if expense is None:
            raise ExpenseNotFoundException()

        return expense

    def update_expense(
        self,
        expense_id: UUID,
        user_id: UUID,
        request: ExpenseUpdate,
    ) -> Expense:
        """
        Update an expense.
        """

        expense = self.expense_repository.get_by_id_and_user(
            expense_id,
            user_id,
        )

        if expense is None:
            raise ExpenseNotFoundException()

        update_data = request.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(
                expense,
                field,
                value,
            )

        return self.expense_repository.update(
            expense,
        )

    def delete_expense(
        self,
        expense_id: UUID,
        user_id: UUID,
    ) -> None:
        """
        Delete an expense.
        """

        expense = self.expense_repository.get_by_id_and_user(
            expense_id,
            user_id,
        )

        if expense is None:
            raise ExpenseNotFoundException()

        self.expense_repository.delete(
            expense,
        )