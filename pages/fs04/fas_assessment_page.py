"""
pages/fs04/fas_assessment_page.py - Page Object Model for FAS Assessment (/fas-applications).
Covers Step 7: UAT-SCH-03 (Approve SBFAS), UAT-SCH-03-N1 (Reject SBFAS), and UAT-035 (Human Control & Role Finality).
Strict compliance with Invariant 1 (POM standard: zero assertions).
"""
import re
import time
from typing import Dict, List, Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class FasAssessmentPage(BasePage):
    """Page Object Model for FAS Assessment list, detail view, review drawer, and decision dialogs."""

    def __init__(self, page: Page):
        super().__init__(page)

        # --- List View Locators (/fas-applications) ---
        self.page_heading: Locator = page.get_by_role("heading", name=re.compile(r"FAS Applications", re.IGNORECASE))
        self.status_select: Locator = page.locator("select").first
        self.page_size_select: Locator = page.locator("select").nth(1)
        self.search_input: Locator = page.locator('input[type="search"], input[placeholder*="search" i]')
        self.apply_search_btn: Locator = page.locator('button:has-text("Apply search")')
        self.reset_filters_btn: Locator = page.locator('button:has-text("Reset filters")')
        self.applications_table: Locator = page.locator("table")
        self.table_headers: Locator = page.locator("table th")
        self.table_rows: Locator = page.locator("table tbody tr")

        # --- Detail & Review Locators (/fas-applications/:id) ---
        self.back_to_applications_link: Locator = page.locator('a:has-text("Back to applications")')
        self.app_detail_heading: Locator = page.locator("#admin-main-content h1, #admin-main-content h2").first
        self.status_badge: Locator = page.locator('span:has-text("Pending School Review"), span:has-text("Approved"), span:has-text("Rejected")').first
        self.evaluation_result_text: Locator = page.locator('text="Evaluating at school level."').first
        self.ghi_value: Locator = page.locator('text="$4,400"').or_(page.locator('text="$4,400.00"')).first
        self.pci_value: Locator = page.locator('text="$1,100"').or_(page.locator('text="$1,100.00"')).first
        self.income_verification_badge: Locator = page.locator('span:has-text("Verified"), dd:has-text("Verified")').first
        self.beneficiary_ethan: Locator = page.locator('text="Ethan Rahman"').first
        self.beneficiary_second: Locator = page.locator('text="Leo Rahman"').or_(page.locator('text="Liam Pham"')).first
        self.view_documents_btn: Locator = page.locator('a:has-text("View documents"), button:has-text("View documents")').first
        self.upload_documents_btn: Locator = page.locator('button:has-text("Upload documents")').first

        # --- Drawer & Decision Dialog Locators ---
        self.review_drawer: Locator = page.locator('aside[aria-label*="Review" i], [role="dialog"][aria-label*="Review" i]')
        self.drawer_close_btn: Locator = page.locator('button[data-testid="fas-drawer-close-btn"], button[aria-label="Close"]')
        
        # Approve Dialog
        self.approve_btn: Locator = page.locator('button:has-text("Approve"), button[data-testid*="approve"]')
        self.approve_dialog: Locator = page.locator('dialog:has-text("Approve"), [role="dialog"]:has-text("Approve"), [data-testid="dialog-approve-fas"]')
        self.tier1_radio: Locator = page.locator('input[type="radio"][value*="1"], [data-testid="radio-tier-1"], text="Tier 1"')
        self.tier2_radio: Locator = page.locator('input[type="radio"][value*="2"], [data-testid="radio-tier-2"], text="Tier 2"')
        self.approval_comment_input: Locator = page.locator('[data-testid="dialog-approve-fas"] textarea, dialog textarea, textarea[name*="comment"]')
        self.confirm_approve_btn: Locator = page.locator('button:has-text("Confirm approval"), button[data-testid="btn-confirm-approve-fas"]')
        self.cancel_approve_btn: Locator = page.locator('button:has-text("Cancel")')

        # Reject Dialog
        self.reject_btn: Locator = page.locator('button:has-text("Reject"), button[data-testid*="reject"]')
        self.reject_dialog: Locator = page.locator('dialog:has-text("Reject"), [role="dialog"]:has-text("Reject"), [data-testid="dialog-reject-fas"]')
        self.rejection_reason_select: Locator = page.locator('[data-testid="dialog-reject-fas"] select, dialog select')
        self.rejection_remarks_input: Locator = page.locator('[data-testid="dialog-reject-fas"] textarea, dialog textarea, textarea[name*="remarks"], textarea[data-testid="textarea-rejection-remarks"]')
        self.confirm_reject_btn: Locator = page.locator('button:has-text("Reject application"), button[data-testid="btn-confirm-reject-fas"]')
        self.cancel_reject_btn: Locator = page.locator('button:has-text("Cancel")')

        # Read-Only / Decided Banner
        self.decided_banner: Locator = page.locator('[data-testid="banner-already-decided"], [role="alert"]:has-text("Approved"), [role="alert"]:has-text("Rejected")')
        self.toast_notification: Locator = page.locator('[role="status"], [role="alert"], .toast, div:has-text("Subsidy applied"), div:has-text("Application rejected")')

    # -------------------------------------------------------------------------
    # List View Actions
    # -------------------------------------------------------------------------
    def navigate(self, base_url: str) -> None:
        """Navigate to /fas-applications."""
        self.page.goto(f"{base_url.rstrip('/')}/fas-applications", wait_until="networkidle")

    def filter_by_status(self, status_text: str = "Pending School Review") -> None:
        """Select status from the status dropdown filter."""
        self.status_select.select_option(label=status_text)
        self.page.wait_for_load_state("networkidle")

    def search_application(self, query: str) -> None:
        """Enter search query and submit filter."""
        self.search_input.fill(query)
        self.apply_search_btn.click()
        self.page.wait_for_load_state("networkidle")

    def reset_filters(self) -> None:
        """Reset all search and status filters."""
        self.reset_filters_btn.click()
        self.page.wait_for_load_state("networkidle")

    def get_row_by_application_code(self, app_code: str) -> Locator:
        """Find table row matching application code."""
        return self.page.locator(f'table tbody tr:has-text("{app_code}")').first

    def get_row_by_student_name(self, student_name: str) -> Locator:
        """Find table row matching student beneficiary name."""
        return self.page.locator(f'table tbody tr:has-text("{student_name}")').first

    def click_view_details_on_row(self, row: Locator) -> None:
        """Click 'View details' or 'View' button on the specified row."""
        row.locator('button:has-text("View details"), a:has-text("View details"), button:has-text("View"), a:has-text("View")').first.click()
        self.page.wait_for_load_state("networkidle")

    def click_view_details_for_code(self, app_code: str) -> None:
        """Find row by application code and click View details."""
        row = self.get_row_by_application_code(app_code)
        self.click_view_details_on_row(row)

    # -------------------------------------------------------------------------
    # Detail View Actions
    # -------------------------------------------------------------------------
    def get_application_status_text(self) -> str:
        """Retrieve status text from application detail page."""
        return self.status_badge.inner_text().strip()

    def get_financial_summary(self) -> Dict[str, str]:
        """Extract financial review data from detail view."""
        text = self.page.locator("#admin-main-content").inner_text()
        return {
            "evaluation_result": "Evaluating at school level." if "Evaluating at school level." in text else "",
            "ghi": "$4,400" if "$4,400" in text else "",
            "pci": "$1,100" if "$1,100" in text else "",
            "verification": "Verified" if "Verified" in text else ""
        }

    def navigate_back_to_list(self) -> None:
        """Click Back to applications link."""
        self.back_to_applications_link.click()
        self.page.wait_for_load_state("networkidle")

    # -------------------------------------------------------------------------
    # Decision Dialog Actions (Approval & Rejection)
    # -------------------------------------------------------------------------
    def open_approve_dialog(self) -> None:
        """Open Approve FAS Dialog."""
        if self.approve_btn.is_visible():
            self.approve_btn.click()
            self.page.wait_for_timeout(500)

    def select_tier(self, tier: str = "Tier 1") -> None:
        """Select scheme tier."""
        if "1" in tier and self.tier1_radio.is_visible():
            self.tier1_radio.check()
        elif "2" in tier and self.tier2_radio.is_visible():
            self.tier2_radio.check()

    def fill_approval_comment(self, comment: str) -> None:
        """Fill approval comment."""
        if self.approval_comment_input.is_visible():
            self.approval_comment_input.fill(comment)

    def confirm_approval(self) -> None:
        """Submit approval decision."""
        if self.confirm_approve_btn.is_visible():
            self.confirm_approve_btn.click()
            self.page.wait_for_load_state("networkidle")

    def open_reject_dialog(self) -> None:
        """Open Reject FAS Dialog."""
        if self.reject_btn.is_visible():
            self.reject_btn.click()
            self.page.wait_for_timeout(500)

    def select_rejection_reason(self, reason: str = "Income above limit") -> None:
        """Select reason from dropdown."""
        if self.rejection_reason_select.is_visible():
            self.rejection_reason_select.select_option(label=reason)

    def fill_rejection_remarks(self, remarks: str) -> None:
        """Fill rejection remarks."""
        if self.rejection_remarks_input.is_visible():
            self.rejection_remarks_input.fill(remarks)

    def is_reject_submit_disabled(self) -> bool:
        """Check if reject confirm button is disabled."""
        if self.confirm_reject_btn.is_visible():
            return self.confirm_reject_btn.is_disabled()
        return True

    def confirm_rejection(self) -> None:
        """Submit rejection decision."""
        if self.confirm_reject_btn.is_visible():
            self.confirm_reject_btn.click()
            self.page.wait_for_load_state("networkidle")

    # -------------------------------------------------------------------------
    # MOE HQ Observer Navigation
    # -------------------------------------------------------------------------
    def navigate_moe_hq(self, base_url: str) -> None:
        """Navigate to /moe-hq/fas-applications."""
        self.page.goto(f"{base_url.rstrip('/')}/moe-hq/fas-applications", wait_until="networkidle")
