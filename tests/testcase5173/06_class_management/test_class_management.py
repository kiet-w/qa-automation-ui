"""Playwright cases mapped one-to-one to testcase5173 TC-CLS-001–018.

Uses the existing ClassManagementPage POM and selectors from the verified BSK
spec. No assertions are placed in page objects.
"""
import re
from time import time_ns

import pytest
from playwright.sync_api import Page, expect

from pages.fs03.class_management_page import ClassManagementPage

BASE_URL = "http://localhost:5173"
ROWS = "table tbody tr"
OFFERING = "#class-schoolLevelOffering"


def require_route_and_school_identity(page: Page, path: str) -> None:
    heading = page.locator("main h1")
    heading.wait_for(state="visible", timeout=10000)
    rendered_heading = heading.inner_text().strip()
    if rendered_heading == "404 - Page Not Found":
        raise AssertionError(f"SCHOOL-authenticated user received the application's 404 at {path}.")
    expect(page.get_by_role("banner").get_by_text("school", exact=True)).to_be_visible()


def class_page(page: Page) -> ClassManagementPage:
    result = ClassManagementPage(page)
    result.open(BASE_URL)
    require_route_and_school_identity(page, "/class-management")
    expect(page.get_by_role("heading", name="Class Management")).to_be_visible()
    return result


def create_page(page: Page) -> ClassManagementPage:
    result = ClassManagementPage(page)
    result.open_create(BASE_URL)
    require_route_and_school_identity(page, "/class-management/new")
    expect(page.get_by_role("heading", name="Create a class")).to_be_visible()
    return result


def select_first_offering(page: Page) -> None:
    combo = page.locator(OFFERING)
    combo.fill("Primary 1")
    option = page.get_by_role("option", name=re.compile(r"Primary 1 · 2026 · "))
    expect(option).to_be_visible()
    option.click()


# TC-CLS-001
def test_tc_cls_001_only_school_approved_levels_are_selectable(page: Page) -> None:
    create_page(page)
    combo = page.locator(OFFERING)
    combo.fill("Secondary 1")
    expect(page.get_by_role("option", name="No school level offerings found")).to_be_disabled()
    combo.fill("Primary")
    options = page.get_by_role("option")
    expect(options.first).to_be_visible()
    for option in options.all():
        assert "Secondary" not in option.inner_text()


# TC-CLS-002
def test_tc_cls_002_duplicate_class_code_is_rejected(page: Page) -> None:
    pom = create_page(page)
    pom.class_code_input.fill("1A1")
    pom.class_name_input.fill("Duplicate class attempt")
    select_first_offering(page)
    pom.submit_btn.click()
    expect(pom.create_error).to_be_visible()
    expect(page.get_by_text("Class code '1A1' already exists for this offering.")).to_be_visible()
    expect(page).to_have_url(re.compile(r"/class-management/new$"))


# TC-CLS-003
def test_tc_cls_003_school_user_can_open_scoped_class_management(page: Page) -> None:
    pom = class_page(page)
    # The module-local browser context is sourced from the shared SCHOOL SSO fixture.
    expect(page.get_by_role("banner").get_by_text("school", exact=True)).to_be_visible()
    expect(page.get_by_role("button", name="Create class")).to_be_visible()
    expect(pom.table_rows.first).to_be_visible()


# TC-CLS-004
def test_tc_cls_004_class_with_students_has_no_delete_action(page: Page) -> None:
    class_page(page)
    row = None
    for candidate in page.locator(ROWS).all():
        active_students = candidate.locator("td:nth-child(6)").inner_text().strip()
        if active_students.isdigit() and int(active_students) > 0:
            row = candidate
            break
    assert row is not None, "The school class list must contain a class with active students."
    row.get_by_role("button", name="Detail").click()
    expect(page.locator("#class-detail-heading")).to_be_visible()
    expect(page.get_by_role("button", name="Delete")).to_have_count(0)


# TC-CLS-005
def test_tc_cls_005_class_list_columns_and_title(page: Page) -> None:
    class_page(page)
    headers = [header.strip() for header in page.get_by_role("table", name="Classes table").locator("thead th").all_inner_texts()]
    for header in ("Class code", "Class name", "Academic level", "Academic year", "Enrolled students", "Active students", "Actions"):
        assert header in headers
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()


