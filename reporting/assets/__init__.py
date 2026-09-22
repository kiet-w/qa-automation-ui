"""
reporting/assets - Manages raw CSS styles and client-side JavaScript files.
"""

from pathlib import Path


def get_report_css() -> str:
    """Reads and returns the complete CSS stylesheet."""
    css_file = Path(__file__).parent / "report.css"
    if css_file.exists():
        return css_file.read_text(encoding="utf-8")
    return ""


def get_report_js() -> str:
    """Reads and returns the complete client-side JavaScript."""
    js_file = Path(__file__).parent / "report.js"
    if js_file.exists():
        return js_file.read_text(encoding="utf-8")
    return ""


__all__ = ["get_report_css", "get_report_js"]
