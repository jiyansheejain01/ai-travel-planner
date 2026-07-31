from nicegui import ui

from components.planning.planning_page import PlanningPage


@ui.page("/planning")
def planning():
    PlanningPage()