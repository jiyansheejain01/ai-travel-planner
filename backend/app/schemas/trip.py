"""
Trip schemas.
"""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.data.database.models.enums import TripStatus


class TripCreateRequest(BaseModel):
    """
    Request body for creating a trip.
    """

    title: str

    primary_destination: str

    start_date: date

    end_date: date

    budget: Decimal

    currency: str

class TripUpdateRequest(BaseModel):
    """
    Request body for updating a trip.
    """

    title: str | None = None

    primary_destination: str | None = None

    start_date: date | None = None

    end_date: date | None = None

    budget: Decimal | None = None

    currency: str | None = None

    status: TripStatus | None = None

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