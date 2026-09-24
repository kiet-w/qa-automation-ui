"""
reporting/core/views_tests.py - Builds the ExtentReports Tests view with Multi-Test Accordion support.

Includes:
- Suite Toolbar: Test counts, status filters (All / Passed / Failed), Expand All & Collapse All.
- Collapsible Accordion Cards for each test case:
  - Master Header: Test Index (#1, #2,...), Status Badge, Jira ID, Story, Duration, Animated Chevron.
  - Per-test SVG Execution Pipeline.
  - Per-test 1080p Embedded Video Player with 2-way playback synchronization.
  - ExtentReports Step Log Table with Status Badge, Timestamp seek links, Expected vs Actual specs,
    and High-Resolution Screenshot Evidence previews with Lightbox zoom.
  - Failure traceback block if test encountered an error.
"""

import html
from typing import Any, Dict, List

from reporting.charts.pipeline import generate_pipeline_svg


def build_extent_tests_html(processed_tests: List[Dict[str, Any]]) -> str:
    """Builds HTML markup for the ExtentReports Tests view with Accordion layout for multi-test suites."""
    if not processed_tests:
        return """
        <div class="card" id="section-video">
            <div class="card-body" style="text-align: center; padding: 40px 20px; color: var(--text-muted); background: var(--bg-card);">
                No test execution data found.
            </div>
        </div>
        """

    total_tests = len(processed_tests)
    passed_tests = sum(1 for t in processed_tests if t.get("outcome", "").lower() == "passed")
    failed_tests = sum(1 for t in processed_tests if t.get("outcome", "").lower() == "failed")
    has_failed = failed_tests > 0

    html_parts = []

    # 1. Top Toolbar with Summary, Filters, and Expand/Collapse Controls
    toolbar_html = f"""
    <div class="test-suite-toolbar" id="section-video">
        <div class="toolbar-left">
            <div class="toolbar-title-group">
                <svg class="toolbar-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                <span class="toolbar-title" data-i18n="test_suite_title">Test Cases & Scenarios</span>
                <span class="badge-total-count">{total_tests} Tests</span>
            </div>
            <div class="test-filter-group">
                <button class="filter-btn active" data-filter="all" onclick="filterTests('all')" title="Show all tests">
                    <span data-i18n="filter_all">All</span>
                    <span class="filter-count count-all">{total_tests}</span>
                </button>
                <button class="filter-btn" data-filter="passed" onclick="filterTests('passed')" title="Show passed tests only">
                    <span data-i18n="filter_passed">Passed</span>
                    <span class="filter-count count-pass">{passed_tests}</span>
                </button>
                <button class="filter-btn" data-filter="failed" onclick="filterTests('failed')" title="Show failed tests only">
                    <span data-i18n="filter_failed">Failed</span>
                    <span class="filter-count count-fail">{failed_tests}</span>
                </button>
            </div>
        </div>
        <div class="toolbar-right">
            <button class="action-btn" onclick="expandAllTests()" title="Expand All Test Cards">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="7 11 12 6 17 11"></polyline>
                    <polyline points="7 18 12 13 17 18"></polyline>
                </svg>
                <span data-i18n="btn_expand_all">Expand All</span>
            </button>
            <button class="action-btn" onclick="collapseAllTests()" title="Collapse All Test Cards">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="7 13 12 18 17 13"></polyline>
                    <polyline points="7 6 12 11 17 6"></polyline>
                </svg>
                <span data-i18n="btn_collapse_all">Collapse All</span>
            </button>
        </div>
    </div>
    """
    html_parts.append(toolbar_html)

    # 2. Individual Test Cards (Collapsible Accordion)
    for test in processed_tests:
        t_idx = test["index"]
        t_name = test["name"]
        t_node = test["nodeid"]
        t_status = test["outcome"].upper()
        t_dur = test["duration"]
        t_video_b64 = test["video_b64"]
        t_steps = test["steps"]
        t_err = test["error_msg"]
        jira_id = test.get("jira_id") or f"TC-{t_idx + 1:03d}"
        user_story = test.get("user_story") or f"US-{t_idx + 1:02d}: Automated UI Scenario {t_idx + 1}"

        if t_status == "PASSED":
            status_class = "badge-pass"
        elif t_status == "SKIPPED":
            status_class = "badge-skip"
        else:
            status_class = "badge-fail"

        # Default open logic:
        # FAILED tests automatically expand first; otherwise test #1 (t_idx == 0) expands
        is_initially_expanded = (test["outcome"].lower() == "failed") if has_failed else (t_idx == 0)
        collapsed_class = "" if is_initially_expanded else "collapsed"
        aria_expanded = "true" if is_initially_expanded else "false"

        card = f"""
        <div class="card test-item-card {collapsed_class}" id="test-card-{t_idx}" data-status="{test['outcome'].lower()}" data-test-idx="{t_idx}">
            <!-- Collapsible Accordion Header -->
            <div class="test-accordion-header" onclick="toggleTestCard({t_idx})" role="button" tabindex="0" aria-expanded="{aria_expanded}" title="Click to expand/collapse test details">
                <div class="accordion-header-left">
                    <span class="test-index-badge" style="color: var(--text-secondary); background: var(--bg-card-subtle); border: 1px solid var(--border-color);">#{t_idx + 1}</span>
                    <span class="badge-status-lg {status_class}">{t_status}</span>
                    <div class="accordion-title-meta">
                        <h3 class="test-title-text">{html.escape(t_name)}</h3>
                        <div class="test-meta-pills">
                            <span class="test-pill" style="color: var(--text-secondary); background: var(--bg-card-subtle); border: 1px solid var(--border-color);">
                                <svg style="width:12px;height:12px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                                    <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
                                </svg>
                                {html.escape(jira_id)}
                            </span>
                            <span class="test-pill" style="color: var(--text-secondary); background: var(--bg-card-subtle); border: 1px solid var(--border-color);">{html.escape(user_story)}</span>
                            <span class="test-pill" style="color: var(--text-secondary); background: var(--bg-card-subtle); border: 1px solid var(--border-color);">
                                <svg style="width:12px;height:12px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="12" cy="12" r="10"></circle>
                                    <polyline points="12 6 12 12 16 14"></polyline>
                                </svg>
                                {t_dur:.2f}s
                            </span>
                            <span class="test-pill" style="color: var(--text-secondary); background: var(--bg-card-subtle); border: 1px solid var(--border-color);">
                                <svg style="width:12px;height:12px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                    <circle cx="12" cy="7" r="4"></circle>
                                </svg>
                                QA Engineer
                            </span>
                        </div>
                    </div>
                </div>
                <div class="accordion-header-right">
                    <div class="chevron-wrapper">
                        <svg class="test-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="6 9 12 15 18 9"></polyline>
                        </svg>
                    </div>
                </div>
            </div>

            <!-- Collapsible Body Section -->
            <div class="test-card-body" id="test-body-{t_idx}">
        """

        # (a) Per-test Execution Pipeline SVG
        if t_steps:
            pipeline_svg = generate_pipeline_svg(t_steps, test_idx=t_idx)
            card += f"""
                <div class="test-pipeline-box" id="pipeline-box-{t_idx}">
                    <div class="section-sub-header">
                        <div class="sub-header-title">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <polyline points="12 6 12 12 14 14"></polyline>
                            </svg>
                            <span data-i18n="pipeline_title">Step Execution Pipeline</span>
                        </div>
                        <span class="sub-header-hint" data-i18n="pipeline_hint">Click any step node to seek video to that step</span>
                    </div>
                    <div class="pipeline-wrapper">
                        {pipeline_svg}
                    </div>
                </div>
            """

        # (b) Embedded Video Player for this test case
        if t_video_b64:
            card += f"""
                <div class="video-card-section" id="video-section-{t_idx}">
                    <div class="video-header-bar">
                        <div class="video-title">
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
                            <span data-i18n="video_title">Execution Video Recording</span>
                        </div>
                        <span class="badge-test-ref" style="color: var(--text-secondary); background: var(--bg-card-subtle); border: 1px solid var(--border-color);">Test #{t_idx + 1}</span>
                    </div>
                    <div class="video-wrapper" id="video-container-{t_idx}">
                        <video id="video-player-{t_idx}" controls preload="metadata" class="video-player" ontimeupdate="syncVideoWithDiagram({t_idx}, this.currentTime)">
                            <source src="{t_video_b64}" type="video/webm">
                            Your browser does not support WebM video playback.
                        </video>
                    </div>
                </div>
            """
        else:
            card += f"""
                <div class="video-card-section" id="video-section-{t_idx}" style="background: var(--bg-card-subtle); border: 1px dashed var(--border-color); border-radius: 8px; padding: 16px; text-align: center; margin-bottom: 20px;">
                    <div style="display: flex; align-items: center; justify-content: center; gap: 8px; color: var(--text-muted); font-size: 13px;">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px; flex-shrink: 0;">
                            <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect>
                            <line x1="2" y1="2" x2="22" y2="22"></line>
                        </svg>
                        <span>No video recording available for this test scenario (strictly isolated).</span>
                    </div>
                </div>
            """

        # (c) ExtentReports Classic Step Log Table with Prominent Screenshot Evidence
        if t_steps:
            card += f"""
                <div class="card steps-table-card" id="section-steps">
                    <div class="card-header">
                        <div class="card-title">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="9 11 12 14 22 4"></polyline>
                                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
                            </svg>
                            <span data-i18n="steps_table_title">Step Execution Log & Evidence</span>
                        </div>
                        <span style="font-size: 12px; color: var(--text-secondary); font-weight: 600;">{len(t_steps)} steps</span>
                    </div>
                    <table class="table-extent">
                        <thead>
                            <tr>
                                <th style="width: 85px;" data-i18n="th_status">Status</th>
                                <th style="width: 105px;" data-i18n="th_timestamp">Timestamp</th>
                                <th data-i18n="th_details">Step Details & Evidence</th>
                            </tr>
                        </thead>
                        <tbody>
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
                s_exp = s.get("expected", "Step completes as expected")
                s_act = s.get("actual", f"Completed in {s_dur:.2f}s with status {s_status}")

                row_id = f"step-row-{t_idx}-{s_idx - 1}"
                card_target_id = f"step-card-{t_idx}-{s_idx - 1}"
                if s_status == "PASSED":
                    badge_class = "badge-pass"
                elif s_status == "SKIPPED":
                    badge_class = "badge-skip"
                else:
                    badge_class = "badge-fail"

                # Error markup if failed
                err_markup = ""
                if s_err:
                    err_markup = f"""
                    <div class="spec-line" style="margin-top: 4px;">
                        <span class="spec-tag tag-err" data-i18n="tag_error">Error:</span>
                        <span style="color: var(--status-fail); font-family: var(--font-mono); font-size: 11.5px;">{html.escape(s_err)}</span>
                    </div>
                    """

                # Prominent Screenshot Evidence Markup (Deliverable + Lightbox Zoom)
                evidence_markup = ""
                if s_b64:
                    safe_title = html.escape(s_title).replace("'", "\\'")
                    evidence_markup = f"""
                    <div class="step-large-evidence" style="background: var(--bg-card-subtle); border: 1px solid var(--border-color);">
                        <div class="evidence-meta-bar">
                            <span class="evidence-badge" style="color: var(--text-secondary);">
                                <svg style="width:14px;height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                                    <circle cx="12" cy="13" r="4"></circle>
                                </svg>
                                <span data-i18n="lbl_screenshot_evidence">Screenshot Evidence Deliverable</span>
                            </span>
                            <span class="evidence-hint" style="color: var(--text-muted);" data-i18n="click_to_zoom">Click image to view in full resolution</span>
                        </div>
                        <div class="evidence-large-frame" onclick="openLightbox('{s_b64}', '{safe_title}')" title="Click to view in full resolution" style="border: 1px solid var(--border-color);">
                            <img src="{s_b64}" alt="Step {s_idx} Evidence" class="evidence-large-img" loading="lazy" />
                            <div class="evidence-zoom-tag">
                                <svg style="width:14px;height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="11" cy="11" r="8"></circle>
                                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                                    <line x1="11" y1="8" x2="11" y2="14"></line>
                                    <line x1="8" y1="11" x2="14" y2="11"></line>
                                </svg>
                                <span data-i18n="btn_zoom">Enlarge Fullscreen</span>
                            </div>
                        </div>
                    </div>
                    """

                card += f"""
                <tr class="step-log-row" id="{row_id}" data-test-idx="{t_idx}" data-start="{s_start:.2f}" data-end="{s_end:.2f}">
                    <td style="vertical-align: top; padding-top: 16px;">
                        <span class="badge-status-pill {badge_class}">{s_status}</span>
                    </td>
                    <td style="vertical-align: top; padding-top: 16px;">
                        <button class="step-time-link" onclick="seekVideoAndScroll({s_start:.2f}, '{card_target_id}', {t_idx}, {s_idx - 1})" title="Seek video to {s_start:.1f}s">
                            ▶ +{s_start:.2f}s
                        </button>
                    </td>
                    <td style="vertical-align: top; padding-top: 14px;">
                        <div class="step-title-bold">{html.escape(s_title)} <span style="font-size: 11px; font-weight: 500; color: var(--text-muted); font-family: var(--font-mono);">({s_dur:.2f}s)</span></div>
                        <div class="step-spec-box" style="background-color: var(--bg-card-subtle); border: 1px solid var(--border-color);">
                            <div class="spec-line">
                                <span class="spec-tag tag-exp" data-i18n="tag_expected">Expected:</span>
                                <span style="color: var(--text-primary);">{html.escape(s_exp)}</span>
                            </div>
                            <div class="spec-line">
                                <span class="spec-tag tag-act" data-i18n="tag_actual">Actual:</span>
                                <span style="color: var(--text-primary);">{html.escape(s_act)}</span>
                            </div>
                            {err_markup}
                        </div>
                        {evidence_markup}
                    </td>
                </tr>
                """

            card += """
                        </tbody>
                    </table>
                </div>
            """

        # (d) Failure Traceback if test encountered failure
        if t_err and t_status in ("FAILED", "ERROR"):
            card += f"""
                <div class="card" style="margin-top: 20px; border: 1px solid var(--status-fail);">
                    <div class="card-header" style="background-color: var(--status-fail-bg); border-bottom: 1px solid var(--status-fail);">
                        <div class="card-title" style="color: var(--status-fail);">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <line x1="12" y1="8" x2="12" y2="12"></line>
                                <line x1="12" y1="16" x2="12.01" y2="16"></line>
                            </svg>
                            <span>Failure Traceback</span>
                        </div>
                    </div>
                    <div class="card-body">
                        <pre style="background: var(--bg-card-subtle); padding: 14px; border-radius: var(--radius-sm); font-family: var(--font-mono); font-size: 12px; color: var(--status-fail); border: 1px solid var(--border-color); overflow-x: auto; white-space: pre-wrap;">{html.escape(t_err)}</pre>
                    </div>
                </div>
            """

        card += """
            </div> <!-- end test-card-body -->
        </div> <!-- end test-item-card -->
        """

        html_parts.append(card)

    return "\n".join(html_parts)


# Alias for backward compatibility
build_test_cards_html = build_extent_tests_html
