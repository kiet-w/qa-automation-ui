"""conftest.py - Shared fixtures, Brave browser setup, and reporting hooks."""
import json
from pathlib import Path
import shutil
import time
from typing import Optional
import pytest
from playwright.sync_api import Page
from playwright_stealth import Stealth

import re
import sys

BRAVE_PATH = "/usr/bin/brave"
WORKSPACE_DIR = Path(__file__).resolve().parent
DEFAULT_REPORTS_DIR = WORKSPACE_DIR / "reports"
REPORTS_DIR = DEFAULT_REPORTS_DIR
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"


def is_parallel_execution(config) -> bool:
    """Check if pytest is running in parallel mode via pytest-xdist (-n > 1 or -n auto/logical)."""
    numproc = getattr(config.option, "numprocesses", None)
    if numproc is not None:
        if isinstance(numproc, int) and numproc > 1:
            return True
        if isinstance(numproc, str):
            if numproc.isdigit() and int(numproc) > 1:
                return True
            if numproc.lower() in ("auto", "logical"):
                return True

    cli_args = list(getattr(config.invocation_params, "args", [])) + sys.argv
    for idx, arg in enumerate(cli_args):
        if arg in ("-n", "--numprocesses"):
            if idx + 1 < len(cli_args) and str(cli_args[idx + 1]) not in ("0", "1"):
                return True
        elif str(arg).startswith(("-n=", "--numprocesses=")):
            val = str(arg).split("=", 1)[1]
            if val not in ("0", "1"):
                return True
    return False


def is_cli_headed_explicit(config) -> bool:
    """Check if --headed was explicitly passed by the user on the CLI."""
    cli_args = list(getattr(config.invocation_params, "args", [])) + sys.argv
    return "--headed" in cli_args


def detect_ticket_folder_from_args(config) -> Optional[str]:
    """Extract ticket folder name (e.g. us01_bing_search) from CLI args or test paths."""
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
                # E.g. tests/us01_bing_search/test_bing_search.py
                return candidate
        elif (WORKSPACE_DIR / "tests" / arg).is_dir():
            return Path(arg).name
    return None


def pytest_configure(config):
    """Dynamically isolate output directories for Playwright video and JSON report per ticket."""
    ticket = detect_ticket_folder_from_args(config)
    config._ticket_name = ticket
    ticket_reports_dir = (DEFAULT_REPORTS_DIR / ticket) if ticket else DEFAULT_REPORTS_DIR
    config._ticket_reports_dir = ticket_reports_dir

    # Isolate video recordings and Playwright artifacts
    curr_out = getattr(config.option, "output", None)
    if not curr_out or curr_out in ("reports/test-results", str(DEFAULT_REPORTS_DIR / "test-results")):
        config.option.output = str(ticket_reports_dir / "test-results")

    # Isolate JSON report per ticket
    curr_json = getattr(config.option, "json_report_file", None)
    if not curr_json or curr_json in ("reports/report.json", str(DEFAULT_REPORTS_DIR / "report.json")):
        config.option.json_report_file = str(ticket_reports_dir / "report.json")

    # Parallel Execution: Automatically switch to Headless when running with xdist (-n)
    # unless --headed was explicitly passed on the CLI.
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
            if getattr(config.option, "output", None) in ("reports/test-results", str(DEFAULT_REPORTS_DIR / "test-results")):
                config.option.output = str(ticket_reports_dir / "test-results")
            if getattr(config.option, "json_report_file", None) in ("reports/report.json", str(DEFAULT_REPORTS_DIR / "report.json")):
                config.option.json_report_file = str(ticket_reports_dir / "report.json")


class StepTracker:
    """Tracks and records execution steps, statuses, durations, and screenshots."""

    def __init__(self, page: Page, json_metadata=None, reports_dir=None, test_name: str = ""):
        self.page = page
        self.json_metadata = json_metadata if json_metadata is not None else {}
        if "steps" not in self.json_metadata:
            self.json_metadata["steps"] = []
        self.steps = self.json_metadata["steps"]
        self.reports_dir = Path(reports_dir) if reports_dir else DEFAULT_REPORTS_DIR
        self.screenshots_dir = self.reports_dir / "screenshots"
        self.test_name = test_name
        self.test_slug = re.sub(r"[^\w]+", "_", test_name.lower()).strip("_") if test_name else ""
        self.current_step = None
        self._step_counter = 0
        self._step_stack = []
        self.test_start_time = time.time()

    def set_page(self, page: Page):
        """Update current active page for taking screenshots when switching context or tab."""
        self.page = page

    def attach_screenshot(self, path: str):
        """Attach a screenshot file path to the current active step (or most recent step)."""
        if self.current_step is not None:
            self.current_step["screenshot"] = str(path)
        elif self.steps:
            self.steps[-1]["screenshot"] = str(path)

    def set_actual(self, actual_text: str):
        """Set actual execution outcome description for the current step."""
        if self.current_step is not None:
            self.current_step["actual"] = actual_text

    def set_expected(self, expected_text: str):
        """Set expected behavior description for the current step."""
        if self.current_step is not None:
            self.current_step["expected"] = expected_text

    def __call__(
        self,
        title: str,
        page: Optional[Page] = None,
        capture_screenshot: bool = False,
        expected: Optional[str] = None,
        actual: Optional[str] = None,
    ):
        """Context manager factory: with step('title', expected=..., actual=...):"""
        return _StepContext(
            tracker=self,
            title=title,
            page=page,
            capture_screenshot=capture_screenshot,
            expected=expected,
            actual=actual,
        )


class _StepContext:
    """Context manager for an individual execution step."""

    def __init__(
        self,
        tracker: StepTracker,
        title: str,
        page: Optional[Page] = None,
        capture_screenshot: bool = False,
        expected: Optional[str] = None,
        actual: Optional[str] = None,
    ):
        self.tracker = tracker
        self.title = title
        self.page = page
        self.capture_screenshot = capture_screenshot
        self.expected = expected
        self.actual = actual
        self.step_data = None
        self.start_time = None
        self.step_index = 0

    def set_page(self, page: Page):
        self.tracker.set_page(page)

    def attach_screenshot(self, path: str):
        self.tracker.attach_screenshot(path)

    def set_actual(self, actual_text: str):
        self.tracker.set_actual(actual_text)

    def set_expected(self, expected_text: str):
        self.tracker.set_expected(expected_text)

    def __enter__(self):
        self.tracker._step_counter += 1
        self.step_index = self.tracker._step_counter
        self.start_time = time.time()
        start_offset = max(0.0, round(self.start_time - self.tracker.test_start_time, 2))

        if self.page is not None:
            self.tracker.set_page(self.page)

        self.step_data = {
            "title": self.title,
            "status": "passed",
            "duration": 0.0,
            "start_offset": start_offset,
            "end_offset": start_offset,
            "expected": self.expected,
            "actual": self.actual,
            "screenshot": None,
            "error": None,
        }
        self.tracker.steps.append(self.step_data)
        self.tracker._step_stack.append(self.step_data)
        self.tracker.current_step = self.step_data
        return self.tracker

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = round(time.time() - self.start_time, 2)
        self.step_data["duration"] = duration
        self.step_data["end_offset"] = round(self.step_data["start_offset"] + duration, 2)

        self.tracker.screenshots_dir.mkdir(parents=True, exist_ok=True)
        timestamp = int(time.time() * 1000)
        prefix = f"{self.tracker.test_slug}_" if self.tracker.test_slug else ""
        active_page = self.page or self.tracker.page

        if exc_type is not None:
            self.step_data["status"] = "failed"
            self.step_data["error"] = str(exc_val)

            fail_filename = f"fail_{prefix}step_{self.step_index}_{timestamp}.png"
            fail_path = self.tracker.screenshots_dir / fail_filename
            try:
                rel_fail_path = str(fail_path.relative_to(WORKSPACE_DIR))
            except Exception:
                rel_fail_path = str(fail_path)
            try:
                if active_page and not active_page.is_closed():
                    active_page.screenshot(path=str(fail_path), full_page=False)
                    self.step_data["screenshot"] = rel_fail_path
            except Exception as err:
                print(f"[StepTracker] Warning: Failed to capture failure screenshot: {err}")

            if self.tracker._step_stack:
                self.tracker._step_stack.pop()
            self.tracker.current_step = (
                self.tracker._step_stack[-1] if self.tracker._step_stack else None
            )
            return False  # Propagate exception to pytest

        # Success case: capture screenshot if requested and not manually attached
        if self.capture_screenshot and not self.step_data.get("screenshot"):
            step_filename = f"{prefix}step_{self.step_index}_{timestamp}.png"
            step_path = self.tracker.screenshots_dir / step_filename
            try:
                rel_step_path = str(step_path.relative_to(WORKSPACE_DIR))
            except Exception:
                rel_step_path = str(step_path)
            try:
                if active_page and not active_page.is_closed():
                    active_page.screenshot(path=str(step_path), full_page=False)
                    self.step_data["screenshot"] = rel_step_path
            except Exception as err:
                print(f"[StepTracker] Warning: Failed to capture step screenshot: {err}")

        if self.tracker._step_stack:
            self.tracker._step_stack.pop()
        self.tracker.current_step = (
            self.tracker._step_stack[-1] if self.tracker._step_stack else None
        )
        return False


@pytest.fixture
def step(request, page: Page, json_metadata):
    """Fixture providing an isolated StepTracker instance for each test method."""
    reports_dir = getattr(request.config, "_ticket_reports_dir", DEFAULT_REPORTS_DIR)
    test_name = request.node.name
    return StepTracker(page=page, json_metadata=json_metadata, reports_dir=reports_dir, test_name=test_name)


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, pytestconfig):
    """
    Configure pytest-playwright to use the system Brave browser (/usr/bin/brave)
    with anti-bot automation flags disabled.
    Automatically forces headless=True when running parallel unless --headed is explicitly passed on CLI.
    """
    args = list(browser_type_launch_args.get("args", []))
    anti_bot_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-infobars",
        "--window-size=1920,1080",
        "--start-maximized",
    ]
    for arg in anti_bot_args:
        if arg not in args:
            args.append(arg)

    opts = {
        **browser_type_launch_args,
        "args": args,
    }
    if Path(BRAVE_PATH).exists():
        opts["executable_path"] = BRAVE_PATH

    # If running parallel and user did not explicitly request --headed on CLI, enforce headless=True
    if is_parallel_execution(pytestconfig) and not is_cli_headed_explicit(pytestconfig):
        opts["headless"] = True
    elif is_cli_headed_explicit(pytestconfig):
        opts["headless"] = False

    return opts


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure realistic desktop browser profile with Full HD 1080p resolution and crisp video recording."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "record_video_size": {"width": 1920, "height": 1080},
        "device_scale_factor": 1,
        "user_agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "locale": "en-US",
        "timezone_id": "America/New_York",
    }


@pytest.fixture(autouse=True)
def setup_page(page: Page, json_metadata, request):
    """
    Apply comprehensive stealth patches and auto-dismiss consent overlays.
    Teardown: Safely closes browser context, captures 1:1 video per test,
    and records video_path into json_metadata["video_path"].
    """
    # 1. Apply Playwright Stealth evasion patches
    stealth = Stealth()
    stealth.apply_stealth_sync(page)

    # 2. Auto-dismiss cookie consent overlays (Bing/Google)
    page.add_init_script("""
        const observer = new MutationObserver(() => {
            const btn = document.querySelector('#bnp_btn_accept a, #bnp_btn_reject a, #bnp_cookie_banner a');
            if (btn) btn.click();
        });
        observer.observe(document.documentElement, { childList: true, subtree: true });
    """)
    yield page

    # Teardown: Safely close context and record video path 1:1 per test
    try:
        video = getattr(page, "video", None)
        context = getattr(page, "context", None)

        if context:
            try:
                context.close()
            except Exception:
                pass

        if video:
            video_path = None
            try:
                video_path = video.path()
            except Exception:
                pass

            # If output directory is defined, save/copy video to test-scoped artifact folder
            reports_dir = getattr(request.config, "_ticket_reports_dir", DEFAULT_REPORTS_DIR)
            test_results_dir = Path(getattr(request.config.option, "output", reports_dir / "test-results"))
            node_slug = re.sub(r"[^\w]+", "-", request.node.nodeid.lower()).strip("-")
            target_video_dir = test_results_dir / node_slug
            target_video_file = target_video_dir / "video.webm"

            try:
                target_video_dir.mkdir(parents=True, exist_ok=True)
                video.save_as(str(target_video_file))
                recorded_path = str(target_video_file)
            except Exception:
                recorded_path = str(video_path) if video_path else None

            if recorded_path:
                json_metadata["video_path"] = recorded_path
    except Exception as err:
        print(f"[conftest] Warning in test video teardown: {err}")


