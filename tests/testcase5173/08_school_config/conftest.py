"""Fixtures for testcase5173 school configuration cases."""
import copy
import json
from pathlib import Path
from typing import Any

import pytest
from playwright.sync_api import Page

from pages.testcase5173.school_config_page import SchoolConfigPage


DATA_PATH = Path(__file__).resolve().parents[3] / "specs" / "testcase5173" / "08_school_config" / "school_config_data.json"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, school_auth_state: Path) -> dict:
    return {**browser_context_args, "storage_state": str(school_auth_state)}


@pytest.fixture(scope="session")
def _raw_school_config_data() -> dict[str, Any]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


@pytest.fixture
def school_config_data(_raw_school_config_data: dict[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(_raw_school_config_data)


@pytest.fixture
def config(page: Page) -> SchoolConfigPage:
    return SchoolConfigPage(page)
