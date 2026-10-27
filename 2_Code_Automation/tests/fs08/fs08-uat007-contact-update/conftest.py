"""
tests/fs08/fs08-uat007-contact-update/conftest.py
Fixtures and teardown restore logic for UAT-007 (US-009 Parent Permitted Contact Update).
Compliant with Invariant 1 (Zero assertions in POM) and Invariant 2 (Zero hardcoded data).
"""
import copy
import json
from pathlib import Path
from typing import Any, Callable, Dict, Generator
import pytest
from playwright.sync_api import Page, expect

from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.home_portal_page import HomePortalPage
from pages.fs08.parent_profile_page import ParentProfilePage

WORKSPACE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = WORKSPACE_DIR / "data" / "fs08" / "fs08_data.json"
COVERAGE_PATH = WORKSPACE_DIR / "data" / "fs08" / "uat007_coverage_cases.json"


@pytest.fixture(autouse=True)
def cleanup_uat007_routes(page: Page) -> Generator[None, None, None]:
    """Guarantee route mocks never leak into the next UAT-007 testcase."""
    yield
    page.unroute_all()


@pytest.fixture(scope="session")
def raw_fs08_data() -> Dict[str, Any]:
    """Load JSON data from data/fs08/fs08_data.json once per test session."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def fs08_data(raw_fs08_data: Dict[str, Any]) -> Dict[str, Any]:
    """Provide a fresh deepcopy of fs08_data for each test to ensure test isolation."""
    return copy.deepcopy(raw_fs08_data)


@pytest.fixture(scope="session")
def raw_uat007_cases() -> Dict[str, Dict[str, Any]]:
    """Load the sourced field matrix and reject duplicate testcase IDs."""
    with open(COVERAGE_PATH, "r", encoding="utf-8") as file_handle:
        cases = json.load(file_handle)
    indexed = {case["id"]: case for case in cases}
    if len(indexed) != len(cases):
        raise ValueError("Duplicate testcase ID in uat007_coverage_cases.json")
    return indexed


@pytest.fixture
def uat007_case_runner(
    raw_uat007_cases: Dict[str, Dict[str, Any]],
) -> Callable[[Any, Dict[str, Any], str], None]:
    """Return a data-driven validator with observable field-level oracles."""
    selectors = {
        "phoneNumber": ParentProfilePage.INPUT_PHONE,
        "email": ParentProfilePage.INPUT_EMAIL,
        "mailingBlock": ParentProfilePage.INPUT_BLOCK,
        "mailingStreet": ParentProfilePage.INPUT_STREET,
        "mailingUnit": ParentProfilePage.INPUT_UNIT,
        "mailingPostalCode": ParentProfilePage.INPUT_POSTAL,
        "mailingCountry": ParentProfilePage.INPUT_COUNTRY,
    }

    def run(test: Any, fs08_data: Dict[str, Any], case_id: str) -> None:
        case = copy.deepcopy(raw_uat007_cases[case_id])
        profile = test.get_page(ParentProfilePage)
        login = test.get_page(SingpassLoginPage)
        login.login_with_persona(
            fs08_data["uat_007"]["persona"]["name"],
            base_url=fs08_data["base_url"],
        )
        profile.open(base_url=fs08_data["base_url"])
        profile.click_update_details()
        selector = selectors[case["field"]]

        test.verify_field_case(case, selector=selector, page_object=profile)
        profile.click_cancel()

    return run


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
def restore_profile_uat007(page: Page, fs08_data: Dict[str, Any]) -> Generator[Dict[str, str], None, None]:
    """Restore the values observed before mutation; surface teardown failures."""
    original: Dict[str, str] = {}
    yield original
    if not original:
        return
    profile = ParentProfilePage(page)
    page.unroute_all()
    profile.open(base_url=fs08_data["base_url"])
    profile.click_update_details()
    profile.fill_contact_and_mailing_form(
        phone=original["phoneNumber"], email=original["email"],
        block=original["mailingBlock"], street=original["mailingStreet"],
        unit=original["mailingUnit"], postal_code=original["mailingPostalCode"],
        country=original["mailingCountry"],
    )
    if not profile.is_save_disabled():
        profile.click_save_changes()
        if not profile.is_confirm_dialog_open(timeout=2000):
            raise AssertionError("Restore confirmation did not open")
        profile.confirm_dialog_save()
        if not profile.is_success_toast_visible(timeout=5000):
            raise AssertionError("Profile restore failed; original contact data may not be present")