# TC-CLS-006
def test_tc_cls_006_class_detail_displays_student_roster(page: Page) -> None:
    class_page(page)
    page.locator(f'{ROWS} button:has-text("Detail")').first.click()
    expect(page.locator("#class-detail-heading")).to_be_visible()
    expect(page.get_by_label("Class overview")).to_be_visible()
    roster = page.get_by_role("table", name=re.compile(r" students$"))
    expect(roster).to_be_visible()
    headers = roster.locator("thead").inner_text()
    for header in ("Student", "Assigned from", "Assigned to", "Status"):
        assert header in headers


# TC-CLS-007
def test_tc_cls_007_search_and_filters_are_available(page: Page) -> None:
    class_page(page)
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    expect(page.locator("#class-filter-academic-level")).to_be_visible()
    expect(page.locator("#class-filter-academic-year")).to_be_visible()
    expect(page.get_by_role("button", name="Search")).to_be_visible()
    expect(page.get_by_role("button", name="Reset filters")).to_be_visible()
    expect(page.get_by_role("button", name="Reset filters")).to_be_disabled()


# TC-CLS-008
def test_tc_cls_008_create_form_loads_school_level_offerings(page: Page) -> None:
    pom = create_page(page)
    expect(page.locator("#class-classCode")).to_be_visible()
    expect(page.locator("#class-className")).to_be_visible()
    expect(page.locator(OFFERING)).to_be_visible()
    # BSK specifies one combined Level Offering (level plus academic year) combobox,
    # not separate Year and Level dropdowns as the matrix wording suggests.
    pom.offering_combobox.click()
    expect(page.get_by_role("option", name=re.compile(r"Primary 1 · 2026 · "))).to_be_visible()


# TC-CLS-009
def test_tc_cls_009_class_code_name_and_offering_are_required(page: Page) -> None:
    pom = create_page(page)
    pom.submit_btn.click()
    for selector in ("#class-classCode", "#class-className", OFFERING):
        expect(page.locator(selector)).to_have_attribute("aria-invalid", "true")
    for message in ("Class code is required.", "Class name is required.", "Select a school level offering."):
        expect(page.get_by_text(message, exact=True).last).to_be_visible()
    expect(page).to_have_url(re.compile(r"/class-management/new$"))


# TC-CLS-010
def test_tc_cls_010_trims_class_code_edges_on_create(page: Page) -> None:
    pom = create_page(page)
    suffix = str(time_ns())[-9:]
    class_code = f"P1TRIM-{suffix}"
    pom.class_code_input.fill(f"  {class_code}  ")
    pom.class_name_input.fill(f"Trimmed class {suffix}")
    select_first_offering(page)
    pom.submit_btn.click()
    expect(page).to_have_url(re.compile(r"/class-management$"))
    pom.search_input.fill(class_code)
    pom.search_button.click()
    row = page.locator(ROWS).filter(has_text=class_code)
    expect(row).to_be_visible()
    expect(row.locator("td").first).to_have_text(class_code)


# TC-CLS-011
def test_tc_cls_011_duplicate_class_code_in_year_is_rejected(page: Page) -> None:
    pom = create_page(page)
    pom.class_code_input.fill("1A1")
    pom.class_name_input.fill("Duplicate class attempt")
    select_first_offering(page)
    pom.submit_btn.click()
    expect(page.get_by_text("Class code '1A1' already exists for this offering.")).to_be_visible()
    expect(page).to_have_url(re.compile(r"/class-management/new$"))


# TC-CLS-012
def test_tc_cls_012_valid_edit_clears_field_validation_state(page: Page) -> None:
    pom = create_page(page)
    pom.submit_btn.click()
    expect(pom.class_name_input).to_have_attribute("aria-invalid", "true")
    pom.class_name_input.fill("Primary 1 A")
    expect(pom.class_name_input).not_to_have_attribute("aria-invalid", "true")


