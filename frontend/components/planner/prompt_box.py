from nicegui import ui

from components.common.card import app_card
from components.common.primary_button import primary_button
from components.planner.suggestion_chips import suggestion_chips


def prompt_box(on_submit):

    with app_card():

        prompt = ui.textarea(
            placeholder="Describe your dream trip..."
        ).props(
            "borderless autogrow"
        ).classes(
            "w-full"
        ).style("""
font-size:18px;
min-height:180px;
""")

        ui.separator().classes("my-5")

        def fill(text):

            prompt.value = f"Plan a trip to {text}"

        with ui.row().classes(
            "justify-between items-center w-full"
        ):

            suggestion_chips(fill)

            primary_button(
                "Generate Trip",
                icon="arrow_forward",
                on_click=lambda: on_submit(prompt.value)
            )