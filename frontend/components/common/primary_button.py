from nicegui import ui


def primary_button(
    text,
    on_click=None,
    icon=None
):

    return ui.button(
        text,
        icon=icon,
        on_click=on_click
    ).classes(
        "primary-button"
    )