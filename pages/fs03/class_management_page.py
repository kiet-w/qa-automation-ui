"""
pages/fs03/class_management_page.py - Page Object for FS03 Class Management screen.
Complies with Invariant 1 (UI actions & state reading only) and Invariant 9 (<250 lines).
"""
from typing import Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class ClassManagementPage(BasePage):
    """POM for Class Management screens (/class-management)."""

    URL_PATH = "/class-management"

    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input: Locator = page.locator('input[placeholder*="Search by class code or name" i]')
        self.level_filter: Locator = page.locator('input[placeholder*="Filter by academic level" i]')
        self.year_filter: Locator = page.locator('input[placeholder*="e.g. 2026" i]')
        self.search_button: Locator = page.locator('button[type="submit"]:has-text("Search")')
        self.reset_button: Locator = page.locator('button:has-text("Reset filters")')
        self.create_button: Locator = page.locator('button:has-text("Create class")')
        self.table_headers: Locator = page.locator("table thead th")
        self.table_rows: Locator = page.locator("table tbody tr")

        # Create Class Form fields
        self.class_code_input: Locator = page.locator("#class-classCode")
        self.class_name_input: Locator = page.locator("#class-className")
        self.academic_level_input: Locator = page.locator("#class-academicLevelId")
        self.academic_year_input: Locator = page.locator("#class-academicYearId")
        self.submit_btn: Locator = page.locator('button[type="submit"]:has-text("Create class")')

    def open(self, base_url: str = "http://localhost:5173") -> None:
        self.page.goto(f"{base_url}{self.URL_PATH}", wait_until="domcontentloaded")
