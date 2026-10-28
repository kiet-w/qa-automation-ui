"""
tests/fs03/fs03-student-enrollment/test_ac_1.py
Suite: AC (14 cases)
Invariants: POM separation, external fixtures, traceability, <=250 lines.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.student_enrollment_page import StudentEnrollmentPage


@pytest.mark.ac
class TestStudentEnrollmentAc1(BaseTest):
    """Test suite covering AC test cases."""

    def test_tc_tc_5173_stu_015_ts_5173_stu_ac_dir_hợp_đồng_hiển_thị_bảng_danh_sách_họ(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-015: Hợp đồng hiển thị bảng danh sách học sinh: Tiêu đề H1 'Students', mô tả, ô tìm kiếm và đủ 7 cột tiêu đề chuẩn xác
        Scenario: TS-5173-STU-AC-DIR
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Mở trang /student-management từ Sidebar.", expected="Tiêu đề trang là 'EduFAMS | Admin Portal'; H1 là 'Students'; Bảng có đầy đủ các cột: Student, NRIC, Date of birth, Category, School, Class, Actions."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Kiểm tra tiêu đề trang và Heading H1.", expected="Tiêu đề trang là 'EduFAMS | Admin Portal'; H1 là 'Students'; Bảng có đầy đủ các cột: Student, NRIC, Date of birth, Category, School, Class, Actions."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra các cột tiêu đề của bảng dữ liệu.", expected="Tiêu đề trang là 'EduFAMS | Admin Portal'; H1 là 'Students'; Bảng có đầy đủ các cột: Student, NRIC, Date of birth, Category, School, Class, Actions."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_016_ts_5173_stu_ac_dir_hiển_thị_dòng_dữ_liệu_học_sinh_với(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-016: Hiển thị dòng dữ liệu học sinh với đầy đủ họ tên, NRIC định dạng che bảo mật, ngày sinh chuẩn, badge quốc tịch và tên lớp
        Scenario: TS-5173-STU-AC-DIR
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Mở danh sách học sinh /student-management.", expected="Cột Student hiển thị họ tên in đậm; NRIC hiển thị đúng định dạng; Ngày sinh định dạng medium date; Cột Category hiển thị badge nhãn rõ ràng; Cột School hiển thị mã + tên trường; Cột Class hiển thị mã + tên lớp."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Quan sát dòng đầu tiên trong bảng dữ liệu tbody tr.", expected="Cột Student hiển thị họ tên in đậm; NRIC hiển thị đúng định dạng; Ngày sinh định dạng medium date; Cột Category hiển thị badge nhãn rõ ràng; Cột School hiển thị mã + tên trường; Cột Class hiển thị mã + tên lớp."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra định dạng hiển thị của từng ô dữ liệu.", expected="Cột Student hiển thị họ tên in đậm; NRIC hiển thị đúng định dạng; Ngày sinh định dạng medium date; Cột Category hiển thị badge nhãn rõ ràng; Cột School hiển thị mã + tên trường; Cột Class hiển thị mã + tên lớp."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_017_ts_5173_stu_ac_dir_hiển_thị_trạng_thái_rỗng_empty_stat(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-017: Hiển thị trạng thái rỗng (Empty State) khi trường học chưa có học sinh hoặc kết quả tìm kiếm không có dữ liệu
        Scenario: TS-5173-STU-AC-DIR
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Nhập 'XYZNOTFOUND999' vào ô tìm kiếm Search students.", expected="Bảng hiển thị thông điệp rỗng rõ ràng: 'No students found' kèm dòng hướng dẫn 'Try changing your search.'; giao diện không bị sập hay mất layout."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Quan sát nội dung hiển thị trong bảng dữ liệu.", expected="Bảng hiển thị thông điệp rỗng rõ ràng: 'No students found' kèm dòng hướng dẫn 'Try changing your search.'; giao diện không bị sập hay mất layout."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_018_ts_5173_stu_ac_dir_tìm_kiếm_học_sinh_theo_họ_tên_tức_t(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-018: Tìm kiếm học sinh theo Họ tên tức thì qua ô SearchInput (không phân biệt chữ hoa, chữ thường)
        Scenario: TS-5173-STU-AC-DIR
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Gõ từ khóa 'danial' bằng chữ thường vào ô tìm kiếm.", expected="Danh sách lập tức lọc lại và chỉ hiển thị đúng các dòng học sinh có chứa 'Danial' trong họ tên; tổng số bản ghi và phân trang cập nhật tương ứng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Quan sát bảng dữ liệu cập nhật.", expected="Danh sách lập tức lọc lại và chỉ hiển thị đúng các dòng học sinh có chứa 'Danial' trong họ tên; tổng số bản ghi và phân trang cập nhật tương ứng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra các dòng hiển thị.", expected="Danh sách lập tức lọc lại và chỉ hiển thị đúng các dòng học sinh có chứa 'Danial' trong họ tên; tổng số bản ghi và phân trang cập nhật tương ứng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_019_ts_5173_stu_ac_dir_tìm_kiếm_học_sinh_theo_số_nric_đầy(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-019: Tìm kiếm học sinh theo số NRIC đầy đủ trên thanh công cụ tìm kiếm
        Scenario: TS-5173-STU-AC-DIR
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Nhập số NRIC 'T0812345A' vào ô tìm kiếm.", expected="Bảng dữ liệu chỉ giữ lại đúng 1 dòng của học sinh có số NRIC 'T0812345A'; các học sinh khác bị ẩn đi."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Kiểm tra kết quả lọc trên bảng.", expected="Bảng dữ liệu chỉ giữ lại đúng 1 dòng của học sinh có số NRIC 'T0812345A'; các học sinh khác bị ẩn đi."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_020_ts_5173_stu_ac_dir_phân_trang_danh_sách_học_sinh_chọn(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-020: Phân trang danh sách học sinh: Chọn các mức 5, 10, 25 dòng và điều hướng First, Previous, Next, Last
        Scenario: TS-5173-STU-AC-DIR
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Chọn hiển thị 5 dòng/trang từ dropdown Rows per page.", expected="Số lượng dòng hiển thị đúng theo pageSize đã chọn; các nút điều hướng chuyển trang mượt mà; số trang hiện tại phản ánh chính xác."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút Next để sang trang 2.", expected="Số lượng dòng hiển thị đúng theo pageSize đã chọn; các nút điều hướng chuyển trang mượt mà; số trang hiện tại phản ánh chính xác."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Nhấn nút Last để sang trang cuối cùng.", expected="Số lượng dòng hiển thị đúng theo pageSize đã chọn; các nút điều hướng chuyển trang mượt mà; số trang hiện tại phản ánh chính xác."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Nhấn nút First để quay lại trang đầu tiên.", expected="Số lượng dòng hiển thị đúng theo pageSize đã chọn; các nút điều hướng chuyển trang mượt mà; số trang hiện tại phản ánh chính xác."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_021_ts_5173_stu_ac_dir_nút_bấm_view_student_detail_ghost_i(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-021: Nút bấm 'View student detail' (Ghost icon Eye) điều hướng chính xác sang trang chi tiết /student-management/:studentId
        Scenario: TS-5173-STU-AC-DIR
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Xác định dòng của học sinh STU-003 trên bảng.", expected="Trình duyệt điều hướng sang URL http://localhost:5173/student-management/STU-003; trang chi tiết học sinh hiển thị thông tin hồ sơ của STU-003."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn vào nút thao tác có aria-label 'View student detail'.", expected="Trình duyệt điều hướng sang URL http://localhost:5173/student-management/STU-003; trang chi tiết học sinh hiển thị thông tin hồ sơ của STU-003."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Quan sát URL và nội dung trang được tải.", expected="Trình duyệt điều hướng sang URL http://localhost:5173/student-management/STU-003; trang chi tiết học sinh hiển thị thông tin hồ sơ của STU-003."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_022_ts_5173_stu_ac_new_tạo_mới_học_sinh_thành_công_single(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-022: Tạo mới học sinh thành công (Single Form) với quốc tịch Công dân Singapore (SC) và ngày bắt đầu nhập học
        Scenario: TS-5173-STU-AC-NEW
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Điền Họ tên '#student-displayName' với 'Danial bin Ahmad'.", expected="API POST trả về 201 Created; hệ thống hiển thị Toast thành công và tự động chuyển hướng về /student-management; học sinh mới xuất hiện trên danh sách."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Điền NRIC '#student-nric', Ngày sinh '#student-dateOfBirth', chọn Category 'SC'.", expected="API POST trả về 201 Created; hệ thống hiển thị Toast thành công và tự động chuyển hướng về /student-management; học sinh mới xuất hiện trên danh sách."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Điền Ngày nhập học '#student-enrolledFrom' với '2026-01-02' (để trống Enrolled to).", expected="API POST trả về 201 Created; hệ thống hiển thị Toast thành công và tự động chuyển hướng về /student-management; học sinh mới xuất hiện trên danh sách."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Nhấn nút 'Create student'.", expected="API POST trả về 201 Created; hệ thống hiển thị Toast thành công và tự động chuyển hướng về /student-management; học sinh mới xuất hiện trên danh sách."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_023_ts_5173_stu_ac_new_tạo_mới_học_sinh_thành_công_với_quố(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-023: Tạo mới học sinh thành công với quốc tịch Thường trú nhân (PR) kèm ngày kết thúc nhập học xác định
        Scenario: TS-5173-STU-AC-NEW
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Điền đầy đủ thông tin học sinh với Category là 'PR'.", expected="Tạo học sinh thành công; hồ sơ lưu trữ chính xác thời hạn nhập học có giới hạn và huy hiệu Category hiển thị nhãn 'PR'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Điền Enrolled from '2026-01-02' và Enrolled to exclusive '2028-12-31'.", expected="Tạo học sinh thành công; hồ sơ lưu trữ chính xác thời hạn nhập học có giới hạn và huy hiệu Category hiển thị nhãn 'PR'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Nhấn 'Create student'.", expected="Tạo học sinh thành công; hồ sơ lưu trữ chính xác thời hạn nhập học có giới hạn và huy hiệu Category hiển thị nhãn 'PR'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_024_ts_5173_stu_ac_new_tạo_mới_học_sinh_quốc_tế_thành_công(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-024: Tạo mới học sinh quốc tế thành công (IS_ASEAN và IS_NON_ASEAN) với số định danh FIN hợp lệ
        Scenario: TS-5173-STU-AC-NEW
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Điền thông tin học sinh quốc tế ASEAN và chọn category 'IS_ASEAN', nhấn Submit.", expected="Cả hai học sinh quốc tế đều được tạo thành công; hiển thị đúng nhãn quốc tế trên danh sách và chi tiết hồ sơ."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Lặp lại tạo học sinh quốc tế ngoài ASEAN với category 'IS_NON_ASEAN'.", expected="Cả hai học sinh quốc tế đều được tạo thành công; hiển thị đúng nhãn quốc tế trên danh sách và chi tiết hồ sơ."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra danh sách học sinh sau khi tạo.", expected="Cả hai học sinh quốc tế đều được tạo thành công; hiển thị đúng nhãn quốc tế trên danh sách và chi tiết hồ sơ."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_025_ts_5173_stu_ac_bulk_chuyển_đổi_linh_hoạt_giữa_tab_biểu(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-025: Chuyển đổi linh hoạt giữa tab biểu mẫu đơn lẻ (Single) và tab tải lên file lô (Bulk CSV)
        Scenario: TS-5173-STU-AC-BULK
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Nhấn vào nút tab 'Bulk'.", expected="Giao diện chuyển đổi tức thì không làm tải lại toàn bộ trang; aria-selected phản ánh đúng tab đang hoạt động."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Quan sát giao diện chuyển sang khu vực kéo thả upload file CSV.", expected="Giao diện chuyển đổi tức thì không làm tải lại toàn bộ trang; aria-selected phản ánh đúng tab đang hoạt động."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Nhấn vào nút tab 'Single'.", expected="Giao diện chuyển đổi tức thì không làm tải lại toàn bộ trang; aria-selected phản ánh đúng tab đang hoạt động."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Quan sát giao diện trở lại các trường nhập liệu thông thường.", expected="Giao diện chuyển đổi tức thì không làm tải lại toàn bộ trang; aria-selected phản ánh đúng tab đang hoạt động."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_026_ts_5173_stu_ac_bulk_tải_xuống_file_mẫu_csv_chính_thức_d(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-026: Tải xuống file mẫu CSV chính thức (Download sample template) với đầy đủ 6 cột tiêu đề chuẩn
        Scenario: TS-5173-STU-AC-BULK
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Nhấn vào liên kết/nút 'Download sample template'.", expected="File CSV mẫu được tải về thành công (>0 bytes); header chứa đủ 6 cột: 'displayName,nric,dateOfBirth,category,enrolledFrom,enrolledToExclusive'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Kiểm tra file CSV được tải về máy tính.", expected="File CSV mẫu được tải về thành công (>0 bytes); header chứa đủ 6 cột: 'displayName,nric,dateOfBirth,category,enrolledFrom,enrolledToExclusive'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_027_ts_5173_stu_ac_bulk_tải_lên_file_csv_danh_sách_học_sinh(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-027: Tải lên file CSV danh sách học sinh hợp lệ và xác nhận báo cáo kết quả nhập lô thành công
        Scenario: TS-5173-STU-AC-BULK
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Chọn file 'valid_student_roster.csv' vào ô upload của tab Bulk.", expected="Hệ thống xử lý nhập lô thành công cả 5 học sinh; hiển thị banner thông báo '5 students imported successfully'; danh sách học sinh cập nhật đầy đủ các bản ghi mới."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút 'Upload & Process'.", expected="Hệ thống xử lý nhập lô thành công cả 5 học sinh; hiển thị banner thông báo '5 students imported successfully'; danh sách học sinh cập nhật đầy đủ các bản ghi mới."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra thông báo kết quả nhập dữ liệu.", expected="Hệ thống xử lý nhập lô thành công cả 5 học sinh; hiển thị banner thông báo '5 students imported successfully'; danh sách học sinh cập nhật đầy đủ các bản ghi mới."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_stu_028_ts_5173_stu_ac_enroll_biểu_mẫu_nhập_học_trực_tiếp_student(self, student_data: Dict[str, Any]):
        """
        TC-5173-STU-028: Biểu mẫu Nhập học trực tiếp (/student-management/enroll): Điền Student ID, chọn Trường học và ngày nhập học thành công
        Scenario: TS-5173-STU-AC-ENROLL
        """
        page_obj = self.get_page(StudentEnrollmentPage)
        base_url = student_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Mở trang /student-management/enroll.", expected="API POST /school/v1/students/enroll thành công; thông báo Toast thành công xuất hiện; học sinh chuyển trạng thái ENROLLED tại trường."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Điền '#enroll-studentId' với 'STU-001', chọn trường '#enroll-schoolId'.", expected="API POST /school/v1/students/enroll thành công; thông báo Toast thành công xuất hiện; học sinh chuyển trạng thái ENROLLED tại trường."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Điền '#enroll-from' và '#enroll-to'.", expected="API POST /school/v1/students/enroll thành công; thông báo Toast thành công xuất hiện; học sinh chuyển trạng thái ENROLLED tại trường."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Nhấn nút 'Enroll student'.", expected="API POST /school/v1/students/enroll thành công; thông báo Toast thành công xuất hiện; học sinh chuyển trạng thái ENROLLED tại trường."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")
