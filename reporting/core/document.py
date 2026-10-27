"""
reporting/core/document.py - Assembles unified Executive Enterprise HTML document.

Google Sheets / Apple Minimalist Clean theme with Bento Grid hero metrics,
interactive step pipeline, synchronized video defect overlay, and defect spotlight.
"""

from pathlib import Path
from typing import Any, Dict, Optional

from reporting.core.enterprise_builder import build_enterprise_html


def assemble_html_document(
    parsed: Dict[str, Any],
    report_data: Dict[str, Any],
    reports_dir: Optional[Path] = None,
    workspace_dir: Optional[Path] = None,
    embed_media: bool = False,
) -> str:
    """
    Assembles the standard, official executive-grade execution report HTML document.
    Google Sheets / Apple Minimalist Clean theme with Bento Grid hero metrics,
    interactive step pipeline, synchronized video defect overlay, and defect spotlight.
    """
    return build_enterprise_html(
        parsed=parsed,
        report_data=report_data,
        reports_dir=reports_dir,
        workspace_dir=workspace_dir,
        embed_media=embed_media,
    )


__all__ = ["assemble_html_document"]
