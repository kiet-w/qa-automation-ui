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
    """Extract ticket folder name (e.g. us01_bing_search, us04_curricula_trainer) from CLI args or test paths."""
    for arg in getattr(config, "args", []):
        if str(arg).startswith("-"):
            continue
        p = Path(arg)
        parts = p.parts
        if "tests" in parts:
            idx = parts.index("tests")
            if idx + 1 < len(parts):
                candidate = parts[idx + 1]
                if not candidate.endswith(".py"):
                    return candidate
                return None
        elif (WORKSPACE_DIR / "tests" / arg).is_dir():
            return Path(arg).name
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
                if len(rel.parts) > 1 and not rel.parts[0].startswith(("_", ".")):
                    tickets.add(rel.parts[0])
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


def organize_test_results_by_run_id(reports_dir: Path, run_id: str, report_json_path: Optional[Path] = None):
    """
    Ensure all test results (videos, Playwright artifacts) are strictly organized
    under reports/<ticket>/test-results/<run_id>/.
    Consolidates duplicate video directories and synchronizes report.json paths.
    """
    test_results_dir = reports_dir / "test-results"
    test_results_dir.mkdir(parents=True, exist_ok=True)

    run_dir = test_results_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    for item in list(test_results_dir.iterdir()):
        if item.is_dir() and item.name != run_id and not item.name.startswith("RUN-"):
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
                meta = test.get("metadata", {})
                v_path = meta.get("video_path")
                if v_path:
                    vp = Path(v_path)
                    if not vp.exists() or run_id not in vp.parts:
                        norm_parent = re.sub(r"[_\W]+", "-", vp.parent.name.lower()).strip("-")
                        matched = None
                        for d in run_dir.iterdir():
                            if d.is_dir() and re.sub(r"[_\W]+", "-", d.name.lower()).strip("-") == norm_parent:
                                cand = d / vp.name
                                if cand.exists() and cand.is_file():
                                    matched = cand
                                    break
                        if matched:
                            meta["video_path"] = str(matched.resolve())
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
