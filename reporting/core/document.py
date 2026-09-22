"""
reporting/core/document.py - Assembles unified Single-Page HTML document.

Features:
- Single-page continuous dashboard flow (KPIs -> Analytics & Pipeline -> Video -> Steps & Evidence -> System Info).
- Left Navigation Sidebar with quick smooth-scroll anchors, Flame Logo, Theme Toggle, and Language Button.
- Top Sticky Navbar with Run ID, timestamp, and status.
- Lightbox and Toast notifications.
"""

import html
from typing import Any, Dict

from reporting.assets import get_report_css, get_report_js
from reporting.core.views_dashboard import (
    build_extent_kpi_and_charts_html,
    build_extent_sysinfo_html,
)
from reporting.core.views_tests import build_extent_tests_html


def assemble_html_document(
    parsed: Dict[str, Any],
    report_data: Dict[str, Any],
) -> str:
    """Assembles the complete self-contained Single-Page ExtentReports HTML document."""
    css_styles = get_report_css()
    js_scripts = get_report_js()

    run_id = parsed.get("run_id", "RUN-UNKNOWN")
    created_str = parsed.get("created_str", "-")
    total_duration = parsed.get("total_duration", 0.0)
    overall_status = parsed.get("overall_status", "PASSED")
    status_badge_class = "badge-top-pass" if overall_status == "PASSED" else "badge-top-fail"

    kpi_and_charts_content = build_extent_kpi_and_charts_html(parsed)
    tests_content = build_extent_tests_html(parsed.get("tests", []))
    sysinfo_content = build_extent_sysinfo_html(parsed)

    # Extent Spark Flame Icon SVG
    spark_flame_svg = """
    <svg viewBox="0 0 24 24" fill="currentColor" class="spark-logo">
        <path d="M12.75 2.05a1 1 0 0 0-1.5 0C8.5 5.5 5 9.5 5 14a7 7 0 0 0 14 0c0-4.5-3.5-8.5-6.25-11.95zM12 19a5 5 0 0 1-5-5c0-2.8 2.2-5.7 4.2-8 1.4 1.8 2.8 3.8 3.5 5.7.5 1.3.3 2.8-.7 3.8-.5.5-1.2.8-2 .5a1 1 0 0 0-1.2.7 1 1 0 0 0 .7 1.2c1.3.4 2.7 0 3.6-1 .2.7.4 1.4.4 2.1a5 5 0 0 1-5 5z"/>
    </svg>
    """

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ExtentReports - {html.escape(run_id)}</title>
    <!-- Inline Presentation Styles (ExtentReports Spark Theme) -->
    <style>
{css_styles}
    </style>
