from pathlib import Path
from nicegui import ui


def load_theme():

    css = Path("theme/styles.css").read_text(
        encoding="utf-8"
    )

    ui.add_head_html(
        """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
"""
    )

    ui.add_head_html(
        f"<style>{css}</style>"
    )