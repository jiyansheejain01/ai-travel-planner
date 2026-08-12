from nicegui import ui, app

from pages.landing_page import build_landing_page
from pages.login_page import build_login_page
from services.planner_service import AuthError, plan_trip

import pages.dashboard


def _current_session() -> dict | None:
    return app.storage.user.get("auth")


@ui.page("/")
def home():

    if not _current_session():
        # Planning requires an account (the Planner agent's results are
        # tied to the signed-in user for the RAG/memory pipeline), so
        # send anonymous visitors to sign in or register first.
        ui.navigate.to("/login")
        return

    prefill = app.storage.user.pop("edit_prefill", None)

    build_landing_page(
        on_submit=start_planner,
        prefill=prefill,
    )


@ui.page("/login")
def login_page():

    if _current_session():
        # Already signed in -- nothing to do here.
        ui.navigate.to("/")
        return

    build_login_page(on_success=lambda session: ui.navigate.to("/"))


async def start_planner(prompt: str):

    session = _current_session()

    if not session:
        ui.notify("Please sign in to plan a trip.", color="negative")
        ui.navigate.to("/login")
        return

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
        result = await plan_trip(prompt, session.get("access_token"))
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

    except AuthError:
        # Token missing/expired/invalid -- the backend rejected the
        # request outright, so the session is no longer good for anything.
        app.storage.user.pop("auth", None)
        ui.notify("Your session expired — please sign in again.", color="negative")
        ui.navigate.to("/login")

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
