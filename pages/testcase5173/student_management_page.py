"""Student management page object based on the testcase5173 live DOM spec."""
from playwright.sync_api import Locator, Page


class StudentManagementPage:
    BASE_URL = "http://localhost:5173"

    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self, path: str = "/student-management") -> None:
        self.page.goto(f"{self.BASE_URL}{path}", wait_until="domcontentloaded")
        if path.startswith("/student-management/new"):
            heading = "Create a student"
        elif path.startswith("/student-management/enroll"):
            heading = "Enroll a student"
        elif path.startswith("/student-management/assign-in-class"):
            heading = "Assign in class"
        else:
            heading = "Students"
        self.page.get_by_role("heading", name=heading, exact=True).wait_for(state="visible")

    @property
    def search(self) -> Locator:
        return self.page.get_by_role("searchbox", name="Search students")

    @property
    def rows(self) -> Locator:
        return self.page.get_by_role("table", name="Students").locator("tbody tr")

    @property
    def students_table(self) -> Locator:
        return self.page.get_by_role("table", name="Students")

    @property
    def detail_button(self) -> Locator:
        return self.page.get_by_role("button", name="View student detail")

    def open_first_student(self) -> str:
        name = self.rows.first.locator("td").first.inner_text().strip()
        self.rows.first.get_by_role("button", name="View student detail").click()
        return name

    @property
    def create_button(self) -> Locator:
        return self.page.get_by_role("button", name="Create student", exact=True)

    @property
    def name_input(self) -> Locator:
        return self.page.get_by_role("textbox", name="Display name")

    @property
    def nric_input(self) -> Locator:
        return self.page.get_by_role("textbox", name="NRIC")

    @property
    def fin_input(self) -> Locator:
        return self.page.get_by_role("textbox", name="FIN")

    @property
    def dob_input(self) -> Locator:
        return self.page.get_by_label("Date of birth")

    @property
    def category_select(self) -> Locator:
        return self.page.get_by_label("Student citizenship")

    @property
    def enrolled_from_input(self) -> Locator:
        return self.page.get_by_label("Enrollment start")

    @property
    def enrolled_to_input(self) -> Locator:
        return self.page.get_by_label("Enrollment end")

    def fill_student_form(self, student: dict[str, str]) -> None:
        self.name_input.fill(student["display_name"])
        self.category_select.select_option(student["category"])
        if student["category"] in {"SC", "PR"}:
            self.nric_input.fill(student["identifier"])
        else:
            self.fin_input.fill(student["identifier"])
        self.dob_input.fill(student["date_of_birth"])
        self.enrolled_from_input.fill(student["enrolled_from"])
        if student.get("enrolled_to_exclusive"):
            self.enrolled_to_input.fill(student["enrolled_to_exclusive"])
        self.submit_button.click()

    @property
    def submit_button(self) -> Locator:
        return self.page.get_by_role("button", name="Create student", exact=True)

    @property
    def error_summary(self) -> Locator:
        return self.page.locator('[role="alert"]')

    @property
    def submit_assign_btn(self) -> Locator:
        return self.page.get_by_role("button", name="Assign in class")

    @property
    def assign_class_combo(self) -> Locator:
        return self.page.get_by_role("combobox", name="Class")

    @property
    def enroll_student_input(self) -> Locator:
        return self.page.get_by_role("textbox", name="Student ID")

    @property
    def enroll_school_combo(self) -> Locator:
        return self.page.get_by_role("combobox", name="School")

    @property
    def enroll_submit_button(self) -> Locator:
        return self.page.get_by_role("button", name="Enroll student")

    @property
    def assigned_from_input(self) -> Locator:
        return self.page.get_by_label("Assignment start")

    @property
    def assigned_to_input(self) -> Locator:
        return self.page.get_by_label("Assignment end")

    @property
    def class_search_input(self) -> Locator:
        return self.page.get_by_role("combobox", name="Class")


class SchoolConfigManagementPage:
    """School configuration page object based on its BSK selectors."""

    BASE_URL = "http://localhost:5173"

    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> None:
        self.page.goto(f"{self.BASE_URL}/school-config", wait_until="domcontentloaded")

    @property
    def year_select(self) -> Locator:
        return self.page.get_by_label("Academic year", exact=True)

    @property
    def school_heading(self) -> Locator:
        return self.page.locator('article:has(button:has-text("Add Academic Levels")) h2')

    @property
    def school_code(self) -> Locator:
        return self.page.locator('article:has(button:has-text("Add Academic Levels")) p:has-text("School code:")')

    @property
    def status_badge(self) -> Locator:
        return self.page.locator('article:has(button:has-text("Add Academic Levels")) div:has(> div > select) > span')

    @property
    def add_levels_button(self) -> Locator:
        return self.page.get_by_role("button", name="Add Academic Levels")

    @property
    def copy_year_button(self) -> Locator:
        return self.page.get_by_role("button", name="Copy Previous Year")

    @property
    def add_class_button(self) -> Locator:
        return self.page.get_by_role("button", name="Add Class")

    @property
    def dialog(self) -> Locator:
        return self.page.locator('[role="dialog"]')

    @property
    def search_level(self) -> Locator:
        return self.page.get_by_role("textbox", name="Search academic levels")
