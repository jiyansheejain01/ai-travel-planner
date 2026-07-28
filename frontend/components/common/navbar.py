from nicegui import ui


def navbar():

    with ui.row().classes(
        "w-full items-center justify-between"
    ).style("height:72px;"):

        with ui.row().classes(
            "items-center gap-3"
        ):

            ui.icon("travel_explore").style("""
font-size:30px;
color:#2563EB;
""")

            ui.label("AI Travel Planner").style("""
font-size:24px;
font-weight:800;
letter-spacing:-0.5px;
""")

        with ui.row().classes(
            "items-center gap-3"
        ):

            ui.button(
                icon="bookmark"
            ).props(
                "flat round"
            )

            ui.button(
                "Saved Trips"
            ).props(
                "flat"
            ).style("""
font-weight:600;
""")