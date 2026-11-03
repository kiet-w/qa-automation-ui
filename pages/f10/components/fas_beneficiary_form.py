"""
pages/f10/components/fas_beneficiary_form.py - Component for Beneficiary & Family Rows.
Compliant with Invariant 1 (Zero assertions) and Invariant 9 (< 150 lines).
"""
from typing import Any, Dict
from playwright.sync_api import Page
from pages.f10 import locators


class FasBeneficiaryForm:
    """Component managing Beneficiary cards and Family Member cards."""

    def __init__(self, page: Page):
        self.page = page

    def fill_beneficiary(self, index: int, data: Dict[str, Any]) -> None:
        """Fill details for beneficiary at specific index (0-based)."""
        card = self.page.locator(locators.CARDS_BENEFICIARY).nth(index)
        if "fullName" in data:
            card.locator(locators.BENEFICIARY_FULL_NAME).fill(data["fullName"])
        if "nric" in data:
            card.locator(locators.BENEFICIARY_NRIC).fill(data["nric"])
        if "dateOfBirth" in data:
            card.locator(locators.BENEFICIARY_DOB).fill(data["dateOfBirth"])
        if "gender" in data:
            card.locator(locators.BENEFICIARY_GENDER).select_option(data["gender"])
        if "schoolName" in data:
            card.locator(locators.BENEFICIARY_SCHOOL).fill(data["schoolName"])
        if "classLevel" in data:
            card.locator(locators.BENEFICIARY_CLASS_LEVEL).select_option(data["classLevel"])
        if "grade" in data:
            card.locator(locators.BENEFICIARY_GRADE).fill(data["grade"])

    def add_beneficiary(self) -> None:
        """Click button to add another beneficiary card."""
        self.page.click(locators.BTN_ADD_BENEFICIARY)

    def remove_beneficiary(self, index: int) -> None:
        """Click remove button on beneficiary card at index."""
        card = self.page.locator(locators.CARDS_BENEFICIARY).nth(index)
        card.locator(locators.BTN_REMOVE_BENEFICIARY).click()

    def is_remove_beneficiary_disabled(self, index: int) -> bool:
        """Check if remove button on beneficiary card at index is disabled."""
        card = self.page.locator(locators.CARDS_BENEFICIARY).nth(index)
        btn = card.locator(locators.BTN_REMOVE_BENEFICIARY)
        return btn.is_disabled()

    def get_beneficiary_count(self) -> int:
        """Count currently rendered beneficiary cards."""
        return self.page.locator(locators.CARDS_BENEFICIARY).count()

    def fill_family_member(self, index: int, data: Dict[str, Any]) -> None:
        """Fill details for family member card at index (0-based)."""
        card = self.page.locator(locators.CARDS_FAMILY).nth(index)
        if "fullName" in data:
            card.locator(locators.FAMILY_FULL_NAME).fill(data["fullName"])
        if "nric" in data:
            card.locator(locators.FAMILY_NRIC).fill(data["nric"])
        if "dateOfBirth" in data:
            card.locator(locators.FAMILY_DOB).fill(data["dateOfBirth"])
        if "gender" in data:
            card.locator(locators.FAMILY_GENDER).select_option(data["gender"])
        if "relationship" in data:
            card.locator(locators.FAMILY_RELATIONSHIP).select_option(data["relationship"])
        if "hasIncome" in data:
            income_control = locators.FAMILY_HAS_INCOME_YES if data["hasIncome"] else locators.FAMILY_HAS_INCOME_NO
            card.locator(locators.FAMILY_HAS_INCOME_GROUP).locator(income_control).check()

    def add_family_member(self) -> None:
        """Click button to add a family member card."""
        self.page.click(locators.BTN_ADD_FAMILY)

    def get_family_count(self) -> int:
        """Count currently rendered family member cards."""
        return self.page.locator(locators.CARDS_FAMILY).count()

    def get_family_error(self, index: int, field_suffix: str) -> str:
        """Get inline error for a field inside family member card."""
        card = self.page.locator(locators.CARDS_FAMILY).nth(index)
        err = card.locator(f"[id$='-{field_suffix}-error']")
        if err.count() > 0:
            return err.inner_text().strip()
        fs_err = card.locator(f"fieldset[id$='-{field_suffix}'] p[role='alert']")
        if fs_err.count() > 0:
            return fs_err.inner_text().strip()
        fallback = card.locator(f"div:has([id$='-{field_suffix}']) p")
        if fallback.count() > 0:
            return fallback.first.inner_text().strip()
        return ""

    def get_beneficiary_error(self, index: int, field_suffix: str) -> str:
        """Get inline error for a field inside beneficiary card."""
        card = self.page.locator(locators.CARDS_BENEFICIARY).nth(index)
        err = card.locator(f"[id$='-{field_suffix}-error']")
        if err.count() > 0:
            return err.inner_text().strip()
        fallback = card.locator(f"div:has([id$='-{field_suffix}']) p")
        if fallback.count() > 0:
            return fallback.first.inner_text().strip()
        return ""

    def is_beneficiary_field_invalid(self, index: int, field_suffix: str) -> bool:
        """Check if a beneficiary input has aria-invalid='true'."""
        card = self.page.locator(locators.CARDS_BENEFICIARY).nth(index)
        el = card.locator(f"[id$='-{field_suffix}']")
        return el.count() > 0 and el.get_attribute("aria-invalid") == "true"
