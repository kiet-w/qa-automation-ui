"""
reporting - Modular UI Automation Report Generator Package.
"""

from pathlib import Path
from typing import Optional

from reporting.core.builder import ReportGenerator


def generate_report(
    json_path: Optional[Path] = None,
    output_html_path: Optional[Path] = None,
) -> Path:
    """Convenience helper to generate an execution report with default or custom paths."""
    generator = ReportGenerator()
    return generator.generate(json_path=json_path, output_html_path=output_html_path)


__all__ = ["ReportGenerator", "generate_report"]
