"""Black-box UI checks for the 18 scenarios in school-user management."""
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from pages.fs03.school_user_create_page import SchoolUserCreatePage
from pages.fs03.school_user_detail_page import SchoolUserDetailPage
from pages.fs03.school_user_management_page import SchoolUserManagementPage

BASE_URL = "http://localhost:5173"


@pytest.fixture
def listing(page: Page) -> SchoolUserManagementPage:
    view = SchoolUserManagementPage(page)
    view.open(BASE_URL)
    return view


@pytest.fixture
def creation(page: Page) -> SchoolUserCreatePage:
    view = SchoolUserCreatePage(page)
    view.open(BASE_URL)
    return view


def unassigned_detail(listing: SchoolUserManagementPage) -> SchoolUserDetailPage:
    row = listing.table_rows.filter(has_text="Unassigned in any school").first
    expect(row).to_be_visible()
    row.get_by_role("button", name="Detail").click()
    detail = SchoolUserDetailPage(listing.page)
    expect(detail.page_heading).to_be_visible()
    return detail


def fill_valid_user(view: SchoolUserCreatePage, digits: str = "5173001") -> None:
    weights = (2, 7, 6, 5, 4, 3, 2)
    checksum = sum(int(n) * weight for n, weight in zip(digits, weights)) % 11
    nric = f"S{digits}{'JZIHGFEDCBA'[checksum]}"
    view.fill_form(nric, "Automation", "Test", f"automation.{digits}@schools.gov.sg")


def select_rosyth(detail: SchoolUserDetailPage) -> None:
    detail.school_combobox.fill("Rosyth")
    option = detail.page.get_by_role("option", name="Rosyth Primary School")
    expect(option).to_be_visible()
    option.click()


def test_tc_usr_001_assign_school_from_user_detail(listing: SchoolUserManagementPage) -> None:
    detail = unassigned_detail(listing)
    select_rosyth(detail)
    expect(detail.assign_button).to_be_enabled()
    detail.assign_button.click()
    expect(detail.school_card).to_contain_text("Rosyth Primary School")


def test_tc_usr_002_unassigned_user_state_is_visible(listing: SchoolUserManagementPage) -> None:
    detail = unassigned_detail(listing)
    expect(detail.school_card).to_contain_text("This user is not assigned to a school yet.")
    expect(detail.school_combobox).to_be_visible()


def test_tc_usr_003_school_role_cannot_open_admin_user_management(school_role_page: Page) -> None:
    school_role_page.goto(f"{BASE_URL}/school-user-management")
    expect(school_role_page).to_have_url(f"{BASE_URL}/")
    expect(school_role_page.get_by_role("button", name="Create School User")).to_have_count(0)


def test_tc_usr_004_current_admin_cannot_delete_self(listing: SchoolUserManagementPage) -> None:
    expect(listing.table_rows.first.get_by_role("button", name="Deactivate")).to_be_visible()
    expect(listing.table.get_by_role("button", name="Delete")).to_have_count(0)


def test_tc_usr_005_list_columns_and_search_control(listing: SchoolUserManagementPage) -> None:
    expect(listing.page_heading).to_have_text("School user management")
    assert [h.inner_text().strip() for h in listing.table_headers.all()] == [
        "Code", "Username", "Full name", "School", "Status", "Actions"
    ]
    expect(listing.search_input).to_be_visible()


def test_tc_usr_006_single_and_bulk_modes(creation: SchoolUserCreatePage) -> None:
    expect(creation.nric_input).to_be_visible()
    creation.switch_to_bulk_tab()
    expect(creation.file_input).to_be_attached()
    expect(creation.import_button).to_be_disabled()
    creation.switch_to_single_tab()
    expect(creation.first_name_input).to_be_visible()


def test_tc_usr_007_detail_account_profile_school(listing: SchoolUserManagementPage) -> None:
    detail = unassigned_detail(listing)
    expect(detail.account_card).to_contain_text("USR-AUTO-01")
    expect(detail.profile_card).to_contain_text("Test Staff")
    expect(detail.school_card).to_be_visible()


def test_tc_usr_008_csv_template_download(creation: SchoolUserCreatePage) -> None:
    creation.switch_to_bulk_tab()
    with creation.page.expect_download() as event:
        creation.get_template_button.click()
    assert event.value.suggested_filename == "school-users-template.xlsx"


def test_tc_usr_009_required_and_malformed_fields(creation: SchoolUserCreatePage) -> None:
    expect(creation.create_button).to_be_disabled()
    creation.fill_nric("not-an-nric")
    creation.fill_first_name("Test")
    creation.fill_last_name("Staff")
    creation.fill_email("validation.test@example.test")
    creation.click_create()
    expect(creation.page.get_by_text("Validation failed", exact=True)).to_be_visible()
    expect(creation.page).to_have_url(f"{BASE_URL}/school-user-management/new")
    expect(creation.result_card).to_be_hidden()


