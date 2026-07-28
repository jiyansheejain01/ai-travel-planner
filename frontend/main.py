from nicegui import ui

from pages.landing_page import build_landing_page


@ui.page("/")
def home():

    build_landing_page(
        on_submit=start_planner
    )


def start_planner(prompt: str):

    print(prompt)

    # TODO:
    # call your planner endpoint here
    # then navigate to planning page


ui.run(
    title="AI Travel Planner",
    reload=True,
)