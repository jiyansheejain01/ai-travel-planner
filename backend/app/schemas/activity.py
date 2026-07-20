"""
Activity schemas.
"""

from datetime import datetime, time
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.data.database.models.activity import ActivityCategory


class ActivityCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: str | None = None

    location_name: str | None = Field(
        default=None,
        max_length=255,
    )
    address: str | None = None
    place_id: str | None = Field(
        default=None,
        max_length=255,
    )

    latitude: Decimal | None = None
    longitude: Decimal | None = None

    start_time: time | None = None
    end_time: time | None = None

    display_order: int = Field(
        default=1,
        ge=1,
    )

    category: ActivityCategory = (
        ActivityCategory.OTHER
    )

    estimated_cost: Decimal | None = Field(
        default=None,
        ge=0,
    )

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    notes: str | None = None


class ActivityUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        max_length=255,
    )
    description: str | None = None

    location_name: str | None = Field(
        default=None,
        max_length=255,
    )
    address: str | None = None
    place_id: str | None = Field(
        default=None,
        max_length=255,
    )

    latitude: Decimal | None = None
    longitude: Decimal | None = None

    start_time: time | None = None
    end_time: time | None = None

    display_order: int | None = Field(
        default=None,
        ge=1,
    )

    category: ActivityCategory | None = None

    estimated_cost: Decimal | None = Field(
        default=None,
        ge=0,
    )

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    notes: str | None = None


class ActivityResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    itinerary_day_id: UUID

    title: str
    description: str | None

    location_name: str | None
    address: str | None
    place_id: str | None

    latitude: Decimal | None
    longitude: Decimal | None

    start_time: time | None
    end_time: time | None

    display_order: int

    category: ActivityCategory

    estimated_cost: Decimal | None
    currency: str | None

    notes: str | None

    created_at: datetime
    updated_at: datetime


class ActivityListResponse(BaseModel):
    activities: list[ActivityResponse]