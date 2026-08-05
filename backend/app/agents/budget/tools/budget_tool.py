from __future__ import annotations

from datetime import date

from app.agents.budget.schemas.budget_output import (
    BudgetBreakdown,
    BudgetLineItem,
    BudgetResult,
)
from app.agents.budget.tools import estimate_cost
from app.agents.budget.tools.currency_service import CurrencyService
from app.agents.flight.schemas.flight_result import FlightResult
from app.agents.hotel.schemas.hotel_result import HotelResult
from app.agents.itinerary.schemas.itinerary_result import ItineraryResult
from app.agents.planner.schemas.trip_intent import TripIntent


DEFAULT_CURRENCY = "USD"


# ---------------------------------------------------------------------------
# Currency detection
# ---------------------------------------------------------------------------

_CURRENCY_SIGNALS: dict[str, str] = {
    "₹": "INR",
    "rs.": "INR",
    "rs": "INR",
    "inr": "INR",
    "rupee": "INR",

    "$": "USD",
    "usd": "USD",
    "dollar": "USD",

    "€": "EUR",
    "eur": "EUR",
    "euro": "EUR",

    "£": "GBP",
    "gbp": "GBP",
    "pound": "GBP",

    "¥": "JPY",
    "jpy": "JPY",
    "yen": "JPY",

    "aud": "AUD",
    "cad": "CAD",
}


_SUGGESTION_TEXT: dict[str, str] = {
    "flights":
        "Look at a cheaper flight option -- it's one of the largest costs in this plan.",

    "hotels":
        "Choose a more affordable hotel to bring down the biggest fixed cost.",

    "food":
        "Reduce discretionary food spending, e.g. fewer sit-down meals.",

    "transport":
        "Rely more on public transportation instead of taxis/rideshares.",

    "activities":
        "Cut back on paid activities or swap in free/low-cost alternatives.",

    "miscellaneous":
        "Trim the contingency reserve if the rest of the plan is firm.",
}


def _infer_currency_from_text(
    budget_text: str | None,
) -> str | None:

    if not budget_text:
        return None

    lowered = budget_text.lower()

    for signal, code in _CURRENCY_SIGNALS.items():

        if signal in lowered:
            return code

    return None


def _date_diff_days(
    start: str | None,
    end: str | None,
) -> int | None:

    if not start or not end:
        return None

    try:

        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)

    except ValueError:
        return None

    delta = (end_date - start_date).days

    return delta if delta > 0 else None


# ===========================================================================
# Budget Tool
# ===========================================================================