</head>
<body data-theme="dark">
    <div class="app-layout">
        <!-- ExtentReports Left Sidebar Navigation (Smooth Scroll Anchors) -->
        <nav class="side-nav">
            <div class="side-nav-inner">
                <div>
                    <div class="side-nav-brand" title="ExtentReports Spark">
                        {spark_flame_svg}
                    </div>
                    <ul class="side-nav-menu">
                        <li class="nav-item">
                            <button id="nav-btn-kpi" class="nav-btn active" onclick="scrollToSection('section-kpi')" title="KPI Summary">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <rect x="3" y="3" width="7" height="7"></rect>
                                    <rect x="14" y="3" width="7" height="7"></rect>
                                    <rect x="14" y="14" width="7" height="7"></rect>
                                    <rect x="3" y="14" width="7" height="7"></rect>
                                </svg>
                            </button>
                        </li>
                        <li class="nav-item">
                            <button id="nav-btn-analytics" class="nav-btn" onclick="scrollToSection('section-analytics')" title="Analytics & Charts">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path>
                                    <path d="M22 12A10 10 0 0 0 12 2v10z"></path>
                                </svg>
                            </button>
                        </li>
                        <li class="nav-item">
                            <button id="nav-btn-pipeline" class="nav-btn" onclick="scrollToSection('section-pipeline')" title="Step Pipeline">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="12" cy="12" r="10"></circle>
                                    <polyline points="12 6 12 12 14 14"></polyline>
                                </svg>
                            </button>
                        </li>
                        <li class="nav-item">
                            <button id="nav-btn-video" class="nav-btn" onclick="scrollToSection('section-video')" title="Video Recording">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect>
                                    <line x1="7" y1="2" x2="7" y2="22"></line>
                                    <line x1="17" y1="2" x2="17" y2="22"></line>
                                    <line x1="2" y1="12" x2="22" y2="12"></line>
                                    <line x1="2" y1="7" x2="7" y2="7"></line>
                                    <line x1="2" y1="17" x2="7" y2="17"></line>
                                    <line x1="17" y1="17" x2="22" y2="17"></line>
                                    <line x1="17" y1="7" x2="22" y2="7"></line>
                                </svg>
                            </button>
                        </li>
                        <li class="nav-item">
                            <button id="nav-btn-steps" class="nav-btn" onclick="scrollToSection('section-steps')" title="Step Log & Evidence">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <line x1="8" y1="6" x2="21" y2="6"></line>
                                    <line x1="8" y1="12" x2="21" y2="12"></line>
                                    <line x1="8" y1="18" x2="21" y2="18"></line>
                                    <line x1="3" y1="6" x2="3.01" y2="6"></line>
                                    <line x1="3" y1="12" x2="3.01" y2="12"></line>
                                    <line x1="3" y1="18" x2="3.01" y2="18"></line>
                                </svg>
                            </button>
                        </li>
                        <li class="nav-item">
                            <button id="nav-btn-system" class="nav-btn" onclick="scrollToSection('section-system')" title="System Info">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect>
                                    <rect x="9" y="9" width="6" height="6"></rect>
                                    <line x1="9" y1="1" x2="9" y2="4"></line>
                                    <line x1="15" y1="1" x2="15" y2="4"></line>
                                    <line x1="9" y1="20" x2="9" y2="23"></line>
                                    <line x1="15" y1="20" x2="15" y2="23"></line>
                                </svg>
                            </button>
                        </li>
                    </ul>
                </div>

                <!-- Bottom Tools: Theme & Language -->
                <ul class="nav-tools">
                    <li class="nav-item">
                        <button class="nav-btn" id="theme-btn" onclick="toggleTheme()" title="Toggle Theme (l)">
                            <span id="theme-icon-container">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="12" cy="12" r="5"></circle>
                                    <line x1="12" y1="1" x2="12" y2="3"></line>
                                    <line x1="12" y1="21" x2="12" y2="23"></line>
                                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                                    <line x1="1" y1="12" x2="3" y2="12"></line>
                                    <line x1="21" y1="12" x2="23" y2="12"></line>
                                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                                </svg>
                            </span>
                        </button>
                    </li>
                    <li class="nav-item">
                        <button class="lang-toggle-btn" id="lang-btn" onclick="toggleLanguage()" title="Switch Language (EN/VI)">
                            EN
                        </button>
                    </li>
                </ul>
            </div>
        </nav>

        <!-- Main Page Layout -->
        <div class="page-container">
            <!-- Top Navbar -->
            <header class="navbar-top">
                <div class="nav-brand-group">
                    <span class="nav-title-main" data-i18n="report_title">ExtentReports</span>
                    <span class="nav-title-sub" data-i18n="report_subtitle">UI Automation Test Report</span>
                </div>
                <div class="nav-meta-group">
                    <span class="pill-meta pill-run-id">
                        <span>ID:</span>
                        <span>{html.escape(run_id)}</span>
                    </span>
                    <span class="pill-meta">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"></circle>
                            <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                        <span>{html.escape(created_str)}</span>
                    </span>
                    <span class="pill-meta">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"></circle>
                            <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                        <span>{total_duration:.2f}s</span>
                    </span>
                    <span class="status-badge-top {status_badge_class}">{overall_status}</span>
                </div>
            </header>

            <!-- Main Content Area: Single Unified Continuous Page -->
            <main class="main-content">
                <!-- 1. KPIs, Charts & Pipeline -->
                {kpi_and_charts_content}

                <!-- 2. Test Execution Video & Step Log with Prominent Evidence -->
                {tests_content}

                <!-- 3. System & Environment Information -->
                {sysinfo_content}
            </main>
        </div>
    </div>

    <!-- Screenshot Lightbox Modal -->
    <div class="lightbox-modal" id="lightboxModal" onclick="closeLightbox()">
        <button class="lightbox-close-btn" onclick="closeLightbox()">&times;</button>
        <div class="lightbox-content" onclick="event.stopPropagation()">
            <img src="" alt="Screenshot Full View" class="lightbox-img" id="lightboxImg" />
        </div>
    </div>

    <!-- Video Seek Toast -->
    <div class="seek-toast" id="seekToast">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="5 3 19 12 5 21 5 3"></polygon>
        </svg>
        <span id="seekToastText">Seeked</span>
    </div>

    <!-- Inline JavaScript -->
    <script>
{js_scripts}
    </script>
</body>
</html>
"""
    return full_html
