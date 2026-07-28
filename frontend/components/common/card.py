from contextlib import contextmanager
from nicegui import ui


@contextmanager
def app_card():

    with ui.card().classes(
        "card w-full"
    ).style(
        "padding:28px;"
    ):
        yield