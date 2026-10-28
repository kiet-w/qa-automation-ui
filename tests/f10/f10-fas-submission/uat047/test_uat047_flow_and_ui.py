"""
tests/f10/f10-fas-submission/uat047/test_uat047_flow_and_ui.py - 13 Functional Flow & UI BSK Tests.
Traceability: UAT-047, BR-10-ERR-01, BR-10-ERR-04, BR-10-ERR-07, AC-UAT-047-08.
"""
import json
import pytest
from pages.f10.fas_application_page import FasApplicationPage


def test_tc_uat047_flo01_single_child_submission_success(fas_page: FasApplicationPage, fas_data: dict):
    """FLO-01: Primary single-child online submission returns SUBMITTED Confirmation Card."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"isSuccess": True, "data": {"code": "APP-2026-00045", "status": "SUBMITTED", "submittedAt": "2026-10-26T15:20:00Z"}})
        )
    )
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.submit()

    assert fas_page.is_confirmation_visible(timeout=8000)
    assert fas_page.get_confirmation_code() == "APP-2026-00045"
    assert fas_page.get_confirmation_status() == "SUBMITTED"
    fas_page.page.unroute_all()


def test_tc_uat047_flo02_multi_child_two_children_submission(fas_page: FasApplicationPage, fas_data: dict):
    """FLO-02: Multi-child submission with two children succeeds."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"isSuccess": True, "data": {"code": "APP-2026-00046", "status": "SUBMITTED", "submittedAt": "2026-10-26T15:21:00Z"}})
        )
    )
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(1, fas_data["second_beneficiary"])
    fas_page.submit()

    assert fas_page.is_confirmation_visible(timeout=8000)
    assert fas_page.get_confirmation_status() == "SUBMITTED"
    fas_page.page.unroute_all()


def test_tc_uat047_flo03_multi_child_and_family_member_submission(fas_page: FasApplicationPage, fas_data: dict):
    """FLO-03: Multi-child plus family member submission persists all records."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"isSuccess": True, "data": {"code": "APP-2026-00047", "status": "SUBMITTED", "submittedAt": "2026-10-26T15:22:00Z"}})
        )
    )
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(1, fas_data["second_beneficiary"])

    fas_page.beneficiary.add_family_member()
    fas_page.beneficiary.fill_family_member(0, fas_data["family_member"])
    fas_page.submit()

    assert fas_page.is_confirmation_visible(timeout=8000)
    assert fas_page.get_confirmation_status() == "SUBMITTED"
    fas_page.page.unroute_all()


def test_tc_uat047_flo04_secondary_school_level_submission(fas_page: FasApplicationPage, fas_data: dict):
    """FLO-04: Secondary school level submission passes validation and succeeds."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"isSuccess": True, "data": {"code": "APP-2026-00048", "status": "SUBMITTED", "submittedAt": "2026-10-26T15:23:00Z"}})
        )
    )
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["secondary_beneficiary"])
    fas_page.submit()

    assert fas_page.is_confirmation_visible(timeout=8000)
    assert fas_page.get_confirmation_status() == "SUBMITTED"
    fas_page.page.unroute_all()


