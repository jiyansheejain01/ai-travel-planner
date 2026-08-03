"""
Maps the raw JSON returned by POST /planner/ into the plain dict shapes
that components/dashboard/*.py already expect (build_trip_header,
build_agent_grid, build_itinerary_and_travel, build_budget_and_insights).

Backend response shape (see app/api/v1/routes/planner.py):
    {
        "trip": TripIntent | None,
        "results": { "planner": AgentResult, "weather": AgentResult, ... },
        "planning_time_seconds": float,
        "agents_registered": int,
    }

Only planner, weather, flight, hotel, itinerary currently exist on the
backend (see app/orchestrator/bootstrap.py). Budget, attraction,
restaurant, transport, events and memory agents have code under
app/agents/ but are not registered yet, so this adapter never invents
data for them -- those sections show an honest "not connected yet"
placeholder instead of fabricated numbers.
"""

from __future__ import annotations

from typing import Any

# Order matters: this is the order agent cards render in.
KNOWN_AGENTS = ["planner", "weather", "flight", "hotel", "itinerary"]

FUTURE_AGENTS = [
    "budget agent",
    "attraction agent",
    "restaurant agent",
    "transport agent",
    "events agent",
    "memory agent",
]

WEATHER_KEYWORDS = {
    "rain": "rain",
    "drizzle": "rain",
    "thunder": "rain",
    "snow": "cloud",
    "fog": "cloud",
    "overcast": "cloud",
    "cloud": "cloud",
    "clear": "sun",
}


def _result(results: dict[str, Any], name: str) -> dict | None:
    return results.get(name)


def _fmt_pct(confidence: float | None) -> str:
    if confidence is None:
        return "—"
    return f"{round(confidence * 100)}%"


def _fmt_time(seconds: float | None) -> str:
    if seconds is None:
        return "—"
    return f"{seconds:.1f}s"


def _weather_icon_key(condition: str) -> str:
    condition_lower = (condition or "").lower()
    for keyword, icon_key in WEATHER_KEYWORDS.items():
        if keyword in condition_lower:
            return icon_key
    return "sun"


# ---------------------------------------------------------------------------
# 1. Trip overview + AI planner summary
# ---------------------------------------------------------------------------
def _build_trip(trip_intent: dict | None, results: dict, agents_registered: int,
                 planning_time_seconds: float | None) -> dict:
    trip_intent = trip_intent or {}

    destination = trip_intent.get("destination") or "Destination not set"
    origin = trip_intent.get("origin")
    start_date = trip_intent.get("start_date")
    end_date = trip_intent.get("end_date")
    duration_days = trip_intent.get("duration_days")
    travelers = trip_intent.get("travelers")
    budget = trip_intent.get("budget")
    trip_type = trip_intent.get("trip_type")
    interests = trip_intent.get("interests") or []

    dates = " – ".join(d for d in (start_date, end_date) if d) or "Dates not set"
    duration = f"{duration_days} days" if duration_days else "Duration not set"
    travelers_label = f"{travelers} traveler{'s' if travelers != 1 else ''}" if travelers else "Travelers not set"

    origin_bit = f" from {origin}" if origin else ""
    interests_bit = f", focused on {', '.join(interests[:3])}" if interests else ""
    summary = f"A {duration.lower()} trip to {destination}{origin_bit}{interests_bit}.".replace(
        "not set trip", "trip"
    )

    itinerary_ok = bool(_result(results, "itinerary") and _result(results, "itinerary").get("success"))
    any_ok = any(
        _result(results, name) and _result(results, name).get("success")
        for name in ("weather", "flight", "hotel")
    )
    status = "Complete" if itinerary_ok else ("Partial" if any_ok else "Limited")

    confidences = [
        r.get("confidence", 0.0)
        for r in results.values()
        if r and r.get("success")
    ]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    success_count = sum(1 for r in results.values() if r and r.get("success"))

    return {
        "title": f"{destination} trip",
        "destination": destination,
        "dates": dates,
        "duration": duration,
        "travelers": travelers_label,
        "budget": budget or "No budget set",
        "trip_type": trip_type or "General",
        "interests": interests,
        "summary": summary,
        "planner_status": status,
        "confidence": _fmt_pct(avg_confidence),
        "planning_time": _fmt_time(planning_time_seconds),
        "agents_used": f"{success_count} of {agents_registered}",
    }


