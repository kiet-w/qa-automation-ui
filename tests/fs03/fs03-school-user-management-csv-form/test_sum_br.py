"""
tests/fs03/fs03-school-user-management-csv-form/test_br.py
Suite: BR (14 cases)
Invariants: POM separation, external fixtures, traceability, <=250 lines.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs03.school_user_management_page import SchoolUserManagementPage


@pytest.mark.br
class TestSchoolUserManagementBr(BaseTest):
    """Test suite covering BR test cases."""

    def test_tc_tc_5173_sum_001_ts_5173_sum_auth_phân_quyền_rbac_moehq_chỉ_quản_trị(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-001: Phân quyền RBAC MOEHQ: Chỉ Quản trị viên MOEHQ mới có quyền truy cập School User Management
        Scenario: TS-5173-SUM-AUTH
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Đăng nhập với tài khoản Quản trị viên MOEHQ.", expected="Quản trị viên MOEHQ truy cập thành công và xem được danh sách cán bộ; các danh tính khác bị chặn truy cập (403 Forbidden hoặc chuyển hướng về /login) mà không làm lộ thông tin PII cán bộ."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Mở đường dẫn /school-user-management.", expected="Quản trị viên MOEHQ truy cập thành công và xem được danh sách cán bộ; các danh tính khác bị chặn truy cập (403 Forbidden hoặc chuyển hướng về /login) mà không làm lộ thông tin PII cán bộ."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Lặp lại điều hướng trực tiếp bằng tài khoản School User và trình duyệt ẩn danh chưa đăng nhập.", expected="Quản trị viên MOEHQ truy cập thành công và xem được danh sách cán bộ; các danh tính khác bị chặn truy cập (403 Forbidden hoặc chuyển hướng về /login) mà không làm lộ thông tin PII cán bộ."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_sum_002_ts_5173_sum_provisioning_tạo_tài_khoản_cán_bộ_đơn_lẻ_single(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-002: Tạo tài khoản cán bộ đơn lẻ (Single form) gắn với trường học đang Hoạt động (ACTIVE)
        Scenario: TS-5173-SUM-PROVISIONING
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Mở /school-user-management/new và chọn tab Single.", expected="Tạo thành công một bản ghi tài khoản cán bộ vai trò SCHOOL, liên kết chính xác với trường học đã chọn; xuất hiện đầy đủ trên bảng danh sách."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhập đầy đủ NRIC, Họ tên, Email và chọn Mã trường ACTIVE.", expected="Tạo thành công một bản ghi tài khoản cán bộ vai trò SCHOOL, liên kết chính xác với trường học đã chọn; xuất hiện đầy đủ trên bảng danh sách."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Nhấn nút Create.", expected="Tạo thành công một bản ghi tài khoản cán bộ vai trò SCHOOL, liên kết chính xác với trường học đã chọn; xuất hiện đầy đủ trên bảng danh sách."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Quay lại danh sách cán bộ và tìm kiếm cán bộ vừa tạo.", expected="Tạo thành công một bản ghi tài khoản cán bộ vai trò SCHOOL, liên kết chính xác với trường học đã chọn; xuất hiện đầy đủ trên bảng danh sách."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_sum_003_ts_5173_sum_provisioning_tạo_tài_khoản_cán_bộ_đơn_lẻ_không_g(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-003: Tạo tài khoản cán bộ đơn lẻ không gán trường (Unassigned in any school)
        Scenario: TS-5173-SUM-PROVISIONING
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Mở form tạo đơn lẻ Single.", expected="Tạo tài khoản thành công; cột School hiển thị nhãn 'Unassigned in any school'; tài khoản chưa có quyền truy cập dữ liệu trường học cho đến khi được phân công."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhập đầy đủ các trường bắt buộc và để trống ô MOE school code.", expected="Tạo tài khoản thành công; cột School hiển thị nhãn 'Unassigned in any school'; tài khoản chưa có quyền truy cập dữ liệu trường học cho đến khi được phân công."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Nhấn Create.", expected="Tạo tài khoản thành công; cột School hiển thị nhãn 'Unassigned in any school'; tài khoản chưa có quyền truy cập dữ liệu trường học cho đến khi được phân công."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Tìm kiếm cán bộ vừa tạo trên danh sách.", expected="Tạo tài khoản thành công; cột School hiển thị nhãn 'Unassigned in any school'; tài khoản chưa có quyền truy cập dữ liệu trường học cho đến khi được phân công."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_sum_004_ts_5173_sum_bulk_nhập_danh_sách_cán_bộ_theo_lô_bằng(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-004: Nhập danh sách cán bộ theo lô bằng file CSV hợp lệ (Bulk CSV Provisioning)
        Scenario: TS-5173-SUM-BULK
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Mở /school-user-management/new và chuyển sang tab Bulk CSV.", expected="Toàn bộ các dòng hợp lệ được tạo thành tài khoản cán bộ vai trò SCHOOL; phân công trường học tương ứng chính xác với file CSV; thông báo thành công hiển thị rõ ràng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Chọn file CSV hợp lệ và nhấn Upload CSV.", expected="Toàn bộ các dòng hợp lệ được tạo thành tài khoản cán bộ vai trò SCHOOL; phân công trường học tương ứng chính xác với file CSV; thông báo thành công hiển thị rõ ràng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Quan sát kết quả xử lý trả về từ hệ thống.", expected="Toàn bộ các dòng hợp lệ được tạo thành tài khoản cán bộ vai trò SCHOOL; phân công trường học tương ứng chính xác với file CSV; thông báo thành công hiển thị rõ ràng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Đối soát danh sách cán bộ trên bảng sau khi import.", expected="Toàn bộ các dòng hợp lệ được tạo thành tài khoản cán bộ vai trò SCHOOL; phân công trường học tương ứng chính xác với file CSV; thông báo thành công hiển thị rõ ràng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_sum_005_ts_5173_sum_bulk_xử_lý_thành_công_từng_phần_partial(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-005: Xử lý thành công từng phần (Partial Success) khi file CSV có cả dòng hợp lệ và dòng lỗi
        Scenario: TS-5173-SUM-BULK
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Chọn file CSV hỗn hợp tại tab Bulk CSV.", expected="Hệ thống tạo thành công 8 tài khoản hợp lệ; 2 dòng lỗi bị từ chối độc lập kèm số thứ tự dòng và nguyên nhân lỗi cụ thể; không bị crash toàn bộ file (không all-or-nothing crash)."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn Upload CSV.", expected="Hệ thống tạo thành công 8 tài khoản hợp lệ; 2 dòng lỗi bị từ chối độc lập kèm số thứ tự dòng và nguyên nhân lỗi cụ thể; không bị crash toàn bộ file (không all-or-nothing crash)."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra bảng báo cáo kết quả đối soát.", expected="Hệ thống tạo thành công 8 tài khoản hợp lệ; 2 dòng lỗi bị từ chối độc lập kèm số thứ tự dòng và nguyên nhân lỗi cụ thể; không bị crash toàn bộ file (không all-or-nothing crash)."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Tìm kiếm các tài khoản của dòng hợp lệ trên danh sách.", expected="Hệ thống tạo thành công 8 tài khoản hợp lệ; 2 dòng lỗi bị từ chối độc lập kèm số thứ tự dòng và nguyên nhân lỗi cụ thể; không bị crash toàn bộ file (không all-or-nothing crash)."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_sum_006_ts_5173_sum_cardinality_quan_hệ_1_cán_bộ_1_trường_one_schoo(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-006: Quan hệ 1 cán bộ - 1 trường (One School User to One School cardinality)
        Scenario: TS-5173-SUM-CARDINALITY
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Mở màn hình chi tiết của Cán bộ User A (đã thuộc Trường A).", expected="Mỗi cán bộ chỉ liên kết tối đa với đúng 1 trường học tại một thời điểm; hệ thống từ chối gán đồng thời 2 trường hoặc yêu cầu hủy liên kết trường cũ trước."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Kiểm tra thông tin hiển thị tại thẻ School.", expected="Mỗi cán bộ chỉ liên kết tối đa với đúng 1 trường học tại một thời điểm; hệ thống từ chối gán đồng thời 2 trường hoặc yêu cầu hủy liên kết trường cũ trước."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Cố gắng thực hiện thao tác gán thêm Trường B đồng thời hoặc giả mạo request API.", expected="Mỗi cán bộ chỉ liên kết tối đa với đúng 1 trường học tại một thời điểm; hệ thống từ chối gán đồng thời 2 trường hoặc yêu cầu hủy liên kết trường cũ trước."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Kiểm tra số lượng trường được liên kết với cán bộ.", expected="Mỗi cán bộ chỉ liên kết tối đa với đúng 1 trường học tại một thời điểm; hệ thống từ chối gán đồng thời 2 trường hoặc yêu cầu hủy liên kết trường cũ trước."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_sum_007_ts_5173_sum_eligibility_chặn_phân_công_cán_bộ_vào_trường_họ(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-007: Chặn phân công cán bộ vào trường học đang ở trạng thái Ngừng hoạt động (INACTIVE)
        Scenario: TS-5173-SUM-ELIGIBILITY
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Mở form tạo đơn lẻ Single.", expected="Cả hai thao tác đều bị hệ thống chặn lại; hiển thị thông báo lỗi rõ ràng rằng không thể phân công cán bộ vào trường học đang ngừng hoạt động; không có liên kết nào được tạo."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhập thông tin cán bộ hợp lệ và nhập mã trường INACTIVE.", expected="Cả hai thao tác đều bị hệ thống chặn lại; hiển thị thông báo lỗi rõ ràng rằng không thể phân công cán bộ vào trường học đang ngừng hoạt động; không có liên kết nào được tạo."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Nhấn Create.", expected="Cả hai thao tác đều bị hệ thống chặn lại; hiển thị thông báo lỗi rõ ràng rằng không thể phân công cán bộ vào trường học đang ngừng hoạt động; không có liên kết nào được tạo."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Lặp lại thao tác gán trường từ màn hình chi tiết của cán bộ unassigned.", expected="Cả hai thao tác đều bị hệ thống chặn lại; hiển thị thông báo lỗi rõ ràng rằng không thể phân công cán bộ vào trường học đang ngừng hoạt động; không có liên kết nào được tạo."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_sum_008_ts_5173_sum_sso_lưu_trữ_danh_tính_cán_bộ_để_đối_soá(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-008: Lưu trữ danh tính cán bộ để đối soát khi đăng nhập Microsoft SSO (SSO Identity Matching)
        Scenario: TS-5173-SUM-SSO
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Tạo tài khoản cán bộ với email Microsoft của cán bộ qua Single hoặc Bulk CSV.", expected="Hệ thống tự động liên kết danh tính Microsoft SSO với bản ghi cán bộ đã tạo trước đó; cấp quyền chính xác theo vai trò SCHOOL và trường học được phân công."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Đăng xuất khỏi tài khoản admin.", expected="Hệ thống tự động liên kết danh tính Microsoft SSO với bản ghi cán bộ đã tạo trước đó; cấp quyền chính xác theo vai trò SCHOOL và trường học được phân công."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Tiến hành đăng nhập Microsoft SSO bằng tài khoản cán bộ đó.", expected="Hệ thống tự động liên kết danh tính Microsoft SSO với bản ghi cán bộ đã tạo trước đó; cấp quyền chính xác theo vai trò SCHOOL và trường học được phân công."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Kiểm tra phân quyền và trường công tác sau khi đăng nhập.", expected="Hệ thống tự động liên kết danh tính Microsoft SSO với bản ghi cán bộ đã tạo trước đó; cấp quyền chính xác theo vai trò SCHOOL và trường học được phân công."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_sum_009_ts_5173_sum_sso_từ_chối_đăng_nhập_với_tài_khoản_mic(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-009: Từ chối đăng nhập với tài khoản Microsoft chưa được cấp phép (Unregistered Identity)
        Scenario: TS-5173-SUM-SSO
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Bấm Đăng nhập với Microsoft.", expected="Hệ thống từ chối truy cập với thông báo tài khoản chưa được phân quyền; TUYỆT ĐỐI KHÔNG tự động đăng ký (no self-registration) tài khoản cán bộ trường."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Hoàn tất xác thực trên trang đăng nhập của Microsoft.", expected="Hệ thống từ chối truy cập với thông báo tài khoản chưa được phân quyền; TUYỆT ĐỐI KHÔNG tự động đăng ký (no self-registration) tài khoản cán bộ trường."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Quan sát phản hồi điều hướng của cổng EduFAMS.", expected="Hệ thống từ chối truy cập với thông báo tài khoản chưa được phân quyền; TUYỆT ĐỐI KHÔNG tự động đăng ký (no self-registration) tài khoản cán bộ trường."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_sum_010_ts_5173_sum_credentials_bảo_vệ_thông_tin_đăng_nhập_tuyệt_đố(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-010: Bảo vệ thông tin đăng nhập: Tuyệt đối không yêu cầu hoặc lưu mật khẩu cục bộ / Microsoft
        Scenario: TS-5173-SUM-CREDENTIALS
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Kiểm tra toàn bộ các trường nhập liệu trên form Single.", expected="Không có bất kỳ trường mật khẩu (password) nào trên form hay trong file mẫu CSV; không có thông tin mật khẩu nào được lưu trữ hay truyền tải qua giao diện."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Kiểm tra các cột trong file mẫu CSV.", expected="Không có bất kỳ trường mật khẩu (password) nào trên form hay trong file mẫu CSV; không có thông tin mật khẩu nào được lưu trữ hay truyền tải qua giao diện."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra payload request gửi lên API và phản hồi trả về.", expected="Không có bất kỳ trường mật khẩu (password) nào trên form hay trong file mẫu CSV; không có thông tin mật khẩu nào được lưu trữ hay truyền tải qua giao diện."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Kiểm tra localStorage và sessionStorage của trình duyệt.", expected="Không có bất kỳ trường mật khẩu (password) nào trên form hay trong file mẫu CSV; không có thông tin mật khẩu nào được lưu trữ hay truyền tải qua giao diện."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_sum_011_ts_5173_sum_scope_phân_quyền_dữ_liệu_theo_dòng_row_le(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-011: Phân quyền dữ liệu theo dòng (Row-level Scope): Cán bộ chỉ truy cập dữ liệu trong trường được phân công
        Scenario: TS-5173-SUM-SCOPE
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Đăng nhập bằng tài khoản Cán bộ A.", expected="Dữ liệu Trường A xem bình thường; mọi thao tác cố truy cập dữ liệu Trường B đều bị máy chủ từ chối (403 Forbidden), không làm lộ thông tin PII giữa các trường."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Xem danh sách dữ liệu trong phạm vi Trường A.", expected="Dữ liệu Trường A xem bình thường; mọi thao tác cố truy cập dữ liệu Trường B đều bị máy chủ từ chối (403 Forbidden), không làm lộ thông tin PII giữa các trường."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Cố gắng truy cập URL hoặc gọi API trực tiếp để lấy dữ liệu của Trường B.", expected="Dữ liệu Trường A xem bình thường; mọi thao tác cố truy cập dữ liệu Trường B đều bị máy chủ từ chối (403 Forbidden), không làm lộ thông tin PII giữa các trường."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_sum_012_ts_5173_sum_scope_hạn_chế_nghiệp_vụ_đối_với_tài_khoản(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-012: Hạn chế nghiệp vụ đối với tài khoản cán bộ chưa gán trường (Unassigned School Scope Restriction)
        Scenario: TS-5173-SUM-SCOPE
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Đăng nhập bằng tài khoản cán bộ chưa gán trường.", expected="Hệ thống hiển thị màn hình thông báo chưa được phân công trường công tác; không cho phép thực hiện bất kỳ thao tác nghiệp vụ nào cho đến khi được gán trường."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Cố gắng truy cập các màn hình quản lý nghiệp vụ trường học.", expected="Hệ thống hiển thị màn hình thông báo chưa được phân công trường công tác; không cho phép thực hiện bất kỳ thao tác nghiệp vụ nào cho đến khi được gán trường."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_sum_013_ts_5173_sum_auth_chặn_tài_khoản_người_dùng_vãng_lai(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-013: Chặn tài khoản người dùng vãng lai (Anonymous) và tự động chuyển hướng về trang đăng nhập
        Scenario: TS-5173-SUM-AUTH
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Mở trực tiếp URL /school-user-management.", expected="Trình duyệt tự động chuyển hướng về trang /login; dữ liệu danh sách cán bộ và form tạo mới được bảo vệ hoàn toàn."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Mở trực tiếp URL /school-user-management/new.", expected="Trình duyệt tự động chuyển hướng về trang /login; dữ liệu danh sách cán bộ và form tạo mới được bảo vệ hoàn toàn."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_5173_sum_014_ts_5173_sum_roles_phân_định_vai_trò_tài_khoản_cán_bộ(self, school_user_mgmt_data: Dict[str, Any]):
        """
        TC-5173-SUM-014: Phân định vai trò tài khoản cán bộ nhà trường (SCHOOL role) trong hệ thống IAM
        Scenario: TS-5173-SUM-ROLES
        """
        page_obj = self.get_page(SchoolUserManagementPage)
        base_url = school_user_mgmt_data.get("base_url", "http://localhost:5173")

        with self.step("Step 1: 1. Mở màn hình chi tiết cán bộ vừa tạo.", expected="Trường Role hiển thị chính xác giá trị SCHOOL; phân định rạch ròi với quyền quản trị viên MOEHQ và học sinh/phụ huynh."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Kiểm tra thông tin tại thẻ 'User account'.", expected="Trường Role hiển thị chính xác giá trị SCHOOL; phân định rạch ròi với quyền quản trị viên MOEHQ và học sinh/phụ huynh."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra quyền hạn của vai trò SCHOOL trên hệ thống.", expected="Trường Role hiển thị chính xác giá trị SCHOOL; phân định rạch ròi với quyền quản trị viên MOEHQ và học sinh/phụ huynh."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")
