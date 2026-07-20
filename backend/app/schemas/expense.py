"""
Expense schemas.
"""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.data.database.models.expense import ExpenseCategory


class ExpenseCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    amount: Decimal = Field(gt=0)

    currency: str = Field(
        min_length=3,
        max_length=3,
    )

    category: ExpenseCategory

    expense_date: date

    notes: str | None = None


class ExpenseUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    amount: Decimal | None = Field(
        default=None,
        gt=0,
    )

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    category: ExpenseCategory | None = None

    expense_date: date | None = None

    notes: str | None = None


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    trip_id: UUID

    title: str

    amount: Decimal

    currency: str

    category: ExpenseCategory

    expense_date: date

    notes: str | None

    created_at: datetime

    updated_at: datetime