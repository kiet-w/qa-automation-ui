"""
tests/testcase5173/03_school_management/conftest.py - Master fixtures for 03_school_management.
Uses authenticated moehq_auth_state from tests/testcase5173/conftest.py.
Complies with Invariant 1 (zero assertions in POM), Invariant 2 (deepcopy fixtures), and clean modular layout.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page

from pages.fs03.school_directory_page import SchoolDirectoryPage
from pages.fs03.school_create_page import SchoolCreatePage
from pages.fs03.school_detail_page import SchoolDetailPage

WORKSPACE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = WORKSPACE_DIR / "data" / "fs03" / "school_directory_data.json"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, moehq_auth_state: Path) -> dict:
    """Pre-authenticate all tests in session as MOEHQ admin."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
        "storage_state": str(moehq_auth_state),
    }


@pytest.fixture(scope="session")
def raw_school_directory_data() -> Dict[str, Any]:
    """Load school directory test data from JSON once per session."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def school_directory_data(raw_school_directory_data: Dict[str, Any]) -> Dict[str, Any]:
    """Provide fresh deepcopy of school directory test data per test."""
    return copy.deepcopy(raw_school_directory_data)


@pytest.fixture
def school_directory_page(page: Page) -> SchoolDirectoryPage:
    """Instantiate SchoolDirectoryPage for current page."""
    return SchoolDirectoryPage(page)


@pytest.fixture
def school_create_page(page: Page) -> SchoolCreatePage:
    """Instantiate SchoolCreatePage for current page."""
    return SchoolCreatePage(page)


@pytest.fixture
def school_detail_page(page: Page) -> SchoolDetailPage:
    """Instantiate SchoolDetailPage for current page."""
    return SchoolDetailPage(page)
