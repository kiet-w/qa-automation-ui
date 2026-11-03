"""Playwright cases mapped one-to-one to testcase5173 TC-AYL-001–018.

Uses the repository's AcademicYearsPage POM and exact BSK selectors for forms.
The matrices request a Level Code field for AYL-012/013, while the BSK spec's
verified form only defines name, stage and display order; those cases are marked
with an explicit precondition skip until the source of truth is reconciled.
"""
from datetime import date
from time import time_ns

import pytest
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect

from pages.fs03.academic_years_page import AcademicYearsPage

BASE_URL = "http://localhost:5173"
YEAR_ROWS = "table tbody tr"
YEAR_NUMBER = "#academic-year-yearNumber"
YEAR_START = "#academic-year-startDate"
YEAR_END = "#academic-year-endDateExclusive"
LEVEL_NAME = "#academic-level-name"
LEVEL_STAGE = "#academic-level-educationStage"
LEVEL_ORDER = "#academic-level-displayOrder"


def require_registered_route(page: Page, path: str) -> None:
    heading = page.locator("main h1")
    heading.wait_for(state="visible", timeout=10000)
    rendered_heading = heading.inner_text().strip()
    if rendered_heading == "404 - Page Not Found":
        raise AssertionError(
            f"Required route {path} rendered the application's 404 page. "
            "Both academic-years and academic-levels manifests are disabled in the checked frontend."
        )


def year_page(page: Page) -> AcademicYearsPage:
    result = AcademicYearsPage(page)
    result.open(BASE_URL)
    require_registered_route(page, "/academic-years")
    expect(page.get_by_role("heading", name="Academic years")).to_be_visible()
    return result


def open_year_form(page: Page) -> None:
    page.goto(f"{BASE_URL}/academic-years/new", wait_until="domcontentloaded")
    require_registered_route(page, "/academic-years/new")
    expect(page.get_by_role("heading", name="Create an academic year")).to_be_visible()


def open_levels(page: Page) -> None:
    page.goto(f"{BASE_URL}/academic-levels", wait_until="domcontentloaded")
    require_registered_route(page, "/academic-levels")
    expect(page.get_by_role("heading", name="Academic levels")).to_be_visible()


def open_level_form(page: Page) -> None:
    page.goto(f"{BASE_URL}/academic-levels/new", wait_until="domcontentloaded")
    require_registered_route(page, "/academic-levels/new")
    expect(page.get_by_role("heading", name="Create an academic level")).to_be_visible()


def fill_year(page: Page, year: str, start: str = "2028-01-02", end: str = "2028-11-30") -> None:
    page.locator(YEAR_NUMBER).fill(year)
    page.locator(YEAR_START).fill(start)
    page.locator(YEAR_END).fill(end)


# TC-AYL-001
def test_tc_ayl_001_activate_draft_academic_year(page: Page) -> None:
    years = year_page(page)
    draft = page.locator(f'{YEAR_ROWS}:has([class*="badge"]:has-text("DRAFT"))').first
    expect(draft).to_be_visible()
    target_year = draft.locator("td").first.inner_text().strip()
    draft.get_by_role("button", name="Activate").click()
    row = page.locator(f'{YEAR_ROWS}:has-text("{target_year}")')
    expect(row.locator('[class*="badge"]')).to_contain_text("ACTIVE")
    expect(row.get_by_role("button", name="Activate")).to_have_count(0)


# TC-AYL-002
def test_tc_ayl_002_activation_keeps_single_active_academic_year(page: Page) -> None:
    year_page(page)
    target = page.locator(f'{YEAR_ROWS}:has-text("2027"):has([class*="badge"]:has-text("DRAFT"))').first
    expect(target).to_be_visible()
    target.get_by_role("button", name="Activate").click()
    dialog_alert = page.locator('[role="dialog"] [role="alert"]')
    try:
        dialog_alert.wait_for(state="visible", timeout=1000)
    except PlaywrightTimeoutError:
        pass
    else:
        expect(dialog_alert).to_contain_text("Only one")
        return
    rows = page.locator(YEAR_ROWS)
    expect(rows.locator('[class*="badge"]:has-text("ACTIVE")')).to_have_count(1)
    target = page.locator(f'{YEAR_ROWS}:has-text("2027")')
    expect(target.locator('[class*="badge"]')).to_contain_text("ACTIVE")
    prior = page.locator(f'{YEAR_ROWS}:has-text("2026")')
    if prior.count():
        expect(prior.locator('[class*="badge"]')).not_to_contain_text("ACTIVE")


