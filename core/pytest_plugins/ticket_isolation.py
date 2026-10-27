"""
core/pytest_plugins/ticket_isolation.py - Ticket-scoped artifact isolation and HTML reporting orchestration.
Manages run_id generation, report directory isolation, and ExtentReports execution.
"""
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shutil
from typing import Optional
import uuid
import pytest
from core.pytest_plugins.browser_engine import is_parallel_execution, is_cli_headed_explicit

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_DIR = REPO_ROOT
DEFAULT_REPORTS_DIR = WORKSPACE_DIR / "reports"


def detect_ticket_folder_from_args(config) -> Optional[str]:
    """Extract ticket folder name (e.g. us01_bing_search, fs08/fs08-parent-profile) from CLI args or test paths."""
    for arg in getattr(config, "args", []):
        if str(arg).startswith("-"):
            continue
        # Strip pytest node selector (e.g. path.py::Class::func) before parsing path parts
        clean_arg = str(arg).split("::")[0]
        p = Path(clean_arg)
        parts = p.parts
        if "tests" in parts:
            idx = parts.index("tests")
            rel_parts = [part for part in parts[idx + 1:] if not part.endswith(".py")]
            if rel_parts:
                return "/".join(rel_parts)
            return None
        elif (WORKSPACE_DIR / "tests" / clean_arg).is_dir():
            return str(Path(clean_arg))
    return None


def pytest_configure(config):
    """Dynamically isolate output directories for Playwright video and JSON report per ticket."""
    ticket = detect_ticket_folder_from_args(config)
    config._ticket_name = ticket
    ticket_reports_dir = (DEFAULT_REPORTS_DIR / ticket) if ticket else DEFAULT_REPORTS_DIR
    config._ticket_reports_dir = ticket_reports_dir

    # Generate or reuse run_id for this test session
    run_id = getattr(config, "_run_id", None) or os.environ.get("PYTEST_RUN_ID")
    if not run_id:
        now = datetime.now()
        hash_suffix = uuid.uuid4().hex[:6].upper()
        run_id = f"RUN-{now.strftime('%Y%m%d')}-{hash_suffix}"
        os.environ["PYTEST_RUN_ID"] = run_id
    config._run_id = run_id

    # Isolate video recordings and Playwright artifacts into test-results/<run_id>
    curr_out = getattr(config.option, "output", None)
    default_outputs = (
        "reports/test-results",
        str(DEFAULT_REPORTS_DIR / "test-results"),
        str(ticket_reports_dir / "test-results"),
    )
    if not curr_out or curr_out in default_outputs:
        config.option.output = str(ticket_reports_dir / "test-results" / run_id)

    # Isolate JSON report per ticket
    curr_json = getattr(config.option, "json_report_file", None)
    if not curr_json or curr_json in ("reports/report.json", str(DEFAULT_REPORTS_DIR / "report.json")):
        config.option.json_report_file = str(ticket_reports_dir / "report.json")

    # Parallel Execution: Automatically switch to Headless when running with xdist (-n)
    if is_parallel_execution(config) and not is_cli_headed_explicit(config):
        if hasattr(config.option, "headed"):
            config.option.headed = False
        config._parallel_headless = True


def pytest_collection_finish(session):
    """Fallback: if ticket was not detected from CLI args, determine from collected items."""
    config = session.config
    if not getattr(config, "_ticket_name", None):
        tickets = set()
        tests_dir = WORKSPACE_DIR / "tests"
        for item in session.items:
            try:
                rel = Path(item.fspath).relative_to(tests_dir)
                rel_dir = rel.parent
                if str(rel_dir) != "." and not any(p.startswith(("_", ".")) for p in rel_dir.parts):
                    tickets.add(str(rel_dir))
            except Exception:
                pass

        if len(tickets) == 1:
            ticket = list(tickets)[0]
            config._ticket_name = ticket
            ticket_reports_dir = DEFAULT_REPORTS_DIR / ticket
            config._ticket_reports_dir = ticket_reports_dir
            run_id = getattr(config, "_run_id", "RUN-DEFAULT")
            curr_out = getattr(config.option, "output", None)
            default_outputs = (
                "reports/test-results",
                str(DEFAULT_REPORTS_DIR / "test-results"),
                str(ticket_reports_dir / "test-results"),
            )
            if not curr_out or curr_out in default_outputs or curr_out.endswith("test-results"):
                config.option.output = str(ticket_reports_dir / "test-results" / run_id)
            if getattr(config.option, "json_report_file", None) in ("reports/report.json", str(DEFAULT_REPORTS_DIR / "report.json")):
                config.option.json_report_file = str(ticket_reports_dir / "report.json")


@pytest.hookimpl(optionalhook=True)
def pytest_json_modifyreport(json_report):
    """Ensure run_id is saved in the pytest JSON report metadata."""
    run_id = os.environ.get("PYTEST_RUN_ID")
    if run_id:
        json_report["run_id"] = run_id


