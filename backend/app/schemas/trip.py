"""
Trip schemas.
"""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.data.database.models.enums import TripStatus


class TripCreateRequest(BaseModel):
    """
    Request body for creating a trip.
    """

    title: str = Field(min_length=1, max_length=200)

    primary_destination: str = Field(min_length=1, max_length=200)

    start_date: date

    end_date: date

    budget: Decimal = Field(gt=0)

    currency: str = Field(min_length=3, max_length=3)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date > self.end_date:
            raise ValueError("start_date must be before or equal to end_date")
        return self

class TripUpdateRequest(BaseModel):
    """
    Request body for updating a trip.
    """

    title: str | None = Field(default=None, min_length=1, max_length=200)

    primary_destination: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    start_date: date | None = None

    end_date: date | None = None

    budget: Decimal | None = Field(default=None, gt=0)

    currency: str | None = Field(default=None, min_length=3, max_length=3)

    status: TripStatus | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if (
            self.start_date is not None
            and self.end_date is not None
            and self.start_date > self.end_date
        ):
            raise ValueError("start_date must be before or equal to end_date")

        return self

class TripResponse(BaseModel):
    """
    Trip response.
    """

    id: UUID

    user_id: UUID

    title: str

    primary_destination: str

    start_date: date

    end_date: date

    budget: Decimal

    currency: str

    status: TripStatus

    planning_context: dict

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )