"""
tests/unit/test_enterprise_reporting.py - Unit tests for Enterprise Execution Report Engine.
"""

from pathlib import Path
import pytest

from reporting.core.enterprise_builder import (
    build_enterprise_html,
    build_test_rows,
    detect_suite_info,
    generate_executive_takeaways,
)
from reporting.core.parser import load_report_json, process_report_data
from reporting.core.builder import ReportGenerator


def test_detect_suite_info_modules():
    workspace = Path(".")
    
    # FS-08
    rep_fs08 = workspace / "reports" / "fs08" / "fs08-parent-profile"
    info_fs08 = detect_suite_info({}, {"tests": []}, rep_fs08)
    assert info_fs08["suite_badge"] == "FS-08"
    assert "Parent Profile" in info_fs08["module_title"]

    # FS-09
    rep_fs09 = workspace / "reports" / "fs09"
    info_fs09 = detect_suite_info({}, {"tests": []}, rep_fs09)
    assert info_fs09["suite_badge"] == "FS-09"
    assert "Outstanding Fees & Payment" in info_fs09["module_title"]

    # Break-It
    rep_brk = workspace / "reports" / "break_it"
    info_brk = detect_suite_info({}, {"tests": []}, rep_brk)
    assert info_brk["suite_badge"] == "BRK"
    assert "Resilience" in info_brk["module_title"]


def test_build_enterprise_html_fs08():
    workspace = Path(".")
    rep_dir = workspace / "reports" / "fs08" / "fs08-parent-profile"
    json_path = rep_dir / "report.json"
    
    if not json_path.exists():
        pytest.skip("FS-08 report.json not found")

    report_data = load_report_json(json_path)
    parsed = process_report_data(report_data, [], rep_dir, workspace)

    html_out = build_enterprise_html(parsed, report_data, rep_dir, workspace)

    # Invariants & Key requirements verification
    assert "FS-08 Parent Profile" in html_out
    assert "SingPass Identity Read-Only Integrity" in html_out
    assert "ĐẠT CHUẨN" in html_out or "PHÁT HIỆN LỖI" in html_out
    assert "defect-spotlight-btn" in html_out
    assert "modal-video-player" in html_out
    assert "modal-pipeline-container" in html_out
    assert "lightbox" in html_out
    assert "enterprise-table" in html_out
    assert "fx" in html_out


def test_build_enterprise_html_fs09_failure_capture():
    workspace = Path(".")
    rep_dir = workspace / "reports" / "fs09"
    json_path = rep_dir / "report.json"

    if not json_path.exists():
        pytest.skip("FS-09 report.json not found")

    report_data = load_report_json(json_path)
    parsed = process_report_data(report_data, [], rep_dir, workspace)

    html_out = build_enterprise_html(parsed, report_data, rep_dir, workspace)

    # Defect capture assertions
    assert "PHÁT HIỆN LỖI" in html_out
    assert "2 Failed" in html_out
    assert "TC-R9-08" in html_out
    assert "FAIL" in html_out
    assert "DEFECT CAPTURE" in html_out
    assert "defect-spotlight-btn" in html_out
    assert "defect-reticle-svg" in html_out


def test_generator_standard_output():
    workspace = Path(".")
    rep_dir = workspace / "reports" / "fs08" / "fs08-parent-profile"
    json_path = rep_dir / "report.json"
    out_path = rep_dir / "execution_report.html"

    if not json_path.exists():
        pytest.skip("FS-08 report.json not found")

    generator = ReportGenerator(workspace_dir=workspace, reports_dir=rep_dir)
    res = generator.generate(json_path=json_path, output_html_path=out_path)

    assert res.exists()
    content = res.read_text(encoding="utf-8")
    assert "FS-08 Parent Profile" in content
    assert "defect-spotlight-btn" in content


def test_error_sanitization_removes_dom_css_dumps():
    from reporting.core.sanitizer import clean_error_message, extract_clean_defect_hint

    raw_pytest_dump = (
        "assert (False or 'unavailable' in '<!doctype html><html lang=\"en\"><head>"
        "<style>._step_pra49 { display: flex; }</style></head><body><h1>Test</h1></body></html>')"
    )
    cleaned = clean_error_message(raw_pytest_dump)
    assert "_step_pra49" not in cleaned
    assert "[HTML Page DOM]" in cleaned

    hint = extract_clean_defect_hint(raw_pytest_dump)
    assert "_step_pra49" not in hint
    assert len(hint) <= 180
    assert "[HTML Page DOM]" in hint