@pytest.fixture(scope="session")
def search_data():
    """Load test input data from data/search_data.json."""
    data_file = WORKSPACE_DIR / "data" / "search_data.json"
    if data_file.exists():
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def pytest_sessionstart(session):
    """
    Ensure test artifact directories exist.
    Preserves historical runs and prior run_id test-results without wiping them.
    Safe for pytest-xdist: ONLY executes setup on the controller (master) process.
    """
    if hasattr(session.config, "workerinput"):
        return

    reports_dir = getattr(session.config, "_ticket_reports_dir", DEFAULT_REPORTS_DIR)
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "screenshots").mkdir(parents=True, exist_ok=True)
    (reports_dir / "history").mkdir(parents=True, exist_ok=True)
    (reports_dir / "test-results").mkdir(parents=True, exist_ok=True)

    run_id = getattr(session.config, "_run_id", None) or os.environ.get("PYTEST_RUN_ID")
    if run_id:
        (reports_dir / "test-results" / run_id).mkdir(parents=True, exist_ok=True)


def extract_hierarchy_from_nodeid(nodeid: str) -> tuple[str, str, str]:
    """
    Extracts 3-level testing hierarchy:
    Level 1: Suite slug (e.g. fs08, fs09, us04_curricula_trainer)
    Level 2: Scenario slug (e.g. ts01_auth_and_session, ts01_personal_info)
    Level 3: Test Case slug (e.g. tc_r8_001_landing_page, tc_pi_001_preferred_name)
    """
    parts = nodeid.split("::")
    file_path = Path(parts[0])

    suite_slug = "suite"
    for i, p in enumerate(file_path.parts):
        if p == "tests" and i + 1 < len(file_path.parts):
            cand = file_path.parts[i + 1]
            if not cand.endswith(".py"):
                suite_slug = cand
            break

    scenario_slug = re.sub(r"^test_", "", file_path.stem)
    if not scenario_slug or scenario_slug == file_path.stem:
        scenario_slug = file_path.stem

    raw_func = parts[-1] if len(parts) > 1 else "test_case"
    clean_func = re.sub(r"\[.*?\]$", "", raw_func)
    tc_slug = re.sub(r"^test_", "", clean_func)

    return suite_slug, scenario_slug, tc_slug


def organize_test_results_by_run_id(reports_dir: Path, run_id: str, report_json_path: Optional[Path] = None):
    """
    Organize all test results into a 3-tier hierarchy:
    reports/<suite>/test-results/<scenario_slug>/<tc_slug>/video.webm & failure.png
    Also preserves historical run isolation in test-results/<run_id>/.
    """
    test_results_dir = reports_dir / "test-results"
    test_results_dir.mkdir(parents=True, exist_ok=True)

    run_dir = test_results_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    for item in list(test_results_dir.iterdir()):
        if item.is_dir() and item.name != run_id and not item.name.startswith("RUN-") and not item.name.startswith("ts"):
            dest = run_dir / item.name
            try:
                if not dest.exists():
                    shutil.move(str(item), str(dest))
                else:
                    for sub in item.iterdir():
                        sub_dest = dest / sub.name
                        if not sub_dest.exists():
                            shutil.move(str(sub), str(sub_dest))
                    shutil.rmtree(item, ignore_errors=True)
            except Exception:
                pass

    subdirs = [d for d in run_dir.iterdir() if d.is_dir()]
    dir_map = {}
    for d in subdirs:
        norm_key = re.sub(r"[_\W]+", "-", d.name.lower()).strip("-")
        dir_map.setdefault(norm_key, []).append(d)

    for norm_key, dirs in dir_map.items():
        if len(dirs) > 1:
            best_dir = next((d for d in dirs if (d / "video.webm").exists()), dirs[0])
            for d in dirs:
                if d != best_dir:
                    for f in d.iterdir():
                        target_f = best_dir / f.name
                        if not target_f.exists():
                            shutil.move(str(f), str(target_f))
                    shutil.rmtree(d, ignore_errors=True)

    if report_json_path and report_json_path.exists():
        try:
            with open(report_json_path, "r", encoding="utf-8") as f:
                report_data = json.load(f)

            updated = False
            if report_data.get("run_id") != run_id:
                report_data["run_id"] = run_id
                updated = True

            for test in report_data.get("tests", []):
                nodeid = test.get("nodeid", "")
                suite_slug, scenario_slug, tc_slug = extract_hierarchy_from_nodeid(nodeid)
                target_tc_dir = test_results_dir / scenario_slug / tc_slug
                target_tc_dir.mkdir(parents=True, exist_ok=True)

                meta = test.get("metadata", {})
                v_path = meta.get("video_path")

                # Match video in run_dir or test_results_dir
                matched_video: Optional[Path] = None
                if v_path and Path(v_path).exists() and Path(v_path).is_file():
                    matched_video = Path(v_path)
                else:
                    norm_tc = re.sub(r"[_\W]+", "-", tc_slug.lower()).strip("-")
                    for d in run_dir.iterdir():
                        if d.is_dir():
                            d_norm = re.sub(r"[_\W]+", "-", d.name.lower()).strip("-")
                            if norm_tc in d_norm or d_norm in norm_tc:
                                cand = d / "video.webm"
                                if cand.exists() and cand.is_file():
                                    matched_video = cand
                                    break

                if matched_video:
                    dest_video = target_tc_dir / "video.webm"
                    if not dest_video.exists() or dest_video != matched_video:
                        try:
                            shutil.copy2(str(matched_video), str(dest_video))
                        except Exception:
                            pass
                    meta["video_path"] = str(dest_video.resolve())
                    updated = True

                # Match screenshots
                for s_idx, step in enumerate(meta.get("steps", [])):
                    s_screen = step.get("screenshot")
                    if s_screen:
                        sp = Path(s_screen)
                        if not sp.is_absolute():
                            sp = WORKSPACE_DIR / sp
                        if sp.exists() and sp.is_file():
                            if step.get("status") == "failed":
                                dest_screen = target_tc_dir / "failure.png"
                                try:
                                    shutil.copy2(str(sp), str(dest_screen))
                                except Exception:
                                    pass
                                step["screenshot"] = str(dest_screen.resolve())
                                updated = True
                            else:
                                dest_screen = target_tc_dir / f"step_{s_idx + 1}.png"
                                try:
                                    shutil.copy2(str(sp), str(dest_screen))
                                except Exception:
                                    pass
                                step["screenshot"] = str(dest_screen.resolve())
                                updated = True

            if updated:
                with open(report_json_path, "w", encoding="utf-8") as f:
                    json.dump(report_data, f, indent=2)
        except Exception:
            pass


