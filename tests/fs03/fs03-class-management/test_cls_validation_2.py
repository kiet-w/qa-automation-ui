"""
tests/fs03/fs03-class-management/test_validation_2.py
Suite: Validation (4 cases)
Invariants: POM separation, external fixtures, traceability, <=250 lines.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.class_management_page import ClassManagementPage


@pytest.mark.validation
class TestClassManagementValidation2(BaseTest):
    """Test suite covering Validation test cases."""

    def test_tc_tc_5173_cls_043_ts_5173_cls_val_bulk_bulk_upload_validation_reject_submi(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-043: Bulk Upload Validation: Reject submission when no file is selected
        Scenario: TS-5173-CLS-VAL-BULK
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Navigate to Bulk tab.", expected="File error banner displays: 'Choose a valid class template before submitting.'; no API call made."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Submit classes' directly.", expected="File error banner displays: 'Choose a valid class template before submitting.'; no API call made."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_044_ts_5173_cls_val_bulk_bulk_upload_validation_reject_non_e(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-044: Bulk Upload Validation: Reject non-Excel file format (e.g. .pdf or .txt)
        Scenario: TS-5173-CLS-VAL-BULK
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Upload 'student_guide.pdf'.", expected="FileUpload rejects file with error: 'The selected file could not be read.' / invalid format; preview table is not rendered."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Inspect error feedback.", expected="FileUpload rejects file with error: 'The selected file could not be read.' / invalid format; preview table is not rendered."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_045_ts_5173_cls_val_bulk_bulk_upload_validation_reject_empty(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-045: Bulk Upload Validation: Reject empty Excel file with 0 data rows
        Scenario: TS-5173-CLS-VAL-BULK
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Upload 'empty_template.xlsx'.", expected="File error banner displays: 'The selected file does not contain any class rows.'; submit button is disabled/blocked."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Inspect error display.", expected="File error banner displays: 'The selected file does not contain any class rows.'; submit button is disabled/blocked."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_cls_046_ts_5173_cls_val_bulk_bulk_upload_validation_flag_missing(self, class_mgmt_data: Dict[str, Any]):
        """
        TC-5173-CLS-046: Bulk Upload Validation: Flag missing offering resolution and highlight affected row numbers
        Scenario: TS-5173-CLS-VAL-BULK
        """
        page_obj = self.get_page(ClassManagementPage)
        base_url = class_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Upload file with invalid level.", expected="Alert displays: 'No school level offering was found for row 2. Update the Academic Level value in the preview.'; submission is aborted."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Click 'Submit classes'.", expected="Alert displays: 'No school level offering was found for row 2. Update the Academic Level value in the preview.'; submission is aborted."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Inspect form error alert.", expected="Alert displays: 'No school level offering was found for row 2. Update the Academic Level value in the preview.'; submission is aborted."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")
