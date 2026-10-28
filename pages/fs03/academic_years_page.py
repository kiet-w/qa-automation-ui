"""
pages/fs03/academic_years_page.py - Page Object for FS03 Academic Years & Levels.
Complies with Invariant 1 (UI actions & state reading only) and Invariant 9 (<250 lines).
"""
from typing import Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class AcademicYearsPage(BasePage):
    """POM for Academic Years & Levels management screens."""

    URL_PATH = "/academic-years"

    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input: Locator = page.locator('input[placeholder*="Search by year" i]')
        self.status_filter: Locator = page.locator('select:has(option[value="DRAFT"])')
        self.search_button: Locator = page.locator('button[type="submit"]:has-text("Search")')
        self.reset_button: Locator = page.locator('button:has-text("Reset filters")')
        self.create_button: Locator = page.locator('button:has-text("Create academic year")')
        self.table_headers: Locator = page.locator("table thead th")
        self.table_rows: Locator = page.locator("table tbody tr")

        # Form fields for /academic-years/new
        self.year_input: Locator = page.locator("#academic-year-yearNumber")
        self.start_date_input: Locator = page.locator("#academic-year-startDate")
        self.end_date_input: Locator = page.locator("#academic-year-endDateExclusive")
        self.submit_create_btn: Locator = page.locator('button[type="submit"]:has-text("Create academic year")')
        self.cancel_btn: Locator = page.locator('button:has-text("Cancel")')

    def open(self, base_url: str = "http://localhost:5173") -> None:
        self.page.goto(f"{base_url}{self.URL_PATH}", wait_until="domcontentloaded")
