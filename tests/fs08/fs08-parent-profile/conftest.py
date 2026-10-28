"""
tests/fs08/fs08-parent-profile/conftest.py - Fixtures for fs08/fs08-parent-profile.
Invariant 2 compliant: All test data loaded via fixtures from data/fs08/parent_profile_data.json.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Page
from pages.fs08.parent_profile_page import ParentProfilePage

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "fs08/parent_profile_data.json"


@pytest.fixture(scope="session")
def raw_parent_profile_data() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def parent_profile_data(raw_parent_profile_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_parent_profile_data)


@pytest.fixture
def parent_profile_page(page: Page) -> ParentProfilePage:
    return ParentProfilePage(page)
