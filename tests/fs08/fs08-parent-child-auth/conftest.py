"""
tests/fs08/fs08-parent-child-auth/conftest.py
Fixtures and configuration for FS08 SingPass Child Authorization (US-005).
Complies with Invariant 2 (Zero hardcoded test data) and AGENTS.md guidelines.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page

from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.home_portal_page import HomePortalPage
from pages.fs08.transactions_page import TransactionsPage

WORKSPACE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = WORKSPACE_DIR / "data" / "fs08" / "fs08_data.json"


@pytest.fixture(scope="session")
def raw_fs08_data() -> Dict[str, Any]:
    """Load JSON data from data/fs08/fs08_data.json once per test session."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def fs08_data(raw_fs08_data: Dict[str, Any]) -> Dict[str, Any]:
    """Provide a fresh deepcopy of fs08_data for each test to ensure test isolation."""
    return copy.deepcopy(raw_fs08_data)


@pytest.fixture
def login_page(page: Page) -> SingpassLoginPage:
    """Fixture providing SingpassLoginPage instance."""
    return SingpassLoginPage(page)


@pytest.fixture
def home_portal(page: Page) -> HomePortalPage:
    """Fixture providing HomePortalPage instance."""
    return HomePortalPage(page)


@pytest.fixture
def transactions_page(page: Page) -> TransactionsPage:
    """Fixture providing TransactionsPage instance."""
    return TransactionsPage(page)
