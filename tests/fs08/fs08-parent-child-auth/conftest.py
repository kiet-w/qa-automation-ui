"""
tests/fs08/fs08-parent-child-auth/conftest.py - Fixtures for fs08/fs08-parent-child-auth.
Invariant 2 compliant: All test data loaded via fixtures from data/fs08/citizen_dashboard_data.json.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page
from pages.fs08.home_portal_page import HomePortalPage

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "fs08/citizen_dashboard_data.json"


@pytest.fixture(scope="session")
def raw_citizen_dashboard_data() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def citizen_dashboard_data(raw_citizen_dashboard_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_citizen_dashboard_data)


@pytest.fixture
def home_portal_page(page: Page) -> HomePortalPage:
    return HomePortalPage(page)
