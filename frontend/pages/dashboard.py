from nicegui import ui, app

from components.dashboard.dashboard_theme import apply_dashboard_theme
from components.dashboard.trip_header import build_trip_header
from components.dashboard.agent_grid import build_agent_grid
from components.dashboard.trip_content import build_itinerary_and_travel
from components.dashboard.trip_insights import build_budget_and_insights

from services.dashboard_adapter import adapt_backend_response

from state.dashboard_state import (
    SAMPLE_TRIP,
    SAMPLE_AGENTS,
    SAMPLE_FUTURE_AGENTS,
    SAMPLE_DAYS,
    SAMPLE_FLIGHT,
    SAMPLE_HOTEL,
    SAMPLE_WEATHER,
    SAMPLE_BUDGET,
    SAMPLE_PLACES,
    SAMPLE_RECOMMENDATIONS,
    SAMPLE_ALERTS,
    SAMPLE_TIMELINE,
)


def _render(trip, agents, future_agents, days, flight, hotel, weather,
            budget, places, recommendations, alerts, timeline_steps,
            selected_day=None) -> None:

    apply_dashboard_theme()
    ui.colors(primary="#5B7C99", secondary="#D4A24C")

    with ui.column().classes("w-full").style(
        "max-width:900px; margin:0 auto; padding:32px 20px; gap:16px;"
    ):
        build_trip_header(trip)
        build_agent_grid(agents, future_agents)

        itinerary_kwargs = {}
        if selected_day is not None:
            itinerary_kwargs["selected_day"] = selected_day

        build_itinerary_and_travel(days, flight, hotel, weather, **itinerary_kwargs)
        build_budget_and_insights(budget, places, recommendations, alerts, timeline_steps)


@ui.page("/dashboard")
def dashboard():
    """
    Renders the most recently planned trip (set by main.py's start_planner
    after a successful call to POST /planner/). If someone lands here
    without having planned a trip yet, send them back to plan one instead
    of showing fabricated sample data.
    """

    raw = app.storage.user.get("trip")

    if not raw:
        ui.notify("Plan a trip first to see its dashboard.", color="warning")
        ui.navigate.to("/")
        return

    data = adapt_backend_response(raw)
    _render(**data)


@ui.page("/dashboard/preview")
def dashboard_preview():
    """Design preview using sample data -- not wired to the backend."""

    _render(
        trip=SAMPLE_TRIP,
        agents=SAMPLE_AGENTS,
        future_agents=SAMPLE_FUTURE_AGENTS,
        days=SAMPLE_DAYS,
        flight=SAMPLE_FLIGHT,
        hotel=SAMPLE_HOTEL,
        weather=SAMPLE_WEATHER,
        budget=SAMPLE_BUDGET,
        places=SAMPLE_PLACES,
        recommendations=SAMPLE_RECOMMENDATIONS,
        alerts=SAMPLE_ALERTS,
        timeline_steps=SAMPLE_TIMELINE,
    )