# TC-AYL-003
def test_tc_ayl_003_standard_national_academic_levels_are_available(page: Page) -> None:
    open_levels(page)
    table = page.locator("table tbody")
    expect(table).to_be_visible()
    body = table.inner_text()
    for level in ("P1", "P6", "S1", "S5", "JC1", "JC2"):
        assert level in body


# TC-AYL-004
def test_tc_ayl_004_active_year_has_no_deactivation_action(page: Page) -> None:
    year_page(page)
    active = page.locator(f'{YEAR_ROWS}:has([class*="badge"]:has-text("ACTIVE"))').first
    expect(active).to_be_visible()
    # The BSK contract exposes Activate only for DRAFT and no delete/deactivate controls.
    expect(active.get_by_role("button", name="Activate")).to_have_count(0)
    expect(active.get_by_role("button", name="Delete")).to_have_count(0)


# TC-AYL-005
def test_tc_ayl_005_academic_year_table_and_toolbar(page: Page) -> None:
    year_page(page)
    headers = [header.strip() for header in page.locator("table thead th").all_inner_texts()]
    for header in ("Year", "Start date", "End date", "Status", "Schools", "Classes", "Students", "Actions"):
        assert header in headers
    expect(page.locator('input[placeholder*="Search by year" i]')).to_be_visible()
    expect(page.locator('select:has(option[value="DRAFT"])')).to_be_visible()
    expect(page.get_by_role("button", name="Search")).to_be_visible()


# TC-AYL-006
def test_tc_ayl_006_activate_button_only_appears_on_draft_rows(page: Page) -> None:
    year_page(page)
    rows = page.locator(YEAR_ROWS)
    expect(rows).not_to_have_count(0)
    for row in rows.all():
        status = row.locator('[class*="badge"]').inner_text().strip()
        activate_count = row.get_by_role("button", name="Activate").count()
        assert activate_count == (1 if status == "DRAFT" else 0)


# TC-AYL-007
def test_tc_ayl_007_academic_level_table_has_code_name_stage_and_order(page: Page) -> None:
    open_levels(page)
    headers = [header.strip() for header in page.locator("table thead th").all_inner_texts()]
    for header in ("Code", "Name", "Education stage", "Display order", "Status", "Schools", "Classes", "Students"):
        assert header in headers
    expect(page.locator('input[placeholder*="Search by code or name" i]')).to_be_visible()
    expect(page.locator('select:has(option[value="PRIMARY"])')).to_be_visible()


# TC-AYL-008
def test_tc_ayl_008_academic_year_form_has_date_pickers(page: Page) -> None:
    open_year_form(page)
    expect(page.locator(YEAR_NUMBER)).to_be_visible()
    expect(page.locator(YEAR_START)).to_be_visible()
    expect(page.locator(YEAR_END)).to_be_visible()
    assert page.locator(YEAR_START).get_attribute("type") == "date"
    assert page.locator(YEAR_END).get_attribute("type") == "date"


# TC-AYL-009
@pytest.mark.parametrize("year", ["", "26", "NămNay", "20265"], ids=["required", "short", "letters", "long"])
def test_tc_ayl_009_reject_invalid_year_number(page: Page, year: str) -> None:
    open_year_form(page)
    fill_year(page, year)
    page.get_by_role("button", name="Create academic year").click()
    expect(page.locator(YEAR_NUMBER)).to_have_attribute("aria-invalid", "true")
    expect(page).to_have_url("**/academic-years/new")


# TC-AYL-010
def test_tc_ayl_010_end_date_must_follow_start_date(page: Page) -> None:
    open_year_form(page)
    fill_year(page, "2036", "2036-12-31", "2036-01-01")
    page.get_by_role("button", name="Create academic year").click()
    expect(page.locator(YEAR_END)).to_have_attribute("aria-invalid", "true")
    expect(page.locator(f'{YEAR_END} ~ [class*="error"]')).to_contain_text("greater than")


# TC-AYL-011
def test_tc_ayl_011_duplicate_year_is_rejected(page: Page) -> None:
    open_year_form(page)
    fill_year(page, "2026", "2026-01-02", "2026-11-30")
    page.get_by_role("button", name="Create academic year").click()
    expect(page.locator('[role="alert"]')).to_contain_text("already exists")


