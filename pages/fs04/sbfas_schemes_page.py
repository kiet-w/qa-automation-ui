"""
pages/fs04/sbfas_schemes_page.py - Page Object for SBFAS Schemes (/sbfas-schemes).
Verified on Live DOM under School Admin (staff1@IAM.edu.vn, Rosyth Primary School).
Strict compliance with Invariant 1 (POM standard: zero assertions).
"""
import time
from typing import Dict, List, Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class SbfasSchemesPage(BasePage):
    """Encapsulates interaction with SBFAS Schemes list, 4-Step Wizard, and Add Fee Component."""

    def __init__(self, page: Page):
        super().__init__(page)

        # --- List View Locators ---
        self.new_scheme_btn = self.page.locator('button:has-text("New scheme"), a[href*="/sbfas-schemes/new"]')
        self.schemes_table = self.page.locator("table")
        self.table_rows = self.page.locator("table tbody tr")
        self.filter_reset_btn = self.page.locator('button:has-text("Reset filters")')

        # --- Wizard Step 1: General Locators ---
        self.name_input = self.page.locator("#sbfas-name")
        self.open_from_input = self.page.locator("#sbfas-open-from")
        self.open_to_input = self.page.locator("#sbfas-open-to")
        self.effective_from_input = self.page.locator("#sbfas-effective-from")
        self.effective_to_input = self.page.locator("#sbfas-effective-to")
        self.budget_input = self.page.locator("#sbfas-budget")
        self.eligibility_desc_input = self.page.locator("#sbfas-eligibility-description")
        self.step1_next_btn = self.page.locator('button[type="submit"]:has-text("Next"), button:has-text("Next")')

        # --- Wizard Step 2: Eligibility Locators ---
        self.nationality_sc_checkbox = self.page.locator("#sbfas-nationality-SC")
        self.nationality_pr_checkbox = self.page.locator("#sbfas-nationality-PR")
        self.ghi_to_input = self.page.locator("#sbfas-ghi-to")
        self.pci_to_input = self.page.locator("#sbfas-pci-to")
        self.step2_next_btn = self.page.locator('button:has-text("Next")')

        # --- Wizard Step 3: Subsidy Locators ---
        self.add_fee_components_btn = self.page.locator('button:has-text("Add fee components")')
        self.fee_picker_modal = self.page.locator("[role='dialog']")
        self.fee_picker_checkboxes = self.page.locator("[role='dialog'] input[type='checkbox']")
        self.fee_picker_apply_btn = self.page.locator('[role="dialog"] button:has-text("Apply")')
        self.subsidy_matrix_inputs = self.page.locator("table input")
        self.step3_review_btn = self.page.locator('button:has-text("Review")')

        # --- Wizard Step 4: Review Locators ---
        self.review_heading = self.page.locator('h2:has-text("Review SBFAS scheme"), h1:has-text("Review")')
        self.back_to_edit_btn = self.page.locator('button:has-text("Back to edit"), button:has-text("Back")')
        self.save_draft_btn = self.page.locator('button:has-text("Save draft")')
        self.publish_btn = self.page.locator('button:has-text("Publish")')
        self.alert_error = self.page.locator('[role="alert"]')

        # --- Add Fee Component Modal (Post-Publish) ---
        self.add_fee_dialog = self.page.locator('[role="dialog"]:has-text("Add fee component")')
        self.add_fee_component_select = self.page.locator('[role="dialog"] select')
        self.add_fee_modal_inputs = self.page.locator('[role="dialog"] input[type="number"], [role="dialog"] input')
        self.add_fee_modal_submit_btn = self.page.locator('[role="dialog"] button:has-text("Add fee")')

    # ==========================================
    # Navigation Actions
    # ==========================================
    def open_list(self, base_url: str = "https://admin.20-255-158-192.sslip.io") -> None:
        """Navigate to SBFAS Schemes list."""
        self.page.goto(f"{base_url}/sbfas-schemes", wait_until="networkidle")

    def open_create_wizard(self, base_url: str = "https://admin.20-255-158-192.sslip.io") -> None:
        """Navigate to Create SBFAS Scheme Wizard."""
        self.page.goto(f"{base_url}/sbfas-schemes/new", wait_until="networkidle")

    def click_new_scheme(self) -> None:
        """Click New scheme button from list view."""
        self.new_scheme_btn.first.click()
        self.page.wait_for_url("**/sbfas-schemes/new", timeout=15000)

    # ==========================================
    # Wizard Step 1: General
    # ==========================================
    def fill_step1_general(
        self,
        name: str,
        open_from: str,
        open_to: str,
        effective_from: str,
        effective_to: Optional[str] = None,
        budget: str = "50000",
        description: str = "",
    ) -> None:
        """Fill Step 1 General details."""
        self.name_input.fill(name)
        self.open_from_input.fill(open_from)
        self.open_to_input.fill(open_to)
        self.effective_from_input.fill(effective_from)
        if effective_to:
            self.effective_to_input.fill(effective_to)
        self.budget_input.fill(budget)
        if description:
            self.eligibility_desc_input.fill(description)

    def submit_step1(self) -> None:
        """Click Next on Step 1."""
        self.step1_next_btn.click()
        self.page.wait_for_load_state("networkidle")

    # ==========================================
    # Wizard Step 2: Eligibility
    # ==========================================
    def fill_step2_eligibility(
        self,
        nationality_sc: bool = True,
        ghi_to: str = "3000",
        pci_to: str = "1000",
    ) -> None:
        """Fill Step 2 Eligibility criteria."""
        if nationality_sc:
            self.nationality_sc_checkbox.check()
        if ghi_to:
            self.ghi_to_input.fill(ghi_to)
        if pci_to:
            self.pci_to_input.fill(pci_to)

    def submit_step2(self) -> None:
        """Click Next on Step 2."""
        self.step2_next_btn.click()
        self.page.wait_for_load_state("networkidle")

    # ==========================================
    # Wizard Step 3: Subsidy Matrix
    # ==========================================
    def pick_fee_component_by_index(self, index: int = 0) -> None:
        """Open fee picker and select a component by index."""
        self.add_fee_components_btn.click()
        self.fee_picker_modal.wait_for(state="visible", timeout=10000)
        self.fee_picker_checkboxes.nth(index).check()
        self.fee_picker_apply_btn.click()
        self.fee_picker_modal.wait_for(state="hidden", timeout=10000)

    def fill_subsidy_rates_all_inputs(self, rate: str = "100") -> None:
        """Fill all rendered grade inputs in the subsidy matrix with rate."""
        inputs = self.subsidy_matrix_inputs.all()
        for inp in inputs:
            inp.fill(rate)

    def submit_step3(self) -> None:
        """Click Review on Step 3."""
        self.step3_review_btn.click()
        self.page.wait_for_load_state("networkidle")

    # ==========================================
    # Wizard Step 4: Review & Publish
    # ==========================================
    def click_publish(self) -> None:
        """Click Publish on Step 4 Review."""
        self.publish_btn.click()
        self.page.wait_for_load_state("networkidle")

    def click_back_to_edit(self) -> None:
        """Click Back to edit on Step 4 Review."""
        self.back_to_edit_btn.click()
        self.page.wait_for_load_state("networkidle")

    def navigate_back_to_step1(self) -> None:
        """Navigate backwards from Review (Step 4) to Step 1 General."""
        for _ in range(5):
            if self.name_input.is_visible():
                break
            back_btn = self.page.locator('button:has-text("Back to edit"), button:has-text("Back")').first
            if back_btn.count() > 0 and back_btn.is_visible():
                back_btn.click()
                self.page.wait_for_timeout(500)
            else:
                break

    def get_alert_error_text(self) -> str:
        """Get text of any visible alert banner error."""
        if self.alert_error.count() > 0 and self.alert_error.first.is_visible():
            return self.alert_error.first.inner_text().strip()
        return ""

    # ==========================================
    # Post-Publish Actions: Add Fee Component
    # ==========================================
    def open_add_fee_dialog_for_scheme(self, scheme_name: str) -> None:
        """Open Add fee modal from row Actions menu."""
        row = self.page.locator(f"table tbody tr:has-text('{scheme_name}')").first
        actions_btn = row.locator("button[aria-label*='Actions'], button:has-text('Actions')").first
        actions_btn.click()
        self.page.wait_for_timeout(300)
        self.page.locator("[role='menuitem']:has-text('Add fee')").click()
        self.add_fee_dialog.wait_for(state="visible", timeout=10000)

    def submit_add_fee_component(
        self,
        component_name: Optional[str] = None,
        rates_per_grade: Optional[List[str]] = None,
    ) -> None:
        """Select fee component, fill grade rates, and submit dialog."""
        if component_name:
            try:
                self.add_fee_component_select.select_option(label=component_name)
            except Exception:
                self.add_fee_component_select.select_option(index=1)
        else:
            self.add_fee_component_select.select_option(index=1)

        inputs = self.add_fee_modal_inputs.all()
        for i, inp in enumerate(inputs):
            rate_val = rates_per_grade[i] if rates_per_grade and i < len(rates_per_grade) else "100"
            inp.fill(rate_val)

        self.add_fee_modal_submit_btn.click()
        self.page.wait_for_load_state("networkidle")
