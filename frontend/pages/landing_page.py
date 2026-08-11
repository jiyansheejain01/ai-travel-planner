"""
Trail map landing page for the AI Travel Planner.

Drop this file into your frontend folder (e.g. frontend/pages/landing_page.py)
and either:
  - import `build_landing_page` and call it inside your own @ui.page('/') route, or
  - run this file directly to preview it standalone: `python landing_page.py`
"""

from datetime import date, datetime

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
    ('ti-map-pin', 'attraction-agent', BLUE),
    ('ti-star', 'recommendation-agent', MUSTARD),
]

CURRENCIES = ['INR', 'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD']

INTERESTS = [
    'Culture', 'Food', 'Nature', 'Nightlife',
    'Shopping', 'Adventure', 'Relaxation', 'History',
]

# Each preset fills in an origin city and explicit dates -- the Planner
# Agent is instructed to never invent missing details, and the Flight /
# Hotel / Itinerary agents only run once origin, destination, and
# start/end dates are all present. Presets without these will still plan
# (weather only) but skip flights, hotels, and the itinerary.
EXAMPLE_TRIPS = [
    {
        'label': 'Kyoto, 6 days',
        'destination': 'Kyoto',
        'origin': 'Bengaluru',
        'start_date': '2027-04-02',
        'end_date': '2027-04-08',
        'travelers': 2,
        'interests': ['Culture', 'Food'],
    },
    {
        'label': 'Bali, 10 days',
        'destination': 'Bali',
        'origin': 'Mumbai',
        'start_date': '2026-12-05',
        'end_date': '2026-12-15',
        'travelers': 2,
        'interests': ['Nature', 'Relaxation'],
    },
    {
        'label': 'Lisbon, weekend',
        'destination': 'Lisbon',
        'origin': 'London',
        'start_date': '2026-09-12',
        'end_date': '2026-09-14',
        'travelers': 1,
        'interests': ['Food', 'Nightlife'],
    },
]


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


def _format_date_human(value: date) -> str:
    # "Apr 2 2027" (no leading zero on the day), matching the old example style.
    return f'{value.strftime("%b")} {value.day} {value.year}'


def compose_trip_message(fields: dict) -> str:
    """
    Turns the structured form fields into a single natural-language
    message -- the same shape the Planner Agent's LLM already expects.
    This keeps the backend contract (`{"message": str}`) unchanged while
    giving users explicit fields instead of a blank prompt to guess at.
    """

    destination = (fields.get('destination') or '').strip()
    origin = (fields.get('origin') or '').strip()
    travelers = fields.get('travelers')
    budget_amount = fields.get('budget_amount')
    budget_currency = (fields.get('budget_currency') or '').strip()
    interests = [i for i in (fields.get('interests') or []) if i]

    start_d = _parse_date(fields.get('start_date'))
    end_d = _parse_date(fields.get('end_date'))

    if start_d and end_d and end_d > start_d:
        duration_days = (end_d - start_d).days
        sentence = f'{duration_days} day{"s" if duration_days != 1 else ""} in {destination or "the destination"}'
    else:
        sentence = f'A trip to {destination or "the destination"}'

    if origin:
        sentence += f' from {origin}'

    if start_d and end_d:
        sentence += f', {_format_date_human(start_d)} to {_format_date_human(end_d)}'

    sentence += '.'

    parts = [sentence]

    if travelers:
        parts.append(f'Travelers: {travelers}.')

    if budget_amount:
        currency_part = f' {budget_currency}' if budget_currency else ''
        parts.append(f'Budget: {budget_amount}{currency_part}.')

    if interests:
        parts.append(f'Interested in: {", ".join(interests)}.')

    return ' '.join(parts)


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


