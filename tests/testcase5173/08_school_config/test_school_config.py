"""Black-box UI checks for TC-CFG-001..018.

The live UAT school has data for 2026, but 2025 and 2027 have no levels.
Write flows are guarded until an isolated, resettable school is available.
"""

import re

import pytest
from playwright.sync_api import expect

from pages.testcase5173.school_config_page import SchoolConfigPage


def _open(config: SchoolConfigPage, year: str = "2026") -> None:
    config.open()
    expect(config.heading).to_be_visible()
    config.choose_year(year)
    expect(config.year.locator("option:checked")).to_have_text(year)
    # Wait for the selected year's data, not merely the select control.
    expect(config.page.get_by_text("Selected Academic Year", exact=True)).to_be_visible()


def _configured_level(config: SchoolConfigPage) -> None:
    config.select_level("PRI-1")
    expect(config.level_detail).to_be_visible()


@pytest.mark.br
def test_tc_cfg_001_school_admin_sees_own_school_and_levels(config: SchoolConfigPage) -> None:
    _open(config)
    expect(config.school_header).to_contain_text("Rosyth Primary School")
    expect(config.school_header).to_contain_text("RPS-0201")
    expect(config.level("PRI-1")).to_be_visible()
    expect(config.add_levels).to_be_enabled()
    _configured_level(config)
    expect(config.class_table).to_be_visible()


@pytest.mark.br
@pytest.mark.skip(reason="2025 has no source levels; copying into configured 2026 changes shared data")
def test_tc_cfg_002_copy_previous_year_reuses_levels_and_classes(config: SchoolConfigPage) -> None:
    _open(config)
    dialog = config.open_copy()
    dialog.get_by_label("Source academic year").select_option(label="2025")
    dialog.get_by_role("button", name="Copy").click()
    expect(config.level("PRI-1")).to_be_visible()


@pytest.mark.br
def test_tc_cfg_003_completed_year_is_read_only(config: SchoolConfigPage) -> None:
    _open(config, "2025")
    expect(config.school_header.get_by_text("CLOSED", exact=True)).to_be_visible()
    expect(config.add_levels).to_be_disabled()
    expect(config.copy_previous_year).to_be_disabled()


@pytest.mark.br
@pytest.mark.skip(reason="Live UI exposes no remove-level action or warning to exercise")
def test_tc_cfg_004_cannot_remove_level_with_active_classes(config: SchoolConfigPage) -> None:
    _open(config)
    _configured_level(config)
    expect(config.class_table.get_by_role("row").filter(has_text="ACTIVE")).to_have_count(10)
    config.page.get_by_role("button", name=re.compile("remove|delete", re.I)).click()
    expect(config.page.get_by_role("alert")).to_contain_text("class")


@pytest.mark.ac
def test_tc_cfg_005_header_fields(config: SchoolConfigPage) -> None:
    _open(config)
    expect(config.school_header).to_contain_text("Rosyth Primary School")
    expect(config.school_header).to_contain_text("RPS-0201")
    expect(config.year).to_be_visible()
    expect(config.school_header.get_by_text("ACTIVE", exact=True)).to_be_visible()
    expect(config.add_levels).to_be_visible()
    expect(config.copy_previous_year).to_be_visible()


@pytest.mark.ac
def test_tc_cfg_006_status_follows_year(config: SchoolConfigPage) -> None:
    _open(config)
    for year, status in (("2027", "DRAFT"), ("2026", "ACTIVE"), ("2025", "CLOSED")):
        config.choose_year(year)
        expect(config.school_header.get_by_text(status, exact=True)).to_be_visible()


@pytest.mark.ac
def test_tc_cfg_007_stage_tabs_filter_levels(config: SchoolConfigPage) -> None:
    _open(config)
    for name in ("All", "Primary", "Secondary", "Pre-University"):
        expect(config.stage(name)).to_be_visible()
    config.stage("Primary").click()
    expect(config.level("PRI-1")).to_be_visible()
    config.stage("Secondary").click()
    expect(config.level("PRI-1")).to_have_count(0)


@pytest.mark.ac
def test_tc_cfg_008_level_detail_shows_class_table(config: SchoolConfigPage) -> None:
    _open(config)
    _configured_level(config)
    expect(config.add_class).to_be_visible()
    table = config.class_table
    expect(table).to_be_visible()
    header = table.get_by_role("row").first
    for title in ("Class code", "Class name", "Active students", "Status"):
        expect(header.get_by_role("columnheader", name=title, exact=True)).to_be_visible()
    expect(table.get_by_role("row").filter(has_text="P1-A")).to_be_visible()


