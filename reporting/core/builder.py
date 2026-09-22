"""
reporting/core/builder.py - Assembles HTML structure, SVG graphics, CSS styles, and JS scripts.
"""

import html
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from reporting.assets import get_report_css, get_report_js
from reporting.charts import (
    generate_donut_chart_svg,
    generate_duration_bar_chart_svg,
    generate_pipeline_svg,
)
from reporting.core.parser import load_report_json, process_report_data


def build_test_cards_html(processed_tests: List[Dict[str, Any]]) -> str:
    """Builds HTML markup for all test case cards, video players, steps, and tracebacks."""
    tests_html_parts = []
    for test in processed_tests:
        t_idx = test["index"]
        t_name = test["name"]
        t_node = test["nodeid"]
        t_status = test["outcome"].upper()
        t_dur = test["duration"]
        t_video_b64 = test["video_b64"]
        t_steps = test["steps"]
        t_err = test["error_msg"]

        status_class = (
            "badge-passed"
            if t_status == "PASSED"
            else ("badge-failed" if t_status == "FAILED" else "badge-skipped")
        )

        test_card = f"""
        <div class="card test-card" id="test-card-{t_idx}">
            <div class="test-header">
                <div class="test-title-box">
                    <span class="status-badge {status_class}">{t_status}</span>
                    <h3 class="test-title">{html.escape(t_name)}</h3>
                </div>
                <div class="test-meta">
                    <span class="meta-tag"><span data-i18n="lbl_duration">Duration:</span> <strong>{t_dur:.2f}s</strong></span>
                    <span class="meta-tag meta-nodeid">{html.escape(t_node)}</span>
                </div>
            </div>
        """

        # Video section if present
        if t_video_b64:
            test_card += f"""
            <div class="video-section" id="video-section-{t_idx}">
                <div class="section-title-bar">
                    <div class="section-title-text">
                        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect>
                            <line x1="7" y1="2" x2="7" y2="22"></line>
                            <line x1="17" y1="2" x2="17" y2="22"></line>
                            <line x1="2" y1="12" x2="22" y2="12"></line>
                            <line x1="2" y1="7" x2="7" y2="7"></line>
                            <line x1="2" y1="17" x2="7" y2="17"></line>
                            <line x1="17" y1="17" x2="22" y2="17"></line>
                            <line x1="17" y1="7" x2="22" y2="7"></line>
                        </svg>
                        <span data-i18n="video_title">Execution Video Recording</span>
                    </div>
                    <div class="video-status-indicators">
                        <span class="video-timestamp-live" id="video-time-display-{t_idx}">00:00.0</span>
                        <span class="badge" style="background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35); font-weight: 700;">Full HD 1080p</span>
                        <span class="badge badge-subtle" data-i18n="video_badge">WebM Playback (Offline)</span>
                    </div>
                </div>
                <div class="video-container" id="video-container-{t_idx}">
                    <video id="video-player-{t_idx}" controls preload="metadata" class="video-player" ontimeupdate="syncVideoWithDiagram({t_idx}, this.currentTime)">
                        <source src="{t_video_b64}" type="video/webm">
                        Your browser does not support WebM video playback.
                    </video>
                </div>
            </div>
            """
        elif test.get("video_path"):
            test_card += """
            <div class="video-section">
                <div class="notice-box" data-i18n="video_missing_file">Video recording file exists on disk but could not be embedded.</div>
            </div>
            """

        # Steps container
        if t_steps:
            test_card += f"""
            <div class="steps-section">
                <div class="section-title-bar">
                    <div class="section-title-text">
                        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="9 11 12 14 22 4"></polyline>
                            <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
                        </svg>
                        <span data-i18n="steps_title">Execution Steps & Evidence</span>
                    </div>
                    <span class="badge badge-subtle">{len(t_steps)} <span data-i18n="lbl_steps_recorded">steps</span></span>
                </div>
                <div class="steps-grid">
            """

            for s in t_steps:
                s_idx = s["index"]
                s_title = s["title"]
                s_status = s["status"].upper()
                s_dur = s["duration"]
                s_start = s["start_time"]
                s_end = s["end_time"]
                s_err = s["error"]
                s_b64 = s["screenshot_b64"]
                s_badge_class = "badge-passed" if s_status == "PASSED" else "badge-failed"

                card_id = f"step-card-{t_idx}-{s_idx - 1}"

                screenshot_markup = ""
                if s_b64:
                    safe_title_attr = html.escape(s_title).replace("'", "\\'")
                    screenshot_markup = f"""
                    <div class="step-evidence-box">
                        <div class="evidence-header">
                            <span class="evidence-label" data-i18n="screenshot_evidence">Screenshot Evidence:</span>
                            <span class="evidence-hint" data-i18n="click_to_zoom">Click to view full resolution</span>
                        </div>
                        <div class="screenshot-thumb-wrapper" onclick="openLightbox('{s_b64}', '{safe_title_attr}')">
                            <img src="{s_b64}" alt="Step {s_idx} Evidence" class="screenshot-thumb" loading="lazy" />
                            <div class="thumb-overlay">
                                <svg class="zoom-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="11" cy="11" r="8"></circle>
                                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                                    <line x1="11" y1="8" x2="11" y2="14"></line>
                                    <line x1="8" y1="11" x2="14" y2="11"></line>
                                </svg>
                                <span data-i18n="expand_image">Enlarge</span>
                            </div>
                        </div>
                    </div>
                    """

                error_markup = ""
                if s_err:
                    error_markup = f"""
                    <div class="step-error-box">
                        <strong data-i18n="step_error_label">Step Failure:</strong>
                        <pre class="code-block">{html.escape(str(s_err))}</pre>
                    </div>
                    """

                test_card += f"""
                <div class="step-card" id="{card_id}" data-test-idx="{t_idx}" data-step-idx="{s_idx - 1}" data-start="{s_start:.2f}" data-end="{s_end:.2f}">
                    <div class="step-card-header">
                        <div class="step-title-wrapper">
                            <span class="step-badge {s_badge_class}">{s_status}</span>
                            <h4 class="step-title">{html.escape(s_title)}</h4>
                        </div>
                        <div class="step-timing-actions">
                            <button class="step-time-btn" onclick="seekVideoAndScroll({s_start:.2f}, '{card_id}', {t_idx}, {s_idx - 1})" title="Seek video to {s_start:.2f}s">
                                <svg class="icon-inline" viewBox="0 0 24 24" fill="currentColor">
                                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                                </svg>
                                <span>{s_start:.1f}s - {s_end:.1f}s</span>
                            </button>
                            <div class="step-duration-pill">{s_dur:.2f}s</div>
                        </div>
                    </div>
                    {error_markup}
                    {screenshot_markup}
                </div>
                """

            test_card += "</div></div>"

        # Traceback if failed
        if t_err:
            test_card += f"""
            <div class="traceback-section">
                <div class="section-title-bar">
                    <span class="section-title-text text-danger" data-i18n="traceback_title">Failure Traceback</span>
                </div>
                <pre class="code-block traceback-block">{html.escape(str(t_err))}</pre>
            </div>
            """

        test_card += "</div>"
        tests_html_parts.append(test_card)

    return "\n".join(tests_html_parts)


