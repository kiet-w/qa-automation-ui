"""
tests/fs03/fs03-academic-years/conftest.py - Fixtures for fs03/fs03-academic-years.
Invariant 2 compliant: All test data loaded via fixtures from data/fs03/academic_years_data.json.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page
from pages.fs03.academic_years_page import AcademicYearsPage

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "fs03/academic_years_data.json"


@pytest.fixture(scope="session")
def raw_academic_years_data() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def academic_years_data(raw_academic_years_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_academic_years_data)


@pytest.fixture
def academic_page(page: Page) -> AcademicYearsPage:
    return AcademicYearsPage(page)