def build_landing_page(on_submit=None, prefill: dict | None = None) -> None:
    """
    Renders the trail-map hero section.

    on_submit: optional callable(str) invoked with the trip description
               when "Start planning" is clicked or an example chip is used.
    prefill: optional dict of field values (same shape as compose_trip_message
             expects) to pre-populate the form with, e.g. when arriving here
             via the dashboard's "Edit trip" action.
    """
    _load_fonts_and_icons()
    _page_style()
    ui.colors(primary=BLUE, secondary=MUSTARD)

    prefill = prefill or {}

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

        # --- Trip form (trailhead waypoints) --------------------------------
        # Explicit fields instead of one blank prompt, so people aren't left
        # guessing what to type. Selections are composed into the same
        # natural-language message the Planner Agent's LLM already expects --
        # the backend contract (`{"message": str}`) is unchanged.

        selected_interests: set[str] = set(prefill.get('interests') or [])
        interest_buttons: dict[str, ui.button] = {}

        def _field_label(text: str) -> None:
            ui.label(text).style(
                f'font-size:11.5px; font-weight:600; letter-spacing:0.3px; '
                f'color:{MUTED}; margin-bottom:2px;'
            )

        def _refresh_interest_styles() -> None:
            for label, btn in interest_buttons.items():
                if label in selected_interests:
                    btn.style(
                        f'border:0.5px solid {BLUE}; background:{BLUE}; border-radius:16px; '
                        f'padding:5px 12px; font-size:12.5px; color:white; font-weight:500;'
                    )
                else:
                    btn.style(
                        f'border:0.5px solid {LINE}; background:{CARD}; border-radius:16px; '
                        f'padding:5px 12px; font-size:12.5px; color:{MUTED}; font-weight:400;'
                    )

        def _toggle_interest(label: str) -> None:
            if label in selected_interests:
                selected_interests.discard(label)
            else:
                selected_interests.add(label)
            _refresh_interest_styles()

        with ui.column().style(
            f'max-width:560px; width:100%; background:{CARD}; border:0.5px solid {LINE}; '
            f'border-radius:14px; padding:20px 22px; gap:14px;'
        ):
            # Destination + Origin
            with ui.row().style('width:100%; gap:14px; flex-wrap:wrap;'):
                with ui.column().style('flex:1 1 220px; min-width:180px; gap:0;'):
                    _field_label('DESTINATION *')
                    destination_input = ui.input(
                        placeholder='e.g. Kyoto', value=prefill.get('destination') or '',
                    ).props('borderless dense').style(
                        f'font-size:15px; color:{INK}; border-bottom:1px solid {LINE};'
                    )
                with ui.column().style('flex:1 1 220px; min-width:180px; gap:0;'):
                    _field_label('FLYING FROM')
                    origin_input = ui.input(
                        placeholder='e.g. Bengaluru', value=prefill.get('origin') or '',
                    ).props('borderless dense').style(
                        f'font-size:15px; color:{INK}; border-bottom:1px solid {LINE};'
                    )

            # Start date + End date
            with ui.row().style('width:100%; gap:14px; flex-wrap:wrap;'):
                with ui.column().style('flex:1 1 220px; min-width:180px; gap:0;'):
                    _field_label('START DATE')
                    start_date_input = ui.input(value=prefill.get('start_date') or '').props(
                        'borderless dense type=date'
                    ).style(
                        f'font-size:15px; color:{INK}; border-bottom:1px solid {LINE};'
                    )
                with ui.column().style('flex:1 1 220px; min-width:180px; gap:0;'):
                    _field_label('END DATE')
                    end_date_input = ui.input(value=prefill.get('end_date') or '').props(
                        'borderless dense type=date'
                    ).style(
                        f'font-size:15px; color:{INK}; border-bottom:1px solid {LINE};'
                    )

            # Travelers + Budget + Currency
            with ui.row().style('width:100%; gap:14px; flex-wrap:wrap;'):
                with ui.column().style('flex:1 1 140px; min-width:120px; gap:0;'):
                    _field_label('TRAVELERS')
                    travelers_input = ui.number(
                        value=prefill.get('travelers') or 2, min=1, max=20, format='%.0f',
                    ).props('borderless dense').style(
                        f'font-size:15px; color:{INK}; border-bottom:1px solid {LINE};'
                    )
                with ui.column().style('flex:1 1 160px; min-width:140px; gap:0;'):
                    _field_label('BUDGET (OPTIONAL)')
                    budget_input = ui.number(
                        value=prefill.get('budget_amount'), min=0, format='%.0f',
                    ).props('borderless dense').style(
                        f'font-size:15px; color:{INK}; border-bottom:1px solid {LINE};'
                    )
                with ui.column().style('flex:1 1 110px; min-width:100px; gap:0;'):
                    _field_label('CURRENCY')
                    currency_select = ui.select(
                        CURRENCIES, value=prefill.get('budget_currency') or 'INR',
                    ).props('borderless dense').style(
                        f'font-size:15px; color:{INK}; border-bottom:1px solid {LINE};'
                    )

            # Interests
            with ui.column().style('width:100%; gap:6px;'):
                _field_label('INTERESTS (OPTIONAL)')
                with ui.row().style('gap:8px; flex-wrap:wrap;'):
                    for label in INTERESTS:
                        btn = ui.button(label, on_click=lambda l=label: _toggle_interest(l)).props(
                            'flat no-caps unelevated dense'
                        )
                        interest_buttons[label] = btn
                    _refresh_interest_styles()

            def _collect_fields() -> dict:
                return {
                    'destination': destination_input.value,
                    'origin': origin_input.value,
                    'start_date': start_date_input.value,
                    'end_date': end_date_input.value,
                    'travelers': travelers_input.value,
                    'budget_amount': budget_input.value,
                    'budget_currency': currency_select.value,
                    'interests': sorted(selected_interests),
                }

            async def _submit():
                fields = _collect_fields()

                if not (fields['destination'] or '').strip():
                    ui.notify('Please enter a destination.', color='negative')
                    return

                message = compose_trip_message(fields)

                if on_submit:
                    await on_submit(message)
                else:
                    ui.notify(f'Planning: {message}')

            ui.button('Start planning', on_click=_submit, color=None).props('unelevated no-caps').style(
                f'background:{BLUE}; color:white; border-radius:8px; font-weight:500; '
                f'align-self:flex-end; padding:8px 20px;'
            )

        # Flight/hotel/itinerary agents only run once origin, destination, and
        # start/end dates are all present -- nudge people toward filling them in.
        ui.label('Tip: add where you\'re flying from and your travel dates to unlock flights, hotels, and a full itinerary.').style(
            f'font-size:11.5px; color:{MUTED}; text-align:center; margin-top:8px; max-width:480px;'
        )

        # --- Example trip presets --------------------------------------------
        with ui.row().classes('justify-center').style('gap:10px; margin-top:16px; flex-wrap:wrap;'):
            for preset in EXAMPLE_TRIPS:
                async def _use_preset(p=preset):
                    destination_input.value = p['destination']
                    origin_input.value = p['origin']
                    start_date_input.value = p['start_date']
                    end_date_input.value = p['end_date']
                    travelers_input.value = p['travelers']
                    selected_interests.clear()
                    selected_interests.update(p['interests'])
                    _refresh_interest_styles()
                    await _submit()

                ui.button(preset['label'], on_click=_use_preset, color=None).props('flat no-caps unelevated').style(
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