@pytest.hookimpl(trylast=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Automatically generate the self-contained Enterprise HTML report in the ticket folder."""
    if hasattr(config, "workerinput"):
        return

    reports_dir = getattr(config, "_ticket_reports_dir", DEFAULT_REPORTS_DIR)
    run_id = getattr(config, "_run_id", None) or os.environ.get("PYTEST_RUN_ID", "RUN-UNKNOWN")

    json_file_path = getattr(config.option, "json_report_file", None)
    report_json = Path(json_file_path) if json_file_path else (reports_dir / "report.json")

    json_plugin = getattr(config, "_json_report", None)
    if json_plugin and hasattr(json_plugin, "save_report"):
        try:
            json_plugin.save_report(str(report_json))
        except Exception:
            pass

    organize_test_results_by_run_id(reports_dir=reports_dir, run_id=run_id, report_json_path=report_json)

    run_results_dir = reports_dir / "test-results" / run_id
    if run_results_dir.exists():
        videos = list(run_results_dir.glob("**/*.webm"))
        if videos:
            terminalreporter.write_sep("=", f"📹 [VIDEO RECORDING SAVED TO RUN ID: {run_id} (FULL HD 1080p)]", bold=True, green=True)
            for v in sorted(videos):
                try:
                    rel_v = v.relative_to(WORKSPACE_DIR)
                except Exception:
                    rel_v = v
                terminalreporter.write_line(f"   -> {rel_v}")

    if report_json.exists():
        try:
            from reporting import ReportGenerator
            generator = ReportGenerator(workspace_dir=WORKSPACE_DIR, reports_dir=reports_dir)
            out_html = generator.generate(json_path=report_json)
            terminalreporter.write_sep("=", "✅ [ENTERPRISE HTML REPORT SUCCESSFULLY GENERATED]", bold=True, green=True)
            terminalreporter.write_line(f"   Latest Report        : {reports_dir / 'execution_report.html'}")
            terminalreporter.write_line(f"   Historical Run Report: {out_html}")
        except Exception as err:
            terminalreporter.write_line(f"[Auto-Report] Error generating report: {err}", red=True)

        try:
            from core.pytest_plugins.excel_evidence_exporter import export_test_execution_evidence
            ticket_name = getattr(config, "_ticket_name", None)
            res = export_test_execution_evidence(
                reports_dir=reports_dir,
                ticket_name=ticket_name,
                report_json_path=report_json,
                run_id=run_id,
            )
            if res:
                terminalreporter.write_sep("=", "📊 [TEST EXECUTION EVIDENCE EXCEL AUTOMATICALLY UPDATED]", bold=True, green=True)
                terminalreporter.write_line(f"   Reports Excel  : {res.get('reports_xlsx')}")
                if res.get("testcases_xlsx"):
                    terminalreporter.write_line(f"   TestCases Excel: {res.get('testcases_xlsx')}")
                terminalreporter.write_line(f"   Summary        : Total {res.get('total')} TCs | Passed {res.get('passed')} | Failed {res.get('failed')} (Single-Tab Enforced)")
        except Exception as err:
            terminalreporter.write_line(f"[Auto-Excel] Error exporting execution evidence: {err}", red=True)


@pytest.fixture(scope="session", autouse=True)
def delete_output_dir():
    """Prevent pytest-xdist worker sessions from wiping each other's output directory."""
    pass


@pytest.fixture(scope="session", autouse=True)
def ensure_reports_dir(request):
    """Ensure reports directory, screenshots, and history directory exist for test evidence and artifacts."""
    reports_dir = getattr(request.config, "_ticket_reports_dir", DEFAULT_REPORTS_DIR)
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "screenshots").mkdir(parents=True, exist_ok=True)
    (reports_dir / "history").mkdir(parents=True, exist_ok=True)
