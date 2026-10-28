"""
tests/fs03/fs03-admin-login/conftest.py - Fixtures for fs03/fs03-admin-login.
Invariant 2 compliant: All test data loaded via fixtures from data/fs03/admin_login_data.json.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page
from pages.fs03.admin_login_page import AdminLoginPage
from pages.fs03.microsoft_simulator_page import MicrosoftSimulatorPage
from pages.fs03.admin_dashboard_shell_page import AdminDashboardShellPage

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "fs03/admin_login_data.json"


@pytest.fixture(scope="session")
def raw_admin_login_data() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def admin_login_data(raw_admin_login_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_admin_login_data)


@pytest.fixture
def admin_login_page(page: Page) -> AdminLoginPage:
    return AdminLoginPage(page)


@pytest.fixture
def simulator_page(page: Page) -> MicrosoftSimulatorPage:
    return MicrosoftSimulatorPage(page)


@pytest.fixture
def shell_page(page: Page) -> AdminDashboardShellPage:
    return AdminDashboardShellPage(page)
