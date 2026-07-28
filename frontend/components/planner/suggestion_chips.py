from nicegui import ui


DESTINATIONS = [
    "Japan",
    "Bali",
    "Switzerland",
    "Italy",
]


def suggestion_chips(callback):

    with ui.row().classes(
        "gap-3"
    ):

        for item in DESTINATIONS:

            ui.button(
                item,
                on_click=lambda x=item: callback(x)
            ).props(
                "outline rounded"
            )