"""
reporting/core/views_tests.py - Builds the ExtentReports Tests view with 3-Tier Hierarchy & Defect Evidence Highlights.

Features:
- Suite Toolbar: Test counts, status filters (All / Passed / Failed / XFailed), Expand All & Collapse All.
- 3-Tier Hierarchy: Suite -> Scenario Groups -> Test Case Cards.
- Prominent Defect Evidence Callouts & Red Glowing Borders for any failure or known defect.
- Per-test SVG Execution Pipeline.
- Embedded Video Player with slow-motion speed controls (0.5x, 0.75x, 1.0x).
- ExtentReports Step Log Table with synchronized seek timestamps and Fullscreen Lightbox screenshots.
"""

import html
import re
from typing import Any, Dict, List, Optional

from reporting.charts.pipeline import generate_pipeline_svg
from reporting.core.sanitizer import clean_error_message, extract_clean_defect_hint


def build_single_test_card_html(test: Dict[str, Any], has_failed: bool) -> str:
    """Renders an individual collapsible test card with defect evidence highlights."""
    t_idx = test["index"]
    t_name = test["name"]
    t_node = test["nodeid"]
    t_status = test["outcome"].upper()
    t_dur = test["duration"]
    t_video_b64 = test.get("video_b64")
    t_video_sources = test.get("video_sources", [])
    t_steps = test["steps"]
    t_err = clean_error_message(test.get("error_msg"))
    jira_id = test.get("jira_id") or f"TC-{t_idx + 1:03d}"
    user_story = test.get("user_story") or f"US-{t_idx + 1:02d}: Scenario {t_idx + 1}"
    friendly_title = test.get("friendly_title") or t_name

    is_failed = test["outcome"].lower() == "failed"

    if t_status == "PASSED":
        status_class = "badge-pass"
    elif t_status == "SKIPPED":
        status_class = "badge-skip"
    elif t_status in ("XFAIL", "XFAILED"):
        status_class = "badge-xfail"
        t_status = "XFAIL (KNOWN BUG)"
    elif t_status in ("XPASS", "XPASSED"):
        status_class = "badge-fail"
        t_status = "XPASS (FIXED BUG)"
    else:
        status_class = "badge-fail"

    # Default open logic: FAILED tests expand first
    is_initially_expanded = (test["outcome"].lower() == "failed") if has_failed else (t_idx == 0)
    collapsed_class = "" if is_initially_expanded else "collapsed"
    card_failed_class = "test-card-failed" if is_failed else ""
    aria_expanded = "true" if is_initially_expanded else "false"

    xfail_banner_html = ""
    if test.get("xfail_reason"):
        xfail_banner_html = f"""
            <div class="xfail-banner" style="display:flex;align-items:center;gap:12px;padding:12px 16px;margin-bottom:16px;background:rgba(210,153,34,0.12);border:1px solid rgba(210,153,34,0.4);border-radius:6px;color:#d29922;">
                <svg style="width:20px;height:20px;flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                    <line x1="12" y1="9" x2="12" y2="13"></line>
                    <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
                <div style="font-size:13.5px;line-height:1.4;">
                    <strong style="color:#e6edf3;">Known Product Defect (Strict XFAIL):</strong> {html.escape(test['xfail_reason'])}
                </div>
            </div>
        """

    # Defect Evidence Banner for Failed Tests
    defect_alert_html = ""
    if is_failed:
        defect_type = "ASSERTION FAILURE"
        if t_err:
            first_line = extract_clean_defect_hint(t_err)
            if "TimeoutError" in first_line or "Timeout" in first_line:
                defect_type = "TIMEOUT ERROR"
            elif "AssertionError" in first_line:
                defect_type = "ASSERTION FAILED"
            elif "BugDetected" in first_line:
                defect_type = "DEFECT DETECTED"
            else:
                m_type = re.search(r"([A-Za-z0-9_]+Error)", first_line)
                if m_type:
                    defect_type = m_type.group(1).upper()

        failed_step = next((s for s in t_steps if s.get("status") == "failed"), None)
        failed_step_name = failed_step.get("title") if failed_step else "Execution Assertion Point"
        clean_err = clean_error_message(failed_step.get("error") if failed_step else None) or t_err or "Step validation assertion failed"

        # Extract target locator if present
        locator_html = ""
        m_loc = re.search(r'locator\(["\'](.*?)["\']\)', clean_err)
        if not m_loc:
            m_loc = re.search(r'waiting for locator\(["\'](.*?)["\']\)', clean_err)
        if m_loc:
            locator_html = f"""
            <div class="defect-locator-tag">
                <strong>Target Locator:</strong> <code>locator("{html.escape(m_loc.group(1))}")</code>
            </div>
            """

        defect_alert_html = f"""
        <div class="defect-evidence-alert-box">
            <div class="defect-alert-header">
                <div class="defect-badge-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="15" y1="9" x2="9" y2="15"></line>
                        <line x1="9" y1="9" x2="15" y2="15"></line>
                    </svg>
                    <span>DEFECT DETECTED & EVIDENCE CAPTURED</span>
                </div>
                <span class="defect-alert-type">{defect_type}</span>
            </div>
            <div class="defect-alert-body">
                <div class="defect-alert-step">
                    <span class="defect-label">Failed Step:</span>
                    <span class="defect-step-name">{html.escape(failed_step_name)}</span>
                </div>
                <div class="defect-alert-message">{html.escape(clean_err.strip())}</div>
                {locator_html}
            </div>
        </div>
        """

    card = f"""
    <div class="card test-item-card {card_failed_class} {collapsed_class}" id="test-card-{t_idx}" data-status="{test['outcome'].lower()}" data-test-idx="{t_idx}">
        <!-- Collapsible Accordion Header -->
        <div class="test-accordion-header" onclick="toggleTestCard({t_idx})" role="button" tabindex="0" aria-expanded="{aria_expanded}" title="Click to expand/collapse test details">
            <div class="accordion-header-left">
                <span class="test-index-badge" style="color: var(--text-secondary); background: var(--bg-card-subtle); border: 1px solid var(--border-color);">#{t_idx + 1}</span>
                <span class="badge-status-lg {status_class}">{t_status}</span>
                <div class="accordion-title-meta">
                    <h3 class="test-title-text" style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                        <span style="font-family:var(--font-mono);font-size:13px;color:var(--accent-primary);">{html.escape(jira_id)}</span>
                        <span>{html.escape(friendly_title)}</span>
                    </h3>
                    <div class="test-meta-pills">
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
            {xfail_banner_html}
            {defect_alert_html}
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

    # (b) Video Player for this test case
    video_sources_html = []
    if t_video_b64:
        video_sources_html.append(f'<source src="{t_video_b64}" type="video/webm">')
    if t_video_sources:
        for v_src in t_video_sources:
            video_sources_html.append(f'<source src="{v_src}" type="video/webm">')

    video_sec_class = "video-card-section video-section-defect" if is_failed else "video-card-section"
    video_title_text = "🔴 EXECUTION VIDEO RECORDING (DEFECT CAPTURE)" if is_failed else "Execution Video Recording"

    if video_sources_html:
        sources_rendered = "\n                        ".join(video_sources_html)
        card += f"""
            <div class="{video_sec_class}" id="video-section-{t_idx}">
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
                        <span>{video_title_text}</span>
                    </div>
                    <div class="video-header-controls" style="display:flex;align-items:center;gap:6px;">
                        <span style="font-size:11.5px;color:var(--text-secondary);font-weight:600;">Speed:</span>
                        <button type="button" class="speed-pill" onclick="setVideoSpeed({t_idx}, 0.5)" title="Slow-Motion 0.5x">0.5x</button>
                        <button type="button" class="speed-pill active" onclick="setVideoSpeed({t_idx}, 0.75)" title="Moderate 0.75x">0.75x</button>
                        <button type="button" class="speed-pill" onclick="setVideoSpeed({t_idx}, 1.0)" title="Normal 1.0x">1.0x</button>
                        <span class="badge-test-ref" style="margin-left:6px;color: var(--text-secondary); background: var(--bg-card-subtle); border: 1px solid var(--border-color);">Test #{t_idx + 1}</span>
                    </div>
                </div>
                <div class="video-wrapper" id="video-container-{t_idx}">
                    <video id="video-player-{t_idx}" controls preload="metadata" class="video-player" ontimeupdate="syncVideoWithDiagram({t_idx}, this.currentTime)">
                        {sources_rendered}
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
                    <span>No video recording available for this test scenario.</span>
                </div>
            </div>
        """

    # (c) Step Execution Log Table
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

            s_is_failed = s_status == "FAILED"
            if s_status == "PASSED":
                badge_class = "badge-pass"
            elif s_status == "SKIPPED":
                badge_class = "badge-skip"
            elif s_status in ("XFAIL", "XFAILED") or (t_status.startswith("XFAIL") and s_status == "FAILED"):
                badge_class = "badge-xfail"
                s_status = "XFAIL (BUG)"
            else:
                badge_class = "badge-fail"

            row_class = "step-log-row step-row-failed" if s_is_failed else "step-log-row"
            spec_box_class = "step-spec-box step-box-defect" if s_is_failed else "step-spec-box"
            tag_act_class = "spec-tag tag-act tag-act-fail" if s_is_failed else "spec-tag tag-act"
            text_act_class = "spec-text-fail" if s_is_failed else ""

            # Error markup if failed
            err_markup = ""
            if s_err:
                err_markup = f"""
                <div class="spec-line" style="margin-top: 6px;">
                    <span class="spec-tag tag-err" data-i18n="tag_error">Error:</span>
                    <span style="color: #ff7b72; font-family: var(--font-mono); font-size: 11.5px; font-weight: 600;">{html.escape(s_err)}</span>
                </div>
                """

            # Prominent Screenshot Evidence
            evidence_markup = ""
            if s_b64:
                safe_title = html.escape(s_title).replace("'", "\\'")
                frame_class = "step-large-evidence evidence-frame-defect" if s_is_failed else "step-large-evidence"
                badge_style = "background: var(--status-fail); color: #fff; font-weight: 800;" if s_is_failed else "color: var(--text-secondary);"
                badge_label = "🔴 DEFECT SCREENSHOT DELIVERABLE" if s_is_failed else "Screenshot Evidence Deliverable"

                evidence_markup = f"""
                <div class="{frame_class}">
                    <div class="evidence-meta-bar">
                        <span class="evidence-badge" style="{badge_style}">
                            <svg style="width:14px;height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                                <circle cx="12" cy="13" r="4"></circle>
                            </svg>
                            <span>{badge_label}</span>
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
            <tr class="{row_class}" id="{row_id}" data-test-idx="{t_idx}" data-start="{s_start:.2f}" data-end="{s_end:.2f}">
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
                    <div class="{spec_box_class}">
                        <div class="spec-line">
                            <span class="spec-tag tag-exp" data-i18n="tag_expected">Expected:</span>
                            <span style="color: var(--text-primary);">{html.escape(s_exp)}</span>
                        </div>
                        <div class="spec-line">
                            <span class="{tag_act_class}" data-i18n="tag_actual">Actual:</span>
                            <span class="{text_act_class}">{html.escape(s_act)}</span>
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

    # (d) Failure Traceback
    if t_err and t_status in ("FAILED", "ERROR"):
        card += f"""
            <div class="card" style="margin-top: 20px; border: 2px solid var(--status-fail);">
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
                    <pre style="background: var(--bg-card-subtle); padding: 14px; border-radius: var(--radius-sm); font-family: var(--font-mono); font-size: 12px; color: #ff7b72; border: 1px solid rgba(207,34,46,0.3); overflow-x: auto; white-space: pre-wrap;">{html.escape(t_err)}</pre>
                </div>
            </div>
        """

    card += """
        </div> <!-- end test-card-body -->
    </div> <!-- end test-item-card -->
    """

    return card


