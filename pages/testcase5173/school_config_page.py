"""UI actions and visible state for school configuration (TC-CFG)."""

import re

from playwright.sync_api import Locator, Page


class SchoolConfigPage:
    URL = "http://localhost:5173/school-config"

    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> None:
        self.page.goto(self.URL, wait_until="domcontentloaded")

    @property
    def year(self) -> Locator:
        return self.page.get_by_label("Academic year", exact=True)

    def choose_year(self, year: str) -> None:
        self.year.select_option(label=year)

    @property
    def heading(self) -> Locator:
        return self.page.get_by_role("heading", name="School configuration", level=1)

    @property
    def school_header(self) -> Locator:
        return self.page.locator("article").filter(has=self.add_levels)

    @property
    def add_levels(self) -> Locator:
        return self.page.get_by_role("button", name="Add Academic Levels", exact=True)

    @property
    def copy_previous_year(self) -> Locator:
        return self.page.get_by_role("button", name="Copy Previous Year", exact=True)

    def level(self, code: str) -> Locator:
        return self.page.get_by_role("button", name=re.compile(rf"^{re.escape(code)}\s"))

    def select_level(self, code: str) -> None:
        self.level(code).click()

    @property
    def level_detail(self) -> Locator:
        return self.page.get_by_role("heading", name="PRI-1 · Primary 1", level=2)

    @property
    def class_table(self) -> Locator:
        return self.page.get_by_role("table")

    @property
    def add_class(self) -> Locator:
        return self.page.get_by_role("button", name="Add Class", exact=True)

    def stage(self, name: str) -> Locator:
        return self.page.get_by_role("tab", name=name, exact=True)

    def open_add_levels(self) -> Locator:
        self.add_levels.click()
        return self.page.get_by_role("dialog", name="Add academic levels")

    def open_copy(self) -> Locator:
        self.copy_previous_year.click()
        return self.page.get_by_role("dialog", name="Copy previous year")
