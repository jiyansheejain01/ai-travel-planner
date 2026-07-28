from components.common.page_container import page_container
from components.common.navbar import navbar
from components.planner.hero import hero
from components.planner.prompt_box import prompt_box


def home_page(on_submit):

    with page_container():

        navbar()

        hero()

        prompt_box(on_submit)