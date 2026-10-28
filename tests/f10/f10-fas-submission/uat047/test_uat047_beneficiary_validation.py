"""
tests/f10/f10-fas-submission/uat047/test_uat047_beneficiary_validation.py - 20 Beneficiary & Cross-Field Validation Tests.
Traceability: UAT-047, BR-10-ERR-03, BR-10-ERR-04, AC-UAT-047-01 to AC-UAT-047-05.
"""
import pytest
from pages.f10.fas_application_page import FasApplicationPage


def test_tc_uat047_val21_beneficiary_empty_mandatory_fields(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-21: Empty beneficiary card triggers required inline error messages."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.submit()

    req_msg = fas_data["expected_messages"]["required"]
    assert req_msg in fas_page.beneficiary.get_beneficiary_error(0, "fullName")
    assert req_msg in fas_page.beneficiary.get_beneficiary_error(0, "nric")
    assert req_msg in fas_page.beneficiary.get_beneficiary_error(0, "schoolName")
    assert req_msg in fas_page.beneficiary.get_beneficiary_error(0, "grade")


def test_tc_uat047_val22_beneficiary_whitespace_trimming(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-22: Beneficiary whitespace strings are trimmed and treated as empty required."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    b_data = dict(fas_data["valid_beneficiary"])
    b_data["fullName"] = fas_data["invalid_inputs"]["whitespace_string"]
    b_data["schoolName"] = fas_data["invalid_inputs"]["whitespace_string"]
    fas_page.beneficiary.fill_beneficiary(0, b_data)
    fas_page.submit()

    req_msg = fas_data["expected_messages"]["required"]
    assert req_msg in fas_page.beneficiary.get_beneficiary_error(0, "fullName")
    assert req_msg in fas_page.beneficiary.get_beneficiary_error(0, "schoolName")


def test_tc_uat047_val23_beneficiary_nric_empty_triggers_error(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-23: Empty beneficiary NRIC triggers required error."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    b_data = dict(fas_data["valid_beneficiary"])
    b_data["nric"] = ""
    fas_page.beneficiary.fill_beneficiary(0, b_data)
    fas_page.submit()
    assert fas_data["expected_messages"]["required"] in fas_page.beneficiary.get_beneficiary_error(0, "nric")


def test_tc_uat047_val24_beneficiary_nric_syntax_invalid(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-24: Invalid syntax on beneficiary NRIC triggers invalidNric message."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    b_data = dict(fas_data["valid_beneficiary"])
    b_data["nric"] = "INVALID123"
    fas_page.beneficiary.fill_beneficiary(0, b_data)
    fas_page.submit()
    assert fas_data["expected_messages"]["invalid_nric"] in fas_page.beneficiary.get_beneficiary_error(0, "nric")


def test_tc_uat047_val25_beneficiary_school_empty_triggers_error(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-25: Empty school name triggers required error."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    b_data = dict(fas_data["valid_beneficiary"])
    b_data["schoolName"] = ""
    fas_page.beneficiary.fill_beneficiary(0, b_data)
    fas_page.submit()
    assert fas_data["expected_messages"]["required"] in fas_page.beneficiary.get_beneficiary_error(0, "schoolName")


def test_tc_uat047_val26_beneficiary_class_level_empty_triggers_error(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-26: Empty class level select triggers required error."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    b_data = dict(fas_data["valid_beneficiary"])
    b_data["classLevel"] = ""
    fas_page.beneficiary.fill_beneficiary(0, b_data)
    fas_page.submit()
    assert fas_data["expected_messages"]["required"] in fas_page.beneficiary.get_beneficiary_error(0, "classLevel")


def test_tc_uat047_val27_beneficiary_grade_empty_triggers_error(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-27: Empty grade input triggers required error."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    b_data = dict(fas_data["valid_beneficiary"])
    b_data["grade"] = ""
    fas_page.beneficiary.fill_beneficiary(0, b_data)
    fas_page.submit()
    assert fas_data["expected_messages"]["required"] in fas_page.beneficiary.get_beneficiary_error(0, "grade")


def test_tc_uat047_val28_beneficiary_bva_age_6_rejected(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-28: BVA Boundary < 7 years old (underage) is rejected with ageRange message."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    b_data = dict(fas_data["valid_beneficiary"])
    b_data["dateOfBirth"] = fas_data["invalid_inputs"]["bva_age_6_dob"]
    fas_page.beneficiary.fill_beneficiary(0, b_data)
    fas_page.submit()
    assert fas_data["expected_messages"]["age_range"] in fas_page.beneficiary.get_beneficiary_error(0, "dateOfBirth")


def test_tc_uat047_val29_beneficiary_bva_age_7_accepted(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-29: BVA Boundary exactly 7 years old is valid and accepted."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    b_data = dict(fas_data["valid_beneficiary"])
    b_data["dateOfBirth"] = fas_data["invalid_inputs"]["bva_age_7_dob"]
    fas_page.beneficiary.fill_beneficiary(0, b_data)
    fas_page.submit()
    assert fas_page.beneficiary.get_beneficiary_error(0, "dateOfBirth") == ""


def test_tc_uat047_val30_beneficiary_bva_age_11_accepted(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-30: Beneficiary mid-range age (11 years old) is valid and accepted."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.submit()
    assert fas_page.beneficiary.get_beneficiary_error(0, "dateOfBirth") == ""


def test_tc_uat047_val31_beneficiary_bva_age_16_accepted(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-31: BVA Boundary exactly 16 years old is valid and accepted."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    b_data = dict(fas_data["valid_beneficiary"])
    b_data["dateOfBirth"] = fas_data["invalid_inputs"]["bva_age_16_dob"]
    fas_page.beneficiary.fill_beneficiary(0, b_data)
    fas_page.submit()
    assert fas_page.beneficiary.get_beneficiary_error(0, "dateOfBirth") == ""


def test_tc_uat047_val32_beneficiary_bva_age_17_rejected(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-32: BVA Boundary > 16 years old (overage) is rejected with ageRange message."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    b_data = dict(fas_data["valid_beneficiary"])
    b_data["dateOfBirth"] = fas_data["invalid_inputs"]["bva_age_17_dob"]
    fas_page.beneficiary.fill_beneficiary(0, b_data)
    fas_page.submit()
    assert fas_data["expected_messages"]["age_range"] in fas_page.beneficiary.get_beneficiary_error(0, "dateOfBirth")


def test_tc_uat047_val33_beneficiary_future_dob_rejected(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-33: Beneficiary date of birth in the future is rejected with futureDate message."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    b_data = dict(fas_data["valid_beneficiary"])
    b_data["dateOfBirth"] = fas_data["invalid_inputs"]["future_dob"]
    fas_page.beneficiary.fill_beneficiary(0, b_data)
    fas_page.submit()
    assert fas_data["expected_messages"]["future_date"] in fas_page.beneficiary.get_beneficiary_error(0, "dateOfBirth")


def test_tc_uat047_val34_beneficiary_duplicate_nric_with_applicant(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-34: Beneficiary NRIC identical to applicant parent NRIC is rejected."""
    fas_page.open()
    same_nric = fas_data["valid_applicant"]["nric"]
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    b_data = dict(fas_data["valid_beneficiary"])
    b_data["nric"] = same_nric
    fas_page.beneficiary.fill_beneficiary(0, b_data)
    fas_page.submit()
    assert fas_data["expected_messages"]["duplicate_nric"] in fas_page.beneficiary.get_beneficiary_error(0, "nric")


def test_tc_uat047_val35_beneficiary_duplicate_nric_between_siblings(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-35: Duplicate NRIC between two sibling beneficiary cards is rejected."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_beneficiary()
    sibling_data = dict(fas_data["second_beneficiary"])
    sibling_data["nric"] = fas_data["valid_beneficiary"]["nric"]
    fas_page.beneficiary.fill_beneficiary(1, sibling_data)
    fas_page.submit()

    assert fas_data["expected_messages"]["duplicate_nric"] in fas_page.beneficiary.get_beneficiary_error(0, "nric")
    assert fas_data["expected_messages"]["duplicate_nric"] in fas_page.beneficiary.get_beneficiary_error(1, "nric")


def test_tc_uat047_val36_family_member_required_income_status(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-36: Adding family member requires explicit selection of hasIncome (Yes/No)."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_family_member()
    fam_data = dict(fas_data["family_member"])
    del fam_data["hasIncome"]  # Leave income unselected
    fas_page.beneficiary.fill_family_member(0, fam_data)
    fas_page.submit()

    assert fas_data["expected_messages"]["has_income_required"] in fas_page.beneficiary.get_family_error(0, "hasIncome")


def test_tc_uat047_val37_family_member_income_status_yes_accepted(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-37: Family member with hasIncome=Yes is valid without error."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_family_member()
    fas_page.beneficiary.fill_family_member(0, fas_data["family_member_income"])
    fas_page.submit()

    assert fas_page.beneficiary.get_family_error(0, "hasIncome") == ""


def test_tc_uat047_val38_family_member_income_status_no_accepted(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-38: Family member with hasIncome=No is valid without error."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_family_member()
    fas_page.beneficiary.fill_family_member(0, fas_data["family_member"])
    fas_page.submit()

    assert fas_page.beneficiary.get_family_error(0, "hasIncome") == ""


def test_tc_uat047_val39_beneficiary_visual_aria_invalid(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-39: Empty beneficiary inputs exhibit aria-invalid=true and red error outline."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.submit()

    child_name_input = fas_page.page.locator("input[id^='beneficiary-'][id$='-fullName']").first
    assert child_name_input.get_attribute("aria-invalid") == "true"


def test_tc_uat047_val40_real_time_error_clear_on_input_change(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-40: Error messages clear immediately when user updates the input field."""
    fas_page.open()
    fas_page.submit()
    assert fas_page.applicant.get_field_error("applicant-fullName") != ""

    fas_page.page.fill("#applicant-fullName", "T")
    assert fas_page.applicant.get_field_error("applicant-fullName") == ""
