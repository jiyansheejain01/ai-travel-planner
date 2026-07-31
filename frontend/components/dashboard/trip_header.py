from nicegui import ui

from components.dashboard.dashboard_theme import (
    CARD_STYLE,
    BLUE,
    GREEN,
    LINE,
    MUSTARD,
    MUTED,
    INK,
    CARD,
    ROUNDEL,
)

# ---------------------------------------------------------------------------
# 1. Trip overview + AI planner summary + quick actions
# ---------------------------------------------------------------------------
def build_trip_header(trip: dict, actions: dict | None = None) -> None:
    """
    trip: {
        title, destination, dates, duration, travelers, budget, trip_type,
        interests: [str], summary,
        planner_status, confidence, planning_time, agents_used
    }
    actions: optional dict of callables keyed by
        'edit', 'regenerate', 'add_activity', 'export', 'save'
    """
    actions = actions or {}
 
    with ui.column().classes('w-full').style(f'{CARD_STYLE} padding:20px 24px; gap:0;').props(''):
        with ui.row().classes('w-full justify-between items-start').style('flex-wrap:wrap; gap:16px; margin-bottom:16px;'):
            with ui.column().style('gap:2px;'):
                ui.label('TRIP OVERVIEW').style(f'font-size:12px; letter-spacing:1.5px; color:{MUSTARD};')
                ui.label(trip['title']).style(
                    f'font-family:Fraunces,serif; font-size:26px; font-weight:500; color:{INK};'
                )
                ui.label(
                    f"{trip['destination']} · {trip['dates']} · {trip['duration']} · {trip['travelers']}"
                ).style(f'font-size:13px; color:{MUTED};')
 
            with ui.row().style('gap:10px; flex-wrap:wrap;'):
                for pill in (trip['budget'], trip['trip_type']):
                    ui.label(pill).style(
                        f'background:{ROUNDEL}; color:{INK}; font-size:12px; padding:6px 12px; border-radius:20px;'
                    )
 
        with ui.row().style('gap:6px; flex-wrap:wrap; margin-bottom:16px;'):
            for interest in trip['interests']:
                ui.label(interest).style(
                    f'border:0.5px solid {LINE}; background:{CARD}; color:{MUTED}; '
                    f'font-size:12px; padding:5px 12px; border-radius:20px;'
                )
 
        ui.label(trip['summary']).style(
            f'background:{CARD}; border:0.5px solid {LINE}; border-radius:12px; '
            f'padding:14px 16px; font-size:13px; color:{MUTED}; line-height:1.6; margin-bottom:16px;'
        )
 
        with ui.row().classes('w-full').style(
            f'background:{CARD}; border:0.5px solid {LINE}; border-radius:12px; '
            f'padding:14px 16px; margin-bottom:16px; gap:0;'
        ):
            stats = [
                ('STATUS', trip['planner_status'], GREEN),
                ('CONFIDENCE', trip['confidence'], INK),
                ('PLANNING TIME', trip['planning_time'], INK),
                ('AGENTS USED', trip['agents_used'], INK),
            ]
            for i, (label, value, color) in enumerate(stats):
                border = f'border-left:0.5px solid {LINE};' if i else ''
                with ui.column().classes('items-center').style(f'flex:1; {border}'):
                    ui.label(label).style(f'font-size:11px; color:{MUTED};')
                    ui.label(value).style(f'font-size:15px; font-weight:500; color:{color}; margin-top:2px;')
 
        with ui.row().style('gap:8px; flex-wrap:wrap;'):
            def action_button(icon: str, text: str, key: str, primary: bool = False):
                style = (
                    f'background:{BLUE}; color:white; border:none;'
                    if primary else
                    f'border:0.5px solid {LINE}; background:{CARD}; color:{INK};'
                )
                icon_color = 'white' if primary else BLUE
                with ui.button(on_click=actions.get(key, lambda: ui.notify(text))).props('flat no-caps').style(
                    f'{style} font-size:12.5px; padding:8px 14px; border-radius:8px;'
                ):
                    with ui.row().classes('items-center').style('gap:6px;'):
                        ui.html(f'<i class="ti {icon}" style="font-size:15px;color:{icon_color};" aria-hidden="true"></i>')
                        ui.label(text)
 
            action_button('ti-edit', 'Edit trip', 'edit')
            action_button('ti-refresh', 'Regenerate plan', 'regenerate')
            action_button('ti-plus', 'Add activity', 'add_activity')
            action_button('ti-download', 'Export', 'export')
            action_button('ti-device-floppy', 'Save trip', 'save', primary=True)
 