def assemble_html_document(
    parsed: Dict[str, Any],
    report_data: Dict[str, Any],
) -> str:
    """Assembles the full HTML string with SVG charts, CSS styles, and client-side JS."""
    total = parsed["total"]
    passed = parsed["passed"]
    failed = parsed["failed"]
    skipped = parsed["skipped"]
    total_duration = parsed["total_duration"]
    pass_rate = parsed["pass_rate"]
    created_str = parsed["created_str"]

    donut_chart_svg = generate_donut_chart_svg(passed, failed, skipped)
    bar_chart_svg = generate_duration_bar_chart_svg(parsed["bar_items"])
    pipeline_svg = generate_pipeline_svg(parsed["primary_steps"], test_idx=0)

    rendered_tests_html = build_test_cards_html(parsed["tests"])

    env_info = report_data.get("environment", {})
    env_browser = env_info.get("Browser", "Brave (Chromium) Headed")
    env_python = env_info.get("Python", sys.version.split()[0])
    env_platform = env_info.get("Platform", sys.platform)

    css_styles = get_report_css()
    js_scripts = get_report_js()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title data-i18n="page_title">UI Automation Execution Report</title>
    <style>
{css_styles}
    </style>
</head>
<body>

    <!-- Header App Bar -->
    <header class="header-bar">
        <div class="brand-box">
            <div class="brand-icon">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2">
                    <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                    <polyline points="2 17 12 22 22 17"></polyline>
                    <polyline points="2 12 12 17 22 12"></polyline>
                </svg>
            </div>
            <div class="brand-title-group">
                <h1 data-i18n="header_title">UI Automation Execution Report</h1>
                <p data-i18n="header_subtitle">Playwright + Pytest Offline Test Intelligence</p>
            </div>
        </div>

        <div class="header-actions">
            <!-- Bilingual Switcher -->
            <div class="lang-switch" role="group" aria-label="Language Selector">
                <button id="btn-lang-en" class="lang-btn active" onclick="setLanguage('en')">
                    <span>🇬🇧</span> English
                </button>
                <button id="btn-lang-vi" class="lang-btn" onclick="setLanguage('vi')">
                    <span>🇻🇳</span> Tiếng Việt
                </button>
            </div>
        </div>
    </header>

    <main class="main-container">

        <!-- Executive KPI Overview -->
        <section class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-header">
                    <span data-i18n="kpi_total">Total Tests</span>
                    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                </div>
                <div class="kpi-value">{total}</div>
                <div class="kpi-sub"><span data-i18n="lbl_collected">Collected tests</span></div>
            </div>

            <div class="kpi-card">
                <div class="kpi-header">
                    <span data-i18n="kpi_passed">Passed</span>
                    <svg class="icon val-pass" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                        <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                </div>
                <div class="kpi-value val-pass">{passed}</div>
                <div class="kpi-sub"><span data-i18n="lbl_success_runs">Successful runs</span></div>
            </div>

            <div class="kpi-card">
                <div class="kpi-header">
                    <span data-i18n="kpi_failed">Failed</span>
                    <svg class="icon val-fail" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="15" y1="9" x2="9" y2="15"></line>
                        <line x1="9" y1="9" x2="15" y2="15"></line>
                    </svg>
                </div>
                <div class="kpi-value val-fail">{failed}</div>
                <div class="kpi-sub"><span data-i18n="lbl_error_runs">Requires attention</span></div>
            </div>

            <div class="kpi-card">
                <div class="kpi-header">
                    <span data-i18n="kpi_duration">Total Duration</span>
                    <svg class="icon val-accent" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12 6 12 12 16 14"></polyline>
                    </svg>
                </div>
                <div class="kpi-value val-accent">{total_duration:.2f}s</div>
                <div class="kpi-sub"><span data-i18n="lbl_wall_time">Execution wall time</span></div>
            </div>

            <div class="kpi-card">
                <div class="kpi-header">
                    <span data-i18n="kpi_rate">Pass Rate</span>
                    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 20V10"></path>
                        <path d="M12 20V4"></path>
                        <path d="M6 20v-6"></path>
                    </svg>
                </div>
                <div class="kpi-value val-pass">{pass_rate}%</div>
                <div class="kpi-sub"><span data-i18n="lbl_reliability">Quality rating</span></div>
            </div>
        </section>

        <!-- Pure SVG Analytics: Donut & Duration Breakdown -->
        <section class="analytics-grid">
            <!-- Donut Chart Card -->
            <div class="card">
                <div class="card-header-clean">
                    <h3 class="card-title">
                        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"></circle>
                            <path d="M12 2a10 10 0 0 1 10 10"></path>
                        </svg>
                        <span data-i18n="chart_donut_title">Result Distribution</span>
                    </h3>
                </div>
                {donut_chart_svg}
                <div class="chart-legend">
                    <div class="legend-item">
                        <span class="legend-dot dot-pass"></span>
                        <span data-i18n="lbl_legend_pass">Passed</span>: <strong>{passed}</strong>
                    </div>
                    <div class="legend-item">
                        <span class="legend-dot dot-fail"></span>
                        <span data-i18n="lbl_legend_fail">Failed</span>: <strong>{failed}</strong>
                    </div>
                    <div class="legend-item">
                        <span class="legend-dot dot-skip"></span>
                        <span data-i18n="lbl_legend_skip">Skipped</span>: <strong>{skipped}</strong>
                    </div>
                </div>
            </div>

            <!-- Duration Bar Chart Card -->
            <div class="card">
                <div class="card-header-clean">
                    <h3 class="card-title">
                        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="18" y1="20" x2="18" y2="10"></line>
                            <line x1="12" y1="20" x2="12" y2="4"></line>
                            <line x1="6" y1="20" x2="6" y2="14"></line>
                        </svg>
                        <span data-i18n="chart_bar_title">Execution Duration Breakdown (Seconds)</span>
                    </h3>
                    <span class="badge badge-subtle" data-i18n="badge_offline_svg">Pure SVG</span>
                </div>
                {bar_chart_svg}
            </div>
        </section>

        <!-- Interactive Flow Pipeline -->
        <section class="card pipeline-card">
            <div class="card-header-clean">
                <h3 class="card-title">
                    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                    </svg>
                    <span data-i18n="pipeline_title">Interactive Step Execution Pipeline</span>
                </h3>
                <span class="badge badge-subtle" data-i18n="pipeline_hint">Click any node to seek video to that step</span>
            </div>
            {pipeline_svg}
        </section>

        <!-- Test Cases & Evidence Container -->
        <section class="test-suite-container">
            {rendered_tests_html}
        </section>

        <!-- Environment & Execution Metadata Footer -->
        <footer class="env-footer">
            <div class="env-items">
                <span class="env-item"><span data-i18n="env_browser">Browser:</span> <strong>{html.escape(env_browser)}</strong></span>
                <span class="env-item"><span data-i18n="env_python">Python:</span> <strong>{html.escape(env_python)}</strong></span>
                <span class="env-item"><span data-i18n="env_platform">Platform:</span> <strong>{html.escape(env_platform)}</strong></span>
                <span class="env-item"><span data-i18n="env_executed">Executed At:</span> <strong>{created_str}</strong></span>
            </div>
            <div class="env-copy">
                <span data-i18n="footer_signature">Self-contained Playwright Test Report Generator</span>
            </div>
        </footer>

    </main>

    <!-- Lightbox Modal for Screenshot Zooming -->
    <div id="lightboxModal" class="lightbox-modal" onclick="handleLightboxClick(event)">
        <div class="lightbox-content" onclick="event.stopPropagation()">
            <div class="lightbox-header">
                <h4 id="lightboxTitle">Execution Evidence Screenshot</h4>
                <button class="lightbox-close" onclick="closeLightbox()" title="Close (Esc)">&times;</button>
            </div>
            <div class="lightbox-body">
                <img id="lightboxImg" src="" alt="Zoomed Screenshot" class="lightbox-img" />
            </div>
        </div>
    </div>

    <!-- Floating Seek Notification Toast -->
    <div id="seekToast" class="seek-toast">
        <svg class="toast-icon" viewBox="0 0 24 24" fill="currentColor">
            <polygon points="5 3 19 12 5 21 5 3"></polygon>
        </svg>
        <span id="seekToastText">Video seeked</span>
    </div>

    <!-- Inline JavaScript -->
    <script>
{js_scripts}
    </script>