# ---------------------------------------------------------------------------
# 2. Agent execution grid
# ---------------------------------------------------------------------------
def _agent_summary(name: str, result: dict | None, trip_intent: dict) -> tuple[str, str]:
    """Returns (status, summary) for one agent card."""

    if result is None:
        # This agent was never scheduled -- explain the specific gap so
        # people understand it's a missing-input issue, not a bug.
        # (see app/orchestrator/orchestrator.py: build_execution_plan)
        if name == "flight":
            missing = [
                label for label, value in (
                    ("an origin city", trip_intent.get("origin")),
                    ("a destination", trip_intent.get("destination")),
                    ("a start date", trip_intent.get("start_date")),
                ) if not value
            ]
            return "queued", f"Skipped — needs {', '.join(missing)}."
        if name == "hotel":
            missing = [
                label for label, value in (
                    ("a destination", trip_intent.get("destination")),
                    ("a start date", trip_intent.get("start_date")),
                    ("an end date", trip_intent.get("end_date")),
                ) if not value
            ]
            return "queued", f"Skipped — needs {', '.join(missing)}."
        if name == "itinerary":
            return "queued", "Skipped — needs weather, flight, and hotel to all run first."
        return "queued", "Skipped — required trip details weren't available."

    if not result.get("success"):
        return "error", result.get("error") or "Agent failed to complete."

    data = result.get("result") or {}

    if name == "planner":
        return "done", "Extracted destination, dates, and traveler details from your request."

    if name == "weather":
        condition = data.get("condition", "")
        temp = data.get("temperature_c")
        temp_bit = f", {temp:.0f}°C" if isinstance(temp, (int, float)) else ""
        return "done", f"{condition}{temp_bit}. {data.get('travel_advice', '')}".strip()

    if name == "flight":
        count = len(data.get("flights") or [])
        if count == 0:
            return "error", "No flight offers found for these dates."
        return "done", f"Found {count} flight option{'s' if count != 1 else ''}."

    if name == "hotel":
        count = len(data.get("hotels") or [])
        if count == 0:
            return "error", "No hotels found for this destination."
        return "done", f"Shortlisted {count} stay{'s' if count != 1 else ''}."

    if name == "itinerary":
        count = len(data.get("days") or [])
        return "done", f"Planned {count} day{'s' if count != 1 else ''} of activities."

    return "done", "Completed."


def _build_agents(results: dict, trip_intent: dict) -> list[dict]:
    agents = []
    for name in KNOWN_AGENTS:
        result = _result(results, name)
        status, summary = _agent_summary(name, result, trip_intent)
        agents.append({
            "name": f"{name.capitalize()} agent",
            "status": status,
            "time": _fmt_time(result.get("execution_time")) if result else "—",
            "confidence": _fmt_pct(result.get("confidence")) if result else "—",
            "summary": summary,
        })
    return agents


# ---------------------------------------------------------------------------
# 3. Daily itinerary + flight / hotel + weather
# ---------------------------------------------------------------------------
def _build_days(itinerary_result: dict | None) -> dict:
    if not itinerary_result or not itinerary_result.get("success"):
        return {
            "Day 1": [{
                "title": "Itinerary not yet generated",
                "time": "—",
                "duration": "—",
                "setting": "—",
                "cost": "—",
                "note": "The itinerary agent needs weather, flight, and hotel results before it can run.",
            }]
        }

    data = itinerary_result.get("result") or {}
    days = data.get("days") or []

    if not days:
        return {
            "Day 1": [{
                "title": "No activities generated",
                "time": "—", "duration": "—", "setting": "—", "cost": "—",
                "note": "",
            }]
        }

    result = {}
    for day in days:
        key = f"Day {day.get('day')}"
        items = []
        for activity in day.get("activities") or []:
            note_parts = [p for p in (activity.get("location"), activity.get("description")) if p]
            items.append({
                "title": activity.get("title", "Untitled activity"),
                "time": activity.get("time", "—"),
                "duration": "—",   # not tracked by the itinerary schema yet
                "setting": "—",    # not tracked by the itinerary schema yet
                "cost": "—",       # not tracked by the itinerary schema yet
                "note": " — ".join(note_parts),
            })
        result[key] = items
    return result


def _build_flight(flight_result: dict | None) -> dict:
    if not flight_result or not flight_result.get("success"):
        return {
            "airline_route": "Flight search unavailable",
            "times": flight_result.get("error") if flight_result else "Origin and destination are required.",
            "price": "—",
            "alt_count": 0,
        }

    data = flight_result.get("result") or {}
    flights = data.get("flights") or []

    if not flights:
        return {
            "airline_route": "No flights found",
            "times": f"{data.get('origin', '?')} → {data.get('destination', '?')}",
            "price": "—",
            "alt_count": 0,
        }

    best = min(flights, key=lambda f: f.get("price", float("inf")))

    return {
        "airline_route": f"{best.get('airline', '—')} · {best.get('departure_airport', '?')} → {best.get('arrival_airport', '?')}",
        "times": f"{best.get('departure_time', '—')} → {best.get('arrival_time', '—')} · {best.get('duration', '—')}",
        "price": f"{best.get('price', 0):.0f} {best.get('currency', '')}".strip(),
        "alt_count": max(len(flights) - 1, 0),
    }


