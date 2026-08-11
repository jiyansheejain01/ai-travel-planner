from nicegui import ui, app

from components.dashboard.dashboard_theme import apply_dashboard_theme
from components.dashboard.trip_header import build_trip_header
from components.dashboard.agent_grid import build_agent_grid
from components.dashboard.trip_content import build_itinerary_and_travel
from components.dashboard.trip_insights import build_budget_and_insights

from services.dashboard_adapter import adapt_backend_response
from services.planner_service import plan_trip

from pages.landing_page import compose_trip_message

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


def _trip_intent_to_fields(trip_intent: dict) -> dict:
    """
    Maps the Planner Agent's raw TripIntent fields onto the same field
    names compose_trip_message() (and the landing page form) expect.
    """
    return {
        "destination": trip_intent.get("destination"),
        "origin": trip_intent.get("origin"),
        "start_date": trip_intent.get("start_date"),
        "end_date": trip_intent.get("end_date"),
        "travelers": trip_intent.get("travelers"),
        "budget_amount": trip_intent.get("budget_amount"),
        "budget_currency": trip_intent.get("budget_currency"),
        "interests": trip_intent.get("interests") or [],
    }


def _build_export_text(data: dict) -> str:
    """Plain-text itinerary summary, built from the already-adapted dashboard data."""

    trip = data["trip"]
    days = data["days"]
    flight = data["flight"]
    hotel = data["hotel"]
    budget = data["budget"]

    lines = [
        trip["title"],
        f'{trip["destination"]} - {trip["dates"]} - {trip["duration"]} - {trip["travelers"]}',
        "",
        trip["summary"],
        "",
    ]

    if flight.get("airline_route"):
        lines.append(f'Flight: {flight["airline_route"]} - {flight.get("price", "")}')
    if hotel.get("name"):
        lines.append(f'Stay: {hotel["name"]} - {hotel.get("price", "")}')
    if budget.get("total"):
        lines.append(f'Estimated total: {budget["total"]}')

    lines.append("")

    for day_name, items in days.items():
        lines.append(day_name.upper())
        for item in items:
            lines.append(f'  {item.get("time", "")} - {item.get("title", "")}')
            if item.get("note"):
                lines.append(f'    {item["note"]}')
        lines.append("")

    return "\n".join(lines)


def _build_actions(raw: dict, data: dict) -> dict:
    """
    Real, working handlers for the Trip Overview quick-action buttons.
    Only wired for the live `/dashboard` route -- the `/dashboard/preview`
    sample route has no backend trip behind it, so its buttons fall back
    to a plain notify (see build_trip_header's default).
    """

    def edit_trip() -> None:
        trip_intent = raw.get("trip") or {}
        # Handed to the landing page via storage so the form arrives
        # pre-filled with this trip's details instead of blank.
        app.storage.user["edit_prefill"] = _trip_intent_to_fields(trip_intent)
        ui.navigate.to("/")

    async def regenerate_plan() -> None:
        trip_intent = raw.get("trip") or {}
        message = compose_trip_message(_trip_intent_to_fields(trip_intent))

        ui.notify("Regenerating your plan — this can take a minute...", type="ongoing")

        try:
            new_result = await plan_trip(message)
            app.storage.user["trip"] = new_result
            ui.notify("Plan regenerated!", type="positive")
            ui.navigate.reload()
        except Exception as exc:
            ui.notify(f"Regenerate failed:\n{exc}", color="negative", multi_line=True)

    def add_activity() -> None:
        itinerary_result = (raw.get("results") or {}).get("itinerary")

        if not itinerary_result or not itinerary_result.get("success"):
            ui.notify("Itinerary hasn't been generated yet — nothing to add to.", color="warning")
            return

        days_list = (itinerary_result.get("result") or {}).get("days") or []
        day_options = [f'Day {d["day"]}' for d in days_list]

        if not day_options:
            ui.notify("No itinerary days to add to yet.", color="warning")
            return

        with ui.dialog() as dialog, ui.card().style("min-width:320px; gap:6px;"):
            ui.label("Add activity").style("font-size:16px; font-weight:600; margin-bottom:6px;")

            day_select = ui.select(day_options, value=day_options[0], label="Day").classes("w-full")
            title_input = ui.input(label="Title").classes("w-full")
            time_input = ui.input(label="Time (e.g. 18:00)").classes("w-full")
            location_input = ui.input(label="Location (optional)").classes("w-full")
            description_input = ui.textarea(label="Description (optional)").classes("w-full")

            def _save() -> None:
                if not (title_input.value or "").strip():
                    ui.notify("Please enter a title.", color="negative")
                    return

                day_num = int(day_select.value.split()[-1])

                for d in days_list:
                    if d.get("day") == day_num:
                        d.setdefault("activities", []).append({
                            "time": (time_input.value or "").strip() or "-",
                            "title": title_input.value.strip(),
                            "description": (description_input.value or "").strip(),
                            "location": (location_input.value or "").strip() or None,
                        })
                        break

                # Persist the mutated itinerary back into session storage.
                app.storage.user["trip"] = raw

                dialog.close()
                ui.notify("Activity added.", type="positive")
                ui.navigate.reload()

            with ui.row().classes("w-full justify-end").style("gap:8px; margin-top:10px;"):
                ui.button("Cancel", on_click=dialog.close).props("flat no-caps")
                ui.button("Add", on_click=_save).props("unelevated no-caps color=primary")

        dialog.open()

    def export_trip() -> None:
        text = _build_export_text(data)
        destination = (data["trip"].get("destination") or "trip").lower().replace(" ", "_")
        ui.download(text.encode("utf-8"), f"{destination}_itinerary.txt")

    return {
        "edit": edit_trip,
        "regenerate": regenerate_plan,
        "add_activity": add_activity,
        "export": export_trip,
    }


def _render(trip, agents, future_agents, days, flight, hotel, weather,
            budget, places, recommendations, alerts, timeline_steps,
            selected_day=None, actions=None) -> None:

    apply_dashboard_theme()
    ui.colors(primary="#5B7C99", secondary="#D4A24C")

    with ui.column().classes("w-full").style(
        "max-width:900px; margin:0 auto; padding:32px 20px; gap:16px;"
    ):
        build_trip_header(trip, actions)
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
    actions = _build_actions(raw, data)
    _render(**data, actions=actions)


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
