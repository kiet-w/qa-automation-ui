"""
tests/f10/f10-fas-submission/uat047/test_uat047_applicant_validation.py - 25 Applicant Validation Test Cases.
Traceability: UAT-047, BR-10-ERR-01, BR-10-ERR-02, AC-UAT-047-01 to AC-UAT-047-05.
"""
import pytest
from pages.f10.fas_application_page import FasApplicationPage


def test_tc_uat047_val01_empty_mandatory_applicant_fields(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-01: Empty applicant fields trigger inline required error messages."""
    fas_page.open()
    fas_page.submit()

    req_msg = fas_data["expected_messages"]["required"]
    assert req_msg in fas_page.applicant.get_field_error("applicant-fullName")
    assert req_msg in fas_page.applicant.get_field_error("applicant-nric")
    assert req_msg in fas_page.applicant.get_field_error("applicant-dateOfBirth")
    assert req_msg in fas_page.applicant.get_field_error("applicant-phoneNumber")
    assert req_msg in fas_page.applicant.get_field_error("applicant-email")
    assert req_msg in fas_page.applicant.get_field_error("applicant-address")
    assert fas_data["expected_messages"]["commitment_required"] in fas_page.applicant.get_field_error("applicant-commitmentAgreed")


def test_tc_uat047_val02_applicant_whitespace_trimming(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-02: Whitespace-only applicant inputs are trimmed and treated as empty required."""
    fas_page.open()
    ws_data = dict(fas_data["valid_applicant"])
    ws_data["fullName"] = fas_data["invalid_inputs"]["whitespace_string"]
    ws_data["address"] = fas_data["invalid_inputs"]["whitespace_string"]
    fas_page.applicant.fill_applicant(ws_data)
    fas_page.submit()

    req_msg = fas_data["expected_messages"]["required"]
    assert req_msg in fas_page.applicant.get_field_error("applicant-fullName")
    assert req_msg in fas_page.applicant.get_field_error("applicant-address")


def test_tc_uat047_val03_applicant_min_valid_name(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-03: Minimum 2-character valid name is accepted without errors."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["fullName"] = "An"
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert fas_page.applicant.get_field_error("applicant-fullName") == ""


def test_tc_uat047_val04_applicant_normal_valid_name(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-04: Standard Singaporean name with apostrophes / spaces is accepted."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["fullName"] = "Tan Ah Teck D'Souza"
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert fas_page.applicant.get_field_error("applicant-fullName") == ""


def test_tc_uat047_val05_applicant_nric_empty_triggers_error(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-05: Empty NRIC field triggers required inline error."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["nric"] = ""
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert fas_data["expected_messages"]["required"] in fas_page.applicant.get_field_error("applicant-nric")


def test_tc_uat047_val06_applicant_nric_s_prefix_valid(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-06: S-prefix Singapore Citizen NRIC is accepted."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["nric"] = "S7812345A"
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert "Please enter a valid Singapore NRIC/FIN" not in fas_page.applicant.get_field_error("applicant-nric")


def test_tc_uat047_val07_applicant_nric_t_prefix_valid(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-07: T-prefix Singapore Citizen NRIC is accepted."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["nric"] = "T0123456Z"
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert "Please enter a valid Singapore NRIC/FIN" not in fas_page.applicant.get_field_error("applicant-nric")


def test_tc_uat047_val08_applicant_nric_foreign_prefix_valid(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-08: Foreign FIN with G or F prefix is accepted."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["nric"] = "G1234567A"
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert "Please enter a valid Singapore NRIC/FIN" not in fas_page.applicant.get_field_error("applicant-nric")


@pytest.mark.parametrize("bad_nric", ["12345678", "S123456", "12345678A"])
def test_tc_uat047_val09_applicant_nric_syntax(fas_page: FasApplicationPage, fas_data: dict, bad_nric: str):
    """VAL-09: Invalid NRIC syntax patterns trigger invalidNric message."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["nric"] = bad_nric
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert fas_data["expected_messages"]["invalid_nric"] in fas_page.applicant.get_field_error("applicant-nric")


def test_tc_uat047_val10_applicant_nric_special_characters(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-10: NRIC containing punctuation or special symbols is rejected."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["nric"] = "S1234#67A"
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert fas_data["expected_messages"]["invalid_nric"] in fas_page.applicant.get_field_error("applicant-nric")


def test_tc_uat047_val11_applicant_dob_empty_triggers_error(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-11: Empty applicant date of birth triggers required error."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["dateOfBirth"] = ""
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert fas_data["expected_messages"]["required"] in fas_page.applicant.get_field_error("applicant-dateOfBirth")


def test_tc_uat047_val12_applicant_dob_future_date_rejected(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-12: Future date of birth is rejected with futureDate message."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["dateOfBirth"] = fas_data["invalid_inputs"]["future_dob"]
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert fas_data["expected_messages"]["future_date"] in fas_page.applicant.get_field_error("applicant-dateOfBirth")


def test_tc_uat047_val13_applicant_phone_empty_triggers_error(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-13: Empty phone number triggers required error."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["phoneNumber"] = ""
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert fas_data["expected_messages"]["required"] in fas_page.applicant.get_field_error("applicant-phoneNumber")


def test_tc_uat047_val14_applicant_phone_sg_prefix_8_valid(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-14: Singapore 8-digit phone starting with 8 is accepted."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["phoneNumber"] = "81234567"
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert "Please enter a valid" not in fas_page.applicant.get_field_error("applicant-phoneNumber")


def test_tc_uat047_val15_applicant_phone_sg_prefix_9_valid(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-15: Singapore 8-digit phone starting with 9 is accepted."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["phoneNumber"] = "98765432"
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert "Please enter a valid" not in fas_page.applicant.get_field_error("applicant-phoneNumber")


def test_tc_uat047_val16_applicant_phone_non_sg_prefix_rejected(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-16: Phone with invalid special formatting (dashes/spaces) is rejected."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["phoneNumber"] = "+65-9123-4567"
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert fas_data["expected_messages"]["invalid_phone"] in fas_page.applicant.get_field_error("applicant-phoneNumber")


@pytest.mark.parametrize("bad_phone", ["abc12345", "1234567890123"])
def test_tc_uat047_val17_applicant_phone_syntax(fas_page: FasApplicationPage, fas_data: dict, bad_phone: str):
    """VAL-17: Non-digit or over-length phone numbers trigger invalidPhone message."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["phoneNumber"] = bad_phone
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert fas_data["expected_messages"]["invalid_phone"] in fas_page.applicant.get_field_error("applicant-phoneNumber")


def test_tc_uat047_val18_applicant_email_empty_triggers_error(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-18: Empty email address triggers required error."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["email"] = ""
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert fas_data["expected_messages"]["required"] in fas_page.applicant.get_field_error("applicant-email")


@pytest.mark.parametrize("bad_email", ["tan@@email.com", "tan.email.com", "tan@"])
def test_tc_uat047_val19_applicant_email_syntax(fas_page: FasApplicationPage, fas_data: dict, bad_email: str):
    """VAL-19: Invalid email syntax patterns trigger invalidEmail message."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["email"] = bad_email
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()
    assert fas_data["expected_messages"]["invalid_email"] in fas_page.applicant.get_field_error("applicant-email")


def test_tc_uat047_val20_applicant_commitment_checkbox_required(fas_page: FasApplicationPage, fas_data: dict):
    """VAL-20: Unchecked commitment terms checkbox blocks submission with commitmentRequired."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["commitmentAgreed"] = False
    fas_page.applicant.fill_applicant(data)
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.submit()
    assert fas_data["expected_messages"]["commitment_required"] in fas_page.applicant.get_field_error("applicant-commitmentAgreed")
    assert not fas_page.is_confirmation_visible()