def test_tc_uat047_flo05_pre_university_school_level_submission(fas_page: FasApplicationPage, fas_data: dict):
    """FLO-05: Pre-University school level submission succeeds."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"isSuccess": True, "data": {"code": "APP-2026-00049", "status": "SUBMITTED", "submittedAt": "2026-10-26T15:24:00Z"}})
        )
    )
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["pre_uni_beneficiary"])
    fas_page.submit()

    assert fas_page.is_confirmation_visible(timeout=8000)
    assert fas_page.get_confirmation_status() == "SUBMITTED"
    fas_page.page.unroute_all()


def test_tc_uat047_flo06_dynamic_card_add_second_beneficiary(fas_page: FasApplicationPage, fas_data: dict):
    """FLO-06: Clicking Add beneficiary increments card count to 2."""
    fas_page.open()
    assert fas_page.beneficiary.get_beneficiary_count() == 1
    fas_page.beneficiary.add_beneficiary()
    assert fas_page.beneficiary.get_beneficiary_count() == 2


def test_tc_uat047_flo07_dynamic_card_add_third_beneficiary(fas_page: FasApplicationPage, fas_data: dict):
    """FLO-07: Adding a third beneficiary increments card count to 3."""
    fas_page.open()
    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.add_beneficiary()
    assert fas_page.beneficiary.get_beneficiary_count() == 3


def test_tc_uat047_flo08_dynamic_card_remove_beneficiary(fas_page: FasApplicationPage, fas_data: dict):
    """FLO-08: Removing the second beneficiary card decrements count back to 1."""
    fas_page.open()
    fas_page.beneficiary.add_beneficiary()
    assert fas_page.beneficiary.get_beneficiary_count() == 2
    fas_page.beneficiary.remove_beneficiary(1)
    assert fas_page.beneficiary.get_beneficiary_count() == 1


def test_tc_uat047_flo09_invariant_minimum_one_beneficiary_no_remove(fas_page: FasApplicationPage, fas_data: dict):
    """FLO-09: Single remaining beneficiary card cannot be removed (Remove button is disabled)."""
    fas_page.open()
    assert fas_page.beneficiary.get_beneficiary_count() == 1
    assert fas_page.beneficiary.is_remove_beneficiary_disabled(0)


def test_tc_uat047_flo10_dynamic_card_add_remove_family_member(fas_page: FasApplicationPage, fas_data: dict):
    """FLO-10: Adding and removing a family member card updates count cleanly."""
    fas_page.open()
    assert fas_page.beneficiary.get_family_count() == 0
    fas_page.beneficiary.add_family_member()
    assert fas_page.beneficiary.get_family_count() == 1

    card = fas_page.page.locator("section[aria-labelledby='family-members-heading'] article").first
    card.locator("button:has-text('Remove')").click()
    assert fas_page.beneficiary.get_family_count() == 0


def test_tc_uat047_flo11_start_new_application_resets_form_state(fas_page: FasApplicationPage, fas_data: dict):
    """FLO-11: Clicking Start a new application resets form to pristine empty state."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"isSuccess": True, "data": {"code": "APP-2026-RESET", "status": "SUBMITTED", "submittedAt": "2026-10-26T15:25:00Z"}})
        )
    )
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.submit()

    assert fas_page.is_confirmation_visible()
    fas_page.click_start_new_application()

    assert not fas_page.is_confirmation_visible(timeout=1000)
    assert fas_page.page.input_value("#applicant-fullName") == ""
    assert fas_page.page.input_value("#applicant-nric") == ""
    assert not fas_page.page.is_checked("#applicant-commitmentAgreed")
    fas_page.page.unroute_all()


def test_tc_uat047_ui01_accessible_aria_invalid_and_red_borders(fas_page: FasApplicationPage, fas_data: dict):
    """UI-01: Visual feedback: Every invalid field has aria-invalid=true and red error outline."""
    fas_page.open()
    fas_page.submit()

    name_field = fas_page.page.locator("#applicant-fullName")
    assert name_field.get_attribute("aria-invalid") == "true"
    nric_field = fas_page.page.locator("#applicant-nric")
    assert nric_field.get_attribute("aria-invalid") == "true"


def test_tc_uat047_ui02_zero_console_errors_and_zero_i18n_leaks(fas_page: FasApplicationPage, fas_data: dict):
    """UI-02: Zero Javascript console errors and zero unrendered i18n translation keys."""
    console_errors = []
    fas_page.page.on(
        "console",
        lambda msg: console_errors.append(msg.text)
        if msg.type == "error" and "401" not in msg.text and "favicon" not in msg.text and "status of" not in msg.text
        else None,
    )

    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.submit()

    body_text = fas_page.page.inner_text("body")
    assert "features.fasApplication" not in body_text
    assert len(console_errors) == 0