@pytest.fixture(scope="session")
def search_data():
    """Load test input data from data/search_data.json."""
    data_file = Path(__file__).parent / "data" / "search_data.json"
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


def pytest_sessionstart(session):
    """
    Clear old test artifacts and videos before starting a new test session.
    Only clears artifacts within the active ticket's reports directory.
    Safe for pytest-xdist: ONLY executes cleanup on the controller (master) process,
    never inside xdist worker processes.
    """
    if hasattr(session.config, "workerinput"):
        # Worker process: never clean or delete directories!
        return

    reports_dir = getattr(session.config, "_ticket_reports_dir", DEFAULT_REPORTS_DIR)
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "screenshots").mkdir(parents=True, exist_ok=True)

    test_results_dir = reports_dir / "test-results"
    if test_results_dir.exists():
        shutil.rmtree(test_results_dir, ignore_errors=True)


@pytest.hookimpl(trylast=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Automatically generate the self-contained Enterprise HTML report in the ticket folder."""
    if hasattr(config, "workerinput"):
        return

    reports_dir = getattr(config, "_ticket_reports_dir", DEFAULT_REPORTS_DIR)
    test_results_dir = reports_dir / "test-results"
    if test_results_dir.exists():
        videos = list(test_results_dir.glob("**/*.webm"))
        if videos:
            terminalreporter.write_sep("=", "📹 [VIDEO MỚI ĐÃ ĐƯỢC GHI HÌNH THÀNH CÔNG (FULL HD 1080p)]", bold=True, green=True)
            for v in sorted(videos):
                try:
                    rel_v = v.relative_to(WORKSPACE_DIR)
                except Exception:
                    rel_v = v
                terminalreporter.write_line(f"   -> {rel_v}")

    json_file_path = getattr(config.option, "json_report_file", None)
    report_json = Path(json_file_path) if json_file_path else (reports_dir / "report.json")

    # Explicitly ensure JSON report is flushed to disk
    json_plugin = getattr(config, "_json_report", None)
    if json_plugin and hasattr(json_plugin, "save_report"):
        try:
            json_plugin.save_report(str(report_json))
        except Exception:
            pass

    if report_json.exists():
        try:
            from reporting import ReportGenerator
            generator = ReportGenerator(workspace_dir=WORKSPACE_DIR, reports_dir=reports_dir)
            out_html = generator.generate(json_path=report_json)
            terminalreporter.write_sep("=", "✅ [BÁO CÁO ENTERPRISE HTML ĐÃ ĐƯỢC TẠO THÀNH CÔNG]", bold=True, green=True)
            terminalreporter.write_line(f"   File báo cáo (Run ID): {out_html}")
            terminalreporter.write_line(f"   File mới nhất        : {reports_dir / 'execution_report.html'}")
        except Exception as err:
            terminalreporter.write_line(f"[Auto-Report] Lỗi khi tạo báo cáo: {err}", red=True)


@pytest.fixture(scope="session", autouse=True)
def delete_output_dir():
    """Prevent pytest-xdist worker sessions from wiping each other's output directory."""
    pass


@pytest.fixture(scope="session", autouse=True)
def ensure_reports_dir(request):
    """Ensure reports directory and screenshots directory exist for test evidence and artifacts."""
    reports_dir = getattr(request.config, "_ticket_reports_dir", DEFAULT_REPORTS_DIR)
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "screenshots").mkdir(parents=True, exist_ok=True)
