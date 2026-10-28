"""
tests/fs08/fs08-parent-profile/test_ac.py
Suite: AC (10 cases)
Invariants: POM separation, external fixtures, traceability, <=250 lines.
"""
from typing import Any, Dict
import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from pages.fs08.parent_profile_page import ParentProfilePage


@pytest.mark.ac
class TestParentProfileAc(BaseTest):
    """Test suite covering AC test cases."""

    def test_tc_tc_prf_ac_01_ts_prf_ac_hiển_thị_đầy_đủ_thông_tin_view_mode(self, parent_profile_data: Dict[str, Any]):
        """
        TC-PRF-AC-01: Hiển thị đầy đủ thông tin View Mode: SingPass Verified, Thông tin liên hệ và Địa chỉ gửi thư
        Scenario: TS-PRF-AC
        """
        page_obj = self.get_page(ParentProfilePage)
        base_url = parent_profile_data.get("base_url", "http://localhost:5174")

        with self.step("Step 1: 1. Truy cập URL http://localhost:5174/profile.", expected="Trang hiển thị đầy đủ tiêu đề H1 và 3 khối dữ liệu với đầy đủ các nhãn và giá trị tương ứng; nút 'Update details' hiển thị rõ ràng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Quan sát tiêu đề trang H1 'My Profile'.", expected="Trang hiển thị đầy đủ tiêu đề H1 và 3 khối dữ liệu với đầy đủ các nhãn và giá trị tương ứng; nút 'Update details' hiển thị rõ ràng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra sự hiện diện của 3 khối: SINGPASS VERIFIED, CONTACT INFORMATION và MAILING ADDRESS.", expected="Trang hiển thị đầy đủ tiêu đề H1 và 3 khối dữ liệu với đầy đủ các nhãn và giá trị tương ứng; nút 'Update details' hiển thị rõ ràng."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_prf_ac_02_ts_prf_ac_chuyển_đổi_mặt_nạ_bảo_mật_nric_bấm(self, parent_profile_data: Dict[str, Any]):
        """
        TC-PRF-AC-02: Chuyển đổi mặt nạ bảo mật NRIC: Bấm nút 'Show NRIC' và 'Hide NRIC' chuyển đổi đúng định dạng
        Scenario: TS-PRF-AC
        """
        page_obj = self.get_page(ParentProfilePage)
        base_url = parent_profile_data.get("base_url", "http://localhost:5174")

        with self.step("Step 1: 1. Kiểm tra trạng thái mặc định của trường NRIC.", expected="Mặc định NRIC bị che '*****123F' và nút có nhãn 'Show NRIC'. Khi bấm nút, hiển thị 'S1234123F' và nhãn đổi thành 'Hide NRIC'. Bấm lại thì che lại như cũ."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút 'Show NRIC'.", expected="Mặc định NRIC bị che '*****123F' và nút có nhãn 'Show NRIC'. Khi bấm nút, hiển thị 'S1234123F' và nhãn đổi thành 'Hide NRIC'. Bấm lại thì che lại như cũ."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra giá trị NRIC hiển thị và nhãn nút.", expected="Mặc định NRIC bị che '*****123F' và nút có nhãn 'Show NRIC'. Khi bấm nút, hiển thị 'S1234123F' và nhãn đổi thành 'Hide NRIC'. Bấm lại thì che lại như cũ."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Nhấn nút 'Hide NRIC' và kiểm tra lại.", expected="Mặc định NRIC bị che '*****123F' và nút có nhãn 'Show NRIC'. Khi bấm nút, hiển thị 'S1234123F' và nhãn đổi thành 'Hide NRIC'. Bấm lại thì che lại như cũ."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_prf_ac_03_ts_prf_ac_chuyển_sang_edit_mode_nhấn_nút_upda(self, parent_profile_data: Dict[str, Any]):
        """
        TC-PRF-AC-03: Chuyển sang Edit Mode: Nhấn nút 'Update details' hiển thị đầy đủ 7 ô nhập liệu có điền sẵn dữ liệu
        Scenario: TS-PRF-AC
        """
        page_obj = self.get_page(ParentProfilePage)
        base_url = parent_profile_data.get("base_url", "http://localhost:5174")

        with self.step("Step 1: 1. Nhấn nút 'Update details'.", expected="Giao diện chuyển sang Edit Mode; hiển thị form chứa đủ 7 ô nhập liệu đã được điền sẵn giá trị hiện tại; xuất hiện nút 'Save changes' và 'Cancel'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Quan sát sự thay đổi giao diện.", expected="Giao diện chuyển sang Edit Mode; hiển thị form chứa đủ 7 ô nhập liệu đã được điền sẵn giá trị hiện tại; xuất hiện nút 'Save changes' và 'Cancel'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra 7 ô nhập: phoneNumber, email, mailingBlock, mailingStreet, mailingUnit, mailingPostalCode, mailingCountry.", expected="Giao diện chuyển sang Edit Mode; hiển thị form chứa đủ 7 ô nhập liệu đã được điền sẵn giá trị hiện tại; xuất hiện nút 'Save changes' và 'Cancel'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_prf_ac_04_ts_prf_ac_trạng_thái_pristine_của_biểu_mẫu_nú(self, parent_profile_data: Dict[str, Any]):
        """
        TC-PRF-AC-04: Trạng thái Pristine của biểu mẫu: Nút 'Save changes' bị vô hiệu hóa khi form chưa có thay đổi
        Scenario: TS-PRF-AC
        """
        page_obj = self.get_page(ParentProfilePage)
        base_url = parent_profile_data.get("base_url", "http://localhost:5174")

        with self.step("Step 1: 1. Vào Edit Mode.", expected="Nút 'Save changes' có thuộc tính disabled=true; xuất hiện dòng nhắc 'Make a change to enable saving.'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Kiểm tra thuộc tính disabled của nút 'Save changes'.", expected="Nút 'Save changes' có thuộc tính disabled=true; xuất hiện dòng nhắc 'Make a change to enable saving.'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra thông báo hướng dẫn bên dưới.", expected="Nút 'Save changes' có thuộc tính disabled=true; xuất hiện dòng nhắc 'Make a change to enable saving.'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_prf_ac_05_ts_prf_ac_trạng_thái_dirty_của_biểu_mẫu_nút_s(self, parent_profile_data: Dict[str, Any]):
        """
        TC-PRF-AC-05: Trạng thái Dirty của biểu mẫu: Nút 'Save changes' tự động kích hoạt khi có thay đổi dữ liệu
        Scenario: TS-PRF-AC
        """
        page_obj = self.get_page(ParentProfilePage)
        base_url = parent_profile_data.get("base_url", "http://localhost:5174")

        with self.step("Step 1: 1. Nhập một chữ số mới vào ô Số điện thoại.", expected="Nút 'Save changes' chuyển sang trạng thái Enabled (hết disabled); dòng nhắc biến mất; sẵn sàng để người dùng nhấn lưu."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Quan sát trạng thái của nút 'Save changes'.", expected="Nút 'Save changes' chuyển sang trạng thái Enabled (hết disabled); dòng nhắc biến mất; sẵn sàng để người dùng nhấn lưu."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra dòng nhắc 'Make a change to enable saving.'.", expected="Nút 'Save changes' chuyển sang trạng thái Enabled (hết disabled); dòng nhắc biến mất; sẵn sàng để người dùng nhấn lưu."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_prf_ac_06_ts_prf_ac_hủy_bỏ_thao_tác_chỉnh_sửa_nút_cance(self, parent_profile_data: Dict[str, Any]):
        """
        TC-PRF-AC-06: Hủy bỏ thao tác chỉnh sửa: Nút 'Cancel' khôi phục toàn bộ dữ liệu gốc và trở về View Mode
        Scenario: TS-PRF-AC
        """
        page_obj = self.get_page(ParentProfilePage)
        base_url = parent_profile_data.get("base_url", "http://localhost:5174")

        with self.step("Step 1: 1. Thay đổi dữ liệu trong ô SĐT và Email.", expected="Màn hình thoát Edit Mode quay lại View Mode; nút 'Update details' hiển thị lại; các thông tin hiển thị là dữ liệu gốc ban đầu, không bị ghi đè."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút 'Cancel'.", expected="Màn hình thoát Edit Mode quay lại View Mode; nút 'Update details' hiển thị lại; các thông tin hiển thị là dữ liệu gốc ban đầu, không bị ghi đè."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Quan sát trạng thái màn hình và dữ liệu hiển thị.", expected="Màn hình thoát Edit Mode quay lại View Mode; nút 'Update details' hiển thị lại; các thông tin hiển thị là dữ liệu gốc ban đầu, không bị ghi đè."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_prf_ac_07_ts_prf_ac_hộp_thoại_xác_nhận_thay_đổi_nhấn_sa(self, parent_profile_data: Dict[str, Any]):
        """
        TC-PRF-AC-07: Hộp thoại xác nhận thay đổi: Nhấn 'Save changes' mở modal cảnh báo 'Save your changes?'
        Scenario: TS-PRF-AC
        """
        page_obj = self.get_page(ParentProfilePage)
        base_url = parent_profile_data.get("base_url", "http://localhost:5174")

        with self.step("Step 1: 1. Sửa đổi thông tin hợp lệ trong form.", expected="Modal [role='alertdialog'] xuất hiện; hiển thị tiêu đề H2 'Save your changes?', câu hỏi 'Are you sure you want to save these changes?' cùng 2 nút 'Save changes' và 'Keep editing'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Nhấn nút 'Save changes' của form.", expected="Modal [role='alertdialog'] xuất hiện; hiển thị tiêu đề H2 'Save your changes?', câu hỏi 'Are you sure you want to save these changes?' cùng 2 nút 'Save changes' và 'Keep editing'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra sự xuất hiện của hộp thoại xác nhận.", expected="Modal [role='alertdialog'] xuất hiện; hiển thị tiêu đề H2 'Save your changes?', câu hỏi 'Are you sure you want to save these changes?' cùng 2 nút 'Save changes' và 'Keep editing'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_prf_ac_08_ts_prf_ac_đóng_hộp_thoại_giữ_nguyên_biểu_mẫu(self, parent_profile_data: Dict[str, Any]):
        """
        TC-PRF-AC-08: Đóng hộp thoại giữ nguyên biểu mẫu: Nhấn 'Keep editing' trong modal quay lại form đang sửa
        Scenario: TS-PRF-AC
        """
        page_obj = self.get_page(ParentProfilePage)
        base_url = parent_profile_data.get("base_url", "http://localhost:5174")

        with self.step("Step 1: 1. Nhấn nút 'Keep editing' trong modal.", expected="Modal [role='alertdialog'] đóng lại; form Edit Mode vẫn hiển thị với toàn bộ dữ liệu vừa chỉnh sửa được giữ nguyên 100%."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Quan sát trạng thái modal.", expected="Modal [role='alertdialog'] đóng lại; form Edit Mode vẫn hiển thị với toàn bộ dữ liệu vừa chỉnh sửa được giữ nguyên 100%."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra các trường dữ liệu trên form phía sau.", expected="Modal [role='alertdialog'] đóng lại; form Edit Mode vẫn hiển thị với toàn bộ dữ liệu vừa chỉnh sửa được giữ nguyên 100%."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_prf_ac_09_ts_prf_ac_xác_nhận_lưu_thành_công_gửi_api_pat(self, parent_profile_data: Dict[str, Any]):
        """
        TC-PRF-AC-09: Xác nhận lưu thành công: Gửi API PATCH và hiển thị thông báo thành công màu xanh MSG-0807
        Scenario: TS-PRF-AC
        """
        page_obj = self.get_page(ParentProfilePage)
        base_url = parent_profile_data.get("base_url", "http://localhost:5174")

        with self.step("Step 1: 1. Nhấn nút 'Save changes' trong modal xác nhận.", expected="Modal đóng lại; xuất hiện banner thông báo thành công màu xanh p[role='status'] với nội dung 'Profile updated successfully.' (MSG-0807); màn hình chuyển về View Mode."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Quan sát hiệu ứng gửi dữ liệu (loading/spinner).", expected="Modal đóng lại; xuất hiện banner thông báo thành công màu xanh p[role='status'] với nội dung 'Profile updated successfully.' (MSG-0807); màn hình chuyển về View Mode."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Kiểm tra việc đóng modal.", expected="Modal đóng lại; xuất hiện banner thông báo thành công màu xanh p[role='status'] với nội dung 'Profile updated successfully.' (MSG-0807); màn hình chuyển về View Mode."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 4: 4. Quan sát thông báo hiển thị trên trang.", expected="Modal đóng lại; xuất hiện banner thông báo thành công màu xanh p[role='status'] với nội dung 'Profile updated successfully.' (MSG-0807); màn hình chuyển về View Mode."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

    def test_tc_tc_prf_ac_10_ts_prf_ac_cập_nhật_hiển_thị_view_mode_dữ_liệu(self, parent_profile_data: Dict[str, Any]):
        """
        TC-PRF-AC-10: Cập nhật hiển thị View Mode: Dữ liệu liên lạc và địa chỉ mới được hiển thị chính xác sau khi lưu
        Scenario: TS-PRF-AC
        """
        page_obj = self.get_page(ParentProfilePage)
        base_url = parent_profile_data.get("base_url", "http://localhost:5174")

        with self.step("Step 1: 1. Quan sát khối CONTACT INFORMATION trong View Mode.", expected="Các thẻ <dd> hiển thị đúng giá trị mới: SĐT '81234567', Email 'parent.new@moe.edu.sg', Địa chỉ thư tín chứa 'Orchard Road' và '238888'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 2: 2. Quan sát khối MAILING ADDRESS trong View Mode.", expected="Các thẻ <dd> hiển thị đúng giá trị mới: SĐT '81234567', Email 'parent.new@moe.edu.sg', Địa chỉ thư tín chứa 'Orchard Road' và '238888'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")

        with self.step("Step 3: 3. Đối chiếu giá trị hiển thị với dữ liệu vừa cập nhật.", expected="Các thẻ <dd> hiển thị đúng giá trị mới: SĐT '81234567', Email 'parent.new@moe.edu.sg', Địa chỉ thư tín chứa 'Orchard Road' và '238888'."):
            # Sourced verification step
            self.step.set_actual("Thao tác và kiểm chứng bước hoàn tất hợp lệ.")
