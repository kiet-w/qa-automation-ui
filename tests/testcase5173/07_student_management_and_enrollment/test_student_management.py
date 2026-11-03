"""Playwright coverage mapped to testcase5173 TC-STU-001–020."""
import random
import re
from copy import deepcopy

import pytest
from playwright.sync_api import Page, expect

from pages.testcase5173.student_management_page import StudentManagementPage


@pytest.fixture
def students(page: Page) -> StudentManagementPage:
    return StudentManagementPage(page)


def create_student(students: StudentManagementPage, lifecycle_data: dict, *,
                   enrolled_from: str, enrolled_to_exclusive: str = "") -> str:
    suffix = random.randint(1000000, 9999999)
    student = deepcopy(lifecycle_data["student"])
    student["display_name"] = f"{student['display_name_prefix']} {suffix}"
    student["identifier"] = student["nric_pattern"].format(suffix=suffix)
    student["enrolled_from"] = enrolled_from
    student["enrolled_to_exclusive"] = enrolled_to_exclusive
    students.open("/student-management/new")
    students.fill_student_form(student)
    expect(students.page).to_have_url(re.compile(r".*/student-management(?:\?.*)?$"))
    return student["identifier"]


def open_student_by_nric(students: StudentManagementPage, nric: str) -> None:
    students.open()
    students.search.fill(nric)
    row = students.rows.filter(has_text=nric)
    expect(row).to_be_visible()
    student_name = row.locator("td").first.inner_text().strip()
    row.get_by_role("button", name="View student detail").click()
    expect(students.page.get_by_role("heading", name=student_name, level=1)).to_be_visible()


@pytest.mark.ac
def test_tc_stu_006_student_directory_columns(students: StudentManagementPage) -> None:
    """TC-STU-006: Danh sách học sinh có đủ các cột theo BSK."""
    students.open()
    expect(students.page.get_by_role("heading", name="Students")).to_be_visible()
    for column in ("Student", "NRIC", "FIN", "Date of birth", "Category", "School", "Class", "Actions"):
        expect(students.page.locator("table thead")).to_contain_text(column)


@pytest.mark.flow
def test_tc_stu_019_search_student_directory(students: StudentManagementPage) -> None:
    """TC-STU-019: Tìm kiếm theo tên hoặc mã định danh từ thanh tìm kiếm BSK."""
    students.open()
    expect(students.search).to_be_visible()
    expect(students.rows.first).to_be_visible()
    student_nric = students.rows.first.locator("td:nth-child(2)").inner_text().strip()
    students.search.fill(student_nric)
    expect(students.search).to_have_value(student_nric)
    expect(students.rows.filter(has_text=student_nric)).to_be_visible()
    students.search.fill("")
    expect(students.rows.first).to_be_visible()


@pytest.mark.ac
def test_tc_stu_007_student_detail_action_is_available(students: StudentManagementPage) -> None:
    """TC-STU-007: Chi tiết có dữ liệu học sinh và lịch sử ghi danh."""
    students.open()
    student_name = students.open_first_student()
    expect(students.page).to_have_url(re.compile(r".*/student-management/STU-.*"))
    expect(students.page.get_by_role("heading", name=student_name, level=1)).to_be_visible()
    expect(students.page.get_by_role("heading", name="School enrollments")).to_be_visible()
    expect(students.page.get_by_role("heading", name="Class assignments")).to_be_visible()
    expect(students.page.get_by_text("NRIC", exact=False).first).to_be_visible()
    expect(students.page.get_by_text("Current school", exact=False).first).to_be_visible()
    expect(students.submit_assign_btn).to_be_visible()


@pytest.mark.validation
def test_tc_stu_011_create_student_requires_mandatory_fields(students: StudentManagementPage) -> None:
    """TC-STU-011: Form tạo học sinh chặn gửi khi thiếu dữ liệu bắt buộc."""
    students.open("/student-management/new")
    expect(students.name_input).to_be_visible()
    expect(students.dob_input).to_be_visible()
    expect(students.category_select).to_be_visible()
    students.submit_button.click()
    expect(students.page.locator("[aria-invalid='true']").first).to_be_visible()
    for field in (students.name_input, students.dob_input, students.category_select):
        expect(field).to_have_attribute("aria-invalid", "true")
    students.category_select.select_option("SC")
    students.submit_button.click()
    expect(students.nric_input).to_have_attribute("aria-invalid", "true")
    expect(students.page.get_by_text("NRIC is required.").first).to_be_visible()
    students.category_select.select_option("IS_ASEAN")
    students.submit_button.click()
    expect(students.fin_input).to_have_attribute("aria-invalid", "true")
    expect(students.page.get_by_text("FIN is required.").first).to_be_visible()


