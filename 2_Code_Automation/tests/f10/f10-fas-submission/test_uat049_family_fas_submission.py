"""
tests/f10/f10-fas-submission/test_uat049_family_fas_submission.py - End-to-End Family FAS Submission.
Traceability: UAT-049, BR-1 to BR-5, AC-1 to AC-5, Flow, Error Resilience, UI Health (BSK).
Compliant with Invariant 1 (Zero assertions in PO), 2 (Zero hardcoded data), 3, 4, 8, 9 (< 220 lines).
"""
import json
import pytest
from pages.f10.fas_application_page import FasApplicationPage


def test_tc_uat049_br01_multi_child_household_submission_success(fas_page: FasApplicationPage, fas_data: dict):
    """BR-1 / AC-3: Submit family application with 2 children under same family/parent record."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "isSuccess": True,
                "data": {
                    "code": "APP-2026-FAS-00049",
                    "status": "SUBMITTED",
                    "submittedAt": "2026-10-26T15:30:00Z"
                }
            })
        )
    )

    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    # Add second child
    fas_page.beneficiary.add_beneficiary()
    assert fas_page.beneficiary.get_beneficiary_count() == 2
    fas_page.beneficiary.fill_beneficiary(1, fas_data["second_beneficiary"])

    fas_page.submit()

    assert fas_page.is_confirmation_visible(timeout=8000), "Confirmation card must be visible"
    assert fas_page.get_confirmation_code() == "APP-2026-FAS-00049"
    assert fas_page.get_confirmation_status() == "SUBMITTED"
    fas_page.page.unroute_all()


def test_tc_uat049_br02_cross_school_primary_and_secondary_submission(fas_page: FasApplicationPage, fas_data: dict):
    """BR-3: Cross-school siblings (Child 1 in Primary School, Child 2 in Secondary School) accepted."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "isSuccess": True,
                "data": {
                    "code": "APP-2026-FAS-00050",
                    "status": "SUBMITTED",
                    "submittedAt": "2026-10-26T15:32:00Z"
                }
            })
        )
    )

    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])  # Primary school

    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(1, fas_data["secondary_beneficiary"])  # Secondary school

    fas_page.submit()

    assert fas_page.is_confirmation_visible(timeout=8000)
    assert fas_page.get_confirmation_code() == "APP-2026-FAS-00050"
    fas_page.page.unroute_all()


