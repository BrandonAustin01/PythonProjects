# converter/themes.py
from pathlib import Path

def load_theme_css(theme_name):
    path = Path(__file__).parent.parent / "themes" / f"{theme_name}.css"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""
