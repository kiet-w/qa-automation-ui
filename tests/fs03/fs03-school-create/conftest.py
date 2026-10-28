"""
tests/fs03/fs03-school-create/conftest.py - Fixtures for FS03 Create School test suites.
Complies with Invariant 2 (Zero hardcoded test data) and ADR-0006 Multi-Project Architecture.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Browser, Page

from pages.fs03.admin_login_page import AdminLoginPage
from pages.fs03.school_create_page import SchoolCreatePage

WORKSPACE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = WORKSPACE_DIR / "data" / "fs03" / "fs03_data.json"
AUTH_STATE_PATH = WORKSPACE_DIR / "data" / "fs03" / "auth_state.json"


@pytest.fixture(scope="session")
def raw_fs03_data() -> Dict[str, Any]:
    """Load JSON data from data/fs03/fs03_data.json once per test session."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def fs03_data(raw_fs03_data: Dict[str, Any]) -> Dict[str, Any]:
    """Provide a fresh deepcopy of fs03_data for each test to ensure test isolation."""
    return copy.deepcopy(raw_fs03_data)


@pytest.fixture(scope="session")
def ensure_admin_session(browser: Browser, raw_fs03_data: Dict[str, Any]) -> Path:
    """
    Ensure a valid authenticated session for MOE HQ Admin exists in auth_state.json.
    Verifies that the stored session cookie is actively accepted by the server.
    If absent or expired, performs fresh SSO login via Microsoft Entra Simulator and saves state.
    """
    AUTH_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    base_url = raw_fs03_data.get("base_url", "http://localhost:5173")

    if AUTH_STATE_PATH.exists():
        try:
            test_context = browser.new_context(
                storage_state=str(AUTH_STATE_PATH),
                viewport={"width": 1280, "height": 800}
            )
            test_page = test_context.new_page()
            test_page.goto(f"{base_url}/school-management/new", timeout=10000, wait_until="domcontentloaded")
            is_valid = "/school-management/new" in test_page.url and "login" not in test_page.url
            test_context.close()

            if is_valid:
                return AUTH_STATE_PATH
        except Exception:
            pass

    # Perform fresh SSO login
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()
    login_page = AdminLoginPage(page)
    login_page.login_with_microsoft_as_admin(base_url=base_url)
    context.close()
    return AUTH_STATE_PATH


@pytest.fixture
def browser_context_args(browser_context_args, ensure_admin_session: Path) -> Dict[str, Any]:
    """Inject storage_state into default pytest-playwright browser context."""
    return {
        **browser_context_args,
        "storage_state": str(ensure_admin_session),
        "viewport": {"width": 1280, "height": 800},
    }


@pytest.fixture
def school_create_page(page: Page, fs03_data: Dict[str, Any]) -> SchoolCreatePage:
    """Fixture providing SchoolCreatePage instance navigated to target URL."""
    create_page = SchoolCreatePage(page)
    create_page.open(base_url=fs03_data["base_url"])
    return create_page
