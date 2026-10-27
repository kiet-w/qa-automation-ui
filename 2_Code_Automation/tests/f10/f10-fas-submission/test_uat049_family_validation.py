"""
tests/f10/f10-fas-submission/test_uat049_family_validation.py - Validation Matrix for Family FAS (2+ Children).
Traceability: UAT-049, VAL-1 to VAL-7 (Cross-Person Duplicate NRIC, Age BVA, Mandatory, Format).
Compliant with Invariant 1 (Zero assertions in PO), 2 (Zero hardcoded data), 3, 4, 8, 9 (< 200 lines).
"""
import pytest
from pages.f10.fas_application_page import FasApplicationPage


def test_tc_uat049_val01_child2_mandatory_fields_show_errors(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-1: Adding Child 2 without filling mandatory fields triggers inline required errors on Child 2."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    # Add Child 2 but leave fields empty
    fas_page.beneficiary.add_beneficiary()
    assert fas_page.beneficiary.get_beneficiary_count() == 2

    fas_page.submit()

    req_msg = fas_data["expected_messages"]["required"]
    assert req_msg in fas_page.beneficiary.get_beneficiary_error(1, "fullName")
    assert req_msg in fas_page.beneficiary.get_beneficiary_error(1, "nric")
    assert req_msg in fas_page.beneficiary.get_beneficiary_error(1, "dateOfBirth")
    assert req_msg in fas_page.beneficiary.get_beneficiary_error(1, "schoolName")
    assert req_msg in fas_page.beneficiary.get_beneficiary_error(1, "grade")
    assert not fas_page.is_confirmation_visible()


def test_tc_uat049_val02_duplicate_nric_between_child1_and_child2(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-2: Child 2 having the exact same NRIC as Child 1 is rejected with duplicateNric error on both cards."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    # Add Child 2 with same NRIC as Child 1
    fas_page.beneficiary.add_beneficiary()
    child2_data = dict(fas_data["second_beneficiary"])
    child2_data["nric"] = fas_data["valid_beneficiary"]["nric"]  # Duplicate NRIC
    fas_page.beneficiary.fill_beneficiary(1, child2_data)

    fas_page.submit()

    dup_msg = fas_data["expected_messages"]["duplicate_nric"]
    child1_nric_err = fas_page.beneficiary.get_beneficiary_error(0, "nric")
    child2_nric_err = fas_page.beneficiary.get_beneficiary_error(1, "nric")
    assert dup_msg in child1_nric_err, f"Expected duplicate error on Child 1, got: '{child1_nric_err}'"
    assert dup_msg in child2_nric_err, f"Expected duplicate error on Child 2, got: '{child2_nric_err}'"
    assert not fas_page.is_confirmation_visible()


def test_tc_uat049_val03_duplicate_nric_between_child2_and_applicant(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-2: Child 2 having the same NRIC as the applicant parent is rejected with duplicateNric error."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    # Add Child 2 with same NRIC as Parent Applicant
    fas_page.beneficiary.add_beneficiary()
    child2_data = dict(fas_data["second_beneficiary"])
    child2_data["nric"] = fas_data["valid_applicant"]["nric"]  # Duplicate with Parent
    fas_page.beneficiary.fill_beneficiary(1, child2_data)

    fas_page.submit()

    dup_msg = fas_data["expected_messages"]["duplicate_nric"]
    parent_nric_err = fas_page.applicant.get_field_error("applicant-nric")
    child2_nric_err = fas_page.beneficiary.get_beneficiary_error(1, "nric")
    assert dup_msg in parent_nric_err, f"Expected duplicate error on Parent, got: '{parent_nric_err}'"
    assert dup_msg in child2_nric_err, f"Expected duplicate error on Child 2, got: '{child2_nric_err}'"
    assert not fas_page.is_confirmation_visible()


def test_tc_uat049_val04_child2_underage_boundary_bva(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-3: BVA - Child 2 aged 6 (< 7) is rejected with ageRange error."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_beneficiary()
    child2_data = dict(fas_data["second_beneficiary"])
    child2_data["dateOfBirth"] = fas_data["invalid_inputs"]["bva_age_6_dob"]
    fas_page.beneficiary.fill_beneficiary(1, child2_data)

    fas_page.submit()

    age_err = fas_page.beneficiary.get_beneficiary_error(1, "dateOfBirth")
    assert fas_data["expected_messages"]["age_range"] in age_err
    assert not fas_page.is_confirmation_visible()


def test_tc_uat049_val05_child2_overage_boundary_bva(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-3: BVA - Child 2 aged 17 (> 16) is rejected with ageRange error."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_beneficiary()
    child2_data = dict(fas_data["second_beneficiary"])
    child2_data["dateOfBirth"] = fas_data["invalid_inputs"]["bva_age_17_dob"]
    fas_page.beneficiary.fill_beneficiary(1, child2_data)

    fas_page.submit()

    age_err = fas_page.beneficiary.get_beneficiary_error(1, "dateOfBirth")
    assert fas_data["expected_messages"]["age_range"] in age_err
    assert not fas_page.is_confirmation_visible()


def test_tc_uat049_val06_child2_future_dob_rejected(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-4: Child 2 date of birth in future is rejected with futureDate error."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_beneficiary()
    child2_data = dict(fas_data["second_beneficiary"])
    child2_data["dateOfBirth"] = fas_data["invalid_inputs"]["future_dob"]
    fas_page.beneficiary.fill_beneficiary(1, child2_data)

    fas_page.submit()

    dob_err = fas_page.beneficiary.get_beneficiary_error(1, "dateOfBirth")
    assert fas_data["expected_messages"]["future_date"] in dob_err
    assert not fas_page.is_confirmation_visible()


def test_tc_uat049_val07_child2_invalid_nric_format(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-5: Child 2 invalid NRIC syntax is rejected with invalidNric error."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_beneficiary()
    child2_data = dict(fas_data["second_beneficiary"])
    child2_data["nric"] = fas_data["invalid_inputs"]["invalid_nrics"][0]  # "12345678"
    fas_page.beneficiary.fill_beneficiary(1, child2_data)

    fas_page.submit()

    nric_err = fas_page.beneficiary.get_beneficiary_error(1, "nric")
    assert fas_data["expected_messages"]["invalid_nric"] in nric_err
    assert not fas_page.is_confirmation_visible()


def test_tc_uat049_val08_child2_exact_min_age_7_accepted(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-3: BVA - Child 2 aged exactly 7 (valid min boundary) is accepted without ageRange error."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_beneficiary()
    child2_data = dict(fas_data["second_beneficiary"])
    child2_data["dateOfBirth"] = fas_data["invalid_inputs"]["bva_age_7_dob"]  # Age 7
    fas_page.beneficiary.fill_beneficiary(1, child2_data)

    fas_page.submit()

    # Should not have ageRange error on child 2
    age_err = fas_page.beneficiary.get_beneficiary_error(1, "dateOfBirth")
    assert fas_data["expected_messages"]["age_range"] not in age_err


def test_tc_uat049_val09_child2_exact_max_age_16_accepted(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-3: BVA - Child 2 aged exactly 16 (valid max boundary) is accepted without ageRange error."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_beneficiary()
    child2_data = dict(fas_data["second_beneficiary"])
    child2_data["dateOfBirth"] = fas_data["invalid_inputs"]["bva_age_16_dob"]  # Age 16
    fas_page.beneficiary.fill_beneficiary(1, child2_data)

    fas_page.submit()

    # Should not have ageRange error on child 2
    age_err = fas_page.beneficiary.get_beneficiary_error(1, "dateOfBirth")
    assert fas_data["expected_messages"]["age_range"] not in age_err


def test_tc_uat049_val10_duplicate_nric_between_child2_and_family_member(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-2: Child 2 having duplicate NRIC with a household Family Member is rejected."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    # Add Child 2
    fas_page.beneficiary.add_beneficiary()
    child2_data = dict(fas_data["second_beneficiary"])
    same_nric = fas_data["family_member"]["nric"]
    child2_data["nric"] = same_nric
    fas_page.beneficiary.fill_beneficiary(1, child2_data)

    # Add Family Member with same NRIC
    fas_page.beneficiary.add_family_member()
    fas_page.beneficiary.fill_family_member(0, fas_data["family_member"])

    fas_page.submit()

    dup_msg = fas_data["expected_messages"]["duplicate_nric"]
    child2_nric_err = fas_page.beneficiary.get_beneficiary_error(1, "nric")
    assert dup_msg in child2_nric_err
    assert not fas_page.is_confirmation_visible()


def test_tc_uat049_val11_child2_missing_date_of_birth(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-4: Child 2 with empty date of birth triggers required error."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_beneficiary()
    child2_data = dict(fas_data["second_beneficiary"])
    child2_data["dateOfBirth"] = ""  # Empty date of birth
    fas_page.beneficiary.fill_beneficiary(1, child2_data)

    fas_page.submit()

    dob_err = fas_page.beneficiary.get_beneficiary_error(1, "dateOfBirth")
    assert fas_data["expected_messages"]["required"] in dob_err
    assert not fas_page.is_confirmation_visible()


