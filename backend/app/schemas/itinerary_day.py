from __future__ import annotations

"""
Itinerary Day schemas.
"""

import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ItineraryDayCreateRequest(BaseModel):
    """
    Request body for creating an itinerary day.
    """

    day_number: int = Field(gt=0)

    date: datetime.date

    summary: str | None = Field(
        default=None,
        max_length=500,
    )


class ItineraryDayUpdateRequest(BaseModel):
    """
    Request body for updating an itinerary day.
    """

    date: datetime.date | None = None

    summary: str | None = Field(
        default=None,
        max_length=500,
    )


class ItineraryDayResponse(BaseModel):
    """
    Itinerary day response.
    """

    id: UUID

    itinerary_id: UUID

    day_number: int

    date: datetime.date

    summary: str | None

    created_at: datetime.datetime

    updated_at: datetime.datetime

    model_config = ConfigDict(
        from_attributes=True,
    )