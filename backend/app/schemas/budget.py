"""
Budget schemas.
"""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BudgetCreate(BaseModel):
    total_budget: Decimal = Field(gt=0)

    currency: str = Field(
        min_length=3,
        max_length=3,
    )

    accommodation_budget: Decimal | None = Field(
        default=None,
        ge=0,
    )

    transport_budget: Decimal | None = Field(
        default=None,
        ge=0,
    )

    food_budget: Decimal | None = Field(
        default=None,
        ge=0,
    )

    activities_budget: Decimal | None = Field(
        default=None,
        ge=0,
    )

    shopping_budget: Decimal | None = Field(
        default=None,
        ge=0,
    )

    misc_budget: Decimal | None = Field(
        default=None,
        ge=0,
    )

    notes: str | None = None


class BudgetUpdate(BaseModel):
    total_budget: Decimal | None = Field(
        default=None,
        gt=0,
    )

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    accommodation_budget: Decimal | None = Field(
        default=None,
        ge=0,
    )

    transport_budget: Decimal | None = Field(
        default=None,
        ge=0,
    )

    food_budget: Decimal | None = Field(
        default=None,
        ge=0,
    )

    activities_budget: Decimal | None = Field(
        default=None,
        ge=0,
    )

    shopping_budget: Decimal | None = Field(
        default=None,
        ge=0,
    )

    misc_budget: Decimal | None = Field(
        default=None,
        ge=0,
    )

    notes: str | None = None


class BudgetResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    trip_id: UUID

    total_budget: Decimal

    currency: str

    accommodation_budget: Decimal | None

    transport_budget: Decimal | None

    food_budget: Decimal | None

    activities_budget: Decimal | None

    shopping_budget: Decimal | None

    misc_budget: Decimal | None

    notes: str | None

    created_at: datetime

    updated_at: datetime

