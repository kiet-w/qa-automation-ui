"""
tests/fs03/fs03-school-directory/test_sch_val.py - Validation & Kiểm tra hợp lệ dữ liệu phân hệ Trường học.
Bao phủ các ca kiểm thử: TC-SCH-011, TC-SCH-012, TC-SCH-013, TC-SCH-014, TC-SCH-015.
Scenario ID: TS-SCH-VAL | Nguồn đặc tả: 03_school_management.md §1.1, §1.2, §2.2; 03_school_create.json
Tuân thủ Invariant 1, 2, 3, 4, 7, 8, 9 (<250 dòng), 13 (100% Tiếng Việt), 14, 15.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.school_directory_page import SchoolDirectoryPage
from pages.fs03.school_create_page import SchoolCreatePage


@pytest.mark.validation
class TestSchoolValidation(BaseTest):
    """Bộ kiểm thử Kiểm tra hợp lệ dữ liệu (Error Validation & BVA) Phân hệ Trường học."""

    def test_tc_sch_011_mandatory_fields_validation(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-011: Kiểm tra bắt buộc nhập Mã MOE, Tên trường, Loại hình trường khi tạo mới trường học.
        Kịch bản: TS-SCH-VAL | Traceability: VAL-SCH-MANDATORY; DOM-SCH §1.2
        """
        auth_mock("moehq")
        create_page = self.get_page(SchoolCreatePage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Mở form tạo mới trường học tại /school-management/new",
            expected="Trang tạo mới hiển thị với form rỗng.",
        ):
            create_page.open(base_url)
            create_page.wait_for_form_ready()
            self.step.set_actual(f"Đã mở trang tạo mới tại {self.page.url}.")

        with self.step(
            "Bước 2: Để trống tất cả các trường và nhấn nút 'Create school'",
            expected="Form chặn submit và hiển thị các thông báo lỗi bắt buộc nhập.",
        ):
            create_page.submit_form()
            self.step.set_actual("Đã nhấn nút submit với form rỗng.")

        with self.step(
            "Bước 3: Quan sát phản hồi lỗi trên form",
            expected="Khung tóm tắt lỗi hoặc thông báo lỗi inline xuất hiện; các ô lỗi bật trạng thái cảnh báo.",
        ):
            expect(create_page.summary_error_banner).to_be_visible()
            expect(create_page.moe_code_inline_error).to_be_visible()
            expect(create_page.name_inline_error).to_be_visible()
            self.highlight_actual_result(
                locator=create_page.summary_error_banner,
                text="Hệ thống chặn submit và hiển thị đầy đủ thông báo lỗi bắt buộc nhập trên form.",
            )
            self.step.set_actual("Đã xác nhận đầy đủ thông báo lỗi bắt buộc nhập cho các trường.")

    def test_tc_sch_012_unique_moe_code_constraint(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-012: Kiểm tra tính duy nhất của Mã MOE (Unique constraint): Chặn tạo trường trùng mã đã có.
        Kịch bản: TS-SCH-VAL | Traceability: VAL-SCH-UNIQUE-CODE; UNIQUE-CONSTRAINT
        """
        auth_mock("moehq")
        create_page = self.get_page(SchoolCreatePage)
        base_url = school_directory_data["environments"]["base_url"]
        dup_code = school_directory_data["validation_data"]["duplicate_code"]

        with self.step(
            "Bước 1: Mở form tạo mới trường học",
            expected="Form tạo mới sẵn sàng nhập liệu.",
        ):
            create_page.open(base_url)
            create_page.wait_for_form_ready()
            self.step.set_actual(f"Mở form tạo mới tại {self.page.url}.")

        with self.step(
            f"Bước 2: Nhập mã trường trùng lặp '{dup_code}', điền tên và chọn loại hình rồi submit",
            expected="Yêu cầu tạo mới được gửi với mã trường đã tồn tại trong cơ sở dữ liệu.",
        ):
            create_page.fill_moe_school_code(dup_code)
            create_page.fill_school_name("Duplicate Code Testing School")
            create_page.select_school_type("GOVERNMENT")
            create_page.select_first_academic_level()
            create_page.submit_form()
            self.step.set_actual(f"Đã gửi form với mã trùng '{dup_code}'.")

        with self.step(
            "Bước 3: Quan sát thông báo lỗi và phản hồi từ hệ thống",
            expected="Hệ thống chặn tạo mới và hiển thị cảnh báo lỗi trùng mã trường.",
        ):
            alert = self.page.locator("[role='alert'], #school-moeSchoolCode-error")
            expect(alert.first).to_be_visible()
            self.highlight_actual_result(
                locator=alert.first,
                text=f"Hệ thống từ chối tạo mới khi trùng mã MOE school code '{dup_code}'.",
            )
            self.step.set_actual("Đã xác nhận chặn tạo mới thành công khi trùng mã trường.")

    def test_tc_sch_013_school_name_bva_length(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-013: Ràng buộc độ dài Tên trường (BVA: Min 3 ký tự, Max 100 ký tự).
        Kịch bản: TS-SCH-VAL | Traceability: VAL-SCH-NAME-BVA; BVA-MIN-MAX
        """
        auth_mock("moehq")
        create_page = self.get_page(SchoolCreatePage)
        base_url = school_directory_data["environments"]["base_url"]
        short_name = school_directory_data["validation_data"]["invalid_short_name"]
        valid_100_name = school_directory_data["validation_data"]["valid_100_name"]

        with self.step(
            f"Bước 1: Nhập tên trường chỉ có 2 ký tự '{short_name}' (< min 3 ký tự) và nhấn Create",
            expected="Form hiển thị cảnh báo yêu cầu tên trường tối thiểu 3 ký tự.",
        ):
            create_page.open(base_url)
            create_page.wait_for_form_ready()
            create_page.fill_moe_school_code("SCH-BVA1")
            create_page.fill_school_name(short_name)
            create_page.select_school_type("GOVERNMENT")
            create_page.select_first_academic_level()
            create_page.submit_form()
            self.step.set_actual(f"Đã nhập tên 2 ký tự: '{short_name}'.")

        with self.step(
            "Bước 2: Quan sát cảnh báo lỗi độ dài tối thiểu",
            expected="Hệ thống từ chối tên trường 2 ký tự và giữ lại form.",
        ):
            expect(create_page.name_inline_error).to_be_visible()
            self.step.set_actual("Cảnh báo tên quá ngắn hiển thị chính xác.")

        with self.step(
            "Bước 3: Nhập tên trường 100 ký tự hợp lệ",
            expected="Tên trường 100 ký tự được chấp nhận hợp lệ trên ô nhập liệu.",
        ):
            create_page.fill_school_name(valid_100_name)
            expect(create_page.school_name_input).to_have_value(valid_100_name)
            self.highlight_actual_result(
                locator=create_page.school_name_input,
                text="Ràng buộc độ dài tên trường tuân thủ đúng chuẩn BVA min/max.",
            )
            self.step.set_actual("Đã xác nhận tên trường 100 ký tự hợp lệ.")

    def test_tc_sch_014_inline_edit_school_row(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-014: Chỉnh sửa nhanh (Inline Edit) trực tiếp trên dòng danh bạ: Cho phép đổi Tên trường và Loại trường hợp lệ.
        Kịch bản: TS-SCH-VAL | Traceability: VAL-SCH-INLINE-EDIT; DOM-SCH §1.1 Inline
        """
        auth_mock("moehq")
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]
        active_school = school_directory_data["sample_schools"]["active_with_students"]
        new_name = school_directory_data["validation_data"]["inline_edit_name"]

        with self.step(
            "Bước 1: Mở danh bạ và nhấn nút Edit trên dòng trường học",
            expected="Kích hoạt chế độ chỉnh sửa trực tiếp trên bảng, hiển thị các ô input.",
        ):
            directory_page.open(base_url)
            directory_page.click_edit(active_school["code"])
            expect(directory_page.inline_name_input).to_be_visible()
            self.step.set_actual(f"Đã bật inline edit cho trường {active_school['code']}.")

        with self.step(
            f"Bước 2: Cập nhật Tên trường thành '{new_name}' và chọn loại trường",
            expected="Các ô nhập liệu trên dòng nhận giá trị mới.",
        ):
            directory_page.fill_inline_name(new_name)
            self.step.set_actual(f"Đã điền tên mới: {new_name}.")

        with self.step(
            "Bước 3: Nhấn nút Save (biểu tượng Check) để lưu thay đổi",
            expected="Chế độ inline edit đóng lại; bảng hiển thị giá trị mới vừa cập nhật.",
        ):
            directory_page.save_inline()
            self.step.set_actual("Đã nhấn lưu inline edit.")

        with self.step(
            "Bước 4: Quan sát dòng dữ liệu vừa cập nhật",
            expected="Dòng trường học thoát khỏi chế độ edit; cập nhật tên mới thành công.",
        ):
            row = directory_page.row_by_code(active_school["code"])
            expect(row).to_be_visible()
            self.highlight_actual_result(
                locator=row,
                text=f"Chỉnh sửa inline trên dòng trường {active_school['code']} thành công.",
            )
            self.step.set_actual("Đã hoàn tất kiểm chứng tính năng inline edit.")

    def test_tc_sch_015_cancel_inline_edit(
        self, school_directory_data: Dict[str, Any], auth_mock
    ) -> None:
        """
        TC-SCH-015: Hủy bỏ chế độ chỉnh sửa nhanh (Cancel Inline Edit) và hoàn nguyên giá trị ban đầu.
        Kịch bản: TS-SCH-VAL | Traceability: VAL-SCH-CANCEL-INLINE; DOM-SCH §1.1
        """
        auth_mock("moehq")
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]
        active_school = school_directory_data["sample_schools"]["active_with_students"]

        with self.step(
            "Bước 1: Bật chế độ inline edit và thay đổi tên trường",
            expected="Ô input tên trường hiển thị giá trị đang sửa tạm thời.",
        ):
            directory_page.open(base_url)
            directory_page.click_edit(active_school["code"])
            expect(directory_page.inline_name_input).to_be_visible()
            directory_page.fill_inline_name("Temporary Unsaved School Name")
            self.step.set_actual("Đã nhập tên tạm thời chưa lưu.")

        with self.step(
            "Bước 2: Nhấn nút Hủy bỏ (icon Cancel / Discard changes)",
            expected="Chế độ inline edit đóng lại mà không gửi lệnh cập nhật lên server.",
        ):
            directory_page.discard_inline_button.click()
            self.step.set_actual("Đã nhấn nút Discard changes.")

        with self.step(
            "Bước 3: Kiểm tra giá trị hiển thị trên dòng",
            expected="Dòng hoàn nguyên tên trường ban đầu; không lưu dữ liệu thay đổi dở dang.",
        ):
            row = directory_page.row_by_code(active_school["code"])
            expect(row).to_be_visible()
            expect(directory_page.inline_name_input).to_have_count(0)
            self.highlight_actual_result(
                locator=row,
                text="Hủy bỏ inline edit thành công, hoàn nguyên chính xác dữ liệu ban đầu.",
            )
            self.step.set_actual("Dữ liệu ban đầu được bảo toàn hoàn hảo.")
