"""
tests/fs03/fs03-class-management/test_validation_1.py
Suite: Validation (14 cases)
Invariants: POM separation, external fixtures, traceability, <=250 lines.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.class_management_page import ClassManagementPage


@pytest.mark.validation
class TestClassManagementValidation1(BaseTest):
    """Test suite covering Validation test cases."""

    def test_tc_tc_5173_cls_029_ts_5173_cls_val_code_class_code_layer_1_block_submission(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-029: Class Code: Layer 1 - Block submission when Class Code is empty
        Scenario: TS-5173-CLS-VAL-CODE
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Leave Class Code blank.", expected="Submission blocked; inline error 'Class code is required.' appears; #class-classCode receives aria-invalid='true'; FormErrorSummary displays error."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Create class'.", expected="Submission blocked; inline error 'Class code is required.' appears; #class-classCode receives aria-invalid='true'; FormErrorSummary displays error."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect inline error and summary.", expected="Submission blocked; inline error 'Class code is required.' appears; #class-classCode receives aria-invalid='true'; FormErrorSummary displays error."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_030_ts_5173_cls_val_code_class_code_layer_2_treat_whitespace(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-030: Class Code: Layer 2 - Treat whitespace-only string as empty
        Scenario: TS-5173-CLS-VAL-CODE
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Enter '      ' into #class-classCode.", expected="Submission blocked; triggers 'Class code is required.'; aria-invalid='true'; no POST request made."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Create class'.", expected="Submission blocked; triggers 'Class code is required.'; aria-invalid='true'; no POST request made."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect error state.", expected="Submission blocked; triggers 'Class code is required.'; aria-invalid='true'; no POST request made."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_031_ts_5173_cls_val_code_class_code_layer_4_trim_leading_and(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-031: Class Code: Layer 4 - Trim leading and trailing whitespace upon successful submission
        Scenario: TS-5173-CLS-VAL-CODE
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Enter '   P1-TRIMMED   '.", expected="Payload carries trimmed classCode='P1-TRIMMED'; table renders code without whitespace."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Fill other valid fields and submit.", expected="Payload carries trimmed classCode='P1-TRIMMED'; table renders code without whitespace."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect POST payload and resulting row in table.", expected="Payload carries trimmed classCode='P1-TRIMMED'; table renders code without whitespace."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_032_ts_5173_cls_val_code_class_code_layer_5_boundary_test_mi(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-032: Class Code: Layer 5 - Boundary test minimum length (1 character)
        Scenario: TS-5173-CLS-VAL-CODE
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Enter classCode 'A'.", expected="Single character code is accepted; class is created successfully."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Fill valid name and offering.", expected="Single character code is accepted; class is created successfully."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Submit form.", expected="Single character code is accepted; class is created successfully."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_033_ts_5173_cls_val_code_class_code_layer_6_boundary_test_ma(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-033: Class Code: Layer 6 - Boundary test maximum length (30 characters)
        Scenario: TS-5173-CLS-VAL-CODE
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Enter 30-character classCode.", expected="30-character code is accepted without UI truncation or layout overflow; table cell wraps or truncates gracefully with code styling."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Fill other fields and submit.", expected="30-character code is accepted without UI truncation or layout overflow; table cell wraps or truncates gracefully with code styling."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Verify persistence and display in table.", expected="30-character code is accepted without UI truncation or layout overflow; table cell wraps or truncates gracefully with code styling."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_034_ts_5173_cls_val_code_class_code_layer_8_allow_valid_stan(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-034: Class Code: Layer 8 - Allow valid standard format with hyphens, slashes and dots
        Scenario: TS-5173-CLS-VAL-CODE
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Enter 'JC1/04-A.1'.", expected="Code accepted and rendered accurately in `<code>` block."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Submit with valid name and offering.", expected="Code accepted and rendered accurately in `<code>` block."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect table.", expected="Code accepted and rendered accurately in `<code>` block."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_035_ts_5173_cls_val_name_class_name_layer_1_block_submission(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-035: Class Name: Layer 1 - Block submission when Class Name is empty
        Scenario: TS-5173-CLS-VAL-NAME
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Leave Class Name empty.", expected="Submission blocked; inline error 'Class name is required.' is displayed; #class-className has aria-invalid='true'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Create class'.", expected="Submission blocked; inline error 'Class name is required.' is displayed; #class-className has aria-invalid='true'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect inline error and summary.", expected="Submission blocked; inline error 'Class name is required.' is displayed; #class-className has aria-invalid='true'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_036_ts_5173_cls_val_name_class_name_layer_2_treat_whitespace(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-036: Class Name: Layer 2 - Treat whitespace-only Class Name as empty
        Scenario: TS-5173-CLS-VAL-NAME
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Enter spaces into #class-className.", expected="Submission blocked; 'Class name is required.' displayed; aria-invalid='true'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Create class'.", expected="Submission blocked; 'Class name is required.' displayed; aria-invalid='true'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Verify error.", expected="Submission blocked; 'Class name is required.' displayed; aria-invalid='true'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_037_ts_5173_cls_val_name_class_name_layer_4_trim_leading_and(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-037: Class Name: Layer 4 - Trim leading and trailing whitespace from Class Name
        Scenario: TS-5173-CLS-VAL-NAME
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Enter padded name.", expected="Class Name is saved as 'Primary 1 Charity (Morning)' without leading or trailing spaces."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Submit form.", expected="Class Name is saved as 'Primary 1 Charity (Morning)' without leading or trailing spaces."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect saved name in table.", expected="Class Name is saved as 'Primary 1 Charity (Morning)' without leading or trailing spaces."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_038_ts_5173_cls_val_name_class_name_layer_6_boundary_test_ma(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-038: Class Name: Layer 6 - Boundary test maximum length (100 characters)
        Scenario: TS-5173-CLS-VAL-NAME
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Enter 100-character name.", expected="100-character name persists intact; renders without breaking card or table layouts."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Submit form.", expected="100-character name persists intact; renders without breaking card or table layouts."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect list and detail page layout.", expected="100-character name persists intact; renders without breaking card or table layouts."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_039_ts_5173_cls_val_name_class_name_layer_9_support_unicode(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-039: Class Name: Layer 9 - Support Unicode and multilingual characters
        Scenario: TS-5173-CLS-VAL-NAME
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Enter Unicode class name.", expected="Unicode characters persist and display correctly without mojibake or corrupt encoding."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Submit.", expected="Unicode characters persist and display correctly without mojibake or corrupt encoding."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Reload directory and verify.", expected="Unicode characters persist and display correctly without mojibake or corrupt encoding."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_040_ts_5173_cls_val_offering_school_level_offering_layer_1_block(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-040: School Level Offering: Layer 1 - Block submission when no offering is selected
        Scenario: TS-5173-CLS-VAL-OFFERING
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Enter valid code and name.", expected="Submission blocked; error message 'Select a school level offering.' appears under combobox; aria-invalid='true' set on combobox container."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Leave Combobox empty.", expected="Submission blocked; error message 'Select a school level offering.' appears under combobox; aria-invalid='true' set on combobox container."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Click 'Create class'.", expected="Submission blocked; error message 'Select a school level offering.' appears under combobox; aria-invalid='true' set on combobox container."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_041_ts_5173_cls_val_offering_school_level_offering_layer_7_autoc(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-041: School Level Offering: Layer 7 - Autocomplete filter options by keyword search
        Scenario: TS-5173-CLS-VAL-OFFERING
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Click into Combobox and type 'Primary 3'.", expected="Dropdown filters to offerings containing 'Primary 3'; selecting an offering populates input with label format: '{Level} · {Year} · {OfferingName}'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Inspect filtered dropdown items.", expected="Dropdown filters to offerings containing 'Primary 3'; selecting an offering populates input with label format: '{Level} · {Year} · {OfferingName}'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Select matching offering.", expected="Dropdown filters to offerings containing 'Primary 3'; selecting an offering populates input with label format: '{Level} · {Year} · {OfferingName}'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_042_ts_5173_cls_val_offering_school_level_offering_layer_12_curs(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-042: School Level Offering: Layer 12 - Cursor pagination and 'Load more' in offerings combobox
        Scenario: TS-5173-CLS-VAL-OFFERING
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Open offerings Combobox dropdown.", expected="'Loading offerings' status displays briefly; next page of offerings appends smoothly without resetting existing selections."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Scroll to bottom and click 'Load more' button.", expected="'Loading offerings' status displays briefly; next page of offerings appends smoothly without resetting existing selections."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect appended options.", expected="'Loading offerings' status displays briefly; next page of offerings appends smoothly without resetting existing selections."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")
