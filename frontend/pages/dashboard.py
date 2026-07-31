from nicegui import ui

from components.dashboard.dashboard_theme import (
    apply_dashboard_theme,
)

from components.dashboard.trip_header import build_trip_header
from components.dashboard.agent_grid import build_agent_grid
from components.dashboard.trip_content import build_itinerary_and_travel
from components.dashboard.trip_insights import build_budget_and_insights

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


@ui.page("/dashboard")
def dashboard():

    apply_dashboard_theme()

    ui.colors(primary="#5B7C99", secondary="#D4A24C")

    with ui.column().classes("w-full").style(
        "max-width:900px; margin:0 auto; padding:32px 20px; gap:16px;"
    ):

        build_trip_header(
            SAMPLE_TRIP
        )

        build_agent_grid(
            SAMPLE_AGENTS,
            SAMPLE_FUTURE_AGENTS
        )

        build_itinerary_and_travel(
            SAMPLE_DAYS,
            SAMPLE_FLIGHT,
            SAMPLE_HOTEL,
            SAMPLE_WEATHER
        )

        build_budget_and_insights(
            SAMPLE_BUDGET,
            SAMPLE_PLACES,
            SAMPLE_RECOMMENDATIONS,
            SAMPLE_ALERTS,
            SAMPLE_TIMELINE
        )