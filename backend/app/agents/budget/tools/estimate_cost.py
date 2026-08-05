from __future__ import annotations


# ---------------------------------------------------------------------------
# Budget allocation configuration
#
# Flight and hotel costs come from real APIs.
#
# Food, local transport, activities and miscellaneous expenses do NOT have
# live pricing yet, so they are estimated from the money remaining after
# flights and hotels.
#
# IMPORTANT:
# These percentages are applied to the REMAINING budget, not the total
# budget. We intentionally do not allocate 100% of the remaining money so
# the user keeps a safety buffer.
# ---------------------------------------------------------------------------

FOOD_SHARE = 0.25
TRANSPORT_SHARE = 0.12
ACTIVITIES_SHARE = 0.25
MISC_SHARE = 0.08


# ---------------------------------------------------------------------------
# Trip type adjustments
# ---------------------------------------------------------------------------

TRIP_TYPE_ACTIVITY_MULTIPLIERS: dict[str, float] = {
    "relaxed": 0.75,
    "budget": 0.65,
    "luxury": 1.30,
    "adventure": 1.20,
    "cultural": 1.10,
    "sightseeing": 1.10,
}


def _activity_multiplier(
    trip_type: str | None,
    interests: list[str] | None,
) -> float:
    """
    Calculate a multiplier for activity spending based on
    trip type and user interests.
    """

    multiplier = 1.0

    if trip_type:
        multiplier = TRIP_TYPE_ACTIVITY_MULTIPLIERS.get(
            trip_type.lower(),
            multiplier,
        )

    if interests:
        # More interests can imply slightly more paid activities.
        # Keep the adjustment small so it does not inflate the budget.
        multiplier += min(len(interests), 4) * 0.03

    return multiplier


def allocate_flexible_budget(
    remaining_budget: float,
    duration_days: int,
    travelers: int,
    trip_type: str | None = None,
    interests: list[str] | None = None,
    activity_count: int | None = None,
) -> dict[str, float]:
    """
    Allocate the remaining trip budget across:

    - food
    - local transport
    - activities
    - miscellaneous expenses

    Flight and hotel costs should already have been deducted before
    calling this function.

    The allocation deliberately uses less than the entire remaining
    budget so the user retains a safety buffer.
    """

    if remaining_budget <= 0:
        return {
            "food": 0.0,
            "transport": 0.0,
            "activities": 0.0,
            "miscellaneous": 0.0,
        }

    # ------------------------------------------------------------------
    # Base allocation
    # ------------------------------------------------------------------

    food = remaining_budget * FOOD_SHARE

    transport = remaining_budget * TRANSPORT_SHARE

    activities = remaining_budget * ACTIVITIES_SHARE

    miscellaneous = remaining_budget * MISC_SHARE

    # ------------------------------------------------------------------
    # Adjust activity spending based on trip type / interests
    # ------------------------------------------------------------------

    activity_multiplier = _activity_multiplier(
        trip_type=trip_type,
        interests=interests,
    )

    activities *= activity_multiplier

    # ------------------------------------------------------------------
    # Adjust based on actual itinerary density
    #
    # ~3 activities per day is considered normal.
    # ------------------------------------------------------------------

    if (
        activity_count is not None
        and activity_count > 0
        and duration_days > 0
    ):

        average_activities_per_day = (
            activity_count / duration_days
        )

        density_factor = max(
            0.7,
            min(
                average_activities_per_day / 3.0,
                1.25,
            ),
        )

        activities *= density_factor

    # ------------------------------------------------------------------
    # IMPORTANT:
    #
    # Activity multipliers could theoretically push the total flexible
    # allocation too high.
    #
    # Never allow flexible spending to consume more than 80% of the
    # remaining budget.
    # ------------------------------------------------------------------

    flexible_total = (
        food
        + transport
        + activities
        + miscellaneous
    )

    maximum_flexible_spend = (
        remaining_budget * 0.80
    )

    if (
        flexible_total > maximum_flexible_spend
        and flexible_total > 0
    ):

        scale = (
            maximum_flexible_spend
            / flexible_total
        )

        food *= scale
        transport *= scale
        activities *= scale
        miscellaneous *= scale

    return {
        "food": round(food, 2),
        "transport": round(transport, 2),
        "activities": round(activities, 2),
        "miscellaneous": round(miscellaneous, 2),
    }


def calculate_remaining_budget(
    total_budget: float,
    flight_cost: float,
    hotel_cost: float,
) -> float:
    """
    Calculate how much money remains after mandatory
    flight and hotel expenses.
    """

    remaining = (
        total_budget
        - flight_cost
        - hotel_cost
    )

    return round(
        max(remaining, 0.0),
        2,
    )


def calculate_total_estimated_cost(
    flight_cost: float,
    hotel_cost: float,
    food_cost: float,
    transport_cost: float,
    activities_cost: float,
    miscellaneous_cost: float,
) -> float:
    """
    Calculate the complete estimated trip cost.
    """

    return round(
        flight_cost
        + hotel_cost
        + food_cost
        + transport_cost
        + activities_cost
        + miscellaneous_cost,
        2,
    )


def calculate_safety_buffer(
    total_budget: float,
    estimated_total: float,
) -> float:
    """
    Money intentionally left unused in the user's budget.
    """

    return round(
        max(
            total_budget - estimated_total,
            0.0,
        ),
        2,
    )