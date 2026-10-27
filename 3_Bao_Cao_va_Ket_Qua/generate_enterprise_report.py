#!/usr/bin/env python3
"""
generate_enterprise_report.py - CLI & Programmatic Enterprise Execution Report Generator.

Theme: Google Sheets / Apple Minimalist Clean (Zero Emoji Clutter, Pure Typography, Clean Pill Dots).
Features:
- Dynamic parsing for ANY test suite (FS-08, FS-09, UAT, Break-It, Unit, etc.).
- Bento Grid Executive Metrics (Scenarios, Steps, Duration, Quality Gate).
- Dynamic Executive Takeaways with actionable business & defect insights.
- Google Sheets Enterprise Test Matrix Table with live fx formula search.
- Dedicated HTML5 Video Player with speed controls (0.5x, 0.75x, 1.0x, 1.25x).
- Synchronized Defect Overlay ("🎯 DEFECT CAPTURE: <error_msg>").
- Interactive Defect Spotlight Reticle with pulsating radar highlight ("🎯 Điểm Lỗi").
- Synchronized active step indicator ("Đang phát: Bước X" / "❌ Bước X: THẤT BẠI").
- Interactive Step Execution Pipeline seeking video directly to s.start on click.
- High-contrast Error Traceback terminal callout box for failed steps.
- High-resolution Screenshot preview with Fullscreen Lightbox zoom.
- 100% Offline-capable via embedded fallback CSS.

Usage:
    python generate_enterprise_report.py [path_to_report_json_or_folder] [output_html_path] [--embed-media]
"""

import sys
from pathlib import Path
from typing import Optional, Union

from reporting.core.builder import ReportGenerator, build_enterprise_html
from reporting.core.parser import load_report_json, process_report_data


def build_enterprise_report_from_file(
    input_path: Union[str, Path],
    output_html_path: Optional[Union[str, Path]] = None,
    workspace_dir: Optional[Path] = None,
    embed_media: bool = False,
) -> Path:
    """
    Compiles report.json into a high-contrast enterprise test execution dashboard.
    Accepts either a directory containing report.json or a direct path to report.json.
    """
    workspace_dir = workspace_dir or Path(__file__).resolve().parent
    in_p = Path(input_path).resolve()

    if in_p.is_dir():
        json_file = in_p / "report.json"
        reports_dir = in_p
    else:
        json_file = in_p
        reports_dir = in_p.parent

    if not json_file.exists():
        raise FileNotFoundError(f"Report JSON not found at: {json_file}")

    if output_html_path:
        out_file = Path(output_html_path).resolve()
    else:
        out_file = reports_dir / "execution_report.html"

    generator = ReportGenerator(workspace_dir=workspace_dir, reports_dir=reports_dir)
    return generator.generate(
        json_path=json_file,
        output_html_path=out_file,
        embed_media=embed_media,
    )


# Backward-compatible helper function
def build_enterprise_html(report_dir_or_json: Union[str, Path]) -> str:
    """
    Loads report data and returns the raw compiled enterprise HTML string.
    Maintains backward compatibility with earlier scripts.
    """
    workspace_dir = Path(__file__).resolve().parent
    in_p = Path(report_dir_or_json).resolve()

    if in_p.is_dir():
        json_file = in_p / "report.json"
        reports_dir = in_p
    else:
        json_file = in_p
        reports_dir = in_p.parent

    report_data = load_report_json(json_file)
    parsed = process_report_data(
        report_data=report_data,
        all_videos=[],
        reports_dir=reports_dir,
        workspace_dir=workspace_dir,
        embed_media=False,
    )

    from reporting.core.enterprise_builder import build_enterprise_html as _core_build
    return _core_build(
        parsed=parsed,
        report_data=report_data,
        reports_dir=reports_dir,
        workspace_dir=workspace_dir,
        embed_media=False,
    )


def main():
    workspace_dir = Path(__file__).resolve().parent
    default_report_dir = workspace_dir / "reports" / "fs08" / "fs08-parent-profile"

    embed_media = "--embed-media" in sys.argv or "--embed-video" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if len(args) > 0:
        target_input = Path(args[0])
    else:
        target_input = default_report_dir

    if len(args) > 1:
        target_output = Path(args[1])
    else:
        if target_input.is_dir():
            target_output = target_input / "execution_report.html"
        else:
            target_output = target_input.parent / "execution_report.html"

    print("=" * 70)
    print("🚀 [Enterprise Report Engine Architect]")
    print(f"   Input       : {target_input}")
    print(f"   Target HTML : {target_output}")
    print(f"   Media Mode  : {'Embedded Base64' if embed_media else 'Linked Relative Media'}")
    print("=" * 70)

    try:
        out_path = build_enterprise_report_from_file(
            input_path=target_input,
            output_html_path=target_output,
            workspace_dir=workspace_dir,
            embed_media=embed_media,
        )
        print(f"✓ Successfully generated enterprise execution report: {out_path}")
    except Exception as exc:
        print(f"[Error] Failed to generate enterprise execution report: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
