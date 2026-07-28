from pydantic import BaseModel, Field

from app.agents.itinerary.schemas.itinerary_item import ItineraryItem


class ItineraryDay(BaseModel):
    """
    Represents one day of the trip.
    """

    day: int = Field(
        ...,
        description="Day number starting from 1.",
    )

    date: str = Field(
        ...,
        description="Date of this itinerary day.",
    )

    summary: str = Field(
        ...,
        description="Short summary of the day.",
    )

    activities: list[ItineraryItem] = Field(
        default_factory=list,
        description="Activities planned for the day.",
    )