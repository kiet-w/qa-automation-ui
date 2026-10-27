"""
tests/f10/f10-fas-submission/test_atomic_applicant_validation.py - Atomic Applicant Validations.
Traceability: UAT-028, 12-Layer Field Validation Matrix, BR-10-SUB-02.
Compliant with Invariant 1, 2, 3, 4, 9 (< 200 lines).
"""
import pytest
from pages.f10.fas_application_page import FasApplicationPage

APPLICANT_REQUIRED_FIELDS = [
    "applicant-fullName",
    "applicant-nric",
    "applicant-dateOfBirth",
    "applicant-phoneNumber",
    "applicant-email",
    "applicant-address",
]


@pytest.mark.atomic
@pytest.mark.parametrize("field_id", APPLICANT_REQUIRED_FIELDS)
def test_tc_uat028_val_applicant_required_fields(fas_page: FasApplicationPage, fas_data: dict, field_id: str):
    """VAL: Individual empty applicant fields trigger inline required error message."""
    fas_page.open()
    fas_page.submit()

    req_msg = fas_data["expected_messages"]["required"]
    err = fas_page.applicant.get_field_error(field_id)
    assert req_msg in err, f"Field '{field_id}' expected '{req_msg}', got: '{err}'"


@pytest.mark.atomic
@pytest.mark.parametrize("field_key,field_id", [("fullName", "applicant-fullName"), ("address", "applicant-address")])
def test_tc_uat028_val_applicant_whitespace_trimming(fas_page: FasApplicationPage, fas_data: dict, field_key: str, field_id: str):
    """VAL: Whitespace-only applicant inputs are trimmed and treated as empty required."""
    fas_page.open()
    ws_data = dict(fas_data["valid_applicant"])
    ws_data[field_key] = fas_data["invalid_inputs"]["whitespace_string"]
    fas_page.applicant.fill_applicant(ws_data)
    fas_page.submit()

    req_msg = fas_data["expected_messages"]["required"]
    assert req_msg in fas_page.applicant.get_field_error(field_id)


@pytest.mark.atomic
@pytest.mark.parametrize("bad_nric", ["12345678", "S123456", "12345678A", "S123456789A", "!@#$%^&*"])
def test_tc_uat028_val_applicant_nric_syntax(fas_page: FasApplicationPage, fas_data: dict, bad_nric: str):
    """VAL: Invalid NRIC syntax patterns trigger invalidNric message."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["nric"] = bad_nric
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()

    nric_err = fas_page.applicant.get_field_error("applicant-nric")
    assert fas_data["expected_messages"]["invalid_nric"] in nric_err


@pytest.mark.atomic
@pytest.mark.parametrize("bad_phone", ["abc12345", "1234567890123", "phone_no", "912345678901"])
def test_tc_uat028_val_applicant_phone_syntax(fas_page: FasApplicationPage, fas_data: dict, bad_phone: str):
    """VAL: Non-digit or over-length phone numbers trigger invalidPhone message."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["phoneNumber"] = bad_phone
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()

    phone_err = fas_page.applicant.get_field_error("applicant-phoneNumber")
    assert fas_data["expected_messages"]["invalid_phone"] in phone_err


@pytest.mark.atomic
@pytest.mark.parametrize("bad_email", ["tan@@email.com", "tan.email.com", "tan@", "@email.com", "tan email@domain.com"])
def test_tc_uat028_val_applicant_email_syntax(fas_page: FasApplicationPage, fas_data: dict, bad_email: str):
    """VAL: Malformed email addresses trigger invalidEmail message."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["email"] = bad_email
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()

    email_err = fas_page.applicant.get_field_error("applicant-email")
    assert fas_data["expected_messages"]["invalid_email"] in email_err


@pytest.mark.atomic
def test_tc_uat028_val_applicant_future_date_of_birth(fas_page: FasApplicationPage, fas_data: dict):
    """VAL: Future date of birth for applicant triggers futureDate message."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["dateOfBirth"] = fas_data["invalid_inputs"]["future_dob"]
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()

    dob_err = fas_page.applicant.get_field_error("applicant-dateOfBirth")
    assert fas_data["expected_messages"]["future_date"] in dob_err


@pytest.mark.atomic
def test_tc_uat028_val_applicant_commitment_required(fas_page: FasApplicationPage, fas_data: dict):
    """VAL (BR-10-SUB-02): Submitting with valid fields but unchecked commitment fails."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["commitmentAgreed"] = False
    fas_page.applicant.fill_applicant(data)
    fas_page.beneficiary.fill_beneficiary(0, fas_data["valid_beneficiary"])
    fas_page.submit()

    commit_err = fas_page.applicant.get_field_error("applicant-commitmentAgreed")
    assert fas_data["expected_messages"]["commitment_required"] in commit_err
    assert not fas_page.is_confirmation_visible()


@pytest.mark.atomic
@pytest.mark.parametrize("valid_name", ["Tan Ah-Teck O'Connor", "陈大德 (Tan Ah Teck)"])
def test_tc_uat028_val_applicant_special_and_unicode_name(fas_page: FasApplicationPage, fas_data: dict, valid_name: str):
    """VAL: Full name with hyphens, apostrophes, and Unicode characters is accepted cleanly."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["fullName"] = valid_name
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()

    name_err = fas_page.applicant.get_field_error("applicant-fullName")
    assert name_err == "", f"Expected no error for valid name '{valid_name}', got: '{name_err}'"


@pytest.mark.atomic
def test_tc_uat028_val_applicant_xss_sanitization(fas_page: FasApplicationPage, fas_data: dict):
    """VAL: Entering XSS payload in fullName does not trigger script execution."""
    fas_page.open()
    data = dict(fas_data["valid_applicant"])
    data["fullName"] = "<script>window._xss_executed=true</script>"
    fas_page.applicant.fill_applicant(data)
    fas_page.submit()

    executed = fas_page.page.evaluate("() => window._xss_executed || false")
    assert not executed, "Security violation: XSS script tag was executed in browser!"


@pytest.mark.atomic
@pytest.mark.parametrize("field_id", ["applicant-fullName", "applicant-nric", "applicant-phoneNumber"])
def test_tc_uat028_val_visual_error_feedback_aria_invalid(fas_page: FasApplicationPage, fas_data: dict, field_id: str):
    """VAL: Failed applicant fields receive visual error indication and aria-invalid='true'."""
    fas_page.open()
    fas_page.submit()

    assert fas_page.applicant.is_field_invalid(field_id), f"Field '{field_id}' should have aria-invalid='true'"
