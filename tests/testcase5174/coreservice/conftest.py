"""Shared UI fixtures for the live, black-box testcase5174 core-service suite."""
import copy
import json
from pathlib import Path
from typing import Any, Dict

import pytest
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from pages.fs08.singpass_login_page import SingpassLoginPage


ROOT = Path(__file__).resolve().parents[3]
FS08_DATA = ROOT / "data" / "fs08" / "fs08_data.json"
FS09_DATA = ROOT / "data" / "fs09" / "fs09_data.json"


def dismiss_welcome_dialog(page: Page) -> None:
    """Dismiss the first-login welcome dialog when it is shown over a portal route."""
    explore = page.get_by_role("button", name="Let me explore", exact=True)
    try:
        explore.wait_for(state="visible", timeout=1500)
        explore.click()
    except PlaywrightTimeoutError:
        pass


def _read_json(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


@pytest.fixture(scope="session")
def raw_fs08_data() -> Dict[str, Any]:
    return _read_json(FS08_DATA)


@pytest.fixture
def fs08_data(raw_fs08_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_fs08_data)


@pytest.fixture(scope="session")
def raw_fs09_data() -> Dict[str, Any]:
    return _read_json(FS09_DATA)


@pytest.fixture
def fs09_data(raw_fs09_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_fs09_data)


@pytest.fixture
def authenticated_parent(page: Page, fs08_data: Dict[str, Any]) -> Page:
    """Sign in through the local Singpass simulator using the configured test persona."""
    base_url = fs08_data["base_url"]
    persona = fs08_data["personas"]["PAR-NORMAL-01"]
    login = SingpassLoginPage(page)
    login.login_with_persona(persona["nric"], base_url=base_url)
    dismiss_welcome_dialog(page)
    return page
