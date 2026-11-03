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
        self.pick_account_heading = self.page.locator(MicrosoftSimulatorLocators.PICK_ACCOUNT_HEADING)
        self.moehq_tile = self.page.locator(MicrosoftSimulatorLocators.MOEHQ_ACCOUNT_TILE)
        self.school_tile = self.page.locator(MicrosoftSimulatorLocators.SCHOOL_ACCOUNT_TILE)
        self.parent_tile = self.page.locator(MicrosoftSimulatorLocators.PARENT_ACCOUNT_TILE)
        self.use_another_account_btn = self.page.locator(MicrosoftSimulatorLocators.USE_ANOTHER_ACCOUNT_BTN)
        self.use_another_account_input = self.page.locator(MicrosoftSimulatorLocators.USE_ANOTHER_ACCOUNT_INPUT)
        self.continue_btn = self.page.locator(MicrosoftSimulatorLocators.CONTINUE_BTN)

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

    def fill_custom_account(self, email: str) -> None:
        """Enter custom account email in simulator input."""
        if self.use_another_account_input.count() > 0:
            self.use_another_account_input.first.fill(email)
        elif self.use_another_account_btn.count() > 0:
            self.use_another_account_btn.first.click()
            self.use_another_account_input.first.fill(email)

    def click_cancel(self) -> None:
        """Cancel authentication using the simulator flow's browser-back behavior."""
        self.page.go_back()
        self.page.wait_for_load_state("domcontentloaded")

    def click_continue(self) -> None:
        """Click continue in simulator."""
        self.continue_btn.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def click_use_another_account(self) -> None:
        """Open custom credentials form in simulator."""
        self.use_another_account_btn.first.click()
