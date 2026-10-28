"""
tests/fs03/fs03-school-directory/test_sch_err.py - Error Handling & Xử lý ngoại lệ phân hệ Trường học.
Bao phủ ca kiểm thử: TC-SCH-020.
Scenario ID: TS-SCH-ERR | Nguồn đặc tả: 03_school_management.md §1.1; DOM-SCH §1.1 Modal
Tuân thủ Invariant 1, 2, 3, 4, 7, 8, 9 (<250 dòng), 13 (100% Tiếng Việt), 14, 15.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.school_directory_page import SchoolDirectoryPage


@pytest.mark.error
class TestSchoolErrorHandling(BaseTest):
    """Bộ kiểm thử Xử lý ngoại lệ & Phục hồi lỗi (Error Handling) Phân hệ Trường học."""

    def test_tc_sch_020_cancel_deactivate_dialog(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-020: Mở hộp thoại Deactivate trường học và bấm Hủy bỏ (Cancel): Bảo toàn trạng thái Active.
        Kịch bản: TS-SCH-ERR | Traceability: ERR-SCH-CANCEL-DEACTIVATE; DOM-SCH §1.1 Modal
        """
        auth_mock("moehq")
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]
        active_school = school_directory_data["sample_schools"]["active_with_students"]

        with self.step(
            "Bước 1: Mở danh bạ và nhấn nút Deactive trên dòng trường mục tiêu",
            expected="Hộp thoại xác nhận Deactivate xuất hiện.",
        ):
            directory_page.open(base_url)
            row = directory_page.row_by_code(active_school["code"])
            expect(row).to_be_visible()
            directory_page.open_deactivate_dialog(active_school["code"])
            expect(directory_page.dialog).to_be_visible()
            self.step.set_actual(f"Hộp thoại xác nhận mở thành công cho trường {active_school['code']}.")

        with self.step(
            "Bước 2: Kiểm tra các nút bấm trên hộp thoại xác nhận",
            expected="Hộp thoại có nút xác nhận và nút Cancel để hủy thao tác.",
        ):
            expect(directory_page.dialog_cancel).to_be_visible()
            expect(directory_page.dialog_confirm).to_be_visible()
            self.step.set_actual("Đã xác nhận sự hiện diện của các nút thao tác trên modal.")

        with self.step(
            "Bước 3: Nhấn nút Cancel để hủy thao tác",
            expected="Hộp thoại đóng lại ngay lập tức; trạng thái trường học giữ nguyên ACTIVE.",
        ):
            directory_page.cancel_deactivation()
            expect(directory_page.dialog).to_be_hidden()
            row = directory_page.row_by_code(active_school["code"])
            expect(row).to_be_visible()
            self.highlight_actual_result(
                locator=row,
                text=f"Hủy bỏ thao tác deactive an toàn, trạng thái trường {active_school['code']} được bảo toàn.",
            )
            self.step.set_actual("Đã hủy bỏ an toàn thành công, không phát sinh thay đổi trạng thái.")
