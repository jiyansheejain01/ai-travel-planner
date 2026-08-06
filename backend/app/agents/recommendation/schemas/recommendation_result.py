from pydantic import BaseModel, Field


class RecommendationItem(BaseModel):
    """
    A single personalized recommendation for the traveler.
    """

    name: str = Field(
        ...,
        description="Name of the place, experience, or activity being recommended.",
    )

    category: str = Field(
        ...,
        description=(
            "Human-readable category, e.g. Food & Dining, Culture, Nightlife, "
            "Nature, Shopping, Relaxation, Hidden Gem."
        ),
    )

    reason: str = Field(
        ...,
        description=(
            "Why this is being recommended to this specific traveler -- tied to "
            "their stated interests, the destination's weather, or trip context. "
            "Must be grounded only in the provided context, never invented."
        ),
    )

    matches_interest: str | None = Field(
        default=None,
        description="Which of the traveler's stated interests this recommendation maps to, if any.",
    )

    best_time: str | None = Field(
        default=None,
        description="Best time of day or trip day to experience this, when it can be reasonably inferred.",
    )

    is_hidden_gem: bool = Field(
        default=False,
        description="True if this is a lesser-known pick rather than a major, obvious landmark.",
    )


class RecommendationResult(BaseModel):
    """
    Final set of personalized recommendations produced by the Recommendation Agent.
    """

    destination: str = Field(
        ...,
        description="Trip destination these recommendations are for.",
    )

    summary: str = Field(
        ...,
        description="Short overview of the recommendation strategy for this traveler.",
    )

    recommendations: list[RecommendationItem] = Field(
        default_factory=list,
        description="Curated, personalized list of recommendations.",
    )
