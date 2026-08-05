"""
Trail map landing page for the AI Travel Planner.

Drop this file into your frontend folder (e.g. frontend/pages/landing_page.py)
and either:
  - import `build_landing_page` and call it inside your own @ui.page('/') route, or
  - run this file directly to preview it standalone: `python landing_page.py`
"""

from nicegui import ui

# ---------------------------------------------------------------------------
# Palette / tokens for the trail-map identity
# ---------------------------------------------------------------------------
BG = '#F7F5F0'
INK = '#33342E'
MUTED = '#6B6D63'
LINE = '#DEDBD0'
BLUE = '#5B7C99'
MUSTARD = '#D4A24C'
CARD = '#FFFFFF'
ROUNDEL = '#EDEBE2'

AGENTS = [
    ('ti-plane', 'flight-agent', BLUE),
    ('ti-bed', 'hotel-agent', BLUE),
    ('ti-sun', 'weather-agent', MUSTARD),
    ('ti-wallet', 'budget-agent', MUSTARD),
]

# Each prompt intentionally includes an origin city and explicit dates --
# the Planner Agent is instructed to never invent missing details, and
# the Flight / Hotel / Itinerary agents only run once origin, destination,
# and start/end dates are all present. Prompts without these will still
# plan (weather only) but skip flights, hotels, and the itinerary.
EXAMPLE_PROMPTS = [
    '6 days in Kyoto from Bengaluru, Apr 2 to Apr 8 2027',
    '10 days in Bali from Mumbai, Dec 5 to Dec 15 2026',
    'Weekend in Lisbon from London, Sep 12 to Sep 14 2026',
]


def _load_fonts_and_icons() -> None:
    """One-time head injection: Tabler icon font + Fraunces display serif."""
    ui.add_head_html('''
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@500&display=swap" rel="stylesheet">
    ''')


def _page_style() -> None:
    ui.query('body').style(f'background:{BG};')
    ui.query('.nicegui-content').classes('items-center')


def build_landing_page(on_submit=None) -> None:
    """
    Renders the trail-map hero section.

    on_submit: optional callable(str) invoked with the trip description
               when "Start planning" is clicked or an example chip is used.
    """
    _load_fonts_and_icons()
    _page_style()
    ui.colors(primary=BLUE, secondary=MUSTARD)

    with ui.column().classes('items-center w-full').style('max-width:720px; margin:0 auto; padding:48px 24px;'):

        # --- Hero: trail line + headline ---------------------------------
        with ui.column().classes('items-center w-full').style('position:relative;'):
            ui.html(f'''
<svg viewBox="0 0 640 60" width="100%" height="60"
     style="position:absolute;top:10px;left:0;opacity:0.5;">
    <path
        d="M 10 40 Q 160 5 320 35 T 630 20"
        fill="none"
        stroke="{BLUE}"
        stroke-width="2"
        stroke-dasharray="1 9"
        stroke-linecap="round"
    />
</svg>
''')

            ui.label('WHERE TO NEXT').style(
                f'position:relative; font-size:13px; letter-spacing:2px; color:{MUSTARD}; margin-bottom:6px;'
            )
            ui.label('Plan a trip that').style(
                f'position:relative; font-family:Fraunces,serif; font-weight:500; '
                f'font-size:40px; line-height:1.15; color:{INK}; text-align:center; margin:0;'
            )
            ui.label('plots its own route').style(
                f'position:relative; font-family:Fraunces,serif; font-weight:500; '
                f'font-size:40px; line-height:1.15; color:{INK}; text-align:center; margin:0;'
            )

        ui.label(
            'A planner agent and its specialists — flights, hotels, weather, budget — '
            'lay out your waypoints while you watch.'
        ).style(f'max-width:440px; text-align:center; font-size:15px; color:{MUTED}; '
                f'line-height:1.6; margin:18px 0 32px;')

        # --- Trip input row (trailhead marker) ----------------------------
        # NOTE: the input must be constructed *inside* the `with ui.row()` block below —
        # constructing it beforehand places it in the DOM at that point, not inside the row.
        async def _submit():
            text = trip_input.value or ''
            if on_submit:
                await on_submit(text)
            else:
                ui.notify(f'Planning: {text}' if text else 'Describe a trip first')

        with ui.row().style(
            f'max-width:560px; width:100%; background:{CARD}; border:0.5px solid {LINE}; '
            f'border-radius:14px; padding:6px 16px; gap:10px; '
            f'display:flex; flex-wrap:nowrap; align-items:center;'
        ):
            ui.html(
                f'<span style="width:10px;height:10px;border-radius:50%;'
                f'background:{MUSTARD};flex-shrink:0;display:block;"></span>'
            )
            trip_input = ui.input(placeholder='Describe your dream trip...').props('borderless').style(
                f'flex:1 1 auto; min-width:0; font-size:15px; color:{INK};'
            )
            ui.button('Start planning', on_click=_submit, color=None).props('unelevated no-caps').style(
                f'background:{BLUE}; color:white; border-radius:8px; font-weight:500; '
                f'flex-shrink:0; white-space:nowrap;'
            )

        # Flight/hotel/itinerary agents only run once origin, destination, and
        # start/end dates are all present -- nudge people toward including them.
        ui.label('Tip: mention where you\'re flying from and your travel dates to unlock flights, hotels, and a full itinerary.').style(
            f'font-size:11.5px; color:{MUTED}; text-align:center; margin-top:8px; max-width:480px;'
        )

        # --- Example prompt chips ------------------------------------------
        with ui.row().classes('justify-center').style('gap:10px; margin-top:16px; flex-wrap:wrap;'):
            for prompt in EXAMPLE_PROMPTS:
                async def _use_prompt(p=prompt):
                    trip_input.value = p
                    await _submit()

                ui.button(prompt, on_click=_use_prompt, color=None).props('flat no-caps unelevated').style(
                    f'border:0.5px solid {LINE}; background:{CARD}; border-radius:20px; '
                    f'padding:6px 14px; font-size:12.5px; color:{MUTED}; font-weight:400;'
                )

        # --- Agent roster ----------------------------------------------------
        with ui.row().classes('justify-center').style('gap:32px; margin-top:44px;'):
            for icon_class, name, color in AGENTS:
                with ui.column().classes('items-center').style('gap:8px;'):
                    ui.html(f'''
                        <div style="width:36px;height:36px;border-radius:50%;background:{ROUNDEL};
                                    display:flex;align-items:center;justify-content:center;">
                            <i class="ti {icon_class}" style="font-size:18px;color:{color};" aria-hidden="true"></i>
                        </div>
                    ''')
                    ui.label(name).style(f'font-size:12px; color:{MUTED};')


# ---------------------------------------------------------------------------
# Standalone preview: `python landing_page.py`
# ---------------------------------------------------------------------------
"""
if __name__ in {'__main__', '__mp_main__'}:
    @ui.page('/')
    def index():
        build_landing_page(on_submit=lambda text: ui.notify(f'Planning: {text}'))

    ui.run(title='AI Travel Planner')
"""