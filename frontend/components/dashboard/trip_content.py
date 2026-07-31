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
 
 
def build_itinerary_and_travel(days: dict, flight: dict, hotel: dict, weather: list[dict],
                                selected_day: str = 'Day 2', on_day_select=None, on_regenerate_day=None) -> None:
    """
    days: { 'Day 1': [item, ...], 'Day 2': [...], ... }  (see _itinerary_row for item shape)
    flight: {airline_route, times, price, alt_count}
    hotel: {name, rating_distance, price, alt_count}
    weather: [{day, condition ('sun'|'cloud'|'rain'), temp}]
    """
    dot_cycle = [MUSTARD, BLUE]
 
    with ui.column().classes('w-full').style(f'{CARD_STYLE} padding:20px 24px; gap:0;'):
        _section_label('DAILY ITINERARY')
 
        with ui.row().classes('w-full items-center').style('gap:6px; margin-bottom:14px; flex-wrap:wrap;'):
            for day_name in days:
                is_selected = day_name == selected_day
                style = (
                    f'background:{BLUE}; color:white;' if is_selected
                    else f'border:0.5px solid {LINE}; background:{CARD}; color:{MUTED};'
                )
                ui.button(day_name, on_click=lambda d=day_name: (on_day_select or (lambda _: None))(d)).props(
                    'flat no-caps'
                ).style(f'{style} font-size:12px; padding:5px 12px; border-radius:20px;')
 
            ui.space()
            with ui.button(on_click=lambda: (on_regenerate_day or (lambda: None))()).props('flat no-caps').style(
                f'border:0.5px solid {LINE}; background:{CARD}; color:{BLUE}; font-size:12px; '
                f'padding:5px 12px; border-radius:8px;'
            ):
                with ui.row().classes('items-center').style('gap:5px;'):
                    ui.html(f'<i class="ti ti-refresh" style="font-size:14px;" aria-hidden="true"></i>')
                    ui.label('Regenerate day')
 
        with ui.column().classes('w-full').style(f'{CARD_STYLE} padding:16px 18px; margin-bottom:18px; gap:0;'):
            for i, item in enumerate(days.get(selected_day, [])):
                _itinerary_row(item, dot_cycle[i % len(dot_cycle)])
 
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
 
            with ui.column().style(f'{CARD_STYLE} padding:14px 16px; flex:1; min-width:220px; gap:0;'):
                with ui.row().classes('w-full justify-between items-center').style('margin-bottom:8px;'):
                    ui.label('RECOMMENDED STAY').style(f'font-size:13px; color:{MUTED};')
                    ui.label(f"{hotel['alt_count']} alternatives").style(
                        f'background:{ROUNDEL}; color:{INK}; font-size:11px; padding:3px 9px; border-radius:20px;'
                    )
                ui.label(hotel['name']).style('font-size:15px; font-weight:500;')
                ui.label(hotel['rating_distance']).style(f'font-size:12.5px; color:{MUTED}; margin-top:2px;')
                ui.label(hotel['price']).style(f'font-size:18px; font-weight:500; color:{INK}; margin-top:8px;')
 
        ui.label('WEATHER FORECAST').style(f'font-size:13px; color:{MUTED}; margin-bottom:10px;')
        with ui.row().classes('w-full').style('gap:8px;'):
            for day in weather:
                icon = WEATHER_ICONS.get(day['condition'], 'ti-sun')
                color = WEATHER_COLORS.get(day['condition'], MUSTARD)
                with ui.column().classes('items-center').style(f'{CARD_STYLE} padding:10px; flex:1; gap:2px;'):
                    ui.label(day['day']).style(f'font-size:11px; color:{MUTED};')
                    ui.html(f'<i class="ti {icon}" style="font-size:18px;color:{color};margin:4px 0;display:block;" aria-hidden="true"></i>')
                    ui.label(day['temp']).style('font-size:13px; font-weight:500;')
 