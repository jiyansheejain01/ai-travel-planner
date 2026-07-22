from pydantic import BaseModel, Field


class TripIntent(BaseModel):
    """
    Structured output from the Planner Agent.
    """

    destination: str | None = None

    start_date: str | None = None

    end_date: str | None = None

    duration_days: int | None = None

    travelers: int = 1

    budget: str | None = None

    trip_type: str | None = Field(
        default=None,
        description=(
            "Purpose of the request such as planning, budget, sightseeing, flights, hotels or itinerary."
        ),
    )

    interests: list[str] = Field(default_factory=list)

    follow_up_questions: list[str] = Field(default_factory=list)