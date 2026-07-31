from nicegui import ui, app

from pages.landing_page import build_landing_page
from services.planner_service import plan_trip
import pages.planning


@ui.page("/")
def home():

    build_landing_page(
        on_submit=start_planner
    )


async def start_planner(prompt: str):

    if not prompt.strip():
        ui.notify(
            "Please describe your trip.",
            color="negative"
        )
        return

    try:
        result = await plan_trip(prompt)

        # Save trip for later pages
        app.storage.user["trip"] = result

        # Go to planning page
        ui.navigate.to("/planning")

    except Exception as e:
        ui.notify(
            f"Planning failed:\n{e}",
            color="negative"
        )


ui.run(
    title="AI Travel Planner",
    reload=True,
    storage_secret="travel-planner-secret",
)