"""
tests/f10/f10-fas-submission/test_integration_fas_submission.py - End-to-End FAS Submission Flows.
Traceability: UAT-028, BR-10-SUB-01, BR-10-SUB-04, BR-10-SUB-05, Error Resilience, UI Health.
Compliant with Invariant 1, 2, 3, 4, 8, 9 (< 240 lines).
"""
import json
import pytest
from pages.f10.fas_application_page import FasApplicationPage


@pytest.mark.integration
def test_tc_uat028_br01_single_child_submission_success(fas_page: FasApplicationPage, fas_data: dict):
    """BR-01 / AC-01: Direct online submission with single primary child returns SUBMITTED Confirmation Card."""
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

    assert fas_page.is_confirmation_visible(timeout=8000), "Expected Confirmation Card to be visible after submit"
    assert fas_page.get_confirmation_code() == "APP-2026-00045"
    assert fas_page.get_confirmation_status() == "SUBMITTED"
    fas_page.page.unroute_all()


@pytest.mark.integration
def test_tc_uat028_br02_multi_child_and_family_submission(fas_page: FasApplicationPage, fas_data: dict):
    """BR-02 / AC-02: Submission with multiple beneficiaries and family member succeeds."""
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
    assert fas_page.beneficiary.get_beneficiary_count() == 2
    fas_page.beneficiary.fill_beneficiary(1, fas_data["second_beneficiary"])
    fas_page.beneficiary.add_family_member()
    assert fas_page.beneficiary.get_family_count() == 1
    fas_page.beneficiary.fill_family_member(0, fas_data["family_member"])
    fas_page.submit()

    assert fas_page.is_confirmation_visible(timeout=8000)
    assert fas_page.get_confirmation_status() == "SUBMITTED"
    fas_page.page.unroute_all()


@pytest.mark.integration
def test_tc_uat028_br03_secondary_school_level_submission(fas_page: FasApplicationPage, fas_data: dict):
    """BR-03 / AC-01: Submission with secondary school student succeeds."""
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
    assert fas_page.get_confirmation_code() == "APP-2026-00048"
    assert fas_page.get_confirmation_status() == "SUBMITTED"
    fas_page.page.unroute_all()


@pytest.mark.integration
def test_tc_uat028_br04_pre_university_level_submission(fas_page: FasApplicationPage, fas_data: dict):
    """BR-04 / AC-01: Submission with Pre-University student succeeds."""
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
    pre_u_child = dict(fas_data["valid_beneficiary"])
    pre_u_child["classLevel"] = "PRE_UNIVERSITY"
    pre_u_child["grade"] = "JC 1"
    fas_page.beneficiary.fill_beneficiary(0, pre_u_child)
    fas_page.submit()

    assert fas_page.is_confirmation_visible(timeout=8000)
    assert fas_page.get_confirmation_code() == "APP-2026-00049"
    assert fas_page.get_confirmation_status() == "SUBMITTED"
    fas_page.page.unroute_all()


@pytest.mark.integration
def test_tc_uat028_flo01_dynamic_card_lifecycle(fas_page: FasApplicationPage, fas_data: dict):
    """FLO-01 (BR-10-SUB-04): Verify dynamic addition and removal of beneficiary and family cards."""
    fas_page.open()
    assert fas_page.beneficiary.get_beneficiary_count() == 1
    assert fas_page.beneficiary.get_family_count() == 0

    fas_page.beneficiary.add_beneficiary()
    assert fas_page.beneficiary.get_beneficiary_count() == 2
    fas_page.beneficiary.remove_beneficiary(1)
    assert fas_page.beneficiary.get_beneficiary_count() == 1

    fas_page.beneficiary.add_family_member()
    assert fas_page.beneficiary.get_family_count() == 1
    card = fas_page.page.locator("section[aria-labelledby='family-members-heading'] article").first
    card.locator("button:has-text('Remove')").click()
    assert fas_page.beneficiary.get_family_count() == 0


@pytest.mark.integration
def test_tc_uat028_flo02_start_new_application_resets_form(fas_page: FasApplicationPage, fas_data: dict):
    """FLO-02 (BR-10-SUB-05): Verify clicking 'Start a new application' resets all fields to empty."""
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
    fas_page.submit()

    assert fas_page.is_confirmation_visible()
    fas_page.click_start_new_application()

    assert not fas_page.is_confirmation_visible(timeout=1000)
    assert fas_page.page.input_value("#applicant-fullName") == ""
    assert fas_page.page.input_value("#applicant-nric") == ""
    assert not fas_page.page.is_checked("#applicant-commitmentAgreed")
    fas_page.page.unroute_all()


@pytest.mark.integration
def test_tc_uat028_err01_server_error_resilience(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-01: HTTP 500 error triggers red Alert banner, preserves entered data, and allows retry."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=500,
            content_type="application/json",
            body=json.dumps({"isSuccess": False, "message": "Internal Server Error"})
        )
    )
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.submit()

    assert fas_page.is_server_error_visible(), "Expected server error alert banner to be visible"
    err_text = fas_page.get_server_error()
    assert "Unable to submit application" in err_text or "Please try again" in err_text
    assert fas_page.page.input_value("#applicant-fullName") == fas_data["valid_applicant"]["fullName"]
    fas_page.page.unroute_all()


@pytest.mark.integration
def test_tc_uat028_err02_ui_health_zero_console_errors_and_zero_i18n_leaks(fas_page: FasApplicationPage):
    """ERR-02 (UI Health): Zero uncaught console errors and zero unrendered translation keys."""
    console_errors = []
    fas_page.page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    fas_page.open()

    body_text = fas_page.page.inner_text("body")
    assert "features.fasApplication." not in body_text, "Found unrendered i18n translation key in page body!"
    assert "validation.required" not in body_text, "Found unrendered validation key in page body!"
    critical_errors = [e for e in console_errors if "favicon" not in e.lower()]
    assert len(critical_errors) == 0, f"Detected console errors on page: {critical_errors}"
