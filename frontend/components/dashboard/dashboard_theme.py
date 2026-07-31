from nicegui import ui

"""
Trip results dashboard for the AI Travel Planner — trail-map theme.
 
Drop into your frontend folder (e.g. frontend/pages/dashboard_page.py).
Data-driven: pass real agent/trip output into `build_dashboard(...)`;
falls back to sample data when run standalone for preview.
 
    python dashboard_page.py
 
Sections implemented here, matching the mockups:
  1. Trip overview + AI planner summary + quick actions
  2. Agent execution grid (+ future agents strip)
  3. Daily itinerary + best flight / hotel + weather strip
  4. Budget breakdown + places to visit + AI recommendations + alerts + timeline
 
Not included (functional, not visual — see notes at bottom of file):
  - Interactive map            -> wire up ui.leaflet() with real coordinates
  - Transportation section     -> reuse `_itinerary_row` pattern below
"""
 
from nicegui import ui
 
# ---------------------------------------------------------------------------
# Shared palette — same tokens as landing_page.py
# ---------------------------------------------------------------------------
BG = '#F7F5F0'
INK = '#33342E'
MUTED = '#6B6D63'
FAINT = '#8A897F'
LINE = '#DEDBD0'
BLUE = '#5B7C99'
MUSTARD = '#D4A24C'
CARD = '#FFFFFF'
ROUNDEL = '#EDEBE2'
GREEN = '#3D6B4E'
GREEN_BG = '#EAF1EC'
GREEN_BORDER = '#C7DACD'
AMBER_BG = '#FBF3E4'
AMBER_BORDER = '#EAD9B4'
AMBER_TEXT = '#7A5A20'
 
BUDGET_COLORS = ['#5B7C99', '#D4A24C', '#8FA998', '#C9C6B6', '#B98F6B', '#DEDBD0']
 
LABEL = f'font-size:12px; letter-spacing:1.5px; color:{MUSTARD}; margin-bottom:10px;'
CARD_STYLE = f'background:{CARD}; border:0.5px solid {LINE}; border-radius:12px;'
 
 
def _load_fonts_and_icons() -> None:
    ui.add_head_html('''
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@500&display=swap" rel="stylesheet">
    ''')
 
 
def _page_style() -> None:
    ui.query('body').style(f'background:{BG};')
 
 
def _section_label(text: str) -> None:
    ui.label(text).style(LABEL)

def apply_dashboard_theme():
    _load_fonts_and_icons()
    _page_style()
    ui.colors(primary=BLUE, secondary=MUSTARD)
 
 