"""
tests/f10/04_step3_documents_and_declaration/conftest.py - Fixtures for f10/04_step3_documents_and_declaration.
Invariant 2 compliant: All test data loaded via fixtures from data/f10/fas04_documents_data.json.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page
from pages.f10.fas_application_page import FasApplicationPage

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "f10/fas04_documents_data.json"


@pytest.fixture(scope="session")
def raw_fas04_data() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def fas04_data(raw_fas04_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_fas04_data)


@pytest.fixture
def fas_page(page: Page) -> FasApplicationPage:
    return FasApplicationPage(page)