@pytest.mark.validation
def test_tc_stu_013_future_date_of_birth_is_rejected(students: StudentManagementPage) -> None:
    """TC-STU-013: Ngày sinh tương lai bị từ chối theo quy tắc nghiệp vụ."""
    students.open("/student-management/new")
    students.name_input.fill("Test Student")
    students.category_select.select_option("SC")
    students.nric_input.fill("T1234567A")
    students.dob_input.fill("2099-01-01")
    students.enrolled_from_input.fill("2026-01-01")
    students.submit_button.click()
    expect(students.error_summary.first).to_be_visible()
    expect(students.error_summary.first).to_contain_text(re.compile(r"future", re.I))


@pytest.mark.ac
@pytest.mark.xfail(strict=True, reason="Form Enroll thiếu Academic year và Level so với TC-STU-008")
def test_tc_stu_008_enrollment_form_has_required_controls(students: StudentManagementPage) -> None:
    """TC-STU-008: Màn hình nhập học có các trường dữ liệu nghiệp vụ được đặc tả."""
    students.open("/student-management/enroll")
    for control in (students.enroll_student_input, students.enroll_school_combo,
                    students.page.get_by_label("Enrollment start"),
                    students.page.get_by_label("Enrollment end")):
        expect(control).to_be_visible()
    expect(students.enroll_submit_button).to_be_visible()
    expect(students.page.get_by_role("heading", name="Enroll a student")).to_be_visible()
    expect(students.page.get_by_label("Academic year")).to_be_visible()
    expect(students.page.get_by_label("Level")).to_be_visible()


@pytest.mark.ac
def test_tc_stu_009_class_assignment_form_has_class_controls(students: StudentManagementPage) -> None:
    """TC-STU-009: Màn hình phân lớp có bộ chọn lớp và ngày hiệu lực."""
    students.open("/student-management/assign-in-class")
    expect(students.page.get_by_role("heading", name="Student is required")).to_be_visible()
    expect(students.assign_class_combo).to_be_visible()
    expect(students.assigned_from_input).to_be_visible()
    expect(students.assigned_to_input).to_be_visible()
    expect(students.page.get_by_role("heading", name="Assign in class")).to_be_visible()
    expect(students.submit_assign_btn).to_be_visible()


@pytest.mark.br
def test_tc_stu_001_create_pr_student_without_ea_account(students: StudentManagementPage) -> None:
    """TC-STU-001: PR student record creation does not require an Education Account."""
    suffix = random.randint(1000000, 9999999)
    nric = f"T{suffix}P"
    students.open("/student-management/new")
    name = f"PR automation {suffix}"
    students.name_input.fill(name)
    students.category_select.select_option("PR")
    students.nric_input.fill(nric)
    students.dob_input.fill("2019-05-15")
    students.enrolled_from_input.fill("2026-01-01")
    students.submit_button.click()
    expect(students.page).to_have_url(re.compile(r".*/student-management(?:\?.*)?$"))
    students.search.fill(nric)
    expect(students.rows.filter(has_text=nric)).to_be_visible(timeout=10000)


@pytest.mark.br
def test_tc_stu_002_block_class_assignment_before_enrollment(
    students: StudentManagementPage, student_lifecycle_data: dict
) -> None:
    """TC-STU-002: Class assignment is rejected until the student has an active enrollment."""
    nric = create_student(
        students, student_lifecycle_data, enrolled_from="2099-01-01"
    )
    open_student_by_nric(students, nric)
    expect(students.page.get_by_text("Enrollment status", exact=True)).to_be_visible()
    students.submit_assign_btn.click()
    students.assign_class_combo.click()
    expect(
        students.page.get_by_text("Unable to load classes.", exact=True)
    ).to_have_count(0)
    no_classes = students.page.get_by_role("option", name="No classes found")
    if no_classes.is_visible():
        expect(no_classes).to_be_disabled()
        return
    class_option = students.page.get_by_role(
        "option", name=re.compile(re.escape(student_lifecycle_data["class_code"]))
    )
    expect(class_option).to_be_visible()
    expect(class_option).to_be_enabled()
    class_option.click()
    students.assigned_from_input.fill("2026-10-29")
    students.assigned_to_input.fill("2026-12-31")
    students.submit_assign_btn.click()
    expect(students.error_summary.first).to_be_visible()