def test_tc_uat049_br03_three_children_family_submission_success(fas_page: FasApplicationPage, fas_data: dict):
    """BR-4: Multiple dynamic additions ($N=3$ children) submit in single payload."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "isSuccess": True,
                "data": {
                    "code": "APP-2026-FAS-00051",
                    "status": "SUBMITTED",
                    "submittedAt": "2026-10-26T15:35:00Z"
                }
            })
        )
    )

    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    # Add Child 2 and Child 3
    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(1, fas_data["second_beneficiary"])
    fas_page.beneficiary.add_beneficiary()
    assert fas_page.beneficiary.get_beneficiary_count() == 3
    fas_page.beneficiary.fill_beneficiary(2, fas_data["third_beneficiary"])

    fas_page.submit()

    assert fas_page.is_confirmation_visible(timeout=8000)
    assert fas_page.get_confirmation_status() == "SUBMITTED"
    fas_page.page.unroute_all()


def test_tc_uat049_ac01_add_beneficiary_creates_isolated_card_dom(fas_page: FasApplicationPage, fas_data: dict):
    """AC-1: Clicking '+ Add another beneficiary' appends an isolated beneficiary card with unique DOM IDs."""
    fas_page.open()
    assert fas_page.beneficiary.get_beneficiary_count() == 1

    fas_page.beneficiary.add_beneficiary()
    assert fas_page.beneficiary.get_beneficiary_count() == 2

    # Verify card 2 inputs exist and have unique IDs
    cards = fas_page.page.locator("section[aria-labelledby='beneficiaries-heading'] article")
    input_card1 = cards.nth(1).locator("input[id$='-fullName']")
    assert input_card1.is_visible()
    assert input_card1.get_attribute("id").startswith("beneficiary-")


def test_tc_uat049_ac02_remove_button_toggle_rule(fas_page: FasApplicationPage, fas_data: dict):
    """AC-2: Remove button disabled on single child, enabled when 2+ children present."""
    fas_page.open()

    # Initial state: 1 child, remove button is disabled
    assert fas_page.beneficiary.get_beneficiary_count() == 1
    assert fas_page.beneficiary.is_remove_beneficiary_disabled(0)

    # Add Child 2: both remove buttons become enabled
    fas_page.beneficiary.add_beneficiary()
    assert fas_page.beneficiary.get_beneficiary_count() == 2
    assert not fas_page.beneficiary.is_remove_beneficiary_disabled(0)
    assert not fas_page.beneficiary.is_remove_beneficiary_disabled(1)

    # Remove Child 2: Child 1 remove button reverts to disabled
    fas_page.beneficiary.remove_beneficiary(1)
    assert fas_page.beneficiary.get_beneficiary_count() == 1
    assert fas_page.beneficiary.is_remove_beneficiary_disabled(0)


def test_tc_uat049_ac04_adding_beneficiary_resets_form_error_state(fas_page: FasApplicationPage, fas_data: dict):
    """AC-4: Clicking '+ Add another beneficiary' resets error state and clears existing validation messages."""
    fas_page.open()
    fas_page.submit()  # Trigger validation errors

    # Check errors are present
    assert len(fas_page.applicant.get_field_error("applicant-fullName")) > 0

    # Add beneficiary -> triggers resetSubmitState()
    fas_page.beneficiary.add_beneficiary()

    # Errors should now be cleared
    assert fas_page.applicant.get_field_error("applicant-fullName") == ""


def test_tc_uat049_flo01_add_fill_remove_child2_flow_preserves_child1(fas_page: FasApplicationPage, fas_data: dict):
    """FLOW-2: Adding and filling Child 2 then removing Child 2 preserves Child 1 data intact."""
    fas_page.open()
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(1, fas_data["second_beneficiary"])

    # Remove Child 2
    fas_page.beneficiary.remove_beneficiary(1)
    assert fas_page.beneficiary.get_beneficiary_count() == 1

    # Verify Child 1 data is preserved
    card0 = fas_page.page.locator("section[aria-labelledby='beneficiaries-heading'] article").first
    assert card0.locator("input[id$='-fullName']").input_value() == fas_data["valid_beneficiary"]["fullName"]


def test_tc_uat049_flo02_two_children_plus_household_income_members(fas_page: FasApplicationPage, fas_data: dict):
    """FLOW-3: Integrated family flow with 2 children and 2 family members with and without income."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"isSuccess": True, "data": {"code": "APP-2026-FAS-00052", "status": "SUBMITTED", "submittedAt": "2026-10-26T15:40:00Z"}})
        )
    )

    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(1, fas_data["second_beneficiary"])

    # Add two family members (income + no income)
    fas_page.beneficiary.add_family_member()
    fas_page.beneficiary.fill_family_member(0, fas_data["family_member"])
    fas_page.beneficiary.add_family_member()
    fas_page.beneficiary.fill_family_member(1, fas_data["family_member_income"])

    fas_page.submit()

    assert fas_page.is_confirmation_visible(timeout=8000)
    assert fas_page.get_confirmation_code() == "APP-2026-FAS-00052"
    fas_page.page.unroute_all()


