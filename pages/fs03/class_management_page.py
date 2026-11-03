"""UI actions and state for the Class Management screens."""
import re
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class ClassManagementPage(BasePage):
    """POM for Class Management screens (/class-management)."""

    URL_PATH = "/class-management"

    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input: Locator = page.get_by_role("searchbox", name="Search")
        self.level_filter: Locator = page.locator("#class-filter-academic-level")
        self.year_filter: Locator = page.locator("#class-filter-academic-year")
        self.search_button: Locator = page.get_by_role("button", name="Search", exact=True)
        self.reset_button: Locator = page.get_by_role("button", name="Reset filters")
        self.create_button: Locator = page.get_by_role("button", name="Create class", exact=True)
        self.table_headers: Locator = page.get_by_role("table", name="Classes table").locator("thead th")
        self.table_rows: Locator = page.get_by_role("table", name="Classes table").locator("tbody tr")

        # Create Class Form fields
        self.class_code_input: Locator = page.locator("#class-classCode")
        self.class_name_input: Locator = page.locator("#class-className")
        self.offering_combobox: Locator = page.locator("#class-schoolLevelOffering")
        self.submit_btn: Locator = page.get_by_role("button", name="Create class", exact=True)
        self.create_error: Locator = page.get_by_role("heading", name="Unable to create class")
        self.detail_heading: Locator = page.locator("#class-detail-heading")
        self.overview: Locator = page.get_by_label("Class overview")
        self.roster: Locator = page.get_by_role("table", name=re.compile(r" students$"))

    def open(self, base_url: str = "http://localhost:5173") -> None:
        self.page.goto(f"{base_url}{self.URL_PATH}", wait_until="domcontentloaded")

    def open_create(self, base_url: str = "http://localhost:5173") -> None:
        self.page.goto(f"{base_url}{self.URL_PATH}/new", wait_until="domcontentloaded")