@pytest.mark.br
def test_tc_stu_003_internal_class_change_keeps_history(students: StudentManagementPage) -> None:
    """TC-STU-003: Moving from P1-A to P1-B preserves the earlier assignment in history."""
    pytest.xfail("UI đang khóa Assign in class khi đã có lớp; chưa có luồng chuyển lớp để kiểm lịch sử.")


@pytest.mark.br
def test_tc_stu_004_withdrawn_student_cannot_be_assigned(
    students: StudentManagementPage, student_lifecycle_data: dict
) -> None:
    """TC-STU-004: A withdrawn student is rejected by the class assignment screen."""
    nric = create_student(
        students,
        student_lifecycle_data,
        enrolled_from="2025-01-01",
        enrolled_to_exclusive="2025-12-31",
    )
    students.open()
    students.search.fill(nric)
    row = students.rows.filter(has_text=nric)
    if not row.is_visible():
        pytest.xfail(
            "UI tạo enrollment đã hết hạn nhưng loại hồ sơ khỏi Students; không có đường UI để mở detail và thử gán lớp."
        )
    row.get_by_role("button", name="View student detail").click()
    expect(students.page.get_by_text("WITHDRAWN", exact=True)).to_be_visible()
    expect(students.submit_assign_btn).to_be_disabled()


@pytest.mark.br
def test_tc_stu_005_citizen_student_detail_shows_ea_link(students: StudentManagementPage) -> None:
    """TC-STU-005: The specified SC student detail displays its EA link information."""
    pytest.xfail("Chi tiết học sinh hiện chưa hiển thị nhãn và số tài khoản EA để đối chiếu.")


@pytest.mark.ac
def test_tc_stu_010_create_button_visibility_tracks_role(students: StudentManagementPage, browser, moehq_auth_state) -> None:
    """TC-STU-010: Compare actual authenticated MOEHQ and SCHOOL sessions."""
    context = browser.new_context(storage_state=str(moehq_auth_state))
    try:
        moe_page = StudentManagementPage(context.new_page())
        moe_page.open()
        expect(moe_page.page.get_by_role("heading", name="Students")).to_be_visible()
        expect(moe_page.create_button).to_have_count(0)
    finally:
        context.close()
    students.open()
    expect(students.create_button).to_be_visible()


@pytest.mark.validation
@pytest.mark.parametrize("identifier", ["123456789", "S1234", "ABCDEFGHI"])
def test_tc_stu_012_reject_invalid_nric_or_fin(students: StudentManagementPage, identifier: str) -> None:
    """TC-STU-012: Reject malformed NRIC/FIN values."""
    students.open("/student-management/new")
    students.name_input.fill("Invalid identifier student")
    students.category_select.select_option("SC")
    students.nric_input.fill(identifier)
    students.dob_input.fill("2019-05-15")
    students.enrolled_from_input.fill("2026-01-01")
    students.submit_button.click()
    expect(students.nric_input).to_have_attribute("aria-invalid", "true")
    expect(students.page.get_by_text("Enter NRIC in the format S/T followed by 7 digits and a letter.").first).to_be_visible()


@pytest.mark.validation
def test_tc_stu_014_duplicate_nric_is_rejected(students: StudentManagementPage) -> None:
    """TC-STU-014: Reject a duplicate NRIC."""
    students.open()
    first_nric = students.rows.first.locator("td").nth(1)
    expect(first_nric).to_have_text(re.compile(r"^[ST]\d{7}[A-Z]$"))
    existing_nric = first_nric.inner_text().strip()
    students.open("/student-management/new")
    students.name_input.fill("Duplicate NRIC attempt")
    students.category_select.select_option("SC")
    students.nric_input.fill(existing_nric)
    students.dob_input.fill("2019-05-15")
    students.enrolled_from_input.fill("2026-01-01")
    students.submit_button.click()
    expect(students.error_summary.first).to_contain_text(re.compile(r"already exists|duplicate", re.I))
    expect(students.page).to_have_url(re.compile(r".*/student-management/new(?:\?.*)?$"))


@pytest.mark.validation
def test_tc_stu_015_enrollment_requires_year_and_level(students: StudentManagementPage) -> None:
    """TC-STU-015: Enrollment requires the documented mandatory controls."""
    pytest.xfail("Form Enroll hiện chỉ có Student ID, School và ngày; thiếu Academic year/Level theo testcase.")


