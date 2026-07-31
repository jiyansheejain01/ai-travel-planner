from nicegui import ui

from components.dashboard.dashboard_theme import (
    CARD,
    CARD_STYLE,
    BUDGET_COLORS,
    GREEN,
    GREEN_BG,
    GREEN_BORDER,
    AMBER_BG,
    AMBER_BORDER,
    AMBER_TEXT,
    BLUE,
    MUSTARD,
    MUTED,
    INK,
    FAINT,
    LINE,
    ROUNDEL,
    _section_label,
)

# ---------------------------------------------------------------------------
# 4. Budget + places + recommendations + alerts + timeline
# ---------------------------------------------------------------------------
def build_budget_and_insights(budget: dict, places: list[dict], recommendations: list[str],
                               alerts: list[dict], timeline_steps: list[str]) -> None:
    """
    budget: {categories: [{name, amount, pct}], total, remaining}
    places: [{name, hidden_gem: bool}]
    alerts: [{type ('warning'|'success'), text}]
    """
    with ui.column().classes('w-full').style(f'{CARD_STYLE} padding:20px 24px; gap:0;'):
        _section_label('BUDGET BREAKDOWN')
 
        with ui.column().classes('w-full').style(f'{CARD_STYLE} padding:16px 18px; margin-bottom:18px; gap:0;'):
            bar_segments = ''.join(
                f'<div style="width:{c["pct"]}%;background:{BUDGET_COLORS[i % len(BUDGET_COLORS)]};"></div>'
                for i, c in enumerate(budget['categories'])
            )
            ui.html(f'<div style="display:flex;height:10px;border-radius:6px;overflow:hidden;margin-bottom:14px;">{bar_segments}</div>')
 
            with ui.row().classes('w-full').style('flex-wrap:wrap; gap:10px 18px;'):
                for i, cat in enumerate(budget['categories']):
                    color = BUDGET_COLORS[i % len(BUDGET_COLORS)]
                    with ui.row().classes('items-center justify-between').style('flex:1 1 30%; min-width:140px; font-size:12.5px;'):
                        with ui.row().classes('items-center').style('gap:6px;'):
                            ui.html(f'<span style="display:inline-block;width:8px;height:8px;border-radius:2px;background:{color};"></span>')
                            ui.label(cat['name'])
                        ui.label(cat['amount'])
 
            with ui.row().classes('w-full justify-between').style(f'border-top:0.5px solid {ROUNDEL}; margin-top:14px; padding-top:12px;'):
                with ui.column().style('gap:0;'):
                    ui.label('TOTAL ESTIMATED').style(f'font-size:11px; color:{MUTED};')
                    ui.label(budget['total']).style('font-size:16px; font-weight:500;')
                with ui.column().classes('items-end').style('gap:0;'):
                    ui.label('UNDER BUDGET BY').style(f'font-size:11px; color:{MUTED};')
                    ui.label(budget['remaining']).style(f'font-size:16px; font-weight:500; color:{GREEN};')
 
        with ui.row().classes('w-full').style('gap:18px; flex-wrap:wrap;'):
            with ui.column().style('flex:1.3 1 320px; gap:0;'):
                _section_label('PLACES TO VISIT')
                with ui.row().style('gap:6px; flex-wrap:wrap; margin-bottom:16px;'):
                    for place in places:
                        label = f"hidden: {place['name']}" if place.get('hidden_gem') else place['name']
                        color = FAINT if place.get('hidden_gem') else INK
                        ui.label(label).style(
                            f'border:0.5px solid {LINE}; background:{CARD}; color:{color}; '
                            f'font-size:12px; padding:5px 12px; border-radius:20px;'
                        )
 
                _section_label('AI RECOMMENDATIONS')
                with ui.column().style('gap:6px;'):
                    for tip in recommendations:
                        with ui.row().classes('items-start').style('gap:6px;'):
                            ui.html(f'<i class="ti ti-bulb" style="font-size:14px;color:{BLUE};margin-top:2px;" aria-hidden="true"></i>')
                            ui.label(tip).style(f'font-size:12.5px; color:{MUTED}; line-height:1.6;')
 
            with ui.column().style('flex:1 1 220px; gap:0;'):
                _section_label('ALERTS')
                for alert in alerts:
                    is_warning = alert['type'] == 'warning'
                    bg, border, color, icon = (
                        (AMBER_BG, AMBER_BORDER, AMBER_TEXT, 'ti-cloud-rain') if is_warning
                        else (GREEN_BG, GREEN_BORDER, INK, 'ti-check')
                    )
                    ui.html(
                        f'<div style="background:{bg};border:0.5px solid {border};border-radius:10px;'
                        f'padding:10px 12px;font-size:12px;color:{color};margin-bottom:8px;">'
                        f'<i class="ti {icon}" style="font-size:14px;margin-right:5px;" aria-hidden="true"></i>{alert["text"]}</div>'
                    )
 
                ui.label('PLANNING TIMELINE').style(f'font-size:12px; letter-spacing:1.5px; color:{MUSTARD}; margin:10px 0 10px;')
                with ui.column().style('gap:6px;'):
                    for step in timeline_steps:
                        ui.label(step).style(f'font-size:12px; color:{MUTED};')
 