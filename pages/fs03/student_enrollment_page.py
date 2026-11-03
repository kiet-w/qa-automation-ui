"""
pages/fs03/student_enrollment_page.py - Page Object for FS03 Student Management & Enrollment screen.
Complies with Invariant 1 (UI actions & state reading only, ZERO assertions) and Invariant 9 (<250 lines).
"""
from typing import List, Optional
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class StudentEnrollmentPage(BasePage):
    """POM for Student Management & Enrollment screens (/student-management)."""

    URL_PATH = "/student-management"

    def __init__(self, page: Page):
        super().__init__(page)
        # Search & Directory Toolbar
        self.search_input: Locator = page.get_by_role("searchbox", name="Search students")
        self.create_student_btn: Locator = page.get_by_role("button", name="Create student", exact=True)
        self.table_headers: Locator = page.get_by_role("table", name="Students").locator("thead th")
        self.table_rows: Locator = page.get_by_role("table", name="Students").locator("tbody tr")
        self.empty_state_msg: Locator = page.get_by_text("No students found")

        # Create Student Form fields
        self.name_input: Locator = page.locator("#student-displayName")
        self.nric_input: Locator = page.locator("#student-nric")
        self.fin_input: Locator = page.locator("#student-fin")
        self.dob_input: Locator = page.locator("#student-dateOfBirth")
        self.category_select: Locator = page.locator("#student-category")
        self.school_assigned_checkbox: Locator = page.locator("#student-isSchoolAssigned")
        self.school_select: Locator = page.locator("#student-schoolId")
        self.enrolled_from_input: Locator = page.locator("#student-enrolledFrom")
        self.enrolled_to_input: Locator = page.locator("#student-enrolledToExclusive")
        self.submit_btn: Locator = page.locator('form button:has-text("Create student")')
        self.cancel_btn: Locator = page.get_by_role("button", name="Cancel")

        # Student Detail & Actions
        self.student_detail_heading: Locator = page.locator("#student-detail-heading")
        self.detail_eyebrow: Locator = page.locator('main p:has-text("Student profile and school enrollment history.")')
        self.assign_class_btn: Locator = page.get_by_role("button", name="Chuyển lớp")
        self.enroll_btn: Locator = page.get_by_role("button", name="Enroll")

        # Class Assignment Form
        self.assign_class_select: Locator = page.locator("#assign-classId, select[name='classId']")
        self.assigned_from_input: Locator = page.locator("#assign-assignedFrom, input[name='assignedFrom']")
        self.assigned_to_input: Locator = page.locator("#assign-assignedToExclusive, input[name='assignedToExclusive']")
        self.submit_assign_btn: Locator = page.locator('button[type="submit"]:has-text("Assign in class"), button:has-text("Save assignment")')

        # Errors & Validation Alerts
        self.error_summary: Locator = page.locator("[role='alert']")
        self.inline_errors: Locator = page.locator("[aria-invalid='true']")

    def open(self, base_url: str = "http://localhost:5173") -> None:
        """Navigate to the student management listing page."""
        self.page.goto(f"{base_url}{self.URL_PATH}", wait_until="domcontentloaded")

    def search_student(self, keyword: str) -> None:
        """Type query into search input."""
        self.search_input.fill(keyword)

    def clear_search(self) -> None:
        """Clear search input."""
        self.search_input.fill("")

    def click_create_student(self) -> None:
        """Click Create student button."""
        self.create_student_btn.click()

    def fill_create_form(
        self,
        name: str,
        nric: Optional[str] = None,
        fin: Optional[str] = None,
        dob: Optional[str] = None,
        category: Optional[str] = None,
    ) -> None:
        """Fill student creation form with citizen NRIC or foreign FIN."""
        if name:
            self.name_input.fill(name)
        if category:
            self.category_select.select_option(category)
        if nric and self.nric_input.is_visible():
            self.nric_input.fill(nric)
        if fin and self.fin_input.is_visible():
            self.fin_input.fill(fin)
        if dob:
            self.dob_input.fill(dob)

    def submit_create(self) -> None:
        """Submit the create student form."""
        self.submit_btn.click()

    def click_view_detail(self, row_index: int = 0) -> None:
        """Click view student detail action on a table row."""
        self.table_rows.nth(row_index).get_by_role("button", name="View student detail").click()

    def get_table_headers(self) -> List[str]:
        """Return list of text for all table headers."""
        return self.table_headers.all_text_contents()

    def get_row_count(self) -> int:
        """Return number of displayed student rows."""
        return self.table_rows.count()

    def is_assign_class_disabled(self) -> bool:
        """Check if assign class button is disabled (due to existing active assignment)."""
        return self.assign_class_btn.is_disabled()

    def fill_class_assignment(
        self,
        class_id: str,
        assigned_from: str,
        assigned_to: Optional[str] = None,
    ) -> None:
        """Fill class assignment form."""
        if class_id:
            self.assign_class_select.select_option(class_id)
        if assigned_from:
            self.assigned_from_input.fill(assigned_from)
        if assigned_to:
            self.assigned_to_input.fill(assigned_to)

    def submit_assignment(self) -> None:
        """Submit class assignment."""
        self.submit_assign_btn.click()
