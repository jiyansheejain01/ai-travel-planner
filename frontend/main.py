from nicegui import ui, app

from pages.landing_page import build_landing_page
from services.planner_service import plan_trip

import pages.dashboard

@ui.page("/")
def home():

    prefill = app.storage.user.pop("edit_prefill", None)

    build_landing_page(
        on_submit=start_planner,
        prefill=prefill,
    )


async def start_planner(prompt: str):

    if not prompt.strip():
        ui.notify(
            "Please describe your trip.",
            color="negative"
        )
        return

    ui.notify(
        "Planning your trip — this can take a minute...",
        type="ongoing",
    )

    try:
        result = await plan_trip(prompt)
        print("\n========== FRONTEND BACKEND RESPONSE ==========")

        print("TRIP:")
        print(result.get("trip"))

        print("\nWEATHER:")
        print(result.get("results", {}).get("weather"))

        print("\nFLIGHT:")
        print(result.get("results", {}).get("flight"))

        print("\nHOTEL:")
        print(result.get("results", {}).get("hotel"))

        print("================================================\n")

        # Save trip for later pages
        app.storage.user["trip"] = result

        ui.notify("Trip planned!", type="positive")

        # Go to dashboard
        ui.navigate.to("/dashboard")

    except Exception as e:
        ui.notify(
            f"Planning failed:\n{e}",
            color="negative",
            multi_line=True,
        )


ui.run(
    title="AI Travel Planner",
    reload=True,
    storage_secret="travel-planner-secret",
)