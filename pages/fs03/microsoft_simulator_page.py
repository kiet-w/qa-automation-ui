"""
pages/fs03/microsoft_simulator_page.py - Page Object for Microsoft Entra ID Simulator (:5288).
Complies with Invariant 1 (Zero assertions in Page Objects) and modularity (<150 lines).
"""
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.fs03.locators import MicrosoftSimulatorLocators


class MicrosoftSimulatorPage(BasePage):
    """Encapsulates interaction with the Microsoft Entra ID Simulator on port 5288."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.moehq_tile = self.page.locator(MicrosoftSimulatorLocators.MOEHQ_ACCOUNT_TILE)
        self.school_tile = self.page.locator(MicrosoftSimulatorLocators.SCHOOL_ACCOUNT_TILE)
        self.parent_tile = self.page.locator(MicrosoftSimulatorLocators.PARENT_ACCOUNT_TILE)
        self.use_another_account_btn = self.page.locator(MicrosoftSimulatorLocators.USE_ANOTHER_ACCOUNT_BTN)
        self.continue_btn = self.page.locator(MicrosoftSimulatorLocators.CONTINUE_BTN)
        self.cancel_btn = self.page.locator(MicrosoftSimulatorLocators.CANCEL_BTN)

    def select_moehq_admin(self) -> None:
        """Select MOE HQ Admin tile (admin@IAM.edu.vn)."""
        self.moehq_tile.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def select_school_staff(self) -> None:
        """Select School Staff tile (staff1@IAM.edu.vn)."""
        self.school_tile.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def select_parent_account(self) -> None:
        """Select Parent role tile (head1@IAM.edu.vn)."""
        self.parent_tile.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def click_cancel(self) -> None:
        """Cancel authentication in simulator and safely return to login (using browser back)."""
        cancel = self.page.locator("a:has-text('Cancel'), button:has-text('Cancel')")
        try:
            if cancel.count() > 0 and cancel.first.is_visible():
                cancel.first.click()
                self.page.wait_for_load_state("domcontentloaded")
                return
        except Exception:
            pass
        self.page.go_back()
        self.page.wait_for_load_state("domcontentloaded")

    def click_continue(self) -> None:
        """Click continue in simulator."""
        self.continue_btn.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def click_use_another_account(self) -> None:
        """Open custom credentials form in simulator."""
        self.use_another_account_btn.first.click()
