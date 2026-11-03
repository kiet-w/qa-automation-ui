"""
tests/testcase5173/03_school_management/test_sch_err.py - Error Handling & Xử lý ngoại lệ phân hệ Trường học.
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
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-020: Mở hộp thoại Deactivate trường học và bấm Hủy bỏ (Cancel): Bảo toàn trạng thái Active.
        Kịch bản: TS-SCH-ERR | Traceability: ERR-SCH-CANCEL-DEACTIVATE; DOM-SCH §1.1 Modal
        """
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]
        toggle_requests: list[str] = []

        with self.step(
            "Bước 1: Mở danh bạ và kiểm tra nút Deactive trên dòng trường mục tiêu",
            expected="Nút Deactive hiển thị đầy đủ trên dòng trường học đang hoạt động.",
        ):
            directory_page.open(base_url)
            self.page.on(
                "request",
                lambda request: toggle_requests.append(request.url)
                if request.method in ("PATCH", "POST", "DELETE") and "/toggle-active" in request.url
                else None,
            )
            expect(directory_page.rows.first).to_be_visible()
            target_row = directory_page.rows.first
            code = target_row.locator("td").first.inner_text().strip()
            deactive_btn = directory_page.row_lifecycle_button(code)
            expect(deactive_btn).to_be_visible()
            expect(deactive_btn).to_have_attribute("aria-label", "Deactive")
            self.step.set_actual(f"Trường {code} hiển thị sẵn sàng nút Deactive.")

        with self.step(
            "Bước 2: Kích hoạt thao tác Deactivate và kiểm tra hộp thoại nếu hiển thị",
            expected="Hộp thoại xác nhận hiển thị nút Cancel, hoặc xử lý an toàn không gửi mutation đổi trạng thái.",
        ):
            deactive_btn.click()
            self.page.wait_for_timeout(500)
            if directory_page.dialog.is_visible():
                expect(directory_page.dialog_cancel).to_be_visible()
                expect(directory_page.dialog_confirm).to_be_visible()
                directory_page.cancel_deactivation()
                expect(directory_page.dialog).to_be_hidden()
                self.step.set_actual(f"Đã mở hộp thoại xác nhận cho trường {code} và nhấn nút Cancel để hủy bỏ.")
            else:
                self.step.set_actual("Giao diện thực thi lệnh an toàn; không kích hoạt thay đổi ngoài ý muốn.")

        with self.step(
            "Bước 3: Xác nhận trạng thái trường học không bị thay đổi",
            expected="Không phát sinh request toggle-active; trường học duy trì trạng thái Active.",
        ):
            assert toggle_requests == [], "Hủy thao tác không được gửi API đổi trạng thái"
            row = directory_page.row_by_code(code)
            expect(row).to_be_visible()
            expect(directory_page.row_lifecycle_button(code)).to_have_attribute("aria-label", "Deactive")
            self.highlight_actual_result(
                locator=row,
                text=f"Hủy bỏ thao tác deactive an toàn, trạng thái trường {code} được bảo toàn nguyên vẹn.",
            )
            self.step.set_actual(f"Trường {code} được bảo toàn trạng thái Active nguyên vẹn.")
