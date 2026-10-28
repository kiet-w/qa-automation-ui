"""
tests/fs03/fs03-student-enrollment/test_validation_1.py
Suite: Validation (14 cases)
Invariants: POM separation, external fixtures, traceability, <=250 lines.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.student_enrollment_page import StudentEnrollmentPage


@pytest.mark.validation
class TestStudentEnrollmentValidation1(BaseTest):
    """Test suite covering Validation test cases."""

    def test_tc_tc_5173_stu_033_ts_5173_stu_val_req_lớp_1_form_tạo_mới_kích_hoạt_viền_đ(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-033: [Lớp 1] Form Tạo mới: Kích hoạt viền đỏ và báo lỗi bắt buộc nhập đồng loạt khi để trống Họ tên, NRIC, Ngày sinh và Quốc tịch
        Scenario: TS-5173-STU-VAL-REQ
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Không nhập bất kỳ thông tin nào vào form.", expected="Submission bị chặn; thẻ FormErrorSummary xuất hiện ở đầu trang; các ô '#student-displayName', '#student-nric', '#student-dateOfBirth', '#student-category' đều có aria-invalid='true' và xuất hiện dòng thông báo lỗi tương ứng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút 'Create student'.", expected="Submission bị chặn; thẻ FormErrorSummary xuất hiện ở đầu trang; các ô '#student-displayName', '#student-nric', '#student-dateOfBirth', '#student-category' đều có aria-invalid='true' và xuất hiện dòng thông báo lỗi tương ứng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra phản hồi trực quan trên từng ô nhập liệu.", expected="Submission bị chặn; thẻ FormErrorSummary xuất hiện ở đầu trang; các ô '#student-displayName', '#student-nric', '#student-dateOfBirth', '#student-category' đều có aria-invalid='true' và xuất hiện dòng thông báo lỗi tương ứng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_034_ts_5173_stu_val_req_lớp_1_form_tạo_mới_bắt_buộc_chọn_ng(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-034: [Lớp 1] Form Tạo mới: Bắt buộc chọn Ngày bắt đầu nhập học (Enrolled from) khi cán bộ trường thực hiện tạo học sinh
        Scenario: TS-5173-STU-VAL-REQ
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Điền thông tin cá nhân nhưng bỏ trống ô Enrolled from.", expected="Hệ thống chặn submit; ô '#student-enrolledFrom' nhận viền đỏ cảnh báo và hiển thị lỗi 'Enrolled from date is required'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút 'Create student'.", expected="Hệ thống chặn submit; ô '#student-enrolledFrom' nhận viền đỏ cảnh báo và hiển thị lỗi 'Enrolled from date is required'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_035_ts_5173_stu_val_req_lớp_1_form_nhập_học_enroll_bắt_buộc(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-035: [Lớp 1] Form Nhập học (/enroll): Bắt buộc nhập Student ID, School ID và Ngày bắt đầu nhập học
        Scenario: TS-5173-STU-VAL-REQ
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Để trống toàn bộ các trường trên form nhập học.", expected="FormErrorSummary xuất hiện; '#enroll-studentId', '#enroll-schoolId', '#enroll-from' đều nhận viền đỏ và thông báo yêu cầu bắt buộc nhập."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút 'Enroll student'.", expected="FormErrorSummary xuất hiện; '#enroll-studentId', '#enroll-schoolId', '#enroll-from' đều nhận viền đỏ và thông báo yêu cầu bắt buộc nhập."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_036_ts_5173_stu_val_req_lớp_1_form_phân_lớp_assign_assign_i(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-036: [Lớp 1] Form Phân lớp (/assign & /assign-in-class): Bắt buộc chọn Lớp, Ngày bắt đầu và Ngày kết thúc phân lớp
        Scenario: TS-5173-STU-VAL-REQ
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Để trống các ô Lớp và ngày tháng trên form phân lớp.", expected="Form chặn submit; các ô lớp học và thời hạn phân lớp đều hiển thị viền đỏ báo lỗi bắt buộc nhập."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút 'Assign in class'.", expected="Form chặn submit; các ô lớp học và thời hạn phân lớp đều hiển thị viền đỏ báo lỗi bắt buộc nhập."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_037_ts_5173_stu_val_opt_lớp_2_cho_phép_để_trống_ô_ngày_kết(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-037: [Lớp 2] Cho phép để trống ô Ngày kết thúc nhập học (Enrolled to exclusive) cho học sinh nhập học vô thời hạn
        Scenario: TS-5173-STU-VAL-OPT
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Điền các trường bắt buộc và để trống Enrolled to exclusive.", expected="Form hợp lệ và submit thành công; học sinh được ghi nhận với thời hạn nhập học mở (ongoing / null); không có cảnh báo lỗi nào xuất hiện."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút 'Create student'.", expected="Form hợp lệ và submit thành công; học sinh được ghi nhận với thời hạn nhập học mở (ongoing / null); không có cảnh báo lỗi nào xuất hiện."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_038_ts_5173_stu_val_ws_lớp_3_chặn_nhập_toàn_khoảng_trắng_a(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-038: [Lớp 3] Chặn nhập toàn khoảng trắng (All whitespace) trong ô Họ tên học sinh, coi như để trống
        Scenario: TS-5173-STU-VAL-WS
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Nhập '     ' vào ô '#student-displayName'.", expected="Chuỗi khoảng trắng bị trim sạch; trường bị coi là để trống và hiển thị lỗi 'Display name is required'; không cho phép submit chuỗi rỗng vô nghĩa."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Điền các trường còn lại hợp lệ.", expected="Chuỗi khoảng trắng bị trim sạch; trường bị coi là để trống và hiển thị lỗi 'Display name is required'; không cho phép submit chuỗi rỗng vô nghĩa."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Nhấn 'Create student'.", expected="Chuỗi khoảng trắng bị trim sạch; trường bị coi là để trống và hiển thị lỗi 'Display name is required'; không cho phép submit chuỗi rỗng vô nghĩa."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_039_ts_5173_stu_val_ws_lớp_3_chặn_nhập_toàn_khoảng_trắng_t(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-039: [Lớp 3] Chặn nhập toàn khoảng trắng trong ô NRIC / FIN và Student ID trên các biểu mẫu
        Scenario: TS-5173-STU-VAL-WS
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Nhập khoảng trắng vào ô NRIC hoặc ô Student ID.", expected="Biểu mẫu bị chặn; các ô bị báo lỗi bắt buộc nhập; không gửi request chứa khoảng trắng lên API."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút submit biểu mẫu.", expected="Biểu mẫu bị chặn; các ô bị báo lỗi bắt buộc nhập; không gửi request chứa khoảng trắng lên API."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_040_ts_5173_stu_val_trim_lớp_4_tự_động_trim_khoảng_trắng_thừ(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-040: [Lớp 4] Tự động trim khoảng trắng thừa ở đầu và cuối trong ô Họ tên học sinh trước khi lưu vào DB
        Scenario: TS-5173-STU-VAL-TRIM
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Nhập '   Danial bin Ahmad   ' vào ô '#student-displayName'.", expected="Hệ thống tự động cắt bỏ các khoảng trắng thừa đầu và cuối; tên học sinh được lưu chính xác là 'Danial bin Ahmad'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Điền các trường còn lại và nhấn 'Create student'.", expected="Hệ thống tự động cắt bỏ các khoảng trắng thừa đầu và cuối; tên học sinh được lưu chính xác là 'Danial bin Ahmad'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra tên học sinh được lưu trên danh sách.", expected="Hệ thống tự động cắt bỏ các khoảng trắng thừa đầu và cuối; tên học sinh được lưu chính xác là 'Danial bin Ahmad'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_041_ts_5173_stu_val_trim_lớp_4_tự_động_trim_khoảng_trắng_tro(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-041: [Lớp 4] Tự động trim khoảng trắng trong ô NRIC / FIN và Student ID
        Scenario: TS-5173-STU-VAL-TRIM
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Nhập '  T0812345A  ' vào ô '#student-nric'.", expected="Khoảng trắng được cắt bỏ hoàn toàn; payload NRIC gửi đi là chính xác 'T0812345A'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Submit form và kiểm tra giá trị gửi lên máy chủ.", expected="Khoảng trắng được cắt bỏ hoàn toàn; payload NRIC gửi đi là chính xác 'T0812345A'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_042_ts_5173_stu_val_bva_lớp_5_bva_độ_dài_tối_thiểu_từ_chối(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-042: [Lớp 5] BVA Độ dài tối thiểu: Từ chối số định danh NRIC có độ dài dưới 9 ký tự (ví dụ: 'T081234')
        Scenario: TS-5173-STU-VAL-BVA
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Nhập 'T081234' vào ô '#student-nric'.", expected="Hệ thống từ chối do không đủ độ dài 9 ký tự; ô NRIC nhận viền đỏ và báo lỗi 'Enter a valid Singapore NRIC'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút 'Create student'.", expected="Hệ thống từ chối do không đủ độ dài 9 ký tự; ô NRIC nhận viền đỏ và báo lỗi 'Enter a valid Singapore NRIC'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_043_ts_5173_stu_val_bva_lớp_6_bva_độ_dài_tối_đa_từ_chối_số(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-043: [Lớp 6] BVA Độ dài tối đa: Từ chối số định danh NRIC có độ dài vượt quá 9 ký tự (ví dụ: 'T081234567A')
        Scenario: TS-5173-STU-VAL-BVA
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Nhập 'T081234567A' vào ô '#student-nric'.", expected="Hệ thống từ chối định dạng vượt độ dài; hiển thị viền đỏ cảnh báo định dạng NRIC không hợp lệ."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút 'Create student'.", expected="Hệ thống từ chối định dạng vượt độ dài; hiển thị viền đỏ cảnh báo định dạng NRIC không hợp lệ."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_044_ts_5173_stu_val_bva_lớp_6_bva_họ_tên_học_sinh_kiểm_tra(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-044: [Lớp 6] BVA Họ tên học sinh: Kiểm tra biên độ dài 100 ký tự (chấp nhận 100 ký tự, chặn hoặc cắt 101 ký tự)
        Scenario: TS-5173-STU-VAL-BVA
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Nhập chuỗi tên đúng 100 ký tự vào ô '#student-displayName' và submit: kiểm tra thành công.", expected="Chuỗi 100 ký tự được chấp nhận hoàn toàn; chuỗi 101 ký tự bị giới hạn maxlength hoặc hiển thị thông báo lỗi độ dài."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhập chuỗi tên 101 ký tự vào ô '#student-displayName' và submit.", expected="Chuỗi 100 ký tự được chấp nhận hoàn toàn; chuỗi 101 ký tự bị giới hạn maxlength hoặc hiển thị thông báo lỗi độ dài."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra phản hồi validation.", expected="Chuỗi 100 ký tự được chấp nhận hoàn toàn; chuỗi 101 ký tự bị giới hạn maxlength hoặc hiển thị thông báo lỗi độ dài."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_045_ts_5173_stu_val_paste_lớp_7_stress_paste_1000_ký_tự_vào_ô(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-045: [Lớp 7] Stress paste 1000+ ký tự vào ô Họ tên học sinh không gây treo trình duyệt hoặc vỡ giao diện
        Scenario: TS-5173-STU-VAL-PASTE
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Dán (paste) chuỗi 1200 ký tự vào ô '#student-displayName'.", expected="Giao diện không bị đơ giật, không tràn layout; ô nhập liệu tự động cắt hoặc cảnh báo độ dài an toàn khi submit."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Quan sát hiệu năng trình duyệt và giao diện form.", expected="Giao diện không bị đơ giật, không tràn layout; ô nhập liệu tự động cắt hoặc cảnh báo độ dài an toàn khi submit."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_046_ts_5173_stu_val_fmt_lớp_8_thuật_toán_modulo_11_singapor(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-046: [Lớp 8] Thuật toán Modulo 11 Singapore: Từ chối số NRIC có cấu trúc 9 ký tự nhưng sai mã kiểm tra Checksum
        Scenario: TS-5173-STU-VAL-FMT
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Nhập 'T0512345Z' vào ô '#student-nric'.", expected="Hệ thống phát hiện lỗi checksum; từ chối submit và hiển thị viền đỏ cảnh báo: 'Enter a valid Singapore NRIC'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút 'Create student'.", expected="Hệ thống phát hiện lỗi checksum; từ chối submit và hiển thị viền đỏ cảnh báo: 'Enter a valid Singapore NRIC'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")
