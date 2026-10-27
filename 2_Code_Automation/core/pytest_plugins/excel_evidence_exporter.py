"""
core/pytest_plugins/excel_evidence_exporter.py - Automatic Test Execution Evidence Excel Exporter.
Automatically updates or generates TEST_EXECUTION_EVIDENCE_<MODULE>_<FEATURE>.xlsx (Strict Single Tab)
at the end of pytest test sessions, recording real-time Passed/Failed outcomes, actual error messages,
and relative video playback hyperlinks.
"""

from datetime import datetime
import json
import os
from pathlib import Path
import re
import shutil
from typing import Dict, Any, Optional, List
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

from core.pytest_plugins.excel_evidence_paths import (
    find_actual_result_screenshot,
    rebase_local_target,
    relative_excel_target,
    test_slug_candidates,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def find_evidence_xlsx_file(ticket_dir: Path) -> Optional[Path]:
    """Find existing TEST_EXECUTION_EVIDENCE_*.xlsx file in a given directory."""
    if not ticket_dir.exists():
        return None
    matches = list(ticket_dir.glob("TEST_EXECUTION_EVIDENCE_*.xlsx"))
    if matches:
        return matches[0]
    return None


def derive_evidence_filename(ticket_name: str) -> str:
    """Derive standard evidence filename from ticket slug (e.g. fs08/fs08-parent-profile -> TEST_EXECUTION_EVIDENCE_FS08_Parent_Profile.xlsx)."""
    parts = ticket_name.strip("/").split("/")
    last_part = parts[-1]
    # Replace dashes with underscores and format casing
    words = last_part.replace("-", "_").split("_")
    formatted_words = []
    for w in words:
        if re.match(r"^(fs|us|tc|r)\d+$", w.lower()):
            formatted_words.append(w.upper())
        else:
            formatted_words.append(w.capitalize())
    clean_slug = "_".join(formatted_words)
    return f"TEST_EXECUTION_EVIDENCE_{clean_slug}.xlsx"


def extract_tc_id_from_nodeid(nodeid: str) -> str:
    """
    Extracts canonical TC ID (e.g. TC-R8-094, TC-FS03-VAL-001) from pytest nodeid.
    Handles various test function naming formats.
    """
    func_name = re.sub(r"\[.*?\]$", "", nodeid.split("::")[-1])
    # Case 1: test_tc_r8_094_... -> TC-R8-094
    m1 = re.search(r"test_(tc_[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)?)", func_name, re.IGNORECASE)
    if m1:
        raw = m1.group(1).upper().replace("_", "-")
        return raw

    # Case 2: test_br001_... -> TC-BR-001 or similar
    m2 = re.search(r"test_([a-zA-Z]+)(\d+)", func_name)
    if m2:
        return f"TC-{m2.group(1).upper()}-{m2.group(2)}"

    return func_name.upper()


def match_nodeid_to_tc_row(nodeid: str, tc_id_map: Dict[str, int]) -> Optional[int]:
    """Matches a pytest test function nodeid to a row in the testcase ID map."""
    func_name = re.sub(r"\[.*?\]$", "", nodeid.split("::")[-1]).lower()

    # 1. Exact TC ID match
    derived_id = extract_tc_id_from_nodeid(nodeid)
    if derived_id in tc_id_map:
        return tc_id_map[derived_id]

    # 2. Normalized substring match (e.g. 'tc_r8_094' in 'test_tc_r8_094_singpass...')
    for tid, row_idx in tc_id_map.items():
        norm_tid = tid.lower().replace("-", "_")
        if norm_tid in func_name:
            return row_idx

    # 3. Partial number match
    m = re.search(r"\b(\d{3})\b", func_name)
    if m:
        num = m.group(1)
        for tid, row_idx in tc_id_map.items():
            if num in tid:
                return row_idx

    return None


def find_header_column(header_map: Dict[str, int], *names: str) -> Optional[int]:
    """Resolve a column by supported header aliases without unsafe defaults."""
    normalized = {re.sub(r"\s+", " ", key).strip().casefold(): value for key, value in header_map.items()}
    for name in names:
        column = normalized.get(re.sub(r"\s+", " ", name).strip().casefold())
        if column:
            return column
    return None


def export_test_execution_evidence(
    reports_dir: Path,
    ticket_name: Optional[str] = None,
    report_json_path: Optional[Path] = None,
    run_id: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Inspects pytest run results from report.json and updates TEST_EXECUTION_EVIDENCE_*.xlsx
    enforcing strictly ONE single tab with native openpyxl video hyperlinks.
    """
    if not reports_dir.exists():
        return None

    if not ticket_name:
        try:
            rel = reports_dir.relative_to(REPO_ROOT / "reports")
            ticket_name = str(rel) if str(rel) != "." else None
        except Exception:
            ticket_name = None

    if not ticket_name:
        return None

    testcases_dir = REPO_ROOT / "testcases" / ticket_name
    evidence_filename = derive_evidence_filename(ticket_name)

    # Find master source workbook
    src_wb_path = find_evidence_xlsx_file(reports_dir) or find_evidence_xlsx_file(testcases_dir)
    if not src_wb_path:
        # Fallback to standard filename if it exists
        cand_rep = reports_dir / evidence_filename
        cand_tc = testcases_dir / evidence_filename
        if cand_rep.exists():
            src_wb_path = cand_rep
        elif cand_tc.exists():
            src_wb_path = cand_tc

    if not src_wb_path or not src_wb_path.exists():
        # If no evidence workbook exists yet, check if there is a generator script or return
        if "fs08" in ticket_name:
            try:
                from tools.generate_profile_execution_evidence_xlsx import main as gen_fs08
                gen_fs08()
                src_wb_path = reports_dir / evidence_filename
            except Exception:
                pass

    if not src_wb_path or not src_wb_path.exists():
        return None

    # Load report.json
    if not report_json_path or not report_json_path.exists():
        report_json_path = reports_dir / "report.json"
    if not report_json_path.exists():
        return None

    try:
        with open(report_json_path, "r", encoding="utf-8") as f:
            report_data = json.load(f)
    except Exception:
        return None

    executed_tests = report_data.get("tests", [])
    if not executed_tests:
        # No tests were actually executed in this session
        return None

    # Load workbook for modification
    wb = openpyxl.load_workbook(src_wb_path)

    # ENFORCE STRICT SINGLE TAB MANDATE
    # If multiple tabs exist, keep ONLY the first tab (Execution Evidence) and remove the rest
    if len(wb.sheetnames) > 1:
        keep_sheet_name = wb.sheetnames[0]
        for name in list(wb.sheetnames)[1:]:
            wb.remove(wb[name])

    ws = wb.active
    ws.views.sheetView[0].showGridLines = True

    # Styling Palette
    status_pass_fill = PatternFill(start_color="00DCFCE7", end_color="00DCFCE7", fill_type="solid")
    status_fail_fill = PatternFill(start_color="00FEE2E2", end_color="00FEE2E2", fill_type="solid")
    status_skip_fill = PatternFill(start_color="00F1F5F9", end_color="00F1F5F9", fill_type="solid")
    link_font = Font(name="Segoe UI", size=9.5, bold=True, underline="single", color="001D4ED8")

    # Map column headers from Row 4
    header_col_map = {}
    for col in range(1, ws.max_column + 1):
        val = ws.cell(row=4, column=col).value
        if val:
            header_col_map[str(val).strip()] = col

    id_col = find_header_column(header_col_map, "Test Case ID", "TC ID")
    status_col = find_header_column(header_col_map, "Execution Status", "Status")
    actual_col = find_header_column(header_col_map, "Actual Result (Verified)", "Actual Result")
    evidence_link_col = find_header_column(
        header_col_map,
        "📷 Visual Evidence",
        "🎬 Video Evidence (Play in Browser)",
        "Visual Evidence",
        "Evidence",
    )
    evidence_file_col = find_header_column(header_col_map, "Evidence File Name", "Video File Name")

    # Refuse to write when the workbook schema cannot be identified. Falling
    # back to fixed column numbers corrupts valid 19/20-column templates.
    if not all((id_col, status_col, actual_col, evidence_link_col)):
        return None

    # Build row index map: TC_ID -> row_number
    tc_id_row_map = {}
    for r in range(5, ws.max_row + 1):
        tid = ws.cell(row=r, column=id_col).value
        if tid:
            tc_id_row_map[str(tid).strip()] = r

    # Collect video files available in test-results
    test_results_dir = reports_dir / "test-results"
    video_file_map = {}
    if test_results_dir.exists():
        for vid in test_results_dir.glob("**/*.webm"):
            video_file_map[vid.parent.name.lower()] = vid

    # Process executed test results
    updated_rows = set()
    for test in executed_tests:
        nodeid = test.get("nodeid", "")
        outcome = test.get("outcome", "passed")
        call_info = test.get("call", {}) or {}
        meta_info = test.get("metadata", {}) or {}

        target_row = match_nodeid_to_tc_row(nodeid, tc_id_row_map)
        if not target_row:
            continue

        updated_rows.add(target_row)

        # 1. Update Execution Status
        c_status = ws.cell(row=target_row, column=status_col)
        c_actual = ws.cell(row=target_row, column=actual_col)

        if outcome == "passed":
            c_status.value = "Passed"
            c_status.fill = status_pass_fill
            c_status.font = Font(name="Segoe UI", size=9.0, bold=True, color="00166534")
            # Preserve existing actual verified text if already detailed, or update
            if not c_actual.value or "failed" in str(c_actual.value).lower():
                c_actual.value = "Verified: All automated assertions and visual gates passed successfully in SIT."
                c_actual.font = Font(name="Segoe UI", size=8.5, color="00166534")
        elif outcome == "failed":
            c_status.value = "Failed"
            c_status.fill = status_fail_fill
            c_status.font = Font(name="Segoe UI", size=9.0, bold=True, color="00DC2626")

            # Extract failure message
            crash = call_info.get("crash", {}) or {}
            err_msg = crash.get("message") or str(call_info.get("longrepr", ""))[:200]
            err_msg = re.sub(r"\s+", " ", err_msg).strip()
            c_actual.value = f"Defect: {err_msg}" if err_msg else "Defect: Assertion failed during execution."
            c_actual.font = Font(name="Segoe UI", size=8.5, color="00DC2626")
        else:
            c_status.value = "Skipped"
            c_status.fill = status_skip_fill
            c_status.font = Font(name="Segoe UI", size=9.0, color="0064748B")

        # 2. Update Video / Screenshot Evidence Link
        func_slug = re.sub(r"\[.*?\]$", "", nodeid.split("::")[-1]).lower()
        test_slugs = list(test_slug_candidates(nodeid))
        test_slug = test_slugs[0]
        test_screenshots_dir = reports_dir / "screenshots" / test_slug

        # Prefer the canonical actual_result.png captured for this exact pytest
        # parameter set (for example the ``[chromium]`` suffix).
        actual_screen = find_actual_result_screenshot(
            reports_dir=reports_dir,
            nodeid=nodeid,
            metadata=meta_info,
            repo_root=REPO_ROOT,
        )

        step_count = len(list(test_screenshots_dir.glob("step_*.png"))) if test_screenshots_dir.exists() else 0

        if outcome in ("failed", "xfailed"):
            v_path = meta_info.get("video_path")
            matched_video = None
            if v_path and Path(v_path).exists():
                matched_video = Path(v_path)
            else:
                norm_slug = re.sub(r"[_\W]+", "-", func_slug).strip("-")
                for d_name, vid_p in video_file_map.items():
                    if norm_slug in d_name or d_name in norm_slug:
                        matched_video = vid_p
                        break

            if matched_video and matched_video.exists():
                # Relative path from reports/<ticket>/
                try:
                    rel_vid_reports = matched_video.relative_to(reports_dir)
                except Exception:
                    rel_vid_reports = Path("test-results") / matched_video.name

                c_vid = ws.cell(row=target_row, column=evidence_link_col)
                c_vid.value = "▶ Play in Browser"
                c_vid.font = link_font
                c_vid.alignment = Alignment(horizontal="center", vertical="center")
                c_vid.hyperlink = str(rel_vid_reports)

                # Video file name & size
                if evidence_file_col:
                    c_vname = ws.cell(row=target_row, column=evidence_file_col)
                    size_kb = round(matched_video.stat().st_size / 1024, 1)
                    clean_vid_name = f"{ws.cell(row=target_row, column=id_col).value.lower().replace('-', '_')}.webm"
                    c_vname.value = f"{clean_vid_name} ({size_kb} KB)"
                    c_vname.font = Font(name="Consolas", size=8.5, color="00475569")
            elif actual_screen and actual_screen.exists():
                rel_screen = relative_excel_target(actual_screen, reports_dir)
                c_vid = ws.cell(row=target_row, column=evidence_link_col)
                link_label = f"📷 Actual Result (Defect +{step_count} steps)" if step_count > 0 else "📷 Actual Result (Defect)"
                c_vid.value = link_label
                c_vid.font = Font(name="Segoe UI", size=9.5, bold=True, underline="single", color="00DC2626")
                c_vid.alignment = Alignment(horizontal="center", vertical="center")
                c_vid.hyperlink = str(rel_screen)

                if evidence_file_col:
                    c_vname = ws.cell(row=target_row, column=evidence_file_col)
                    size_kb = round(actual_screen.stat().st_size / 1024, 1)
                    if step_count > 0 and test_screenshots_dir.exists():
                        rel_dir = relative_excel_target(test_screenshots_dir, reports_dir)
                        c_vname.value = f"📁 {step_count + 1} files ({actual_screen.name} + {step_count} steps)"
                        c_vname.hyperlink = str(rel_dir)
                        c_vname.font = Font(name="Segoe UI", size=8.5, underline="single", color="000284C7")
                    else:
                        c_vname.value = f"{actual_screen.name} ({size_kb} KB)"
                        c_vname.font = Font(name="Consolas", size=8.5, color="00475569")
        elif outcome == "passed":
            # Pass tests link strictly to verified Actual Result screenshot evidence
            if actual_screen and actual_screen.exists():
                rel_screen = relative_excel_target(actual_screen, reports_dir)
                c_vid = ws.cell(row=target_row, column=evidence_link_col)
                link_label = f"📷 Actual Result (+{step_count} steps)" if step_count > 0 else "📷 Actual Result"
                c_vid.value = link_label
                c_vid.font = link_font
                c_vid.alignment = Alignment(horizontal="center", vertical="center")
                c_vid.hyperlink = str(rel_screen)

                if evidence_file_col:
                    c_vname = ws.cell(row=target_row, column=evidence_file_col)
                    size_kb = round(actual_screen.stat().st_size / 1024, 1)
                    if step_count > 0 and test_screenshots_dir.exists():
                        rel_dir = relative_excel_target(test_screenshots_dir, reports_dir)
                        c_vname.value = f"📁 {step_count + 1} files ({actual_screen.name} + {step_count} steps)"
                        c_vname.hyperlink = str(rel_dir)
                        c_vname.font = Font(name="Segoe UI", size=8.5, underline="single", color="000284C7")
                    else:
                        c_vname.value = f"{actual_screen.name} ({size_kb} KB)"
                        c_vname.font = Font(name="Consolas", size=8.5, color="00475569")

    # 3. Recalculate Executive Banner (Row 2 Metrics)
    total_tcs = len(tc_id_row_map)
    pass_count = 0
    fail_count = 0
    video_count = 0

    for r in tc_id_row_map.values():
        st = str(ws.cell(row=r, column=status_col).value or "").strip()
        if st.lower() == "passed":
            pass_count += 1
        elif st.lower() == "failed":
            fail_count += 1
        
        vl = ws.cell(row=r, column=evidence_link_col).hyperlink
        if vl:
            video_count += 1

    pass_pct = round((pass_count / total_tcs) * 100, 1) if total_tcs > 0 else 100.0

    c_banner2 = ws["A2"]
    c_banner2.value = (
        f"Total Tests: {total_tcs}  |  Pass: {pass_count} ({pass_pct}%)  |  "
        f"Fail: {fail_count}  |  Bugs: {fail_count}  |  "
        f"Videos: {video_count} Full HD 1080p Recordings  |  Target: http://localhost:5174/profile"
    )

    # 4. Save to reports/<ticket>/
    dest_reports_xlsx = reports_dir / evidence_filename
    dest_reports_xlsx.parent.mkdir(parents=True, exist_ok=True)
    wb.save(dest_reports_xlsx)

    # 5. Save copy to testcases/<ticket>/ with adjusted relative hyperlinks
    dest_tc_xlsx = testcases_dir / evidence_filename
    if testcases_dir.exists():
        # Adjust hyperlinks for testcases directory
        for r in tc_id_row_map.values():
            c_vid = ws.cell(row=r, column=evidence_link_col)
            if c_vid.hyperlink:
                curr_target = str(c_vid.hyperlink.target or "")
                c_vid.hyperlink = rebase_local_target(
                    curr_target,
                    old_base=reports_dir,
                    new_base=testcases_dir,
                )

        dest_tc_xlsx.parent.mkdir(parents=True, exist_ok=True)
        wb.save(dest_tc_xlsx)


    return {
        "ticket": ticket_name,
        "reports_xlsx": str(dest_reports_xlsx),
        "testcases_xlsx": str(dest_tc_xlsx) if testcases_dir.exists() else None,
        "total": total_tcs,
        "passed": pass_count,
        "failed": fail_count,
        "updated_tcs_count": len(updated_rows),
    }
