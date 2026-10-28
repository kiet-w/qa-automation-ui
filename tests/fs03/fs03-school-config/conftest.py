"""
tests/fs03/fs03-school-config/conftest.py - Fixtures for fs03/fs03-school-config.
Invariant 2 compliant: All test data loaded via fixtures from data/fs03/school_config_data.json.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page
from pages.fs03.school_config_page import SchoolConfigPage

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "fs03/school_config_data.json"


@pytest.fixture(scope="session")
def raw_school_config_data() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def school_config_data(raw_school_config_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_school_config_data)


@pytest.fixture
def config_page(page: Page) -> SchoolConfigPage:
    return SchoolConfigPage(page)
