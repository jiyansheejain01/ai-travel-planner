from pydantic import BaseModel, Field


class BudgetLineItem(BaseModel):
    """
    One category of trip spend, always expressed in the user's currency.
    """

    label: str

    amount: float

    currency: str

    is_estimate: bool = Field(
        default=True,
        description=(
            "False when this figure comes from a real price returned by "
            "another agent (flights/hotels). True when it's a heuristic "
            "estimate (food/transport/activities/miscellaneous) -- see "
            "estimate_cost.py."
        ),
    )

    source_currency: str | None = Field(
        default=None,
        description="Original currency before conversion, if a conversion was applied.",
    )


class BudgetBreakdown(BaseModel):
    flights: BudgetLineItem
    hotels: BudgetLineItem
    food: BudgetLineItem
    transport: BudgetLineItem
    activities: BudgetLineItem
    miscellaneous: BudgetLineItem


class BudgetResult(BaseModel):
    """
    Final output of the Budget Agent.
    """

    currency: str = Field(
        ...,
        description="The user's currency. All amounts in this result are in this currency.",
    )

    total_budget: float | None = Field(
        default=None,
        description="The user's stated total budget, if one was provided.",
    )

    breakdown: BudgetBreakdown

    estimated_total: float = Field(
        ...,
        description="Sum of every category in `breakdown`, including the contingency reserve.",
    )

    remaining_budget: float | None = Field(
        default=None,
        description="total_budget - estimated_total. Null when no total_budget was provided.",
    )

    amount_over_budget: float | None = Field(
        default=None,
        description="Positive amount by which estimated_total exceeds total_budget, when over budget.",
    )

    within_budget: bool | None = Field(
        default=None,
        description="Null when no total_budget was provided to compare against.",
    )

    budget_used_pct: float | None = Field(
        default=None,
        description="estimated_total as a percentage of total_budget.",
    )

    daily_budget: float | None = Field(
        default=None,
        description="Rough spendable amount per day after flights, hotels, and contingency are set aside.",
    )

    contingency_reserve: float = Field(
        default=0.0,
        description="The miscellaneous/contingency amount set aside, same as breakdown.miscellaneous.amount.",
    )

    warnings: list[str] = Field(default_factory=list)

    suggestions: list[str] = Field(
        default_factory=list,
        description="Only populated when within_budget is False.",
    )

    incomplete: bool = Field(
        default=False,
        description=(
            "True when an essential price (flight/hotel) or the trip "
            "duration was unavailable, so estimated_total should be read "
            "as a lower bound rather than an exact figure."
        ),
    )
