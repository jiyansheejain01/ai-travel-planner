from nicegui import ui

from components.dashboard.dashboard_theme import (
    CARD,
    CARD_STYLE,
    FAINT,
    BLUE,
    MUSTARD,
    LINE,
    MUTED,
    INK,
    ROUNDEL,
    _section_label,
)

# ---------------------------------------------------------------------------
# 3. Daily itinerary + flight / hotel + weather
# ---------------------------------------------------------------------------
WEATHER_ICONS = {'sun': 'ti-sun', 'cloud': 'ti-cloud', 'rain': 'ti-cloud-rain'}
WEATHER_COLORS = {'sun': MUSTARD, 'cloud': BLUE, 'rain': BLUE}


def _itinerary_row(item: dict, dot_color: str) -> None:
    """item: {title, time, duration, setting ('indoor'|'outdoor'), cost, note}"""
    with ui.row().classes('w-full').style('gap:12px; padding:8px 0; border-bottom:0.5px solid #EDEBE2;'):
        ui.html(f'<span style="width:8px;height:8px;border-radius:50%;background:{dot_color};margin-top:5px;display:block;flex-shrink:0;"></span>')
        with ui.column().style('gap:0; flex:1;'):
            ui.label(item['title']).style('font-size:13.5px; font-weight:500;')
            ui.label(f"{item['time']} · {item['duration']} · {item['setting']} · {item['cost']}").style(
                f'font-size:12px; color:{MUTED};'
            )
            if item.get('note'):
                ui.label(item['note']).style(f'font-size:12px; color:{FAINT}; margin-top:3px;')


def _option_row(
    primary: str,
    secondary: str,
    price: str,
    converted_note: str | None = None,
) -> None:
    """One alternative flight/hotel row inside the dedicated options card."""

    with ui.column().classes('w-full').style(
        'gap:2px; padding:9px 0; border-bottom:0.5px solid #EDEBE2;'
    ):

        with ui.row().classes('w-full items-center justify-between').style(
            'gap:10px;'
        ):
            with ui.column().style('gap:0;'):
                ui.label(primary).style(
                    'font-size:13px; font-weight:500;'
                )
                ui.label(secondary).style(
                    f'font-size:12px; color:{MUTED};'
                )

            ui.label(price).style(
                f'font-size:13px; font-weight:500; color:{INK}; white-space:nowrap;'
            )

        if converted_note:
            ui.label(converted_note).style(
                f'font-size:12px; color:{MUTED};'
            )

