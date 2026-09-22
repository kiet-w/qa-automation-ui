#!/usr/bin/env python3
"""
generate_report.py - CLI Entrypoint for UI Automation HTML Report Generator.

Modular Architecture:
Core reporting logic is organized under the `reporting/` package:
- reporting/parser.py     : Reads report.json, calculates step timelines, extracts KPIs.
- reporting/media.py      : Matches WebM videos and PNG screenshots, encodes to Base64.
- reporting/svg_charts.py : Renders pure SVG Donut, Duration Bar, and Step Pipeline diagrams.
- reporting/styles.py     : Manages responsive Dark-theme CSS, animations, and modal styles.
- reporting/scripts.py    : Client-side JS (scroll-to-video-then-play, i18n EN/VI, lightbox).
- reporting/builder.py    : Assembles complete self-contained HTML document.

Usage:
    python generate_report.py [path_to_json] [output_html_path]
"""

import sys
from pathlib import Path

from reporting import ReportGenerator


def main():
    workspace_dir = Path(__file__).resolve().parent
    reports_dir = workspace_dir / "reports"

    json_path = Path(sys.argv[1]) if len(sys.argv) > 1 else (reports_dir / "report.json")
    output_html_path = Path(sys.argv[2]) if len(sys.argv) > 2 else (reports_dir / "execution_report.html")

    generator = ReportGenerator(workspace_dir=workspace_dir)
    try:
        generator.generate(json_path=json_path, output_html_path=output_html_path)
    except Exception as exc:
        print(f"[Error] Failed to generate execution report: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
