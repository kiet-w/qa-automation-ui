"""
tests/f01/f01-education-accounts/conftest.py - Fixtures for F01 Education Accounts.
Complies with Invariant 2 (Zero hardcoded test data) and Invariant 9 (< 100 lines).
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Browser, Page

from pages.f01.education_accounts_page import EducationAccountsPage
from pages.fs03.admin_login_page import AdminLoginPage

WORKSPACE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = WORKSPACE_DIR / "data" / "f01" / "f01_data.json"
AUTH_STATE_PATH = WORKSPACE_DIR / "data" / "fs03" / "auth_state.json"


@pytest.fixture(scope="session")
def raw_f01_data() -> Dict[str, Any]:
    """Load JSON data from data/f01/f01_data.json once per test session."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def f01_data(raw_f01_data: Dict[str, Any]) -> Dict[str, Any]:
    """Provide a fresh deepcopy of f01_data for each test to ensure test isolation."""
    return copy.deepcopy(raw_f01_data)


@pytest.fixture(scope="session")
def ensure_admin_session(browser: Browser, raw_f01_data: Dict[str, Any]) -> Path:
    """
    Ensure a valid authenticated session for MOE HQ Admin exists in auth_state.json.
    If absent or expired, performs fresh SSO login via Microsoft Entra Simulator and saves state.
    """
    AUTH_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    base_url = raw_f01_data.get("base_url", "http://localhost:5173")

    if AUTH_STATE_PATH.exists():
        try:
            test_context = browser.new_context(
                storage_state=str(AUTH_STATE_PATH),
                viewport={"width": 1280, "height": 800}
            )
            test_page = test_context.new_page()
            test_page.goto(f"{base_url}/education-accounts", timeout=10000, wait_until="domcontentloaded")
            is_valid = "/education-accounts" in test_page.url and "login" not in test_page.url
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
def ea_page(page: Page) -> EducationAccountsPage:
    """Fixture returning an initialized EducationAccountsPage instance."""
    return EducationAccountsPage(page)
