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

    budget_amount: float | None = Field(
        default=None,
        description=(
            "Numeric total budget extracted from the user's message, "
            "e.g. 200000 for '₹2,00,000' or 3000 for '$3000'."
        ),
    )

    budget_currency: str | None = Field(
        default=None,
        description=(
            "ISO 4217 currency code the budget is stated in, e.g. INR, "
            "USD, EUR, GBP, JPY. Inferred from explicit symbols/words in "
            "the user's message (₹/Rs/INR, $/USD, €/EUR, £/GBP, ¥/JPY, "
            "etc.) -- never assumed from nationality or destination."
        ),
    )

    display_currency: str | None = Field(
        default=None,
        description=(
            "ISO 4217 currency code in which trip prices should be displayed, "
            "for example INR, USD, EUR, GBP, JPY. "
            "If the user explicitly requests a currency, use it. "
            "Otherwise, if the user gives a budget with a currency, use that. "
            "Otherwise infer the normal local currency from the trip origin. "
            "For example, Bangalore implies INR, New York implies USD, "
            "London implies GBP, and Tokyo implies JPY. "
            "These are examples only; infer currencies for other locations too. "
            "If it cannot be determined reliably, return null."
        ),
    )

    trip_type: str | None = Field(
        default=None,
        description=(
            "Purpose of the request such as planning, budget, sightseeing, flights, hotels or itinerary."
        ),
    )

    interests: list[str] | None = None

    follow_up_questions: list[str] | None = None