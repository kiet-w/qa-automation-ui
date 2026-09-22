"""
reporting/assets - Manages raw CSS styles and modular client-side JavaScript files.
"""

from pathlib import Path


def get_report_css() -> str:
    """Reads and returns the complete CSS stylesheet."""
    css_file = Path(__file__).parent / "report.css"
    if css_file.exists():
        return css_file.read_text(encoding="utf-8")
    return ""


def get_report_js() -> str:
    """
    Reads and returns the complete client-side JavaScript.
    Loads modular scripts from `js/` directory in sequence, or falls back to `report.js`.
    """
    js_dir = Path(__file__).parent / "js"
    if js_dir.exists():
        ordered_modules = ["i18n.js", "views.js", "video.js", "lightbox.js", "main.js"]
        module_contents = []
        for mod in ordered_modules:
            mod_path = js_dir / mod
            if mod_path.exists():
                module_contents.append(mod_path.read_text(encoding="utf-8"))
        if module_contents:
            return "(function () {\n\"use strict\";\n\n" + "\n\n".join(module_contents) + "\n})();"

    js_file = Path(__file__).parent / "report.js"
    if js_file.exists():
        return js_file.read_text(encoding="utf-8")
    return ""


__all__ = ["get_report_css", "get_report_js"]
