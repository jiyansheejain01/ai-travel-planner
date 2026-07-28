from contextlib import contextmanager
from nicegui import ui


@contextmanager
def page_container():

    with ui.column().classes(
        "page w-full min-h-screen"
    ).style(
        "padding-top:32px; padding-bottom:60px;"
    ):
        yield