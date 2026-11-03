"""
pages/fs03/school_config_page.py - Page Object for FS03 School Configuration screen.
Complies with Invariant 1 (UI actions & state reading only) and Invariant 9 (<250 lines).
"""
from typing import Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class SchoolConfigPage(BasePage):
    """POM for School Configuration screen (/school-config)."""

    URL_PATH = "/school-config"

    def __init__(self, page: Page):
        super().__init__(page)
        self.year_select: Locator = page.get_by_label("Academic year", exact=True)
        self.add_level_btn: Locator = page.get_by_role("button", name="Add Academic Levels")
        self.copy_prev_year_btn: Locator = page.get_by_role("button", name="Copy Previous Year")
        self.search_level_input: Locator = page.get_by_role("textbox", name="Search academic levels")
        self.add_class_btn: Locator = page.get_by_role("button", name="Add Class")
        self.classes_table: Locator = page.locator('article:has(button:has-text("Add Class")) table')

    def open(self, base_url: str = "http://localhost:5173") -> None:
        self.page.goto(f"{base_url}{self.URL_PATH}", wait_until="domcontentloaded")