class BudgetTool:
    """
    Computes a complete budget breakdown.

    Real costs:
        - flights
        - hotels

    Estimated / flexible costs:
        - food
        - transport
        - activities
        - miscellaneous

    Flexible expenses are allocated only AFTER real flight and hotel
    expenses have been deducted from the user's total budget.

    This ensures the planner treats the user's budget as a maximum rather
    than estimating arbitrary expenses and checking the budget afterwards.
    """

    def __init__(
        self,
        currency_service: CurrencyService | None = None,
    ) -> None:

        self.currency_service = (
            currency_service
            or CurrencyService()
        )

    # ===================================================================
    # Build Budget
    # ===================================================================

    async def build_budget(
        self,
        trip: TripIntent,
        flight: FlightResult | None,
        hotel: HotelResult | None,
        itinerary: ItineraryResult | None,
    ) -> BudgetResult:

        # ---------------------------------------------------------------
        # User currency
        # ---------------------------------------------------------------

        user_currency = (
            trip.display_currency
            or trip.budget_currency
            or _infer_currency_from_text(trip.budget)
        )

        if not user_currency:
            raise ValueError(
                "Unable to determine the user's display currency."
            )

        user_currency = user_currency.upper()
        print(
            ">>> FLIGHTS ENTERING BUDGET:",
            len(flight.flights) if flight and flight.flights else 0
        )
        await self._convert_flight_options(
            flight,
            user_currency,
        )

        await self._convert_hotel_options(
            hotel,
            user_currency,
        )

        warnings: list[str] = []

        incomplete = False

        # ---------------------------------------------------------------
        # 1. REAL FLIGHT COST
        # ---------------------------------------------------------------
        

        flights_line, flight_missing = (
            await self._flights_line(
                flight,
                user_currency,
            )
        )

        if flight_missing:

            warnings.append(
                "No flight price is available yet -- "
                "flights are excluded from the total."
            )

            incomplete = True

        # ---------------------------------------------------------------
        # 2. REAL HOTEL COST
        # ---------------------------------------------------------------

        hotels_line, hotel_missing = (
            await self._hotels_line(
                hotel,
                trip,
                user_currency,
            )
        )

        if hotel_missing:

            warnings.append(
                "No hotel price is available yet -- "
                "hotels are excluded from the total."
            )

            incomplete = True

        # ---------------------------------------------------------------
        # 3. TRIP DURATION
        # ---------------------------------------------------------------

        duration_days = (
            trip.duration_days
            or _date_diff_days(
                trip.start_date,
                trip.end_date,
            )
            or (
                len(itinerary.days)
                if itinerary and itinerary.days
                else None
            )
        )

        travelers = trip.travelers or 1

        # ---------------------------------------------------------------
        # Activity count from itinerary
        # ---------------------------------------------------------------

        activity_count = (
            sum(
                len(day.activities)
                for day in itinerary.days
            )
            if itinerary and itinerary.days
            else None
        )

        # ---------------------------------------------------------------
        # 4. USER TOTAL BUDGET
        # ---------------------------------------------------------------

        total_budget = trip.budget_amount

        # ---------------------------------------------------------------
        # 5. FIXED COSTS
        # ---------------------------------------------------------------

        fixed_costs = (
            flights_line.amount
            + hotels_line.amount
        )

        # ---------------------------------------------------------------
        # 6. FLEXIBLE BUDGET
        # ---------------------------------------------------------------

        if total_budget is not None:

            remaining_after_fixed = (
                estimate_cost.calculate_remaining_budget(
                    total_budget=total_budget,
                    flight_cost=flights_line.amount,
                    hotel_cost=hotels_line.amount,
                )
            )

        else:

            remaining_after_fixed = 0.0

        # ---------------------------------------------------------------
        # Check whether fixed costs ALONE exceed budget
        # ---------------------------------------------------------------

        fixed_costs_over_budget = (
            total_budget is not None
            and fixed_costs > total_budget
        )

        if fixed_costs_over_budget:

            warnings.append(
                "Flight and hotel costs alone exceed the "
                "user's total budget. A cheaper flight or hotel "
                "is required."
            )

        # ---------------------------------------------------------------
        # 7. ESTIMATE FLEXIBLE COSTS
        # ---------------------------------------------------------------

        if not duration_days:

            warnings.append(
                "Trip duration is unknown -- food, transport, "
                "and activity estimates could not be calculated."
            )

            food_line = self._empty_line(
                "Food",
                user_currency,
            )

            transport_line = self._empty_line(
                "Transport",
                user_currency,
            )

            activities_line = self._empty_line(
                "Activities",
                user_currency,
            )

            misc_line = self._empty_line(
                "Miscellaneous",
                user_currency,
            )

            incomplete = True

        elif total_budget is None:

            # -----------------------------------------------------------
            # Without a user budget we cannot perform budget-aware
            # allocation.
            # -----------------------------------------------------------

            warnings.append(
                "No numeric budget was provided, so flexible "
                "trip expenses cannot be allocated against a "
                "spending limit."
            )

            food_line = self._empty_line(
                "Food",
                user_currency,
            )

            transport_line = self._empty_line(
                "Transport",
                user_currency,
            )

            activities_line = self._empty_line(
                "Activities",
                user_currency,
            )

            misc_line = self._empty_line(
                "Miscellaneous",
                user_currency,
            )

            incomplete = True

        elif remaining_after_fixed <= 0:

            # -----------------------------------------------------------
            # Flight + hotel consumed the whole budget.
            # -----------------------------------------------------------

            food_line = self._empty_line(
                "Food",
                user_currency,
            )

            transport_line = self._empty_line(
                "Transport",
                user_currency,
            )

            activities_line = self._empty_line(
                "Activities",
                user_currency,
            )

            misc_line = self._empty_line(
                "Miscellaneous",
                user_currency,
            )

        else:

            # -----------------------------------------------------------
            # Budget-aware allocation
            # -----------------------------------------------------------

            allocation = (
                estimate_cost.allocate_flexible_budget(
                    remaining_budget=remaining_after_fixed,
                    duration_days=duration_days,
                    travelers=travelers,
                    trip_type=trip.trip_type,
                    interests=trip.interests,
                    activity_count=activity_count,
                )
            )

            food_line = BudgetLineItem(
                label="Food",
                amount=allocation["food"],
                currency=user_currency,
                is_estimate=True,
            )

            transport_line = BudgetLineItem(
                label="Transport",
                amount=allocation["transport"],
                currency=user_currency,
                is_estimate=True,
            )

            activities_line = BudgetLineItem(
                label="Activities",
                amount=allocation["activities"],
                currency=user_currency,
                is_estimate=True,
            )

            misc_line = BudgetLineItem(
                label="Miscellaneous",
                amount=allocation["miscellaneous"],
                currency=user_currency,
                is_estimate=True,
            )

        # ---------------------------------------------------------------
        # 8. BREAKDOWN
        # ---------------------------------------------------------------

        breakdown = BudgetBreakdown(
            flights=flights_line,
            hotels=hotels_line,
            food=food_line,
            transport=transport_line,
            activities=activities_line,
            miscellaneous=misc_line,
        )

        # ---------------------------------------------------------------
        # 9. FINAL ESTIMATED TOTAL
        # ---------------------------------------------------------------

        estimated_total = (
            estimate_cost.calculate_total_estimated_cost(
                flight_cost=flights_line.amount,
                hotel_cost=hotels_line.amount,
                food_cost=food_line.amount,
                transport_cost=transport_line.amount,
                activities_cost=activities_line.amount,
                miscellaneous_cost=misc_line.amount,
            )
        )

        # ---------------------------------------------------------------
        # 10. BUDGET COMPARISON
        # ---------------------------------------------------------------

        remaining_budget = None
        amount_over_budget = None
        within_budget = None
        budget_used_pct = None
        daily_budget = None

        if total_budget is not None:

            remaining_budget = round(
                total_budget - estimated_total,
                2,
            )

            within_budget = (
                remaining_budget >= 0
            )

            if total_budget > 0:

                budget_used_pct = round(
                    (
                        estimated_total
                        / total_budget
                    )
                    * 100,
                    1,
                )

            if not within_budget:

                amount_over_budget = round(
                    -remaining_budget,
                    2,
                )

            # -----------------------------------------------------------
            # Daily discretionary allowance
            # -----------------------------------------------------------

            if duration_days:

                discretionary_spend = (
                    food_line.amount
                    + transport_line.amount
                    + activities_line.amount
                    + misc_line.amount
                )

                daily_budget = round(
                    discretionary_spend
                    / duration_days,
                    2,
                )

        else:

            warnings.append(
                "No numeric budget was provided, so the plan "
                "cannot be checked against a spending limit."
            )

        # ---------------------------------------------------------------
        # 11. SAFETY BUFFER
        # ---------------------------------------------------------------

        safety_buffer = None

        if total_budget is not None:

            safety_buffer = (
                estimate_cost.calculate_safety_buffer(
                    total_budget=total_budget,
                    estimated_total=estimated_total,
                )
            )

        # ---------------------------------------------------------------
        # 12. WARN ABOUT SAFETY BUFFER
        # ---------------------------------------------------------------

        if (
            safety_buffer is not None
            and safety_buffer > 0
            and within_budget
        ):

            warnings.append(
                f"{safety_buffer:.2f} {user_currency} remains "
                "unallocated as a safety buffer."
            )

        # ---------------------------------------------------------------
        # 13. SUGGESTIONS
        # ---------------------------------------------------------------

        suggestions = self._build_suggestions(
            breakdown,
            within_budget,
        )

        # ---------------------------------------------------------------
        # 14. RETURN
        # ---------------------------------------------------------------

        return BudgetResult(
            currency=user_currency,
            total_budget=total_budget,
            breakdown=breakdown,
            estimated_total=estimated_total,
            remaining_budget=remaining_budget,
            amount_over_budget=amount_over_budget,
            within_budget=within_budget,
            budget_used_pct=budget_used_pct,
            daily_budget=daily_budget,
            contingency_reserve=misc_line.amount,
            warnings=warnings,
            suggestions=suggestions,
            incomplete=incomplete,
        )

    # ===================================================================
    # Convert individual flight/hotel options
    # ===================================================================

    async def _convert_flight_options(
        self,
        flight: FlightResult | None,
        user_currency: str,
    ) -> None:
        """
        Add an individual converted price to every flight option.
        """

        if not flight or not flight.flights:
            return

        for option in flight.flights:

            if option.price is None:
                continue

            source_currency = (
                option.currency or DEFAULT_CURRENCY
            ).upper()

            converted = await self.currency_service.convert(
                option.price,
                source_currency,
                user_currency,
            )

            object.__setattr__(
                option,
                "converted_price",
                converted,
            )

            object.__setattr__(
                option,
                "converted_currency",
                user_currency,
            )

    async def _convert_hotel_options(
        self,
        hotel: HotelResult | None,
        user_currency: str,
    ) -> None:
        """
        Add an individual converted price to every hotel option.
        """

        if not hotel or not hotel.hotels:
            return

        for option in hotel.hotels:

            if option.price is None:
                continue

            source_currency = (
                option.currency or DEFAULT_CURRENCY
            ).upper()

            converted = await self.currency_service.convert(
                option.price,
                source_currency,
                user_currency,
            )

            object.__setattr__(
                option,
                "converted_price",
                converted,
            )

            object.__setattr__(
                option,
                "converted_currency",
                user_currency,
            )

    # ===================================================================
    # Flight
    # ===================================================================

    async def _flights_line(
        self,
        flight: FlightResult | None,
        user_currency: str,
    ) -> tuple[BudgetLineItem, bool]:

        if not flight or not flight.flights:

            return (
                self._empty_line(
                    "Flights",
                    user_currency,
                ),
                True,
            )

        cheapest = min(
            flight.flights,
            key=lambda f: f.price,
        )

        source_currency = (
            cheapest.currency
            or DEFAULT_CURRENCY
        ).upper()

        converted = (
            await self.currency_service.convert(
                cheapest.price,
                source_currency,
                user_currency,
            )
        )

        line = BudgetLineItem(
            label="Flights",
            amount=converted,
            currency=user_currency,
            is_estimate=False,
            source_currency=(
                source_currency
                if source_currency != user_currency
                else None
            ),
        )

        return line, False

    # ===================================================================
    # Hotel
    # ===================================================================

    async def _hotels_line(
        self,
        hotel: HotelResult | None,
        trip: TripIntent,
        user_currency: str,
    ) -> tuple[BudgetLineItem, bool]:

        if not hotel or not hotel.hotels:

            return (
                self._empty_line(
                    "Hotels",
                    user_currency,
                ),
                True,
            )

        priced = [
            h
            for h in hotel.hotels
            if h.price is not None
        ]

        if not priced:

            return (
                self._empty_line(
                    "Hotels",
                    user_currency,
                ),
                True,
            )

        cheapest = min(
            priced,
            key=lambda h: h.price,
        )

        # Hotelbeds price is already the total stay price.
        # Do NOT multiply by nights.

        source_currency = (
            cheapest.currency
            or DEFAULT_CURRENCY
        ).upper()

        converted = (
            await self.currency_service.convert(
                cheapest.price,
                source_currency,
                user_currency,
            )
        )

        line = BudgetLineItem(
            label="Hotels",
            amount=converted,
            currency=user_currency,
            is_estimate=False,
            source_currency=(
                source_currency
                if source_currency != user_currency
                else None
            ),
        )

        return line, False

    # ===================================================================
    # Empty line
    # ===================================================================

    def _empty_line(
        self,
        label: str,
        user_currency: str,
    ) -> BudgetLineItem:

        return BudgetLineItem(
            label=label,
            amount=0.0,
            currency=user_currency,
            is_estimate=True,
        )

    # ===================================================================
    # Suggestions
    # ===================================================================

    def _build_suggestions(
        self,
        breakdown: BudgetBreakdown,
        within_budget: bool | None,
    ) -> list[str]:

        if within_budget is not False:
            return []

        ranked = sorted(
            breakdown.model_dump().items(),
            key=lambda item: item[1]["amount"],
            reverse=True,
        )

        return [
            _SUGGESTION_TEXT[name]
            for name, _ in ranked
            if name in _SUGGESTION_TEXT
        ][:3]