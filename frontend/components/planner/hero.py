from nicegui import ui


def hero():

    with ui.column().classes(
        "w-full items-center section"
    ):

        ui.label(
            "Plan Your Next Adventure"
        ).style("""
font-size:56px;
font-weight:800;
letter-spacing:-2px;
""")

        ui.label(
            "Multi-agent AI that plans complete trips with flights, hotels, weather and itineraries."
        ).style("""
margin-top:16px;
font-size:20px;
color:#64748B;
max-width:760px;
text-align:center;
line-height:1.7;
""")