@pytest.mark.ac
def test_tc_cfg_009_active_year_actions_enabled(config: SchoolConfigPage) -> None:
    _open(config)
    expect(config.school_header.get_by_text("ACTIVE", exact=True)).to_be_visible()
    expect(config.add_levels).to_be_enabled()
    expect(config.copy_previous_year).to_be_enabled()


@pytest.mark.validation
def test_tc_cfg_010_add_levels_requires_selection(config: SchoolConfigPage) -> None:
    _open(config, "2027")
    dialog = config.open_add_levels()
    expect(dialog.get_by_role("combobox", name="Education stages")).to_be_visible()
    expect(dialog.get_by_text("0 selected", exact=True)).to_be_visible()
    expect(dialog.get_by_role("button", name="Save changes")).to_be_disabled()


@pytest.mark.validation
@pytest.mark.skip(reason="Submitting empty 2025 source could alter shared 2027 configuration")
def test_tc_cfg_011_empty_source_year_is_rejected(config: SchoolConfigPage) -> None:
    _open(config, "2027")
    dialog = config.open_copy()
    dialog.get_by_label("Source academic year").select_option(label="2025")
    dialog.get_by_role("button", name="Copy").click()
    expect(config.page.get_by_role("alert")).to_contain_text("no configuration")


@pytest.mark.validation
@pytest.mark.skip(reason="Overwrite confirmation requires a populated source and isolated destination")
def test_tc_cfg_012_overwrite_requires_confirmation(config: SchoolConfigPage) -> None:
    _open(config)
    dialog = config.open_copy()
    dialog.get_by_label("Source academic year").select_option(label="2025")
    dialog.get_by_role("button", name="Copy").click()
    expect(config.page.get_by_role("alertdialog")).to_contain_text("configuration")


@pytest.mark.flow
def test_tc_cfg_013_switching_year_refreshes_configuration(config: SchoolConfigPage) -> None:
    _open(config)
    expect(config.level("PRI-1")).to_be_visible()
    config.choose_year("2027")
    expect(config.school_header.get_by_text("DRAFT", exact=True)).to_be_visible()
    expect(config.page.get_by_text("No academic levels are configured for this academic year.")).to_be_visible()
    config.choose_year("2026")
    expect(config.school_header.get_by_text("ACTIVE", exact=True)).to_be_visible()
    expect(config.level("PRI-1")).to_be_visible()


@pytest.mark.flow
@pytest.mark.skip(reason="Adding stages would persist to the shared school; isolated resettable data required")
def test_tc_cfg_014_add_levels_to_draft_year(config: SchoolConfigPage) -> None:
    _open(config, "2027")
    dialog = config.open_add_levels()
    dialog.get_by_role("combobox", name="Education stages").click()
    dialog.get_by_text("Primary · 6").click()
    dialog.get_by_role("button", name="Save changes").click()
    expect(config.level("PRI-1")).to_be_visible()
    expect(config.level("PRI-2")).to_be_visible()


@pytest.mark.flow
@pytest.mark.skip(reason="2025 source is empty and successful copy would alter shared configuration")
def test_tc_cfg_015_copy_year_configuration_successfully(config: SchoolConfigPage) -> None:
    _open(config, "2027")
    dialog = config.open_copy()
    dialog.get_by_label("Source academic year").select_option(label="2025")
    dialog.get_by_role("button", name="Copy").click()
    expect(config.level("PRI-1")).to_be_visible()


@pytest.mark.flow
def test_tc_cfg_016_stage_filter_across_primary_and_secondary(config: SchoolConfigPage) -> None:
    _open(config)
    config.stage("Primary").click()
    expect(config.level("PRI-1")).to_be_visible()
    config.stage("Secondary").click()
    expect(config.level("SEC-1")).to_be_visible()
    expect(config.level("PRI-1")).to_have_count(0)


@pytest.mark.error
def test_tc_cfg_017_cancel_copy_preserves_configuration(config: SchoolConfigPage) -> None:
    _open(config)
    before = config.page.get_by_text("Total Academic Levels", exact=True).locator("..").inner_text()
    dialog = config.open_copy()
    expect(dialog.get_by_label("Source academic year")).to_be_visible()
    dialog.get_by_role("button", name="Cancel").click()
    expect(dialog).to_be_hidden()
    assert config.page.get_by_text("Total Academic Levels", exact=True).locator("..").inner_text() == before
    expect(config.level("PRI-1")).to_be_visible()


@pytest.mark.error
def test_tc_cfg_018_completed_year_locks_actions(config: SchoolConfigPage) -> None:
    _open(config, "2025")
    expect(config.school_header.get_by_text("CLOSED", exact=True)).to_be_visible()
    expect(config.add_levels).to_be_disabled()
    expect(config.copy_previous_year).to_be_disabled()
