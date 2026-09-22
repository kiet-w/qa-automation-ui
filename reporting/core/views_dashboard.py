"""
reporting/core/views_dashboard.py - Builds the ExtentReports Dashboard view.

Includes:
- 4 Executive KPI Cards (Tests, Steps, Start Time, Duration).
- Result Status Donut SVG Chart.
- Step Duration Timeline Bar SVG Chart.
- Interactive Step Execution Pipeline SVG.
- ExtentReports System / Environment Information Table.
"""

import html
import sys
from typing import Any, Dict

from reporting.charts import (
    generate_donut_chart_svg,
    generate_duration_bar_chart_svg,
    generate_pipeline_svg,
)


def build_extent_kpi_and_charts_html(parsed: Dict[str, Any]) -> str:
    """Builds HTML markup for the ExtentReports KPIs, Charts, and Step Pipeline."""
    total_tests = parsed.get("total", 0)
    passed_tests = parsed.get("passed", 0)
    failed_tests = parsed.get("failed", 0)
    skipped_tests = parsed.get("skipped", 0)

    steps = parsed.get("primary_steps", [])
    total_steps = len(steps)
    passed_steps = sum(1 for s in steps if s.get("status") == "passed")
    failed_steps = sum(1 for s in steps if s.get("status") == "failed")

    total_duration = parsed.get("total_duration", 0.0)
    created_str = parsed.get("created_str", "-")
    triggered_by = parsed.get("triggered_by", "Manual")
    target_env = parsed.get("target_env", "Staging")

    # SVG Charts
    donut_svg = generate_donut_chart_svg(
        passed=passed_tests if total_tests > 1 else passed_steps,
        failed=failed_tests if total_tests > 1 else failed_steps,
        skipped=skipped_tests,
    )
    bar_svg = generate_duration_bar_chart_svg(parsed.get("bar_items", []))
    pipeline_svg = generate_pipeline_svg(steps, test_idx=0)

    # Dynamic KPI Card status classes and sub-stats
    tests_card_class = "kpi-fail" if failed_tests > 0 else "kpi-pass"
    steps_card_class = "kpi-fail" if failed_steps > 0 else "kpi-pass"

    if failed_tests > 0:
        tests_sub_stats = f'<span class="sub-pill-fail">{failed_tests} failed</span>'
        if passed_tests > 0:
            tests_sub_stats += f' <span class="sub-pill-pass">{passed_tests} <span data-i18n="lbl_passed">passed</span></span>'
    else:
        tests_sub_stats = f'<span class="sub-pill-pass">{passed_tests} <span data-i18n="lbl_passed">passed</span></span>'

    if failed_steps > 0:
        steps_sub_stats = f'<span class="sub-pill-fail">{failed_steps} failed</span>'
        if passed_steps > 0:
            steps_sub_stats += f' <span class="sub-pill-pass">{passed_steps} <span data-i18n="lbl_passed">passed</span></span>'
    else:
        steps_sub_stats = f'<span class="sub-pill-pass">{passed_steps} <span data-i18n="lbl_passed">passed</span></span>'

    return f"""
    <!-- 4 KPI Summary Cards -->
    <div class="kpi-grid" id="section-kpi">
        <div class="card kpi-card {tests_card_class}">
            <div class="card-body">
                <div class="kpi-label" data-i18n="kpi_tests">TESTS</div>
                <div class="kpi-val-main">{total_tests}</div>
                <div class="kpi-sub-stats">
                    {tests_sub_stats}
                </div>
            </div>
        </div>

        <div class="card kpi-card {steps_card_class}">
            <div class="card-body">
                <div class="kpi-label" data-i18n="kpi_steps">STEPS</div>
                <div class="kpi-val-main">{total_steps}</div>
                <div class="kpi-sub-stats">
                    {steps_sub_stats}
                </div>
            </div>
        </div>

        <div class="card kpi-card kpi-neutral" style="border-left-color: var(--border-color);">
            <div class="card-body">
                <div class="kpi-label" data-i18n="kpi_start_time">START TIME</div>
                <div class="kpi-val-main" style="font-size: 18px; line-height: 1.5; font-family: var(--font-mono); color: var(--text-primary);">{html.escape(created_str)}</div>
                <div class="kpi-sub-stats" style="color: var(--text-muted);">
                    {html.escape(triggered_by)}
                </div>
            </div>
        </div>

        <div class="card kpi-card kpi-neutral" style="border-left-color: var(--border-color);">
            <div class="card-body">
                <div class="kpi-label" data-i18n="kpi_duration">DURATION</div>
                <div class="kpi-val-main" style="color: var(--text-primary);">{total_duration:.2f}s</div>
                <div class="kpi-sub-stats" style="color: var(--text-muted);">
                    Env: <strong style="color: var(--text-primary);">{html.escape(target_env)}</strong>
                </div>
            </div>
        </div>
    </div>

    <!-- Charts Row: Donut & Bar -->
    <div class="charts-grid" id="section-analytics">
        <div class="card">
            <div class="card-header">
                <div class="card-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path>
                        <path d="M22 12A10 10 0 0 0 12 2v10z"></path>
                    </svg>
                    <span data-i18n="chart_status_title">Tests & Steps Status</span>
                </div>
            </div>
            <div class="card-body">
                {donut_svg}
                <div class="chart-legend">
                    <div class="legend-dot-item">
                        <div class="dot-indicator dot-pass"></div>
                        <span data-i18n="lbl_legend_pass">Passed</span>
                    </div>
                    <div class="legend-dot-item">
                        <div class="dot-indicator dot-fail"></div>
                        <span data-i18n="lbl_legend_fail">Failed</span>
                    </div>
                    <div class="legend-dot-item">
                        <div class="dot-indicator dot-skip"></div>
                        <span data-i18n="lbl_legend_skip">Skipped</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <div class="card-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="20" x2="18" y2="10"></line>
                        <line x1="12" y1="20" x2="12" y2="4"></line>
                        <line x1="6" y1="20" x2="6" y2="14"></line>
                    </svg>
                    <span data-i18n="chart_duration_title">Timeline & Step Durations</span>
                </div>
            </div>
            <div class="card-body">
                {bar_svg}
            </div>
        </div>
    </div>

    <!-- Pipeline Section -->
    <div class="card" id="section-pipeline">
        <div class="card-header">
            <div class="card-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 14 14"></polyline>
                </svg>
                <span data-i18n="pipeline_title">Step Execution Pipeline</span>
            </div>
            <span style="font-size: 11.5px; color: var(--text-secondary);" data-i18n="pipeline_hint">Click any step node to seek video to that step</span>
        </div>
        <div class="card-body pipeline-wrapper">
            {pipeline_svg}
        </div>
    </div>
    """


