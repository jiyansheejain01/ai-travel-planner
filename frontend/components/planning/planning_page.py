from nicegui import ui


class PlanningPage:

    def __init__(self):

        with ui.column().classes("items-center w-full").style(
            "padding-top:80px;"
        ):

            ui.label("Planning your adventure...").classes(
                "text-3xl font-bold"
            )

            ui.label(
                "Our AI agents are preparing your itinerary."
            ).classes(
                "text-gray-500"
            )

            ui.separator()

            ui.label("🧠 Planner Agent")
            ui.label("☀️ Weather Agent")
            ui.label("✈️ Flight Agent")
            ui.label("🏨 Hotel Agent")
            ui.label("💰 Budget Agent")
            ui.label("🗺️ Itinerary Agent")