from nicegui import ui

from components.dashboard.dashboard_theme import (
    CARD_STYLE,
    GREEN,
    MUSTARD,
    BLUE,
    FAINT,
    LINE,
    ROUNDEL,
    MUTED,
    INK,
    _section_label,
)

# ---------------------------------------------------------------------------
# 2. Agent execution grid
# ---------------------------------------------------------------------------
def build_agent_grid(agents: list[dict], future_agents: list[str], on_view_details=None) -> None:
    """
    agents: [{ name, status ('done'|'running'|'queued'|'error'), time, confidence, summary }]
    future_agents: [str] plain names, shown muted
    on_view_details: optional callable(agent_name)
    """
    status_colors = {'done': GREEN, 'running': MUSTARD, 'queued': FAINT, 'error': '#B23A3A'}
 
    with ui.column().classes('w-full').style(f'{CARD_STYLE} padding:20px 24px; gap:0;'):
        _section_label('AGENT EXECUTION')
 
        with ui.row().classes('w-full').style('flex-wrap:wrap; gap:12px;'):
            for agent in agents:
                dot_color = status_colors.get(agent['status'], FAINT)
                with ui.column().style(
                    f'{CARD_STYLE} padding:14px 16px; flex:1 1 190px; min-width:190px; gap:0;'
                ):
                    with ui.row().classes('w-full justify-between items-center').style('margin-bottom:8px;'):
                        ui.label(agent['name']).style('font-size:13.5px; font-weight:500;')
                        ui.html(f'<span style="width:7px;height:7px;border-radius:50%;background:{dot_color};display:block;"></span>')
                    ui.label(f"{agent['time']} · {agent['confidence']} confidence").style(
                        f'font-size:11.5px; color:{MUTED}; margin-bottom:6px;'
                    )
                    ui.label(agent['summary']).style(
                        f'font-size:12.5px; color:{MUTED}; line-height:1.4; margin-bottom:8px;'
                    )
                    ui.link('View details', '#').style(f'font-size:12px; color:{BLUE};').on(
                        'click', lambda a=agent['name']: (on_view_details or (lambda _: None))(a)
                    )
 
        with ui.column().classes('w-full').style(f'margin-top:16px; padding-top:14px; border-top:0.5px solid {LINE}; gap:8px;'):
            ui.label('COMING SOON').style(f'font-size:11px; color:{MUTED};')
            with ui.row().style('gap:8px; flex-wrap:wrap;'):
                for name in future_agents:
                    ui.label(name).style(
                        f'background:{ROUNDEL}; color:{FAINT}; font-size:12px; padding:6px 12px; border-radius:20px;'
                    )
 
 