def _build_hotel(hotel_result: dict | None) -> dict:
    if not hotel_result or not hotel_result.get("success"):
        return {
            "name": "Hotel search unavailable",
            "rating_distance": hotel_result.get("error") if hotel_result else "Destination is required.",
            "price": "—",
            "alt_count": 0,
        }

    data = hotel_result.get("result") or {}
    hotels = data.get("hotels") or []

    if not hotels:
        return {
            "name": "No hotels found",
            "rating_distance": data.get("city", "—"),
            "price": "—",
            "alt_count": 0,
        }

    # rating/price aren't populated by the current Geoapify integration —
    # fall back to the first result rather than sorting by an absent field.
    best = hotels[0]
    rating = best.get("rating")
    rating_bit = f"{rating} rating · " if rating is not None else ""

    price = best.get("price")
    currency = best.get("currency") or ""
    price_label = f"{price:.0f} {currency} / night" if price is not None else "Price unavailable"

    return {
        "name": best.get("name", "Unknown hotel"),
        "rating_distance": f"{rating_bit}{best.get('address', 'Address unavailable')}",
        "price": price_label,
        "alt_count": max(len(hotels) - 1, 0),
    }


def _build_weather(weather_result: dict | None) -> list[dict]:
    if not weather_result or not weather_result.get("success"):
        return [{"day": "Weather", "condition": "cloud", "temp": "—"}]

    data = weather_result.get("result") or {}
    temp = data.get("temperature_c")
    temp_label = f"{temp:.0f}°C" if isinstance(temp, (int, float)) else "—"

    return [{
        "day": data.get("location", "Forecast"),
        "condition": _weather_icon_key(data.get("condition", "")),
        "temp": temp_label,
    }]


# ---------------------------------------------------------------------------
# 4. Budget + places + recommendations + alerts + timeline
#    (budget/attraction/recommendation agents aren't wired in yet —
#     these are honest placeholders, not fabricated numbers)
# ---------------------------------------------------------------------------
def _build_budget(trip_intent: dict | None) -> dict:
    stated_budget = (trip_intent or {}).get("budget")
    return {
        "categories": [],
        "total": stated_budget or "Not calculated",
        "remaining": "Budget agent isn't connected yet",
    }


def _build_alerts(results: dict) -> list[dict]:
    alerts = []
    for name in ("weather", "flight", "hotel", "itinerary"):
        result = _result(results, name)
        if result and not result.get("success"):
            alerts.append({"type": "warning", "text": f"{name.capitalize()} agent: {result.get('error') or 'failed.'}"})

    if not alerts:
        alerts.append({"type": "success", "text": "All connected agents completed successfully."})

    return alerts


def _build_timeline(results: dict) -> list[str]:
    steps = ["Request received"]
    if _result(results, "planner") and _result(results, "planner").get("success"):
        steps.append("Trip details extracted")

    ran = [name for name in ("weather", "flight", "hotel") if _result(results, name)]
    if ran:
        steps.append(" · ".join(ran))

    if _result(results, "itinerary") and _result(results, "itinerary").get("success"):
        steps.append("Itinerary generated")

    return steps


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
def adapt_backend_response(raw: dict) -> dict:
    """
    raw: the parsed JSON body from POST /planner/
    Returns kwargs ready to pass into the four dashboard build_* functions,
    plus 'selected_day' for build_itinerary_and_travel.
    """

    trip_intent = raw.get("trip")
    results = raw.get("results") or {}
    agents_registered = raw.get("agents_registered") or len(KNOWN_AGENTS)
    planning_time = raw.get("planning_time_seconds")

    days = _build_days(_result(results, "itinerary"))

    return {
        "trip": _build_trip(trip_intent, results, agents_registered, planning_time),
        "agents": _build_agents(results, trip_intent or {}),
        "future_agents": FUTURE_AGENTS,
        "days": days,
        "selected_day": next(iter(days), "Day 1"),
        "flight": _build_flight(_result(results, "flight")),
        "hotel": _build_hotel(_result(results, "hotel")),
        "weather": _build_weather(_result(results, "weather")),
        "budget": _build_budget(trip_intent),
        "places": [],
        "recommendations": [
            "Attraction and recommendation agents aren't connected yet — "
            "this section will populate once they're added."
        ],
        "alerts": _build_alerts(results),
        "timeline_steps": _build_timeline(results),
    }