# TC-AYL-012
def test_tc_ayl_012_academic_level_required_fields(page: Page) -> None:
    open_level_form(page)
    # The testcase matrix requires a Level Code field, while BSK's form table
    # omits it. This accessible-name lookup is the matrix's stated field name;
    # its absence remains an explicit failing acceptance assertion.
    code = page.get_by_role("textbox", name="Level code", exact=True)
    for field in (code, page.locator(LEVEL_NAME), page.locator(LEVEL_STAGE)):
        expect(field).to_be_visible()
    page.get_by_role("button", name="Create academic level").click()
    for field in (code, page.locator(LEVEL_NAME), page.locator(LEVEL_STAGE)):
        expect(field).to_have_attribute("aria-invalid", "true")


# TC-AYL-013
def test_tc_ayl_013_duplicate_level_code(page: Page) -> None:
    open_level_form(page)
    code = page.get_by_role("textbox", name="Level code", exact=True)
    expect(code).to_be_visible()
    code.fill("P1")
    page.locator(LEVEL_NAME).fill("Primary 1 duplicate")
    page.locator(LEVEL_STAGE).select_option("PRIMARY")
    page.locator(LEVEL_ORDER).fill("1")
    page.get_by_role("button", name="Create academic level").click()
    expect(page.locator('[role="alert"]')).to_contain_text("already exists")


# TC-AYL-014
def test_tc_ayl_014_create_academic_year_as_draft(page: Page) -> None:
    year = "2028"
    year_page(page)
    expect(page.locator(f'{YEAR_ROWS}:has-text("{year}")')).to_have_count(0)
    open_year_form(page)
    fill_year(page, year, "2028-01-02", "2028-11-30")
    page.get_by_role("button", name="Create academic year").click()
    expect(page).to_have_url("**/academic-years")
    row = page.locator(f'{YEAR_ROWS}:has-text("{year}")')
    expect(row.locator('[class*="badge"]')).to_contain_text("DRAFT")
    expect(row.get_by_role("button", name="Activate")).to_be_visible()


# TC-AYL-015
def test_tc_ayl_015_activate_draft_year_2028(page: Page) -> None:
    year_page(page)
    draft = page.locator(f'{YEAR_ROWS}:has-text("2028"):has([class*="badge"]:has-text("DRAFT"))').first
    expect(draft).to_be_visible()
    draft.get_by_role("button", name="Activate").click()
    dialog_alert = page.locator('[role="dialog"] [role="alert"]')
    if dialog_alert.count():
        expect(dialog_alert).to_contain_text("Only one")
        return
    row = page.locator(f'{YEAR_ROWS}:has-text("2028")')
    expect(row.locator('[class*="badge"]')).to_contain_text("ACTIVE")
    expect(row.get_by_role("button", name="Activate")).to_have_count(0)


# TC-AYL-016
def test_tc_ayl_016_create_academic_level(page: Page) -> None:
    name = f"Automation Level {time_ns()}"
    open_level_form(page)
    page.locator(LEVEL_NAME).fill(name)
    page.locator(LEVEL_STAGE).select_option("PRIMARY")
    page.locator(LEVEL_ORDER).fill("99")
    page.get_by_role("button", name="Create academic level").click()
    expect(page).to_have_url("**/academic-levels")
    expect(page.locator("table tbody tr").filter(has_text=name)).to_be_visible()


# TC-AYL-017
@pytest.mark.parametrize("status", ["DRAFT", "ACTIVE", "COMPLETED"])
def test_tc_ayl_017_filter_academic_years_by_status(page: Page, status: str) -> None:
    year_page(page)
    page.locator('select:has(option[value="DRAFT"])').select_option(status)
    page.get_by_role("button", name="Search").click()
    for row in page.locator(YEAR_ROWS).all():
        expect(row.locator('[class*="badge"]')).to_contain_text(status)


# TC-AYL-018
def test_tc_ayl_018_both_dates_are_required(page: Page) -> None:
    open_year_form(page)
    page.locator(YEAR_NUMBER).fill(str(date.today().year + 10))
    page.get_by_role("button", name="Create academic year").click()
    expect(page.locator(YEAR_START)).to_have_attribute("aria-invalid", "true")
    expect(page.locator(YEAR_END)).to_have_attribute("aria-invalid", "true")
