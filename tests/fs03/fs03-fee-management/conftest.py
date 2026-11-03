"""
tests/fs03/fs03-fee-management/conftest.py - Fixtures cho Test Suite Fee Management & Rate Rules.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict
import pytest
from playwright.sync_api import Browser, Page, expect

from pages.fs03.fee_management_page import FeeManagementPage

WORKSPACE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = WORKSPACE_DIR / "data" / "fs03" / "fee_management_data.json"


@pytest.fixture(scope="session")
def raw_fee_data() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def fee_data(raw_fee_data: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(raw_fee_data)


@pytest.fixture(scope="session")
def authenticated_state(browser: Browser, raw_fee_data: Dict[str, Any], tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Đăng nhập 1 lần duy nhất qua Microsoft Simulator và lưu session storage_state."""
    base_url = raw_fee_data["base_url"]
    email = raw_fee_data["auth"]["persona_email"]

    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    try:
        page.goto(f"{base_url}/login", wait_until="networkidle")
        page.locator('button:has-text("Sign in with Microsoft")').click()
        page.wait_for_url("**/microsoft-provider/**", timeout=20000)
        page.locator(f"text={email}").first.click()
        page.wait_for_url(f"{base_url}/", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_load_state("networkidle")
        page.locator("text=System Admin").first.wait_for(state="visible", timeout=15000)

        state_path = tmp_path_factory.mktemp("auth") / "moehq_state.json"
        context.storage_state(path=str(state_path))
        return state_path
    finally:
        context.close()


@pytest.fixture
def auth_page(browser: Browser, authenticated_state: Path) -> Page:
    """Tạo browser context độc lập nạp storage_state đã xác thực cho từng test."""
    context = browser.new_context(storage_state=str(authenticated_state), ignore_https_errors=True)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def fee_page(auth_page: Page) -> FeeManagementPage:
    return FeeManagementPage(auth_page)