def test_tc_usr_010_duplicate_user_is_rejected(creation: SchoolUserCreatePage) -> None:
    fill_valid_user(creation)
    creation.fill_email("staff1@IAM.edu.vn")
    creation.click_create()
    expect(creation.alerts.first).to_be_visible()


def test_tc_usr_011_malformed_csv_is_rejected(creation: SchoolUserCreatePage, tmp_path: Path) -> None:
    creation.switch_to_bulk_tab()
    bad = tmp_path / "missing_columns.csv"
    bad.write_text("No,NRIC,First Name,Last Name\n1,S9123451A,John,Doe\n", encoding="utf-8")
    creation.file_input.set_input_files(str(bad))
    creation.import_button.click()
    expect(creation.alerts.first).to_contain_text("Missing CSV column: School User Email")


def test_tc_usr_012_csv_over_limit_is_rejected(creation: SchoolUserCreatePage, tmp_path: Path) -> None:
    creation.switch_to_bulk_tab()
    oversized = tmp_path / "over_limit.csv"
    header = "No,School User NRIC,School User Email,First Name,Last Name,School Code (optional)\n"
    rows = "".join(f"{i},S9123451A,user{i}@example.test,Test,User,RPS-0201\n" for i in range(1, 1002))
    oversized.write_text(header + rows, encoding="utf-8")
    creation.file_input.set_input_files(str(oversized))
    creation.import_button.click()
    expect(creation.alerts.first).to_contain_text("The CSV file may contain at most 1000 rows.")


def test_tc_usr_013_create_user_with_school_assignment(creation: SchoolUserCreatePage) -> None:
    fill_valid_user(creation)
    creation.fill_school_code("RPS-0201")
    creation.click_create()
    expect(creation.result_card).to_be_visible()
    expect(creation.result_card).to_contain_text("Rosyth Primary School")


def test_tc_usr_014_bulk_import_result(creation: SchoolUserCreatePage, tmp_path: Path) -> None:
    creation.switch_to_bulk_tab()
    csv_file = tmp_path / "three_valid.csv"
    csv_file.write_text(
        "No,School User NRIC,School User Email,First Name,Last Name,School Code (optional)\n"
        "1,S9123451A,auto.1@example.test,Auto,One,RPS-0201\n"
        "2,S9123452B,auto.2@example.test,Auto,Two,RPS-0201\n"
        "3,S9123453C,auto.3@example.test,Auto,Three,RPS-0201\n",
        encoding="utf-8",
    )
    creation.file_input.set_input_files(str(csv_file))
    creation.import_button.click()
    expect(creation.import_result_heading).to_be_visible()
    expect(creation.import_result_table.locator("tbody tr")).to_have_count(3)


def test_tc_usr_015_assign_school_and_return_to_list(listing: SchoolUserManagementPage) -> None:
    detail = unassigned_detail(listing)
    select_rosyth(detail)
    detail.assign_button.click()
    expect(detail.school_card).to_contain_text("Rosyth Primary School")
    detail.back_to_list_button.click()
    expect(listing.table_rows.filter(has_text="Test Staff")).to_contain_text("Rosyth Primary School")


def test_tc_usr_016_search_by_username_and_clear(listing: SchoolUserManagementPage) -> None:
    expect(listing.table_rows).to_have_count(2)
    listing.search_input.fill("staff1")
    expect(listing.table_rows).to_have_count(1)
    expect(listing.table_rows.first).to_contain_text("staff1")
    listing.search_input.fill("")
    expect(listing.table_rows).to_have_count(2)


def test_tc_usr_017_partial_csv_line_error(creation: SchoolUserCreatePage, tmp_path: Path) -> None:
    creation.switch_to_bulk_tab()
    csv_file = tmp_path / "partial.csv"
    csv_file.write_text(
        "No,School User NRIC,School User Email,First Name,Last Name,School Code (optional)\n"
        "1,S9123451A,auto.1@example.test,Auto,One,RPS-0201\n"
        "2,S9123452B,auto.2@example.test,Auto,Two,RPS-0201\n"
        "3,INVALID_NRIC,bad@example.test,Bad,User,RPS-0201\n",
        encoding="utf-8",
    )
    creation.file_input.set_input_files(str(csv_file))
    creation.import_button.click()
    expect(creation.import_result_table.locator("tbody tr")).to_have_count(3)
    expect(creation.import_result_table).to_contain_text("NRIC must contain 1 letter, 7 digits, and 1 letter.")


def test_tc_usr_018_delete_cancel_preserves_row(listing: SchoolUserManagementPage) -> None:
    row = listing.table_rows.first
    code = row.locator("td").first.inner_text()
    row.get_by_role("button", name="Deactivate").click()
    dialog = listing.page.get_by_role("dialog", name="Deactivate school user")
    expect(dialog).to_contain_text("This changes the user's ability to sign in immediately.")
    dialog.get_by_role("button", name="Close").click()
    expect(dialog).to_be_hidden()
    expect(listing.table_rows.first.locator("td").first).to_have_text(code)
    expect(listing.table_rows.first).to_contain_text("Active")