</body>
</html>
"""


class ReportGenerator:
    """Coordinates data loading, media encoding, SVG rendering, and file export."""

    def __init__(self, workspace_dir: Optional[Path] = None):
        self.workspace_dir = workspace_dir or Path(__file__).resolve().parent.parent.parent
        self.reports_dir = self.workspace_dir / "reports"
        self.test_results_dir = self.reports_dir / "test-results"

    def generate(
        self,
        json_path: Optional[Path] = None,
        output_html_path: Optional[Path] = None,
    ) -> Path:
        """Executes full report generation and writes self-contained HTML file."""
        json_file = json_path or (self.reports_dir / "report.json")
        target_html = output_html_path or (self.reports_dir / "execution_report.html")

        print("=" * 65)
        print("🚀 [UI Automation Report Generator (Modular)]")
        print(f"   Input JSON : {json_file}")
        print(f"   Output HTML: {target_html}")
        print("=" * 65)

        self.reports_dir.mkdir(parents=True, exist_ok=True)
        report_data = load_report_json(json_file)

        all_videos: List[Path] = []
        if self.test_results_dir.exists():
            all_videos = sorted(list(self.test_results_dir.glob("**/*.webm")))
            if all_videos:
                print(f"📹 Found {len(all_videos)} video recording(s) in {self.test_results_dir.name}")
                for v in all_videos:
                    size_mb = v.stat().st_size / (1024 * 1024)
                    print(f"   -> {v.name} ({size_mb:.2f} MB)")

        parsed_data = process_report_data(
            report_data=report_data,
            all_videos=all_videos,
            reports_dir=self.reports_dir,
            workspace_dir=self.workspace_dir,
        )

        full_html = assemble_html_document(
            parsed=parsed_data,
            report_data=report_data,
        )

        target_html.parent.mkdir(parents=True, exist_ok=True)
        with open(target_html, "w", encoding="utf-8") as f:
            f.write(full_html)

        file_size_mb = target_html.stat().st_size / (1024 * 1024)
        print("✅ Report successfully generated!")
        print(f"   Location : {target_html}")
        print(f"   File Size: {file_size_mb:.2f} MB (100% self-contained)")
        print("=" * 65)

        return target_html
