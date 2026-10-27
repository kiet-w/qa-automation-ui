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

    embed_media = "--embed-media" in sys.argv or "--embed-video" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    json_path = Path(args[0]) if len(args) > 0 else (reports_dir / "report.json")
    output_html_path = Path(args[1]) if len(args) > 1 else None

    generator = ReportGenerator(workspace_dir=workspace_dir)
    try:
        html_out = generator.generate(
            json_path=json_path,
            output_html_path=output_html_path,
            embed_media=embed_media,
        )

        # Also auto-generate Minimalist Clean Report
        import shutil
        from reporting.clean_report import generate_clean_report
        clean_html_path = json_path.parent / "bao_cao_tinh_gon.html"
        generate_clean_report(json_path=json_path, output_html_path=clean_html_path)
        print(f"✨ Minimalist Clean Report generated: {clean_html_path}")

        # Also maintain workspace-level root reports/bao_cao_tinh_gon.html
        root_clean_html = workspace_dir / "reports" / "bao_cao_tinh_gon.html"
        if clean_html_path.resolve() != root_clean_html.resolve():
            root_clean_html.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(clean_html_path, root_clean_html)
    except Exception as exc:
        print(f"[Error] Failed to generate execution report: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
