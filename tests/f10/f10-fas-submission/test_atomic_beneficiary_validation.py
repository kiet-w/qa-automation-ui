"""
tests/f10/f10-fas-submission/test_atomic_beneficiary_validation.py - Atomic Beneficiary & Family Validations.
Traceability: UAT-028, BR-10-SUB-03, Age 7-16 Boundaries, Duplicate NRIC.
Compliant with Invariant 1, 2, 3, 4, 9 (< 200 lines).
"""
import pytest
from pages.f10.fas_application_page import FasApplicationPage

BENEFICIARY_REQUIRED_FIELDS = [
    "fullName",
    "nric",
    "dateOfBirth",
    "schoolName",
    "grade"
]


@pytest.mark.atomic
@pytest.mark.parametrize("suffix", BENEFICIARY_REQUIRED_FIELDS)
def test_tc_uat028_val_beneficiary_required_fields(fas_page: FasApplicationPage, fas_data: dict, suffix: str):
    """VAL: Individual empty beneficiary card fields trigger inline required error messages."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.submit()

    req_msg = fas_data["expected_messages"]["required"]
    err = fas_page.beneficiary.get_beneficiary_error(0, suffix)
    assert req_msg in err, f"Beneficiary field '{suffix}' expected '{req_msg}', got: '{err}'"


@pytest.mark.atomic
@pytest.mark.parametrize("invalid_dob", ["2023-01-01", "2021-06-15", "2008-01-01", "2007-05-20"])
def test_tc_uat028_val_beneficiary_ineligible_age_boundaries(fas_page: FasApplicationPage, fas_data: dict, invalid_dob: str):
    """VAL (BR-10-SUB-03): Beneficiary under 7 or over 16 years old is rejected with ageRange message."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    child = dict(fas_data["valid_beneficiary"])
    child["dateOfBirth"] = invalid_dob
    fas_page.beneficiary.fill_beneficiary(0, child)
    fas_page.submit()

    dob_err = fas_page.beneficiary.get_beneficiary_error(0, "dateOfBirth")
    assert fas_data["expected_messages"]["age_range"] in dob_err


@pytest.mark.atomic
@pytest.mark.parametrize("valid_dob", ["2019-01-01", "2015-08-20", "2010-01-01"])
def test_tc_uat028_val_beneficiary_eligible_age_boundaries(fas_page: FasApplicationPage, fas_data: dict, valid_dob: str):
    """VAL (BR-10-SUB-03): Beneficiary aged 7 to 16 years old is accepted without ageRange error."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    child = dict(fas_data["valid_beneficiary"])
    child["dateOfBirth"] = valid_dob
    fas_page.beneficiary.fill_beneficiary(0, child)
    fas_page.submit()

    dob_err = fas_page.beneficiary.get_beneficiary_error(0, "dateOfBirth")
    assert fas_data["expected_messages"]["age_range"] not in dob_err


@pytest.mark.atomic
def test_tc_uat028_val_beneficiary_future_dob_rejected(fas_page: FasApplicationPage, fas_data: dict):
    """VAL: Future date of birth is rejected with futureDate message."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    child = dict(fas_data["valid_beneficiary"])
    child["dateOfBirth"] = fas_data["invalid_inputs"]["future_dob"]
    fas_page.beneficiary.fill_beneficiary(0, child)
    fas_page.submit()

    dob_err = fas_page.beneficiary.get_beneficiary_error(0, "dateOfBirth")
    assert fas_data["expected_messages"]["future_date"] in dob_err


@pytest.mark.atomic
def test_tc_uat028_val_beneficiary_duplicate_nric_with_applicant(fas_page: FasApplicationPage, fas_data: dict):
    """VAL (BR-10-SUB-03): Beneficiary NRIC matching Applicant NRIC triggers duplicateNric on both."""
    fas_page.open()
    same_nric = fas_data["valid_applicant"]["nric"]
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    child = dict(fas_data["valid_beneficiary"])
    child["nric"] = same_nric
    fas_page.beneficiary.fill_beneficiary(0, child)
    fas_page.submit()

    dup_msg = fas_data["expected_messages"]["duplicate_nric"]
    assert dup_msg in fas_page.beneficiary.get_beneficiary_error(0, "nric")
    assert dup_msg in fas_page.applicant.get_field_error("applicant-nric")


@pytest.mark.atomic
def test_tc_uat028_val_beneficiary_duplicate_nric_between_siblings(fas_page: FasApplicationPage, fas_data: dict):
    """VAL (BR-10-SUB-03): Duplicate NRIC between two sibling beneficiaries triggers duplicateNric."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_beneficiary()
    sibling = dict(fas_data["second_beneficiary"])
    sibling["nric"] = fas_data["valid_beneficiary"]["nric"]
    fas_page.beneficiary.fill_beneficiary(1, sibling)
    fas_page.submit()

    dup_msg = fas_data["expected_messages"]["duplicate_nric"]
    assert dup_msg in fas_page.beneficiary.get_beneficiary_error(0, "nric")
    assert dup_msg in fas_page.beneficiary.get_beneficiary_error(1, "nric")


@pytest.mark.atomic
def test_tc_uat028_val_family_member_required_income_status(fas_page: FasApplicationPage, fas_data: dict):
    """VAL: Family member added without selecting hasIncome triggers hasIncomeRequired."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])

    fas_page.beneficiary.add_family_member()
    member = dict(fas_data["family_member"])
    del member["hasIncome"]  # Leave income unselected
    fas_page.beneficiary.fill_family_member(0, member)
    fas_page.submit()

    err = fas_page.page.locator("p#familyMembers-0-hasIncome-error, section[aria-labelledby='family-members-heading'] p").first
    assert fas_data["expected_messages"]["has_income_required"] in err.inner_text()


@pytest.mark.atomic
@pytest.mark.parametrize("suffix", ["fullName", "nric", "schoolName"])
def test_tc_uat028_val_beneficiary_visual_aria_invalid(fas_page: FasApplicationPage, fas_data: dict, suffix: str):
    """VAL: Failed beneficiary inputs receive visual error indication and aria-invalid='true'."""
    fas_page.open()
    fas_page.applicant.fill_applicant(fas_data["valid_applicant"])
    fas_page.submit()

    assert fas_page.beneficiary.is_beneficiary_field_invalid(0, suffix)
