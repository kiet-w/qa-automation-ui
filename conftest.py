"""conftest.py - Shared fixtures, Brave browser setup, and reporting hooks."""
import json
from pathlib import Path
import shutil
import time
from typing import Optional
import pytest
from playwright.sync_api import Page
from playwright_stealth import Stealth

BRAVE_PATH = "/usr/bin/brave"
REPORTS_DIR = Path(__file__).parent / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"


class StepTracker:
    """Tracks and records execution steps, statuses, durations, and screenshots."""

    def __init__(self, page: Page, json_metadata=None):
        self.page = page
        self.json_metadata = json_metadata if json_metadata is not None else {}
        if "steps" not in self.json_metadata:
            self.json_metadata["steps"] = []
        self.steps = self.json_metadata["steps"]
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

    def __call__(
        self,
        title: str,
        page: Optional[Page] = None,
        capture_screenshot: bool = False,
    ):
        """Context manager factory: with step('title', page=..., capture_screenshot=...):"""
        return _StepContext(
            tracker=self,
            title=title,
            page=page,
            capture_screenshot=capture_screenshot,
        )


class _StepContext:
    """Context manager for an individual execution step."""

    def __init__(
        self,
        tracker: StepTracker,
        title: str,
        page: Optional[Page] = None,
        capture_screenshot: bool = False,
    ):
        self.tracker = tracker
        self.title = title
        self.page = page
        self.capture_screenshot = capture_screenshot
        self.step_data = None
        self.start_time = None
        self.step_index = 0

    def set_page(self, page: Page):
        self.tracker.set_page(page)

    def attach_screenshot(self, path: str):
        self.tracker.attach_screenshot(path)

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

        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = int(time.time())
        active_page = self.page or self.tracker.page

        if exc_type is not None:
            self.step_data["status"] = "failed"
            self.step_data["error"] = str(exc_val)

            fail_filename = f"fail_step_{self.step_index}_{timestamp}.png"
            fail_path = SCREENSHOTS_DIR / fail_filename
            rel_fail_path = f"reports/screenshots/{fail_filename}"
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
            step_filename = f"step_{self.step_index}_{timestamp}.png"
            step_path = SCREENSHOTS_DIR / step_filename
            rel_step_path = f"reports/screenshots/{step_filename}"
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
def step(page: Page, json_metadata):
    """Fixture providing a StepTracker instance to record and manage test steps."""
    return StepTracker(page=page, json_metadata=json_metadata)


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    Configure pytest-playwright to use the system Brave browser (/usr/bin/brave)
    with anti-bot automation flags disabled.
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
def setup_page(page):
    """
    Apply comprehensive stealth patches and auto-dismiss consent overlays.
    - Uses playwright-stealth to patch CDP/navigator leaks, WebGL, plugins.
    - Auto-clicks cookie consent buttons when they appear.
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


@pytest.fixture(scope="session")
def search_data():
    """Load test input data from data/search_data.json."""
    data_file = Path(__file__).parent / "data" / "search_data.json"
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


def pytest_sessionstart(session):
    """
    Clear old test artifacts and videos before starting a new test session.
    Safe for pytest-xdist: only executes on the controller (master) process,
    preventing workers from deleting each other's recordings mid-session.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    if not hasattr(session.config, "workerinput"):
        test_results_dir = REPORTS_DIR / "test-results"
        if test_results_dir.exists():
            shutil.rmtree(test_results_dir, ignore_errors=True)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Log freshly generated Full HD video files and automatically generate HTML report."""
    if not hasattr(session.config, "workerinput"):
        test_results_dir = REPORTS_DIR / "test-results"
        if test_results_dir.exists():
            videos = list(test_results_dir.glob("**/*.webm"))
            if videos:
                print("\n" + "=" * 65)
                print("📹 [VIDEO MỚI ĐÃ ĐƯỢC GHI HÌNH THÀNH CÔNG (FULL HD 1080p)]:")
                for v in sorted(videos):
                    print(f"   -> {v.relative_to(Path(__file__).parent)}")
                print("=" * 65 + "\n")

        # Automatically generate HTML report right after pytest finishes
        report_script = Path(__file__).parent / "generate_report.py"
        report_json = REPORTS_DIR / "report.json"
        if report_script.exists():
            try:
                import subprocess
                import sys
                print("[Auto-Report] Pytest đã kết thúc. Đang tự động cập nhật báo cáo HTML...")
                subprocess.run(
                    [sys.executable, str(report_script), str(report_json)],
                    cwd=str(Path(__file__).parent),
                    check=False,
                )
            except Exception as err:
                print(f"[Auto-Report] Lỗi khi tạo báo cáo: {err}")


@pytest.fixture(scope="session", autouse=True)
def delete_output_dir():
    """Prevent pytest-xdist worker sessions from wiping each other's output directory."""
    pass


@pytest.fixture(scope="session", autouse=True)
def ensure_reports_dir():
    """Ensure reports directory and screenshots directory exist for test evidence and artifacts."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
