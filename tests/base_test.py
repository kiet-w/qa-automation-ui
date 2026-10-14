"""
tests/base_test.py - Base Test Class for pytest test suites.

Provides shared fixtures, automatic page object initialization,
step tracking helpers, and evidence collection for child test classes.
"""
import copy
import json
from pathlib import Path
import re
from typing import Any, Dict, Optional, Type, TypeVar, Union
import pytest
from playwright.sync_api import Page

from pages.bing_home_page import BingHomePage
from pages.bing_results_page import BingResultsPage
from pages.youtube_page import YouTubePage

WORKSPACE_DIR = Path(__file__).resolve().parent.parent
T = TypeVar("T")


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
    - self.curricula: CurriculaTrainerPage instance (lazy loaded)
    - self.get_page(page_cls): Dynamically get or instantiate any Page Object
    - self.request: Pytest FixtureRequest for metadata & node inspection
    """

    page: Page
    step: Any
    search_data: Dict[str, Any]
    bing_home: BingHomePage
    bing_results: BingResultsPage
    youtube: YouTubePage
    request: Any
    _page_cache: Dict[Any, Any]

    @pytest.fixture(autouse=True)
    def _setup_base(self, page: Page, search_data, step, request):
        """Automatically setup page, fixtures, and common page objects for each test method."""
        self.page = page
        self.step = step
        self.search_data = search_data
        self.request = request
        self._page_cache = {}

        # Initialize common Page Objects for backward compatibility
        self.bing_home = BingHomePage(page)
        self.bing_results = BingResultsPage(page)
        self.youtube = YouTubePage(page)

    def get_page(self, page_cls: Type[T]) -> T:
        """Dynamically retrieve or lazily instantiate any Page Object class against self.page."""
        if not hasattr(self, "_page_cache") or self._page_cache is None:
            self._page_cache = {}
        if page_cls not in self._page_cache:
            self._page_cache[page_cls] = page_cls(self.page)
        return self._page_cache[page_cls]

    @property
    def curricula(self):
        """Lazy accessor for CurriculaTrainerPage, preventing AttributeError when AI generates tests."""
        from pages.curricula_trainer_page import CurriculaTrainerPage
        return self.get_page(CurriculaTrainerPage)

    def get_fixture_file(self, rel_path: Union[str, Path]) -> Path:
        """Return absolute Path for a test fixture file in data/fixtures/."""
        p = Path(rel_path)
        if p.is_absolute() and p.exists():
            return p
        return (WORKSPACE_DIR / p).resolve()

    def load_json_data(self, rel_path: str) -> Dict[str, Any]:
        """Load and return JSON test data from workspace root with deepcopy safety."""
        target = (WORKSPACE_DIR / rel_path).resolve()
        if target.exists():
            with open(target, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}


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

    def get_report_path(self, filename: str, test_scoped: bool = True) -> str:
        """
        Returns the full path inside the ticket's isolated reports directory.
        Image files (.png, .jpg, etc.) are automatically routed to the 'screenshots' subfolder.
        Historical run reports (RUN-*.html) are routed to the 'history' subfolder.
        By default (test_scoped=True or running in parallel), automatically appends the test slug
        suffix to guarantee 1:1 file isolation and prevent filename collisions between test runs.
        Example: execution_step5.png -> reports/<ticket>/screenshots/execution_step5_test_user_story_1.png
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
                target_name = f"{stem}_{clean_slug}{ext}"

        target_path = Path(target_name)
        # Automatically route image files into screenshots/ subdirectory
        if target_path.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"):
            if "screenshots" not in target_path.parts:
                target = self.reports_dir / "screenshots" / target_path
            else:
                target = self.reports_dir / target_path
        elif target_path.suffix.lower() in (".html", ".htm") and target_name.startswith("RUN-"):
            if "history" not in target_path.parts:
                target = self.reports_dir / "history" / target_path
            else:
                target = self.reports_dir / target_path
        else:
            target = self.reports_dir / target_path

        target.parent.mkdir(parents=True, exist_ok=True)
        return str(target)

