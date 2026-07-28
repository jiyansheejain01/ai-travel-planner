from pydantic import BaseModel, Field


class ItineraryItem(BaseModel):
    """
    Represents a single activity in the itinerary.
    """

    time: str = Field(
        ...,
        description="Suggested time for the activity.",
    )

    title: str = Field(
        ...,
        description="Short title of the activity.",
    )

    description: str = Field(
        ...,
        description="Brief explanation of the activity.",
    )

    location: str | None = Field(
        default=None,
        description="Location where the activity takes place.",
    )