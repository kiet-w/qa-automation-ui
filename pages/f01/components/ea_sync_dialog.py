"""
pages/f01/components/ea_sync_dialog.py - Sub-component for Sync Confirmation Dialog.
BSK-Verified: Dialog title is "Sync citizen data" (role="dialog").
Complies with Invariant 1 (Zero assertions in Page Objects) and Invariant 9 (< 150 lines).

BSK Source: specs/ui_bsk/localhost-5173/finance-and-fas/01_education_accounts.md
"""
from playwright.sync_api import Page
from pages.f01 import locators


class EaSyncDialog:
    """
    Encapsulates interaction with the Citizen Sync Confirmation Dialog.
    BSK-verified title: "Sync citizen data" (role="dialog" or role="alertdialog").
    """

    def __init__(self, page: Page):
        self.page = page
        # Dual selector: BSK-confirmed role="dialog" title "Sync citizen data" takes precedence
        self.dialog = self.page.locator(locators.SYNC_DIALOG)
        self.title = self.page.locator(locators.SYNC_DIALOG_TITLE)
        self.description = self.page.locator(locators.SYNC_DIALOG_DESC)
        # Buttons are scoped globally since they appear only within the open dialog context
        self.confirm_button = self.page.locator(locators.SYNC_CONFIRM_BTN)
        self.cancel_button = self.page.locator(locators.SYNC_CANCEL_BTN)

    def is_visible(self, timeout: int = 5000) -> bool:
        """Check if sync dialog is visible within given timeout (ms). Returns False on timeout."""
        try:
            self.dialog.first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def get_title_text(self) -> str:
        """Return title text of the sync dialog."""
        try:
            return self.title.first.inner_text().strip()
        except Exception:
            return ""

    def get_description_text(self) -> str:
        """Return description paragraph text of the sync dialog."""
        try:
            return self.description.first.inner_text().strip()
        except Exception:
            return ""

    def confirm(self) -> None:
        """
        Click 'Confirm' button to trigger citizen sync mutation.
        Waits for dialog to close after confirmation (POST request fired).
        """
        self.confirm_button.first.click()
        # Wait for dialog to dismiss (sync in progress)
        self.dialog.first.wait_for(state="hidden", timeout=15000)

    def cancel(self) -> None:
        """
        Click 'Cancel' button to abort synchronization.
        Dialog should close without firing any network mutation.
        Uses short timeout to avoid anti-hang (Invariant 8 Directive 15).
        """
        if self.cancel_button.first.is_visible(timeout=2000):
            self.cancel_button.first.click()
            self.dialog.first.wait_for(state="hidden", timeout=5000)