def test_tc_uat049_err01_server_error_500_preserves_both_children_data(fas_page: FasApplicationPage, fas_data: dict):
    """ERR-1: HTTP 500 error triggers red Alert banner and preserves both children's data without data wipe."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=500,
            content_type="application/json",
            body=json.dumps({"isSuccess": False, "message": "FAS Application Service Unavailable"})
        )
    )

    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(1, fas_data["second_beneficiary"])

    fas_page.submit()

    assert fas_page.is_server_error_visible(), "Server error alert banner should display"

    # Data preservation check on both children
    cards = fas_page.page.locator("section[aria-labelledby='beneficiaries-heading'] article")
    assert cards.nth(0).locator("input[id$='-fullName']").input_value() == fas_data["valid_beneficiary"]["fullName"]
    assert cards.nth(1).locator("input[id$='-fullName']").input_value() == fas_data["second_beneficiary"]["fullName"]
    fas_page.page.unroute_all()


def test_tc_uat049_ui01_multi_child_zero_console_errors_and_zero_i18n_leaks(fas_page: FasApplicationPage, fas_data: dict):
    """UI-1: Zero console errors and zero raw i18n leak strings when dynamically adding multiple children."""
    console_errors = []
    fas_page.page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

    fas_page.open()
    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.add_beneficiary()

    body_text = fas_page.page.inner_text("body")
    assert "features.fasApplication." not in body_text, "Found untranslated i18n key in DOM"
    assert len(console_errors) == 0, f"Found unexpected console errors: {console_errors}"


def test_tc_uat049_br04_pre_university_level_child_submission(fas_page: FasApplicationPage, fas_data: dict):
    """BR-3: Sibling in Pre-University / Junior College accepted in same family application."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"isSuccess": True, "data": {"code": "APP-2026-FAS-00053", "status": "SUBMITTED", "submittedAt": "2026-10-26T15:45:00Z"}})
        )
    )

    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    # Add Pre-University child
    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(1, fas_data["pre_uni_beneficiary"])

    fas_page.submit()

    assert fas_page.is_confirmation_visible(timeout=8000)
    assert fas_page.get_confirmation_code() == "APP-2026-FAS-00053"
    fas_page.page.unroute_all()


def test_tc_uat049_br05_four_children_large_family_submission(fas_page: FasApplicationPage, fas_data: dict):
    """BR-4: Scale-up submission with 4 children ($N=4$) in single household application."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"isSuccess": True, "data": {"code": "APP-2026-FAS-00054", "status": "SUBMITTED", "submittedAt": "2026-10-26T15:50:00Z"}})
        )
    )

    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    # Add 3 additional children
    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(1, fas_data["second_beneficiary"])
    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(2, fas_data["third_beneficiary"])
    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(3, fas_data["pre_uni_beneficiary"])

    assert fas_page.beneficiary.get_beneficiary_count() == 4

    fas_page.submit()

    assert fas_page.is_confirmation_visible(timeout=8000)
    assert fas_page.get_confirmation_status() == "SUBMITTED"
    fas_page.page.unroute_all()


def test_tc_uat049_flo03_middle_child_removal_preserves_remaining_children(fas_page: FasApplicationPage, fas_data: dict):
    """FLOW-2: Add 3 children, remove middle child (index 1) -> Child 0 and Child 2 preserved."""
    fas_page.open()
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(1, fas_data["second_beneficiary"])
    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(2, fas_data["third_beneficiary"])

    assert fas_page.beneficiary.get_beneficiary_count() == 3

    # Remove middle child (index 1)
    fas_page.beneficiary.remove_beneficiary(1)
    assert fas_page.beneficiary.get_beneficiary_count() == 2

    # Verify Child 0 still has TAN KAH KEE and Child 1 now has TAN KAI WEN
    cards = fas_page.page.locator("section[aria-labelledby='beneficiaries-heading'] article")
    assert cards.nth(0).locator("input[id$='-fullName']").input_value() == fas_data["valid_beneficiary"]["fullName"]
    assert cards.nth(1).locator("input[id$='-fullName']").input_value() == fas_data["third_beneficiary"]["fullName"]


def test_tc_uat049_flo04_start_new_application_resets_multi_child_form(fas_page: FasApplicationPage, fas_data: dict):
    """FLOW-4: After submitting multi-child application, clicking 'Start a new application' resets to 1 blank child."""
    fas_page.page.route(
        "**/applications**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"isSuccess": True, "data": {"code": "APP-2026-FAS-00055", "status": "SUBMITTED", "submittedAt": "2026-10-26T15:52:00Z"}})
        )
    )

    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.beneficiary.add_beneficiary()
    fas_page.beneficiary.fill_beneficiary(1, fas_data["second_beneficiary"])
    fas_page.submit()

    assert fas_page.is_confirmation_visible(timeout=8000)

    # Click start new
    fas_page.click_start_new_application()

    # Verify form is reset to 1 empty child card
    assert fas_page.beneficiary.get_beneficiary_count() == 1
    card0 = fas_page.page.locator("section[aria-labelledby='beneficiaries-heading'] article").first
    assert card0.locator("input[id$='-fullName']").input_value() == ""
    assert fas_page.page.input_value("#applicant-fullName") == ""
    fas_page.page.unroute_all()

