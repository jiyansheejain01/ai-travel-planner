"""
Dashboard service.

Contains dashboard business logic.
"""

from decimal import Decimal
from uuid import UUID

from app.core.exceptions.trip import TripNotFoundException
from app.data.repositories.dashboard_repository import DashboardRepository
from app.data.repositories.trip_repository import TripRepository
from app.schemas.dashboard import (
    BudgetSummary,
    DashboardResponse,
    ExpenseCategorySummary,
    ExpenseSummary,
    ItinerarySummary,
)


class DashboardService:
    """
    Dashboard business logic.
    """

    def __init__(
        self,
        dashboard_repository: DashboardRepository,
        trip_repository: TripRepository,
    ) -> None:
        self.dashboard_repository = dashboard_repository
        self.trip_repository = trip_repository

    def get_dashboard(
        self,
        trip_id: UUID,
        user_id: UUID,
    ) -> DashboardResponse:
        """
        Retrieve dashboard for a trip.
        """

        trip = self.trip_repository.get_by_id_and_user(
            trip_id,
            user_id,
        )

        if trip is None:
            raise TripNotFoundException()

        budget = self.dashboard_repository.get_budget(
            trip_id,
        )

        expense_count, total_amount = (
            self.dashboard_repository.get_total_expenses(
                trip_id,
            )
        )

        category_rows = (
            self.dashboard_repository.get_expenses_by_category(
                trip_id,
            )
        )

        total_days = (
            self.dashboard_repository.get_total_days(
                trip_id,
            )
        )

        total_activities = (
            self.dashboard_repository.get_total_activities(
                trip_id,
            )
        )

        category_summary = ExpenseCategorySummary()

        for category, amount in category_rows:
            setattr(
                category_summary,
                category.value,
                amount,
            )

        total_budget = (
            budget.total_budget
            if budget
            else Decimal("0")
        )

        currency = (
            budget.currency
            if budget
            else trip.currency
        )

        remaining_budget = (
            total_budget - total_amount
        )

        return DashboardResponse(
            trip_id=trip.id,
            trip_title=trip.title,
            budget=BudgetSummary(
                total_budget=total_budget,
                spent_budget=total_amount,
                remaining_budget=remaining_budget,
                currency=currency,
            ),
            expenses=ExpenseSummary(
                total_expenses=expense_count,
                total_amount=total_amount,
                by_category=category_summary,
            ),
            itinerary=ItinerarySummary(
                total_days=total_days,
                total_activities=total_activities,
            ),
        )