def build_extent_tests_html(
    processed_tests: List[Dict[str, Any]],
    scenarios: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """Builds HTML markup for the ExtentReports Tests view with 3-tier Scenario grouping."""
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
    xfailed_tests = sum(1 for t in processed_tests if t.get("outcome", "").lower() in ("xfailed", "xfail"))
    has_failed = failed_tests > 0

    html_parts = []

    # 1. Top Toolbar with Summary, Filters, and Expand/Collapse Controls
    xfail_btn_html = ""
    if xfailed_tests > 0:
        xfail_btn_html = f"""
                <button class="filter-btn" data-filter="xfailed" onclick="filterTests('xfailed')" title="Show known bugs / XFailed tests only">
                    <span data-i18n="filter_xfail">XFailed (Bugs)</span>
                    <span class="filter-count count-xfail">{xfailed_tests}</span>
                </button>
        """

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
{xfail_btn_html}
                <button class="filter-btn" data-filter="failed" onclick="filterTests('failed')" title="Show failed tests only">
                    <span data-i18n="filter_failed">Failed</span>
                    <span class="filter-count count-fail">{failed_tests}</span>
                </button>
            </div>
        </div>
        <div class="toolbar-right">
            <button class="action-btn" onclick="expandAllTests()" title="Expand All Scenarios & Test Cards">
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

    # 2. Render Cards Grouped by Scenarios (3-Tier Hierarchy)
    if scenarios and len(scenarios) > 0:
        for s_idx, sc in enumerate(scenarios):
            sc_id = sc.get("id", f"TS-{s_idx + 1:02d}")
            sc_title = sc.get("title", f"Scenario {s_idx + 1}")
            sc_tests = sc.get("tests", [])
            sc_total = sc.get("total", len(sc_tests))
            sc_passed = sc.get("passed", 0)
            sc_failed = sc.get("failed", 0)
            sc_xfailed = sc.get("xfailed", 0)
            sc_dur = sc.get("duration", 0.0)

            sc_has_failed = sc_failed > 0
            sc_status = "FAILED" if sc_has_failed else ("PASSED" if sc_passed > 0 else "UNKNOWN")
            sc_status_badge = "badge-fail" if sc_has_failed else "badge-pass"
            sc_group_class = "has-failures" if sc_has_failed else ""

            # Auto collapse passed scenarios if there are failed scenarios
            sc_collapsed = "collapsed" if (has_failed and not sc_has_failed) else ""

            failed_pill = f'<span class="scenario-pill pill-fail">{sc_failed} Failed</span>' if sc_failed > 0 else ""
            xfail_pill = f'<span class="scenario-pill pill-xfail">{sc_xfailed} XFailed</span>' if sc_xfailed > 0 else ""

            cards_in_scenario = [build_single_test_card_html(t, has_failed) for t in sc_tests]
            rendered_cards = "\n".join(cards_in_scenario)

            sc_html = f"""
            <div class="scenario-accordion-group {sc_group_class} {sc_collapsed}" id="scenario-group-{s_idx}" data-scenario-status="{sc_status.lower()}">
                <div class="scenario-accordion-header" onclick="toggleScenarioCard({s_idx})" role="button" tabindex="0" title="Click to expand/collapse scenario">
                    <div class="scenario-header-left">
                        <span class="badge-scenario-id">{html.escape(sc_id)}</span>
                        <div class="scenario-title-box">
                            <h2 class="scenario-title-text">{html.escape(sc_title)}</h2>
                            <div class="scenario-meta-pills">
                                <span class="scenario-pill">{sc_total} Tests</span>
                                <span class="scenario-pill pill-pass">{sc_passed} Passed</span>
                                {failed_pill}
                                {xfail_pill}
                                <span class="scenario-pill pill-dur">{sc_dur:.2f}s</span>
                            </div>
                        </div>
                    </div>
                    <div class="scenario-header-right">
                        <span class="badge-scenario-status {sc_status_badge}">{sc_status}</span>
                        <div class="chevron-wrapper">
                            <svg class="scenario-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="6 9 12 15 18 9"></polyline>
                            </svg>
                        </div>
                    </div>
                </div>
                <div class="scenario-test-cards-wrapper" id="scenario-body-{s_idx}">
                    {rendered_cards}
                </div>
            </div>
            """
            html_parts.append(sc_html)
    else:
        # Fallback to flat list of cards
        for test in processed_tests:
            html_parts.append(build_single_test_card_html(test, has_failed))

    return "\n".join(html_parts)


# Alias for backward compatibility
build_test_cards_html = build_extent_tests_html
