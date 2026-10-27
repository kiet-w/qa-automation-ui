"""
pages/f10/components/fas_applicant_form.py - Component for Applicant Fields interaction.
Compliant with Invariant 1 (Zero assertions) and Invariant 9 (< 150 lines).
"""
from typing import Any, Dict
from playwright.sync_api import Page
from pages.f10 import locators


class FasApplicantForm:
    """Component managing the Applicant Section fields and errors."""

    def __init__(self, page: Page):
        self.page = page

    def fill_applicant(self, applicant_data: Dict[str, Any]) -> None:
        """Fill all fields in the Applicant details card."""
        card = self.page.locator(locators.CARD_APPLICANT)
        if "fullName" in applicant_data:
            card.locator(locators.APPLICANT_FULL_NAME).fill(applicant_data["fullName"])
        if "nric" in applicant_data:
            card.locator(locators.APPLICANT_NRIC).fill(applicant_data["nric"])
        if "dateOfBirth" in applicant_data:
            card.locator(locators.APPLICANT_DOB).fill(applicant_data["dateOfBirth"])
        if "gender" in applicant_data:
            card.locator(f"input[name='applicant-gender'][value='{applicant_data['gender']}']").check(force=True)
        if "nationality" in applicant_data:
            card.locator(locators.APPLICANT_NATIONALITY).select_option(applicant_data["nationality"])
        if "race" in applicant_data:
            card.locator(locators.APPLICANT_RACE).select_option(applicant_data["race"])
        if "relationshipToBeneficiary" in applicant_data:
            card.locator(locators.APPLICANT_RELATIONSHIP).select_option(applicant_data["relationshipToBeneficiary"])
        if "phoneNumber" in applicant_data:
            card.locator(locators.APPLICANT_PHONE).fill(applicant_data["phoneNumber"])
        if "email" in applicant_data:
            card.locator(locators.APPLICANT_EMAIL).fill(applicant_data["email"])
        if "address" in applicant_data:
            card.locator(locators.APPLICANT_ADDRESS).fill(applicant_data["address"])
        if "commitmentAgreed" in applicant_data:
            self.set_commitment(applicant_data["commitmentAgreed"])
        if "forwardToSchoolAgreed" in applicant_data:
            self.set_forward_to_school(applicant_data["forwardToSchoolAgreed"])

    def set_commitment(self, checked: bool) -> None:
        """Check or uncheck the declaration & commitment checkbox."""
        cb = self.page.locator(locators.APPLICANT_COMMITMENT)
        if checked:
            cb.check()
        else:
            cb.uncheck()

    def set_forward_to_school(self, checked: bool) -> None:
        """Check or uncheck the forward to school consent checkbox."""
        cb = self.page.locator(locators.APPLICANT_FORWARD_SCHOOL)
        if checked:
            cb.check()
        else:
            cb.uncheck()

    def get_field_error(self, field_id: str) -> str:
        """Get the inline error message associated with an applicant field."""
        err_locator = self.page.locator(f"#{field_id}-error")
        if err_locator.count() > 0:
            return err_locator.inner_text().strip()
        sibling = self.page.locator(f"#{field_id} ~ p, #{field_id} ~ span")
        if sibling.count() > 0:
            return sibling.first.inner_text().strip()
        return ""

    def is_field_invalid(self, field_id: str) -> bool:
        """Check if an applicant input has aria-invalid='true'."""
        el = self.page.locator(f"#{field_id}")
        return el.count() > 0 and el.get_attribute("aria-invalid") == "true"
