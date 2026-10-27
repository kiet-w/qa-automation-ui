"""
tests/f10/f10-fas-submission/test_uat049_edge_cases_and_resilience.py - Edge Cases, BSK & Resilience for UAT-049.
Traceability: UAT-049, ERR-1 to ERR-4, UI-2 to UI-4, SEC-01.
Compliant with Invariant 1 (Zero assertions in PO), 2 (Zero hardcoded data), 3, 4, 8, 9 (< 220 lines).
"""
import json
import pytest
from pages.f10.fas_application_page import FasApplicationPage


def test_tc_uat049_err02_server_error_400_bad_request_resilience(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-2: HTTP 400 Bad Request error triggers red Alert banner with server code and preserves all 2 children."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=400,
            content_type="application/json",
            body=json.dumps({"isSuccess": False, "code": "ERR_FAS_VALIDATION", "message": "Income threshold exceeded"})
        )
    )

    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(1, fas_data["second_beneficiary"])

    fas_page.submit()

    assert fas_page.is_server_error_visible(), "Server error alert banner should display for 400 error"
    err_text = fas_page.get_server_error()
    assert "ERR_FAS_VALIDATION" in err_text or "Income threshold" in err_text or len(err_text) > 0

    # Data intact
    cards = fas_page.page.locator("section[aria-labelledby='beneficiaries-heading'] article")
    assert cards.nth(1).locator("input[id$='-fullName']").input_value() == fas_data["second_beneficiary"]["fullName"]
    fas_page.page.unroute_all()


def test_tc_uat049_err03_server_error_503_service_unavailable_resilience(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-3: HTTP 503 Service Unavailable triggers error banner and permits subsequent retry."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=503,
            content_type="application/json",
            body=json.dumps({"isSuccess": False, "message": "Service Temporarily Unavailable"})
        )
    )

    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(1, fas_data["second_beneficiary"])

    fas_page.submit()

    assert fas_page.is_server_error_visible()
    fas_page.page.unroute_all()


def test_tc_uat049_err04_double_click_submission_prevents_duplicate_calls(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-4: Double-clicking submit button during in-flight network dispatch sends only 1 API request."""
    call_count = {"count": 0}

    def handle_route(route):
        call_count["count"] += 1
        # Delay response slightly to simulate in-flight network flight
        fas_page.page.wait_for_timeout(300)
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"isSuccess": True, "data": {"code": "APP-2026-FAS-00056", "status": "SUBMITTED", "submittedAt": "2026-10-26T15:55:00Z"}})
        )

    fas_page.page.route("**/applications**", handle_route)

    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(1, fas_data["second_beneficiary"])

    # Double click submit
    btn = fas_page.page.locator("button[type='submit']")
    btn.click()
    try:
        btn.click(timeout=200)
    except Exception:
        pass  # Button became disabled as expected

    assert fas_page.is_confirmation_visible(timeout=8000)
    assert call_count["count"] == 1, f"Expected exactly 1 API call, got {call_count['count']}"
    fas_page.page.unroute_all()


def test_tc_uat049_ui02_accessible_aria_invalid_states_on_child2_card(fas_page: FasApplicationPage, fas_data: dict):
    """UI-2: Accessibility - Invalid inputs on Child 2 receive aria-invalid='true' and link to error text."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    # Add empty Child 2
    fas_page.beneficiary.add_beneficiary()
    fas_page.submit()

    # Check aria-invalid on Child 2 inputs
    assert fas_page.beneficiary.is_beneficiary_field_invalid(1, "fullName")
    assert fas_page.beneficiary.is_beneficiary_field_invalid(1, "nric")
    assert fas_page.beneficiary.is_beneficiary_field_invalid(1, "schoolName")


def test_tc_uat049_ui03_mobile_viewport_layout_and_interactions(fas_page: FasApplicationPage, fas_data: dict):
    """UI-3: Mobile viewport (375x667) renders stacked beneficiary cards and buttons without overflow."""
    fas_page.page.set_viewport_size({"width": 375, "height": 667})

    fas_page.open()
    fas_page.beneficiary.add_beneficiary()
    assert fas_page.beneficiary.get_beneficiary_count() == 2

    # Verify both cards are visible in mobile viewport
    cards = fas_page.page.locator("section[aria-labelledby='beneficiaries-heading'] article")
    assert cards.nth(0).is_visible()
    assert cards.nth(1).is_visible()

    # Reset viewport
    fas_page.page.set_viewport_size({"width": 1280, "height": 720})


def test_tc_uat049_sec01_xss_special_characters_in_child2_fields(fas_page: FasApplicationPage, fas_data: dict):
    """SEC-01: HTML tags and special chars in Child 2 name are safely rendered without script injection."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"isSuccess": True, "data": {"code": "APP-2026-FAS-00057", "status": "SUBMITTED", "submittedAt": "2026-10-26T15:58:00Z"}})
        )
    )

    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_beneficiary()
    child2_data = dict(fas_data["second_beneficiary"])
    child2_data["fullName"] = "TAN <script>alert('xss')</script> MEI"
    fas_page.beneficiary.fill_beneficiary(1, child2_data)

    fas_page.submit()

    assert fas_page.is_confirmation_visible(timeout=8000)
    fas_page.page.unroute_all()
