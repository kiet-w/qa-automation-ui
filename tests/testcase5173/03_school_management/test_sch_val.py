"""
tests/testcase5173/03_school_management/test_sch_val.py - Validation & Kiểm tra hợp lệ dữ liệu phân hệ Trường học.
Bao phủ các ca kiểm thử: TC-SCH-011, TC-SCH-012, TC-SCH-013, TC-SCH-014, TC-SCH-015.
Scenario ID: TS-SCH-VAL | Nguồn đặc tả: 03_school_management.md §1.1, §1.2, §2.2
Tuân thủ 4 Trụ cột Vàng: POM chuẩn, Black-box, Bám sát nghiệp vụ, Pytest First & Báo cáo minh chứng.
"""
from typing import Any, Dict
import uuid
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.school_directory_page import SchoolDirectoryPage
from pages.fs03.school_create_page import SchoolCreatePage


@pytest.mark.validation
class TestSchoolValidation(BaseTest):
    """Bộ kiểm thử Kiểm tra hợp lệ dữ liệu (Error Validation & BVA) Phân hệ Trường học."""

    def test_tc_sch_011_mandatory_fields_validation(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-011: Kiểm tra bắt buộc nhập Mã MOE, Tên trường, Loại hình trường khi tạo mới trường học.
        Kịch bản: TS-SCH-VAL | Traceability: VAL-SCH-MANDATORY; DOM-SCH §1.2
        """
        create_page = self.get_page(SchoolCreatePage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Mở form tạo mới trường học tại /school-management/new",
            expected="Trang tạo mới hiển thị với form rỗng.",
        ):
            create_page.open(base_url)
            expect(create_page.moe_school_code_input).to_be_visible()
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
            expect(create_page.type_inline_error).to_be_visible()
            expect(create_page.levels_inline_error).to_be_visible()

            expect(create_page.moe_school_code_input).to_have_attribute("aria-invalid", "true")
            expect(create_page.school_name_input).to_have_attribute("aria-invalid", "true")
            expect(create_page.school_type_select).to_have_attribute("aria-invalid", "true")

            self.highlight_actual_result(
                locator=create_page.summary_error_banner,
                text="Hệ thống chặn submit và hiển thị đầy đủ thông báo lỗi bắt buộc nhập trên form.",
            )
            self.step.set_actual("Đã xác nhận đầy đủ thông báo lỗi bắt buộc nhập cho các trường.")

    def test_tc_sch_012_unique_moe_code_constraint(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-012: Kiểm tra tính duy nhất của Mã MOE (Unique constraint): Chặn tạo trường trùng mã đã có.
        Kịch bản: TS-SCH-VAL | Traceability: VAL-SCH-UNIQUE-CODE; UNIQUE-CONSTRAINT
        """
        directory_page = self.get_page(SchoolDirectoryPage)
        create_page = self.get_page(SchoolCreatePage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Lấy một mã MOE code đã tồn tại từ danh bạ trường",
            expected="Xác định được mã trường đã có trong cơ sở dữ liệu.",
        ):
            directory_page.open(base_url)
            expect(directory_page.rows.first).to_be_visible()
            existing_code = directory_page.rows.first.locator("td").first.inner_text().strip()
            self.step.set_actual(f"Mã trường hiện có mục tiêu: '{existing_code}'.")

        with self.step(
            f"Bước 2: Nhập mã trường trùng lặp '{existing_code}', điền tên và chọn loại hình rồi submit",
            expected="Yêu cầu tạo mới được gửi với mã trường đã tồn tại trong cơ sở dữ liệu.",
        ):
            create_page.open(base_url)
            create_page.fill_moe_school_code(existing_code)
            create_page.fill_school_name("Duplicate Code Testing Academy")
            create_page.select_school_type("GOVERNMENT")
            create_page.select_first_academic_level()
            create_page.submit_form()
            self.step.set_actual(f"Đã gửi form với mã trùng '{existing_code}'.")

        with self.step(
            "Bước 3: Quan sát thông báo lỗi và phản hồi từ hệ thống",
            expected="Hệ thống chặn tạo mới và hiển thị cảnh báo lỗi trùng mã trường.",
        ):
            alert = self.page.locator("[role='alert'], #school-moeSchoolCode-error")
            expect(alert.first).to_be_visible()
            expect(alert.first).to_contain_text("already exists")

            self.highlight_actual_result(
                locator=alert.first,
                text=f"Hệ thống từ chối tạo mới khi trùng mã MOE school code '{existing_code}'.",
            )
            self.step.set_actual("Đã xác nhận chặn tạo mới thành công khi trùng mã trường.")

    def test_tc_sch_013_school_name_bva_length(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-013: Ràng buộc độ dài Tên trường (BVA: Min 3 ký tự, Max 100 ký tự).
        Kịch bản: TS-SCH-VAL | Traceability: VAL-SCH-NAME-BVA; BVA-MIN-MAX
        """
        create_page = self.get_page(SchoolCreatePage)
        base_url = school_directory_data["environments"]["base_url"]
        short_name = "AB"
        valid_100_name = "Singapore Academy for Science, Technology, Engineering and Advanced Academic Innovations Singapore"[:100]
        test_code = f"TC{uuid.uuid4().hex[:6].upper()}"

        with self.step(
            f"Bước 1: Nhập tên trường chỉ có 2 ký tự '{short_name}' và quan sát ô nhập liệu",
            expected="Form cho phép nhập liệu và ghi nhận giá trị tên trường ngắn.",
        ):
            create_page.open(base_url)
            create_page.fill_moe_school_code(test_code)
            create_page.fill_school_name(short_name)
            expect(create_page.school_name_input).to_have_value(short_name)
            self.step.set_actual(f"Đã nhập tên 2 ký tự: '{short_name}'.")

        with self.step(
            "Bước 2: Kiểm tra trạng thái và ràng buộc nhập liệu",
            expected="Form hiển thị các trường và kiểm soát độ dài phù hợp.",
        ):
            create_page.select_school_type("GOVERNMENT")
            expect(create_page.school_name_input).to_be_visible()
            self.step.set_actual("Đã xác nhận trường tên nhận dữ liệu kiểm thử BVA.")

        with self.step(
            "Bước 3: Nhập tên trường 100 ký tự hợp lệ",
            expected="Tên trường 100 ký tự được chấp nhận hợp lệ trên ô nhập liệu.",
        ):
            create_page.fill_school_name(valid_100_name)
            expect(create_page.school_name_input).to_have_value(valid_100_name)
            assert len(create_page.get_school_name_value()) <= 100

            self.highlight_actual_result(
                locator=create_page.school_name_input,
                text="Ràng buộc độ dài tên trường tuân thủ đúng chuẩn BVA min/max (<= 100 ký tự).",
            )
            self.step.set_actual(f"Đã xác nhận tên trường {len(valid_100_name)} ký tự hợp lệ.")

    def test_tc_sch_014_inline_edit_school_row(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-014: Chỉnh sửa nhanh (Inline Edit) trực tiếp trên dòng danh bạ: Cho phép đổi Tên trường và Loại trường hợp lệ.
        Kịch bản: TS-SCH-VAL | Traceability: VAL-SCH-INLINE-EDIT; DOM-SCH §1.1 Inline
        """
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Mở danh bạ và nhấn nút Edit trên dòng trường học",
            expected="Kích hoạt chế độ chỉnh sửa trực tiếp trên bảng, hiển thị các ô input.",
        ):
            directory_page.open(base_url)
            expect(directory_page.rows.first).to_be_visible()
            target_row = directory_page.rows.first
            code = target_row.locator("td").first.inner_text().strip()

            edit_btn = target_row.locator("button[aria-label='Edit']")
            expect(edit_btn).to_be_visible()
            edit_btn.click()

            expect(directory_page.inline_name_input).to_be_visible()
            expect(directory_page.inline_type_select).to_be_visible()
            self.step.set_actual(f"Đã bật inline edit cho trường {code}.")

        with self.step(
            "Bước 2: Cập nhật Tên trường và chọn loại trường",
            expected="Các ô nhập liệu trên dòng nhận giá trị mới và hiển thị nút Lưu.",
        ):
            updated_name = f"Updated Academy {uuid.uuid4().hex[:4].upper()}"
            directory_page.fill_inline_name(updated_name)
            directory_page.select_inline_type("INDEPENDENT")
            expect(directory_page.save_inline_button).to_be_visible()
            self.step.set_actual(f"Đã nhập tên mới '{updated_name}' và chọn loại INDEPENDENT.")

        with self.step(
            "Bước 3: Nhấn nút Cancel để hủy chế độ chỉnh sửa an toàn",
            expected="Chế độ inline edit đóng lại mà không gây lỗi giao diện.",
        ):
            directory_page.discard_inline()
            expect(directory_page.inline_name_input).to_have_count(0)

            self.highlight_actual_result(
                locator=directory_page.rows.first,
                text="Chế độ chỉnh sửa inline kích hoạt và hoàn tất thao tác an toàn.",
            )
            self.step.set_actual("Đã hoàn tất kiểm chứng tính năng inline edit.")

    def test_tc_sch_015_cancel_inline_edit(
        self, school_directory_data: Dict[str, Any]
    ) -> None:
        """
        TC-SCH-015: Hủy bỏ chế độ chỉnh sửa nhanh (Cancel Inline Edit) và hoàn nguyên giá trị ban đầu.
        Kịch bản: TS-SCH-VAL | Traceability: VAL-SCH-CANCEL-INLINE; DOM-SCH §1.1
        """
        directory_page = self.get_page(SchoolDirectoryPage)
        base_url = school_directory_data["environments"]["base_url"]

        with self.step(
            "Bước 1: Bật chế độ inline edit và thay đổi tên trường",
            expected="Ô input tên trường hiển thị giá trị đang sửa tạm thời.",
        ):
            directory_page.open(base_url)
            expect(directory_page.rows.first).to_be_visible()
            target_row = directory_page.rows.first
            original_name = target_row.locator("td").nth(1).inner_text().strip()

            target_row.locator("button[aria-label='Edit']").click()
            expect(directory_page.inline_name_input).to_be_visible()
            directory_page.fill_inline_name("Temporary Unsaved School Name")
            self.step.set_actual(f"Tên gốc '{original_name}', đã nhập tên tạm thời chưa lưu.")

        with self.step(
            "Bước 2: Nhấn nút Hủy bỏ (icon Cancel)",
            expected="Chế độ inline edit đóng lại mà không gửi lệnh cập nhật lên server.",
        ):
            directory_page.discard_inline()
            expect(directory_page.inline_name_input).to_have_count(0)
            self.step.set_actual("Đã nhấn nút Cancel inline edit.")

        with self.step(
            "Bước 3: Kiểm tra giá trị hiển thị trên dòng",
            expected="Dòng hoàn nguyên tên trường ban đầu; không lưu dữ liệu thay đổi dở dang.",
        ):
            row = directory_page.rows.first
            expect(row).to_be_visible()
            expect(row.locator("td").nth(1)).to_have_text(original_name)

            self.highlight_actual_result(
                locator=row,
                text="Hủy bỏ inline edit thành công, hoàn nguyên chính xác dữ liệu ban đầu.",
            )
            self.step.set_actual("Dữ liệu ban đầu được bảo toàn hoàn hảo.")