def build_itinerary_and_travel(days: dict, flight: dict, hotel: dict, weather: list[dict],
                                selected_day: str | None = None, on_day_select=None) -> None:
    """
    days: { 'Day 1': [item, ...], 'Day 2': [...], ... }  (see _itinerary_row for item shape)
    flight: {airline_route, times, price, converted_note, alt_count, options: [{airline_route, times, price}, ...]}
    hotel: {name, rating_distance, price, converted_note, alt_count, options: [{name, rating_distance, price}, ...]}
    weather: [{day, condition ('sun'|'cloud'|'rain'), temp}]
    """
    dot_cycle = [MUSTARD, BLUE]
    day_names = list(days.keys())

    # Mutable holder so the nested refreshable closures below can share and
    # update which day is currently on screen. Previously the day chips'
    # on_click had nowhere to write the new selection back to, so clicking
    # a day did nothing and the itinerary was stuck on whatever day was
    # passed in at page-load time.
    state = {'day': selected_day if selected_day in days else (day_names[0] if day_names else None)}

    def _select_day(day_name: str) -> None:
        state['day'] = day_name
        if on_day_select:
            on_day_select(day_name)
        day_chips.refresh()
        day_body.refresh()

    @ui.refreshable
    def day_chips() -> None:
        with ui.row().classes('w-full items-center').style('gap:6px; margin-bottom:14px; flex-wrap:wrap;'):
            for day_name in day_names:
                is_selected = day_name == state['day']
                style = (
                    f'background:{BLUE}; color:white;' if is_selected
                    else f'border:0.5px solid {LINE}; background:{CARD}; color:{MUTED};'
                )
                # color=None stops NiceGUI/Quasar from adding its default
                # `text-primary` class. That class carries `!important` and
                # otherwise fights with the color set in .style() below --
                # it's exactly why the selected (blue) chip's label used to
                # go invisible (blue text forced onto the blue background).
                ui.button(day_name, on_click=lambda d=day_name: _select_day(d), color=None).props(
                    'flat no-caps'
                ).style(f'{style} font-size:12px; padding:5px 12px; border-radius:20px;')

    @ui.refreshable
    def day_body() -> None:
        with ui.column().classes('w-full').style(f'{CARD_STYLE} padding:16px 18px; margin-bottom:18px; gap:0;'):
            for i, item in enumerate(days.get(state['day'], [])):
                _itinerary_row(item, dot_cycle[i % len(dot_cycle)])

    with ui.column().classes('w-full').style(f'{CARD_STYLE} padding:20px 24px; gap:0;'):
        _section_label('DAILY ITINERARY')

        day_chips()
        day_body()

        with ui.row().classes('w-full').style('gap:14px; margin-bottom:18px; flex-wrap:wrap;'):
            with ui.column().style(f'{CARD_STYLE} padding:14px 16px; flex:1; min-width:220px; gap:0;'):
                with ui.row().classes('w-full justify-between items-center').style('margin-bottom:8px;'):
                    ui.label('BEST FLIGHT').style(f'font-size:13px; color:{MUTED};')
                    ui.label(f"{flight['alt_count']} alternatives").style(
                        f'background:{ROUNDEL}; color:{INK}; font-size:11px; padding:3px 9px; border-radius:20px;'
                    )
                ui.label(flight['airline_route']).style('font-size:15px; font-weight:500;')
                ui.label(flight['times']).style(f'font-size:12.5px; color:{MUTED}; margin-top:2px;')
                ui.label(flight['price']).style(f'font-size:18px; font-weight:500; color:{INK}; margin-top:8px;')
                if flight.get('converted_note'):
                    ui.label(flight['converted_note']).style(f'font-size:12px; color:{MUTED};')

            with ui.column().style(f'{CARD_STYLE} padding:14px 16px; flex:1; min-width:220px; gap:0;'):
                with ui.row().classes('w-full justify-between items-center').style('margin-bottom:8px;'):
                    ui.label('RECOMMENDED STAY').style(f'font-size:13px; color:{MUTED};')
                    ui.label(f"{hotel['alt_count']} alternatives").style(
                        f'background:{ROUNDEL}; color:{INK}; font-size:11px; padding:3px 9px; border-radius:20px;'
                    )
                ui.label(hotel['name']).style('font-size:15px; font-weight:500;')
                ui.label(hotel['rating_distance']).style(f'font-size:12.5px; color:{MUTED}; margin-top:2px;')
                ui.label(hotel['price']).style(f'font-size:18px; font-weight:500; color:{INK}; margin-top:8px;')
                if hotel.get('converted_note'):
                    ui.label(hotel['converted_note']).style(f'font-size:12px; color:{MUTED};')

        # --- Dedicated space for the remaining flight / hotel options -------
        # `options` is the full ranked list (best option included at index 0),
        # so skip the first entry here since it's already shown above.
                # --- Dedicated space for remaining options ---

        flight_alternatives = (flight.get('options') or [])[1:]
        hotel_alternatives = (hotel.get('options') or [])[1:]

        print("\n========== CURRENCY DEBUG ==========")

        for i, opt in enumerate(flight_alternatives[:3]):
            print(
                f"FLIGHT {i}:",
                "price =", opt.get("price"),
                "| converted_note =", opt.get("converted_note"),
            )

        for i, opt in enumerate(hotel_alternatives[:3]):
            print(
                f"HOTEL {i}:",
                "price =", opt.get("price"),
                "| converted_note =", opt.get("converted_note"),
            )

        print("====================================\n")

        if flight_alternatives or hotel_alternatives:

            with ui.row().classes('w-full').style(
                'gap:14px; margin-bottom:18px; '
                'flex-wrap:wrap; align-items:flex-start;'
            ):

                if flight_alternatives:

                    with ui.column().style(
                        f'{CARD_STYLE} padding:14px 16px; '
                        f'flex:1; min-width:220px; gap:0;'
                    ):

                        ui.label('OTHER FLIGHT OPTIONS').style(
                            f'font-size:13px; color:{MUTED}; margin-bottom:4px;'
                        )

                        for opt in flight_alternatives[:3]:

                            _option_row(
                                opt['airline_route'],
                                opt['times'],
                                opt['price'],
                                opt.get('converted_note'),
                            )

                if hotel_alternatives:

                    with ui.column().style(
                        f'{CARD_STYLE} padding:14px 16px; '
                        f'flex:1; min-width:220px; gap:0;'
                    ):

                        ui.label('OTHER STAY OPTIONS').style(
                            f'font-size:13px; color:{MUTED}; margin-bottom:4px;'
                        )

                        for opt in hotel_alternatives[:3]:

                            _option_row(
                                opt['name'],
                                opt['rating_distance'],
                                opt['price'],
                                opt.get('converted_note'),
                            )

        ui.label('WEATHER FORECAST').style(f'font-size:13px; color:{MUTED}; margin-bottom:10px;')
        with ui.row().classes('w-full').style('gap:8px;'):
            for day in weather:
                icon = WEATHER_ICONS.get(day['condition'], 'ti-sun')
                color = WEATHER_COLORS.get(day['condition'], MUSTARD)
                with ui.column().classes('items-center').style(f'{CARD_STYLE} padding:10px; flex:1; gap:2px;'):
                    ui.label(day['day']).style(f'font-size:11px; color:{MUTED};')
                    ui.html(f'<i class="ti {icon}" style="font-size:18px;color:{color};margin:4px 0;display:block;" aria-hidden="true"></i>')
                    ui.label(day['temp']).style('font-size:13px; font-weight:500;')
