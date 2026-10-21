"""
tests/fs08/conftest.py - Fixtures and configuration for FS-08: Parent Portal test suites.
Complies with Invariant 2 (Zero hardcoded test data) and ADR-0006 Multi-Project Architecture.
"""
import copy
import json
from pathlib import Path
from typing import Any, Dict, Generator
import pytest
from playwright.sync_api import Page

from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.home_portal_page import HomePortalPage
from pages.fs08.parent_profile_page import ParentProfilePage

WORKSPACE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = WORKSPACE_DIR / "data" / "fs08" / "fs08_data.json"


@pytest.fixture(scope="session")
def raw_fs08_data() -> Dict[str, Any]:
    """Load JSON data from data/fs08/fs08_data.json once per test session."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def fs08_data(raw_fs08_data: Dict[str, Any]) -> Dict[str, Any]:
    """Provide a fresh deepcopy of fs08_data for each test to ensure test isolation."""
    return copy.deepcopy(raw_fs08_data)


@pytest.fixture
def login_page(page: Page) -> SingpassLoginPage:
    """Fixture providing SingpassLoginPage instance."""
    return SingpassLoginPage(page)


@pytest.fixture
def home_portal(page: Page) -> HomePortalPage:
    """Fixture providing HomePortalPage instance."""
    return HomePortalPage(page)


@pytest.fixture
def profile_page(page: Page) -> ParentProfilePage:
    """Fixture providing ParentProfilePage instance."""
    return ParentProfilePage(page)


@pytest.fixture
def auth_helper(page: Page, fs08_data: Dict[str, Any]):
    """
    Helper function to authenticate any specified persona through Mockpass
    and navigate safely to the home portal.
    """
    def _login_as(persona_key: str = "PAR-NORMAL-01"):
        persona = fs08_data["personas"][persona_key]
        login = SingpassLoginPage(page)
        login.login_with_persona(persona["name"], base_url=fs08_data["base_url"])
        home = HomePortalPage(page)
        home.wait_for_portal_loaded()
        return home

    return _login_as


@pytest.fixture
def restore_profile_tan_wei_ming(page: Page, fs08_data: Dict[str, Any]) -> Generator[None, None, None]:
    """
    Teardown fixture that restores TAN WEI MING's profile contact info
    back to standard initial state after tests in Stream 3.
    """
    yield
    try:
        # Run restore only if on profile page or logged in
        restore_payload = fs08_data.get("profile_update_restore", {})
        profile = ParentProfilePage(page)
        profile.open(base_url=fs08_data["base_url"])
        if profile.is_view_mode_rendered():
            profile.click_update_details()
            profile.fill_contact_and_mailing_form(
                phone=restore_payload.get("phoneNumber"),
                email=restore_payload.get("email"),
                block=restore_payload.get("mailingBlock"),
                street=restore_payload.get("mailingStreet"),
                unit=restore_payload.get("mailingUnit"),
                postal_code=restore_payload.get("mailingPostalCode"),
                country=restore_payload.get("mailingCountry"),
            )
            if not profile.is_save_disabled():
                profile.click_save_changes()
                if profile.is_confirm_dialog_open(timeout=2000):
                    profile.confirm_dialog_save()
    except Exception:
        # Gracefully pass during teardown to avoid shadowing primary test results
        pass
