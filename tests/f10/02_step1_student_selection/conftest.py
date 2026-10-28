"""
tests/f10/02_step1_student_selection/conftest.py - Fixtures for f10/02_step1_student_selection.
Invariant 2 compliant: All test data loaded via fixtures from data/f10/fas02_student_data.json.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page
from pages.f10.fas_application_page import FasApplicationPage

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "f10/fas02_student_data.json"


@pytest.fixture(scope="session")
def raw_fas02_data() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def fas02_data(raw_fas02_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_fas02_data)


@pytest.fixture
def fas_page(page: Page) -> FasApplicationPage:
    return FasApplicationPage(page)
