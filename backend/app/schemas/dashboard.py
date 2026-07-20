"""
Dashboard schemas.
"""

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class BudgetSummary(BaseModel):
    """
    Budget summary.
    """

    total_budget: Decimal

    spent_budget: Decimal

    remaining_budget: Decimal

    currency: str


class ExpenseCategorySummary(BaseModel):
    """
    Expense totals by category.
    """

    accommodation: Decimal = Decimal("0")

    transport: Decimal = Decimal("0")

    food: Decimal = Decimal("0")

    activities: Decimal = Decimal("0")

    shopping: Decimal = Decimal("0")

    misc: Decimal = Decimal("0")


class ExpenseSummary(BaseModel):
    """
    Expense summary.
    """

    total_expenses: int

    total_amount: Decimal

    by_category: ExpenseCategorySummary


class ItinerarySummary(BaseModel):
    """
    Itinerary summary.
    """

    total_days: int

    total_activities: int


class DashboardResponse(BaseModel):
    """
    Dashboard response.
    """

    trip_id: UUID

    trip_title: str

    budget: BudgetSummary

    expenses: ExpenseSummary

    itinerary: ItinerarySummary