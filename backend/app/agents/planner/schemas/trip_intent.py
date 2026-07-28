from pydantic import BaseModel, Field


class TripIntent(BaseModel):
    """
    Structured output from the Planner Agent.
    """

    destination: str | None = None

    origin: str | None = None

    origin_airport: str | None = None

    destination_airport: str | None = None

    start_date: str | None = None

    end_date: str | None = None

    duration_days: int | None = None

    travelers: int | None = None

    budget: str | None = None

    trip_type: str | None = Field(
        default=None,
        description=(
            "Purpose of the request such as planning, budget, sightseeing, flights, hotels or itinerary."
        ),
    )

    interests: list[str] | None = None

    follow_up_questions: list[str] | None = None