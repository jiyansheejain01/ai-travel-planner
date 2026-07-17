"""
Itinerary schemas.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ItineraryCreateRequest(BaseModel):
    """
    Request schema for creating an itinerary.
    """

    pass


class ItineraryResponse(BaseModel):
    """
    Response schema for an itinerary.
    """

    id: UUID
    trip_id: UUID
    generated_by_ai: bool
    version: int
    last_generated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)