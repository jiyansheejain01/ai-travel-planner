"""
Budget service.

Contains budget business logic.
"""

from uuid import UUID

from app.core.exceptions.budget import (
    BudgetAlreadyExistsException,
    BudgetNotFoundException,
)
from app.core.exceptions.trip import TripNotFoundException
from app.data.database.models.budget import Budget
from app.data.repositories.budget_repository import BudgetRepository
from app.data.repositories.trip_repository import TripRepository
from app.schemas.budget import (
    BudgetCreate,
    BudgetUpdate,
)


class BudgetService:
    """
    Budget business logic.
    """

    def __init__(
        self,
        budget_repository: BudgetRepository,
        trip_repository: TripRepository,
    ) -> None:
        self.budget_repository = budget_repository
        self.trip_repository = trip_repository

    def create_budget(
        self,
        trip_id: UUID,
        user_id: UUID,
        request: BudgetCreate,
    ) -> Budget:
        """
        Create a budget for a trip.
        """

        trip = self.trip_repository.get_by_id_and_user(
            trip_id,
            user_id,
        )

        if trip is None:
            raise TripNotFoundException()

        existing_budget = (
            self.budget_repository.get_by_trip_id(
                trip_id,
            )
        )

        if existing_budget is not None:
            raise BudgetAlreadyExistsException()

        budget = Budget(
            trip_id=trip_id,
            **request.model_dump(),
        )

        return self.budget_repository.create(
            budget,
        )

    def get_budget(
        self,
        trip_id: UUID,
        user_id: UUID,
    ) -> Budget:
        """
        Retrieve the budget for a trip.
        """

        trip = self.trip_repository.get_by_id_and_user(
            trip_id,
            user_id,
        )

        if trip is None:
            raise TripNotFoundException()

        budget = self.budget_repository.get_by_trip_id(
            trip_id,
        )

        if budget is None:
            raise BudgetNotFoundException()

        return budget

    def update_budget(
        self,
        budget_id: UUID,
        user_id: UUID,
        request: BudgetUpdate,
    ) -> Budget:
        """
        Update an existing budget.
        """

        budget = self.budget_repository.get_by_id_and_user(
            budget_id,
            user_id,
        )

        if budget is None:
            raise BudgetNotFoundException()

        update_data = request.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(
                budget,
                field,
                value,
            )

        return self.budget_repository.update(
            budget,
        )

    def delete_budget(
        self,
        budget_id: UUID,
        user_id: UUID,
    ) -> None:
        """
        Delete a budget.
        """

        budget = self.budget_repository.get_by_id_and_user(
            budget_id,
            user_id,
        )

        if budget is None:
            raise BudgetNotFoundException()

        self.budget_repository.delete(
            budget,
        )