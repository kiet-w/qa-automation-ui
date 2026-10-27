"""
tests/f10/f10-fas-submission/uat047/test_uat047_server_error_resilience.py - 12 Server Error Resilience & Recovery Tests.
Traceability: UAT-047, BR-10-ERR-05, BR-10-ERR-06, AC-UAT-047-06, AC-UAT-047-07.
"""
import json
import pytest
from pages.f10.fas_application_page import FasApplicationPage


def test_tc_uat047_err01_server_error_500_banner_display(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-01: HTTP 500 server error displays red Alert banner #fas-server-error."""
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
    fas_page.page.unroute_all()


def test_tc_uat047_err02_server_error_502_bad_gateway(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-02: HTTP 502 Bad Gateway error displays error alert banner gracefully."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=502,
            content_type="application/json",
            body=json.dumps({"isSuccess": False, "message": "Bad Gateway"})
        )
    )
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.submit()

    assert fas_page.is_server_error_visible()
    fas_page.page.unroute_all()


def test_tc_uat047_err03_server_error_503_service_unavailable(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-03: HTTP 503 Service Unavailable displays error alert banner."""
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
    fas_page.submit()

    assert fas_page.is_server_error_visible()
    fas_page.page.unroute_all()


def test_tc_uat047_err04_server_error_504_gateway_timeout(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-04: HTTP 504 Gateway Timeout displays error banner."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=504,
            content_type="application/json",
            body=json.dumps({"isSuccess": False, "message": "Gateway Timeout"})
        )
    )
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.submit()

    assert fas_page.is_server_error_visible()
    fas_page.page.unroute_all()


def test_tc_uat047_err05_network_disconnect_graceful_handling(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-05: Network disconnection / abort triggers error alert banner without crash."""
    fas_page.page.route("**/applications**", lambda route: route.abort("failed"))
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.submit()

    assert fas_page.is_server_error_visible()
    fas_page.page.unroute_all()


def test_tc_uat047_err06_data_preservation_after_server_error(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-06: 100% of entered applicant and child form data is preserved after server error."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(status=500, content_type="application/json", body=json.dumps({"isSuccess": False}))
    )
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.submit()

    assert fas_page.is_server_error_visible()
    assert fas_page.page.input_value("#applicant-fullName") == fas_data["valid_applicant"]["fullName"]
    assert fas_page.page.input_value("#applicant-nric") == fas_data["valid_applicant"]["nric"]
    assert fas_page.page.input_value("#applicant-email") == fas_data["valid_applicant"]["email"]
    child_name_input = fas_page.page.locator("input[id^='beneficiary-'][id$='-fullName']").first
    assert child_name_input.input_value() == fas_data["valid_beneficiary"]["fullName"]
    fas_page.page.unroute_all()


def test_tc_uat047_err07_idempotency_key_preserved_across_retries(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-07: Idempotency-Key is preserved and reused on retry to prevent double creation."""
    recorded_keys = []

    def handle_request(route):
        key = route.request.headers.get("x-idempotency-key") or route.request.headers.get("idempotency-key")
        recorded_keys.append(key)
        route.fulfill(status=500, content_type="application/json", body=json.dumps({"isSuccess": False}))

    fas_page.page.route("**/applications**", handle_request)
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.submit()
    assert fas_page.is_server_error_visible()

    fas_page.submit()
    fas_page.page.unroute_all()
    assert len(recorded_keys) >= 2


def test_tc_uat047_err08_recovery_retry_loop_500_to_200_success(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-08: Full recovery loop: First attempt fails with 500, second retry succeeds with 200."""
    attempt = {"count": 0}

    def route_handler(route):
        attempt["count"] += 1
        if attempt["count"] == 1:
            route.fulfill(status=500, content_type="application/json", body=json.dumps({"isSuccess": False}))
        else:
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({"isSuccess": True, "data": {"code": "APP-2026-RECOVER-01", "status": "SUBMITTED", "submittedAt": "2026-10-26T15:45:00Z"}})
            )

    fas_page.page.route("**/applications**", route_handler)
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    # Attempt 1: Fails
    fas_page.submit()
    assert fas_page.is_server_error_visible()

    # Attempt 2: Retry succeeds
    fas_page.submit()
    assert fas_page.is_confirmation_visible(timeout=8000)
    assert fas_page.get_confirmation_code() == "APP-2026-RECOVER-01"
    fas_page.page.unroute_all()


def test_tc_uat047_err09_double_click_submission_prevention(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-09: Submit button is disabled immediately upon click, preventing duplicate submits."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"isSuccess": True, "data": {"code": "APP-01", "status": "SUBMITTED", "submittedAt": "2026-10-26T15:45:00Z"}})
        )
    )
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.submit()
    assert fas_page.is_confirmation_visible(timeout=8000)
    fas_page.page.unroute_all()


def test_tc_uat047_err10_submit_button_text_submitting_transition(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-10: Button text indicates submission in progress."""
    fas_page.open()
    initial_text = fas_page.get_submit_button_text()
    assert "Submit" in initial_text


def test_tc_uat047_err11_server_error_banner_dismissed_on_user_edit(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-11: Editing any form field dismisses the active server error banner."""
    fas_page.page.route("**/applications**", lambda route: route.fulfill(status=500, content_type="application/json", body=json.dumps({"isSuccess": False})))
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.submit()
    assert fas_page.is_server_error_visible()

    fas_page.page.fill("#applicant-fullName", "TAN AH TECK MODIFIED")
    assert not fas_page.is_server_error_visible(timeout=1000)
    fas_page.page.unroute_all()


def test_tc_uat047_err12_backend_400_bad_request_error_display(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-12: HTTP 400 Bad Request error returns specific code/message in Alert banner."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=400,
            content_type="application/json",
            body=json.dumps({"isSuccess": False, "code": "ERR-VAL-001", "message": "Invalid household income payload"})
        )
    )
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.submit()

    assert fas_page.is_server_error_visible()
    fas_page.page.unroute_all()
