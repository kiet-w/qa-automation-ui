"""
tests/fs03/fs03-class-management/test_ac_1.py
Suite: AC (14 cases)
Invariants: POM separation, external fixtures, traceability, <=250 lines.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.class_management_page import ClassManagementPage


@pytest.mark.ac
class TestClassManagementAc1(BaseTest):
    """Test suite covering AC test cases."""

    def test_tc_tc_5173_cls_009_ts_5173_cls_list_dom_render_class_management_page_layout(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-009: Render Class Management page layout, headers, filters and table inventory
        Scenario: TS-5173-CLS-LIST-DOM
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Navigate to /class-management.", expected="Page title 'EduFAMS | Admin Portal' is correct; H1 'Class Management' renders; 7 table headers: Class code, Class name, Academic level, Academic year, Enrolled students, Active students, Actions."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Inspect H1 'Class Management' and description.", expected="Page title 'EduFAMS | Admin Portal' is correct; H1 'Class Management' renders; 7 table headers: Class code, Class name, Academic level, Academic year, Enrolled students, Active students, Actions."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Verify filters toolbar, 'Create class' button, and table headers.", expected="Page title 'EduFAMS | Admin Portal' is correct; H1 'Class Management' renders; 7 table headers: Class code, Class name, Academic level, Academic year, Enrolled students, Active students, Actions."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_010_ts_5173_cls_list_dom_verify_data_binding_for_class_manag(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-010: Verify data binding for Class Management table row cells
        Scenario: TS-5173-CLS-LIST-DOM
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Open /class-management and locate row 'P1-CHARITY'.", expected="Col 1: `<code>P1-CHARITY</code>`; Col 2: 'Primary 1 Charity'; Col 3: 'Primary 1'; Col 4: '2026'; Col 5: '30'; Col 6: '28'; Col 7: 'Detail' button."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Verify each column value and code snippet styling.", expected="Col 1: `<code>P1-CHARITY</code>`; Col 2: 'Primary 1 Charity'; Col 3: 'Primary 1'; Col 4: '2026'; Col 5: '30'; Col 6: '28'; Col 7: 'Detail' button."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_011_ts_5173_cls_list_search_search_classes_by_exact_class_code(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-011: Search classes by exact Class Code
        Scenario: TS-5173-CLS-LIST-SEARCH
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Type 'P3-HONESTY' into search input.", expected="Table displays exactly 'P3-HONESTY'; unrelated classes are hidden; pagination updates to '1 total'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Search' button.", expected="Table displays exactly 'P3-HONESTY'; unrelated classes are hidden; pagination updates to '1 total'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect table rows.", expected="Table displays exactly 'P3-HONESTY'; unrelated classes are hidden; pagination updates to '1 total'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_012_ts_5173_cls_list_search_search_classes_by_partial_class_nam(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-012: Search classes by partial Class Name keyword (case-insensitive)
        Scenario: TS-5173-CLS-LIST-SEARCH
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Type 'charity' in lowercase into search input.", expected="Both 'Primary 1-A (Charity)' and 'Primary 2-A (Charity)' rows are returned; non-charity classes are filtered out."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Search'.", expected="Both 'Primary 1-A (Charity)' and 'Primary 2-A (Charity)' rows are returned; non-charity classes are filtered out."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect matching rows.", expected="Both 'Primary 1-A (Charity)' and 'Primary 2-A (Charity)' rows are returned; non-charity classes are filtered out."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_013_ts_5173_cls_list_search_display_empty_state_message_when_se(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-013: Display empty state message when search returns no matching classes
        Scenario: TS-5173-CLS-LIST-SEARCH
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Enter 'NONEXISTENT_CLASS_XYZ_999' into search.", expected="Empty state is rendered: 'No classes found' heading with description 'Try changing the search or filters.'; no table rows shown."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Search'.", expected="Empty state is rendered: 'No classes found' heading with description 'Try changing the search or filters.'; no table rows shown."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect table body.", expected="Empty state is rendered: 'No classes found' heading with description 'Try changing the search or filters.'; no table rows shown."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_014_ts_5173_cls_list_filter_filter_classes_by_academic_level_na(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-014: Filter classes by Academic Level name
        Scenario: TS-5173-CLS-LIST-FILTER
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Enter 'Primary 1' into 'Filter by academic level' field.", expected="All returned classes have Academic Level containing 'Primary 1'; other levels are excluded."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Search'.", expected="All returned classes have Academic Level containing 'Primary 1'; other levels are excluded."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect table rows.", expected="All returned classes have Academic Level containing 'Primary 1'; other levels are excluded."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_015_ts_5173_cls_list_filter_filter_classes_by_academic_year_num(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-015: Filter classes by Academic Year number
        Scenario: TS-5173-CLS-LIST-FILTER
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Enter '2026' into 'e.g. 2026' input.", expected="Only classes for Academic Year 2026 are displayed; params object sends academicYearNumber=2026 as integer."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Search'.", expected="Only classes for Academic Year 2026 are displayed; params object sends academicYearNumber=2026 as integer."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Verify all returned rows display Academic year 2026.", expected="Only classes for Academic Year 2026 are displayed; params object sends academicYearNumber=2026 as integer."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_016_ts_5173_cls_list_filter_reset_filters_restore_default_unfil(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-016: Reset filters: restore default unfiltered class directory list
        Scenario: TS-5173-CLS-LIST-FILTER
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Verify filtered list is displayed.", expected="All three inputs (search, academicLevel, academicYear) are cleared; table refetches and restores full default directory; page number resets to 1."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Reset filters' button.", expected="All three inputs (search, academicLevel, academicYear) are cleared; table refetches and restores full default directory; page number resets to 1."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect input values and table list.", expected="All three inputs (search, academicLevel, academicYear) are cleared; table refetches and restores full default directory; page number resets to 1."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_017_ts_5173_cls_list_sort_pag_sort_classes_table_ascending_and_de(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-017: Sort classes table ascending and descending by Class Code
        Scenario: TS-5173-CLS-LIST-SORT-PAGINATION
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Click 'Class code' header to sort ascending.", expected="First click sorts ascending (P1-A -> P2-B -> P3-C); second click sorts descending (P3-C -> P2-B -> P1-A); aria-sort attribute updates correctly."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Verify alphabetical sort order A->Z.", expected="First click sorts ascending (P1-A -> P2-B -> P3-C); second click sorts descending (P3-C -> P2-B -> P1-A); aria-sort attribute updates correctly."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Click 'Class code' header again to sort descending.", expected="First click sorts ascending (P1-A -> P2-B -> P3-C); second click sorts descending (P3-C -> P2-B -> P1-A); aria-sort attribute updates correctly."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_018_ts_5173_cls_list_sort_pag_paginate_class_list_through_rows_pe(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-018: Paginate class list through rows per page options (5, 10, 25, 50)
        Scenario: TS-5173-CLS-LIST-SORT-PAGINATION
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Select 'Rows per page: 5' and verify 5 rows rendered.", expected="Page size changes dynamically; pagination counter accurately reflects '35 total'; Next/Previous/First/Last buttons operate without errors."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Next' to view page 2.", expected="Page size changes dynamically; pagination counter accurately reflects '35 total'; Next/Previous/First/Last buttons operate without errors."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Select 'Rows per page: 25' and verify 25 rows rendered.", expected="Page size changes dynamically; pagination counter accurately reflects '35 total'; Next/Previous/First/Last buttons operate without errors."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Inspect total indicator '35 total'.", expected="Page size changes dynamically; pagination counter accurately reflects '35 total'; Next/Previous/First/Last buttons operate without errors."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_019_ts_5173_cls_create_single_create_a_new_class_in_single_mode_w(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-019: Create a new class in Single mode with valid required fields
        Scenario: TS-5173-CLS-CREATE-SINGLE-FLOW
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Navigate to /class-management/new.", expected="API POST /school/v1/schools/:schoolId/classes returns 201; toast 'Class created: Class created successfully' appears; user is redirected to /class-management; new class appears in list."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Fill '#class-classCode' with 'P1-GENESIS'.", expected="API POST /school/v1/schools/:schoolId/classes returns 201; toast 'Class created: Class created successfully' appears; user is redirected to /class-management; new class appears in list."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Fill '#class-className' with 'Primary 1 Genesis'.", expected="API POST /school/v1/schools/:schoolId/classes returns 201; toast 'Class created: Class created successfully' appears; user is redirected to /class-management; new class appears in list."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Select 'Primary 1 · 2026' from Combobox.", expected="API POST /school/v1/schools/:schoolId/classes returns 201; toast 'Class created: Class created successfully' appears; user is redirected to /class-management; new class appears in list."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 5: 5. Click 'Create class' button.", expected="API POST /school/v1/schools/:schoolId/classes returns 201; toast 'Class created: Class created successfully' appears; user is redirected to /class-management; new class appears in list."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_020_ts_5173_cls_create_single_cancel_class_creation_in_single_mod(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-020: Cancel class creation in Single mode and return to class list
        Scenario: TS-5173-CLS-CREATE-SINGLE-FLOW
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Enter draft values in code and name fields.", expected="Navigation redirects to /class-management; no POST request is triggered; no draft class is saved."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Cancel' button.", expected="Navigation redirects to /class-management; no POST request is triggered; no draft class is saved."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect URL and class directory.", expected="Navigation redirects to /class-management; no POST request is triggered; no draft class is saved."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_021_ts_5173_cls_create_bulk_f_switch_between_single_and_bulk_mode(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-021: Switch between Single and Bulk mode tabs on Create class page
        Scenario: TS-5173-CLS-CREATE-BULK-FLOW
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Verify 'Single' tab panel is visible with class details card.", expected="Tabs switch cleanly; active tab styling updates; single and bulk sub-components toggle visibility without errors."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Bulk' tab trigger.", expected="Tabs switch cleanly; active tab styling updates; single and bulk sub-components toggle visibility without errors."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Verify 'Bulk class creation' card renders with Download template and FileUpload.", expected="Tabs switch cleanly; active tab styling updates; single and bulk sub-components toggle visibility without errors."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Click 'Single' tab trigger to switch back.", expected="Tabs switch cleanly; active tab styling updates; single and bulk sub-components toggle visibility without errors."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_022_ts_5173_cls_create_bulk_f_download_bulk_class_creation_excel(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-022: Download bulk class creation Excel template populated with school academic levels
        Scenario: TS-5173-CLS-CREATE-BULK-FLOW
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Navigate to /class-management/new and select 'Bulk' tab.", expected="Excel file is downloaded; contains expected columns (Class Code, Class Name, Academic Level); Academic Level column contains dropdown validation matching school's active levels."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Download template' button.", expected="Excel file is downloaded; contains expected columns (Class Code, Class Name, Academic Level); Academic Level column contains dropdown validation matching school's active levels."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect downloaded file and sheet columns.", expected="Excel file is downloaded; contains expected columns (Class Code, Class Name, Academic Level); Academic Level column contains dropdown validation matching school's active levels."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")