def build_extent_sysinfo_html(parsed: Dict[str, Any]) -> str:
    """Builds HTML markup for the ExtentReports System & Environment Info table."""
    run_id = parsed.get("run_id", "RUN-UNKNOWN")
    triggered_by = parsed.get("triggered_by", "Manual")
    target_env = parsed.get("target_env", "Staging")
    git_info = parsed.get("git_info", {})
    git_ref = f"{git_info.get('branch', 'main')} ({git_info.get('commit', 'latest')})"

    return f"""
    <!-- System / Environment Info (ExtentReports Style) -->
    <div class="card" id="section-system">
        <div class="card-header">
            <div class="card-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect>
                    <rect x="9" y="9" width="6" height="6"></rect>
                    <line x1="9" y1="1" x2="9" y2="4"></line>
                    <line x1="15" y1="1" x2="15" y2="4"></line>
                    <line x1="9" y1="20" x2="9" y2="23"></line>
                    <line x1="15" y1="20" x2="15" y2="23"></line>
                    <line x1="20" y1="9" x2="23" y2="9"></line>
                    <line x1="20" y1="14" x2="23" y2="14"></line>
                    <line x1="1" y1="9" x2="4" y2="9"></line>
                    <line x1="1" y1="14" x2="4" y2="14"></line>
                </svg>
                <span data-i18n="sysinfo_title">Environment & System Information</span>
            </div>
        </div>
        <div class="card-body" style="padding: 0;">
            <table class="table-sysinfo">
                <thead>
                    <tr>
                        <th data-i18n="th_param">Parameter</th>
                        <th data-i18n="th_value">Value</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="sysinfo-param">Operating System</td>
                        <td class="sysinfo-val">Linux (x86_64)</td>
                    </tr>
                    <tr>
                        <td class="sysinfo-param">Python Version</td>
                        <td class="sysinfo-val">{sys.version.split()[0]}</td>
                    </tr>
                    <tr>
                        <td class="sysinfo-param">Automation Framework</td>
                        <td class="sysinfo-val">Playwright & pytest</td>
                    </tr>
                    <tr>
                        <td class="sysinfo-param">Browser Engine</td>
                        <td class="sysinfo-val">Chromium (1920x1080 Headed)</td>
                    </tr>
                    <tr>
                        <td class="sysinfo-param">Target Environment</td>
                        <td class="sysinfo-val">{html.escape(target_env)}</td>
                    </tr>
                    <tr>
                        <td class="sysinfo-param">Git Branch & Commit</td>
                        <td class="sysinfo-val">{html.escape(git_ref)}</td>
                    </tr>
                    <tr>
                        <td class="sysinfo-param">Run ID</td>
                        <td class="sysinfo-val" style="color: var(--text-primary); font-weight: 700;">{html.escape(run_id)}</td>
                    </tr>
                    <tr>
                        <td class="sysinfo-param">Triggered By</td>
                        <td class="sysinfo-val">{html.escape(triggered_by)}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    """


def build_extent_dashboard_html(parsed: Dict[str, Any]) -> str:
    """Full dashboard html for backward compatibility."""
    return build_extent_kpi_and_charts_html(parsed) + build_extent_sysinfo_html(parsed)
