"""
tests/fs03/fs03-class-management/conftest.py - Fixtures for fs03/fs03-class-management.
Invariant 2 compliant: All test data loaded via fixtures from data/fs03/class_management_data.json.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page
from pages.fs03.class_management_page import ClassManagementPage

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "fs03/class_management_data.json"


@pytest.fixture(scope="session")
def raw_class_mgmt_data() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def class_mgmt_data(raw_class_mgmt_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_class_mgmt_data)


@pytest.fixture
def class_page(page: Page) -> ClassManagementPage:
    return ClassManagementPage(page)
