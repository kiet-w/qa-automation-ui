"""
tests/base_test.py - Base Test Class for pytest test suites.

Provides shared fixtures, automatic page object initialization,
step tracking helpers, and evidence collection for child test classes.
"""
import re
from pathlib import Path
from typing import Any, Dict, Optional
import pytest
from playwright.sync_api import Page

from pages.bing_home_page import BingHomePage
from pages.bing_results_page import BingResultsPage
from pages.youtube_page import YouTubePage


class BaseTest:
    """
    Base test class providing common fixtures and page objects via inheritance.

    Subclasses automatically have access to:
    - self.page: Playwright Page instance
    - self.step: StepTracker fixture for reporting & timeline
    - self.search_data: Loaded JSON test data
    - self.bing_home: BingHomePage instance
    - self.bing_results: BingResultsPage instance
    - self.youtube: YouTubePage instance
    - self.request: Pytest FixtureRequest for metadata & node inspection
    """

    page: Page
    step: Any
    search_data: Dict[str, Any]
    bing_home: BingHomePage
    bing_results: BingResultsPage
    youtube: YouTubePage
    request: Any

    @pytest.fixture(autouse=True)
    def _setup_base(self, page: Page, search_data, step, request):
        """Automatically setup page, fixtures, and common page objects for each test method."""
        self.page = page
        self.step = step
        self.search_data = search_data
        self.request = request

        # Initialize common Page Objects
        self.bing_home = BingHomePage(page)
        self.bing_results = BingResultsPage(page)
        self.youtube = YouTubePage(page)

    def assert_contains(self, actual: str, expected_fragment: str, message: str = ""):
        """Helper assertion method to verify substring presence with descriptive error."""
        error_msg = message or f"Expected '{expected_fragment}' to be in '{actual}'"
        assert expected_fragment.lower() in actual.lower(), error_msg

    def get_test_slug(self) -> str:
        """
        Returns a sanitized, filesystem-safe slug of the current test name or scenario id.
        Example: 'test_user_story_1_parallel_scenario[chromium-US01-TC01]' -> 'chromium_us01_tc01'
        """
        if hasattr(self, "request") and hasattr(self.request, "node"):
            callspec = getattr(self.request.node, "callspec", None)
            if callspec and getattr(callspec, "id", None):
                raw_name = str(callspec.id)
            else:
                raw_name = self.request.node.name
        else:
            raw_name = getattr(self, "__name__", "test")

        slug = re.sub(r"[^\w]+", "_", raw_name.lower()).strip("_")
        return slug or "test"

    def is_parallel(self) -> bool:
        """Check if test execution is running under pytest-xdist worker process."""
        if hasattr(self, "request") and hasattr(self.request, "config"):
            config = self.request.config
            if hasattr(config, "workerinput"):
                return True
            numproc = getattr(config.option, "numprocesses", None)
            if numproc is not None:
                if isinstance(numproc, int) and numproc > 1:
                    return True
                if isinstance(numproc, str) and (
                    (numproc.isdigit() and int(numproc) > 1)
                    or numproc.lower() in ("auto", "logical")
                ):
                    return True
        return False

    @property
    def reports_dir(self) -> Path:
        """Returns the isolated reports directory for the current test ticket."""
        if hasattr(self, "step") and hasattr(self.step, "reports_dir"):
            return Path(self.step.reports_dir)
        return Path(__file__).resolve().parent.parent / "reports"

    def get_report_path(self, filename: str, test_scoped: bool = False) -> str:
        """
        Returns the full path inside the ticket's isolated reports directory.
        If test_scoped=True or running in parallel, automatically appends the test slug
        suffix to avoid filename collisions between concurrent test runs.
        Example: execution_step5.png -> execution_step5_chromium_us01_tc01.png
        """
        target_name = filename
        if test_scoped or self.is_parallel():
            p = Path(filename)
            stem = p.stem
            ext = p.suffix
            slug = self.get_test_slug()
            clean_stem = re.sub(r"[^\w]+", "_", stem.lower()).strip("_")
            clean_slug = re.sub(r"[^\w]+", "_", slug.lower()).strip("_")
            if clean_slug and clean_slug not in clean_stem:
                slug_parts = [part for part in clean_slug.split("_") if len(part) >= 4]
                if not any(part in clean_stem for part in slug_parts):
                    target_name = f"{stem}_{clean_slug}{ext}"

        target = self.reports_dir / target_name
        target.parent.mkdir(parents=True, exist_ok=True)
        return str(target)

