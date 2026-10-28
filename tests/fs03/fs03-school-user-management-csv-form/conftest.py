"""
tests/fs03/fs03-school-user-management-csv-form/conftest.py - Fixtures for fs03/fs03-school-user-management-csv-form.
Invariant 2 compliant: All test data loaded via fixtures from data/fs03/fs03_school_user_mgmt.json.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page
from pages.fs03.school_user_management_page import SchoolUserManagementPage

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "fs03/fs03_school_user_mgmt.json"


@pytest.fixture(scope="session")
def raw_school_user_mgmt_data() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def school_user_mgmt_data(raw_school_user_mgmt_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_school_user_mgmt_data)


@pytest.fixture
def user_mgmt_page(page: Page) -> SchoolUserManagementPage:
    return SchoolUserManagementPage(page)
