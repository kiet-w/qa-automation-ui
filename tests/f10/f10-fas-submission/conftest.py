"""
tests/f10/f10-fas-submission/conftest.py - Fixtures for FAS Submission test suite.
Complies with Invariant 2 (Zero hardcoded data) and Invariant 9 (< 100 lines).
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page

from pages.f10.fas_application_page import FasApplicationPage

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "f10" / "f10_fas_submission_data.json"


@pytest.fixture(scope="session")
def raw_fas_data() -> Dict[str, Any]:
    """Load JSON test data once per session."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def fas_data(raw_fas_data: Dict[str, Any]) -> Dict[str, Any]:
    """Return an isolated deepcopy of test data for each test case."""
    return copy.deepcopy(raw_fas_data)


@pytest.fixture
def fas_page(page: Page) -> FasApplicationPage:
    """Fixture providing an instance of FasApplicationPage."""
    return FasApplicationPage(page)
