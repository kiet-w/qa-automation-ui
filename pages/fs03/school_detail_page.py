"""
pages/fs03/school_detail_page.py - Page Object for FS03 School detail (/school-management/:schoolId).
Source: 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5173/academic-and-users/03_school_management.md §1.3.
Complies with Invariant 1 (zero assertions in Page Objects).
"""
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage
from pages.fs03.locators import SchoolDetailLocators as L


class SchoolDetailPage(BasePage):
    """POM for the school detail screen reached from the directory Detail action."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.back_link: Locator = page.locator(L.BACK_LINK)
        self.status_badge: Locator = page.locator(L.STATUS_BADGE)
        self.overview_section: Locator = page.locator(L.OVERVIEW_SECTION)
        self.students_table: Locator = page.locator(L.STUDENTS_TABLE)

    def wait_loaded(self, timeout: int = 10000) -> None:
        """Wait until the detail shell (Back link) is rendered."""
        self.back_link.wait_for(state="visible", timeout=timeout)

    def get_status_text(self) -> str:
        return self.status_badge.first.inner_text().strip() if self.status_badge.count() else ""

    def is_overview_visible(self) -> bool:
        return self.overview_section.first.is_visible()

    def get_overview_text(self) -> str:
        return self.overview_section.first.inner_text().strip() if self.is_overview_visible() else ""

    def is_students_table_visible(self) -> bool:
        return self.students_table.first.is_visible()

    def get_students_table_text(self) -> str:
        return self.students_table.first.inner_text().strip() if self.is_students_table_visible() else ""

    def click_back_to_list(self) -> None:
        self.back_link.click()