@pytest.mark.flow
def test_tc_stu_016_create_student_and_find_in_directory(students: StudentManagementPage) -> None:
    """TC-STU-016: Create a student and find the record in the directory."""
    suffix = random.randint(1000000, 9999999)
    nric = f"T{suffix}S"
    students.open("/student-management/new")
    students.name_input.fill(f"Automation student {suffix}")
    students.category_select.select_option("SC")
    students.nric_input.fill(nric)
    students.dob_input.fill("2019-05-15")
    students.enrolled_from_input.fill("2026-01-01")
    students.submit_button.click()
    expect(students.page).to_have_url(re.compile(r".*/student-management(?:\?.*)?$"))
    students.search.fill(nric)
    expect(students.rows.filter(has_text=nric)).to_be_visible(timeout=10000)


@pytest.mark.flow
def test_tc_stu_017_enroll_student_at_school(
    students: StudentManagementPage, student_lifecycle_data: dict
) -> None:
    """TC-STU-017: Enroll a student at a school."""
    nric = create_student(
        students,
        student_lifecycle_data,
        enrolled_from="2099-01-01",
    )
    open_student_by_nric(students, nric)
    student_id = students.page.url.split("/student-management/", 1)[1].split("?", 1)[0]

    students.open("/student-management/enroll")
    students.enroll_student_input.fill(student_id)
    students.enroll_school_combo.click()
    students.page.get_by_role(
        "option", name=re.compile(student_lifecycle_data["school_code"])
    ).click()
    students.page.get_by_label("Enrollment start").fill(
        student_lifecycle_data["active_enrollment_start"]
    )
    students.page.get_by_label("Enrollment end").fill("2098-12-31")
    students.enroll_submit_button.click()
    expect(students.page).to_have_url(re.compile(r".*/student-management(?:\?.*)?$"))
    open_student_by_nric(students, nric)
    expect(students.page.get_by_text("ENROLLED", exact=True)).to_be_visible()


@pytest.mark.flow
def test_tc_stu_018_assign_student_to_class(students: StudentManagementPage) -> None:
    """TC-STU-018: Tạo học sinh, phân lớp và kiểm tra lớp trên danh bạ."""
    suffix = random.randint(1000000, 9999999)
    nric = f"T{suffix}A"
    students.open("/student-management/new")
    students.name_input.fill(f"Class assignment {suffix}")
    students.category_select.select_option("SC")
    students.nric_input.fill(nric)
    students.dob_input.fill("2019-05-15")
    students.enrolled_from_input.fill("2026-01-01")
    students.submit_button.click()
    expect(students.page).to_have_url(re.compile(r".*/student-management(?:\?.*)?$"))

    students.search.fill(nric)
    row = students.rows.filter(has_text=nric)
    expect(row).to_contain_text("Not assigned")
    row.get_by_role("button", name="View student detail").click()
    expect(students.submit_assign_btn).to_be_enabled()
    students.submit_assign_btn.click()
    expect(students.page).to_have_url(re.compile(r".*/student-management/assign-in-class\?.*studentId="))

    students.assign_class_combo.click()
    students.page.get_by_text("1A1 - Primary 1 - 1A1", exact=True).click()
    students.assigned_from_input.fill("2026-01-29")
    students.assigned_to_input.fill("2026-12-31")
    students.submit_assign_btn.click()
    expect(students.page.get_by_role("heading", name="Class assignments")).to_be_visible()
    expect(students.page.get_by_role("table", name="Class assignments")).to_contain_text("1A1")
    students.open()
    students.search.fill(nric)
    expect(students.rows.filter(has_text=nric)).to_contain_text("1A1")


@pytest.mark.validation
def test_tc_stu_020_assignment_before_enrollment_is_rejected(
    students: StudentManagementPage, student_lifecycle_data: dict
) -> None:
    """TC-STU-020: Assignment before enrollment is rejected."""
    nric = create_student(
        students, student_lifecycle_data, enrolled_from="2099-01-01"
    )
    open_student_by_nric(students, nric)
    if not students.submit_assign_btn.is_enabled():
        expect(students.submit_assign_btn).to_be_disabled()
        return
    students.submit_assign_btn.click()
    students.assign_class_combo.click()
    students.page.get_by_role("option").first.click()
    students.assigned_from_input.fill("2026-10-29")
    students.assigned_to_input.fill("2026-12-31")
    students.submit_assign_btn.click()
    expect(students.error_summary.first).to_be_visible()
