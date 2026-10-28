"""
pages/fs03/student_enrollment_page.py - Page Object for FS03 Student Management & Enrollment screen.
Complies with Invariant 1 (UI actions & state reading only) and Invariant 9 (<250 lines).
"""
from typing import Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class StudentEnrollmentPage(BasePage):
    """POM for Student Management & Enrollment screens (/student-management)."""

    URL_PATH = "/student-management"

    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input: Locator = page.locator('input[placeholder*="Search students" i], input[aria-label="Search students"]')
        self.create_student_btn: Locator = page.locator('button:has-text("Create student")')
        self.table_headers: Locator = page.locator("table thead th")
        self.table_rows: Locator = page.locator("table tbody tr")

        # Create Student Form fields
        self.name_input: Locator = page.locator("#student-displayName")
        self.nric_input: Locator = page.locator("#student-nric")
        self.dob_input: Locator = page.locator("#student-dateOfBirth")
        self.submit_btn: Locator = page.locator('button[type="submit"]:has-text("Create student")')

    def open(self, base_url: str = "http://localhost:5173") -> None:
        self.page.goto(f"{base_url}{self.URL_PATH}", wait_until="domcontentloaded")
