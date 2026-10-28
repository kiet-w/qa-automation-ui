"""
tests/fs03/fs03-student-enrollment/conftest.py - Fixtures for fs03/fs03-student-enrollment.
Invariant 2 compliant: All test data loaded via fixtures from data/fs03/student_enrollment_data.json.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page
from pages.fs03.student_enrollment_page import StudentEnrollmentPage

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "fs03/student_enrollment_data.json"


@pytest.fixture(scope="session")
def raw_student_data() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def student_data(raw_student_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_student_data)


@pytest.fixture
def student_page(page: Page) -> StudentEnrollmentPage:
    return StudentEnrollmentPage(page)