# TC-CLS-013
def test_tc_cls_013_create_class_and_find_it_in_list(page: Page) -> None:
    pom = create_page(page)
    suffix = str(time_ns())[-9:]
    class_code = f"A{suffix}"
    class_name = f"Automation class {suffix}"
    pom.class_code_input.fill(class_code)
    pom.class_name_input.fill(class_name)
    select_first_offering(page)
    pom.submit_btn.click()
    expect(page).to_have_url(re.compile(r"/class-management$"))
    pom.search_input.fill(class_code)
    pom.search_button.click()
    row = page.locator(ROWS).filter(has_text=class_code)
    expect(row).to_be_visible()
    expect(row.locator("td:nth-child(5)")).to_have_text("0")
    expect(row.locator("td:nth-child(6)")).to_have_text("0")


# TC-CLS-014
def test_tc_cls_014_search_by_code_or_name_and_reset(page: Page) -> None:
    pom = class_page(page)
    pom.search_input.fill("1A1")
    pom.search_button.click()
    expect(pom.table_rows.filter(has_text="1A1").first).to_be_visible()
    for row in pom.table_rows.all():
        assert "1A1" in row.inner_text()
    pom.reset_button.click()
    expect(pom.search_input).to_have_value("")
    expect(pom.table_rows.first).to_be_visible()
    assert any("1A2" in row.inner_text() for row in pom.table_rows.all())


# TC-CLS-015
def test_tc_cls_015_filter_by_academic_level_and_year(page: Page) -> None:
    pom = class_page(page)
    pom.level_filter.fill("Primary 1")
    pom.year_filter.fill("2026")
    pom.search_button.click()
    expect(pom.table_rows.first).to_contain_text("Primary 1")
    for row in pom.table_rows.all():
        cells = row.locator("td").all_inner_texts()
        assert "Primary 1" in cells[2]
        assert cells[3].strip() == "2026"


# TC-CLS-016
def test_tc_cls_016_class_detail_roster_matches_student_metrics(page: Page) -> None:
    pom = class_page(page)
    target_row = None
    for candidate in page.locator(ROWS).all():
        active_students = candidate.locator("td:nth-child(6)").inner_text().strip()
        count_match = re.search(r"\d+", active_students)
        if count_match and int(count_match.group()) > 0:
            target_row = candidate
            break
    assert target_row is not None, "A class with active students must be available for this flow."

    target_row.get_by_role("button", name="Detail").click()
    expect(pom.detail_heading).to_be_visible()
    expect(page.get_by_label("Class overview")).to_be_visible()
    expect(pom.roster).to_be_visible()

    metric_values = re.findall(r"\d+", page.get_by_label("Active students").inner_text())
    assert len(metric_values) >= 2, "The Active students metric must show active and total counts."
    expected_active, expected_total = map(int, metric_values[:2])

    roster_rows = pom.roster.locator("tbody tr").all()
    active_rows = 0
    for row in roster_rows:
        status = row.locator("td").last.inner_text().strip()
        assert status in {"ACTIVE", "CANCELLED"}
        active_rows += status == "ACTIVE"

    assert len(roster_rows) == expected_total
    assert active_rows == expected_active


# TC-CLS-017
def test_tc_cls_017_no_match_displays_empty_state(page: Page) -> None:
    pom = class_page(page)
    pom.search_input.fill("LopKhongTonTai999")
    pom.search_button.click()
    # DataTable renders its empty-state message inside the table body row.
    expect(page.get_by_text("No classes found")).to_be_visible()


# TC-CLS-018
def test_tc_cls_018_class_list_shows_error_and_recovers_after_network_failure(page: Page) -> None:
    def drop_fetch(route):
        if route.request.resource_type in ("fetch", "xhr") and "classes" in route.request.url:
            route.abort()
        else:
            route.continue_()

    page.route("**/*", drop_fetch)
    page.goto(f"{BASE_URL}/class-management", wait_until="domcontentloaded")
    expect(page.get_by_role("alert")).to_be_visible()
    page.unroute("**/*", drop_fetch)
    retry = page.get_by_role("button", name=re.compile("retry|try again", re.IGNORECASE))
    expect(retry).to_be_visible()
    retry.click()
    expect(page.get_by_role("table", name="Classes table")).to_be_visible()
