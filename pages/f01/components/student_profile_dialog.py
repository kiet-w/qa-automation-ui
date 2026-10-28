"""
pages/f01/components/student_profile_dialog.py - Sub-component for Student Profile Details Dialog.
Complies with Invariant 1 (Zero assertions in Page Objects) and Invariant 9 (< 150 lines).
"""
from typing import Dict, Optional
from playwright.sync_api import Locator, Page
from pages.f01 import locators


class StudentProfileDialog:
    """Encapsulates interaction with the Student Profile Details Dialog."""

    def __init__(self, page: Page):
        self.page = page
        self.dialog = self.page.locator(locators.PROFILE_DIALOG)
        self.heading = self.page.locator(locators.PROFILE_DIALOG_HEADING)
        self.close_button = self.page.locator(locators.PROFILE_CLOSE_BTN)
        self.x_button = self.page.locator(locators.PROFILE_X_BTN)

    def is_visible(self, timeout: int = 5000) -> bool:
        """Check if details dialog is visible."""
        try:
            self.dialog.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def get_content_text(self) -> str:
        """Return full text content of dialog."""
        return self.dialog.inner_text()

    def get_field_value(self, label: str) -> Optional[str]:
        """Extract value corresponding to a field label inside dialog."""
        text = self.get_content_text()
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for idx, line in enumerate(lines):
            if line.lower() == label.lower() and idx + 1 < len(lines):
                return lines[idx + 1]
        return None

    def close(self) -> None:
        """Click Close button to dismiss the dialog."""
        if self.close_button.is_visible(timeout=2000):
            self.close_button.click()
        elif self.x_button.is_visible(timeout=2000):
            self.x_button.click()
        self.dialog.wait_for(state="hidden", timeout=5000)
