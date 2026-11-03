# Cổng Dịch vụ Phụ huynh EduSave — Đăng nhập & Singpass MockPass (:5174 / :5288) — Đặc tả Kiểm thử 5 Trụ Cột

## 1. Tổng quan Test Suites

| Pillar | Test Suite | Số ca |
| --- | --- | --- |
| AC | Tiêu chí nghiệm thu (AC) | 2 |
| BR | Quy tắc nghiệp vụ (BR) | 2 |
| Tech/UI | Kiểm tra hợp lệ (Validation) | 2 |
| Tech/UI | Luồng chức năng (Function Flow) | 2 |
| Tech/UI | Xử lý lỗi (Error Handling) | 2 |

## 2. Ma trận testcase (20 cột)

### BR

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-AUTH-01 | TS-AUTH-BR | Quyền truy cập dịch vụ công dân: Phụ huynh có con liên kết mới vào được cổng EduSave | Quy tắc nghiệp vụ (BR) | Đăng nhập Cổng Phụ huynh | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Tài khoản Singpass Phụ huynh hợp lệ | Tài khoản: S1234567A | 3 | 1. Mở trang Đăng nhập Cổng Phụ huynh.<br>2. Chọn Đăng nhập với Singpass MockPass.<br>3. Chọn tài khoản phụ huynh hợp lệ. | Đăng nhập thành công vào Cổng phụ huynh; hiển thị thông tin các con liên kết và số dư quỹ EduSave. |  | BR-AUTH-01; CITIZEN-SCOPE |  | BR-AUTH-01; CITIZEN-SCOPE | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-AUTH-02 | TS-AUTH-BR | Kiểm soát an toàn phiên làm việc: Hết hạn phiên tự động bảo vệ dữ liệu phụ huynh | Quy tắc nghiệp vụ (BR) | Đăng nhập Cổng Phụ huynh | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Phiên làm việc phụ huynh đang mở | Thời gian chờ không thao tác | 3 | 1. Đăng nhập vào Cổng phụ huynh.<br>2. Để yên không thao tác trên màn hình vượt quá thời gian quy định.<br>3. Nhấp vào một chức năng bất kỳ. | Hệ thống tự động kết thúc phiên làm việc an toàn và chuyển hướng về màn hình Đăng nhập. |  | BR-AUTH-SESSION; SECURITY-IDLE |  | BR-AUTH-SESSION; SECURITY-IDLE | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### AC

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-AUTH-03 | TS-AUTH-AC | Hiển thị giao diện Đăng nhập đầy đủ logo, tiêu đề và nút Đăng nhập Singpass MockPass | Tiêu chí nghiệm thu (AC) | Đăng nhập Cổng Phụ huynh | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Trình duyệt ở phiên mới | Nút Singpass MockPass | 2 | 1. Mở trình duyệt và truy cập trang Đăng nhập Phụ huynh.<br>2. Quan sát khung hiển thị và tiêu đề trang. | Tiêu đề 'Đăng nhập Cổng phụ huynh' hiển thị rõ ràng; nút Đăng nhập Singpass MockPass sẵn sàng thao tác. |  | AC-AUTH-01; DOM-LOGIN |  | AC-AUTH-01; DOM-LOGIN | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-AUTH-04 | TS-AUTH-AC | Đăng nhập thành công với tài khoản mẫu Singpass chuyển hướng ngay vào Trang chủ | Tiêu chí nghiệm thu (AC) | Đăng nhập Cổng Phụ huynh | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Trang MockPass đang mở | Tài khoản mẫu: Tan Ah Teck (S1234567A) | 3 | 1. Nhấp nút Đăng nhập với Singpass MockPass.<br>2. Chọn tài khoản phụ huynh Tan Ah Teck.<br>3. Nhấn Xác nhận đăng nhập. | Đăng nhập thành công; chuyển hướng mượt mà vào Trang chủ Cổng dịch vụ công dân EduSave. |  | AC-AUTH-SUCCESS; REDIRECT-HOME |  | AC-AUTH-SUCCESS; REDIRECT-HOME | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### Tech/UI

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-AUTH-05 | TS-AUTH-VAL | Bỏ trống ô chọn tài khoản trên cổng MockPass: Hiển thị cảnh báo yêu cầu chọn tài khoản | Kiểm tra hợp lệ (Validation) | Đăng nhập Cổng Phụ huynh | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Trang xác thực MockPass | Không chọn tài khoản nào | 2 | 1. Mở màn hình đăng nhập MockPass.<br>2. Không chọn tài khoản nào và nhấn Xác nhận. | Hệ thống chặn lại và hiển thị cảnh báo: 'Vui lòng chọn một tài khoản phụ huynh để tiếp tục'. |  | VAL-12 Lớp 1; MANDATORY |  | VAL-12 Lớp 1; MANDATORY | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-AUTH-06 | TS-AUTH-VAL | Kiểm tra cấu trúc mã định danh Singpass NRIC hợp lệ khi nhập liệu | Kiểm tra hợp lệ (Validation) | Đăng nhập Cổng Phụ huynh | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Biểu mẫu nhập NRIC thủ công | NRIC sai định dạng: 'ABC123' | 2 | 1. Nhập mã NRIC sai định dạng vào ô kiểm thử.<br>2. Nhấn nút Đăng nhập. | Ô nhập hiển thị viền đỏ cảnh báo: 'Mã NRIC không hợp lệ (phải bắt đầu bằng chữ cái và đúng 9 ký tự)'. |  | VAL-12 Lớp 4; NRIC-FORMAT |  | VAL-12 Lớp 4; NRIC-FORMAT | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-AUTH-07 | TS-AUTH-FLOW | Quy trình đăng nhập Singpass MockPass hoàn chỉnh từ đầu đến cuối | Luồng chức năng (Function Flow) | Đăng nhập Cổng Phụ huynh | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Tài khoản mẫu hợp lệ | Tan Ah Teck | 3 | 1. Nhấp nút Singpass MockPass.<br>2. Chọn danh tính phụ huynh.<br>3. Nhấn Đăng nhập và kiểm tra Trang chủ. | Quy trình diễn ra liên tục, thuận tiện; Trang chủ mở ra với đầy đủ thông tin cá nhân của phụ huynh. |  | FLOW-AUTH-LOGIN; HAPPY-PATH |  | FLOW-AUTH-LOGIN; HAPPY-PATH | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-AUTH-08 | TS-AUTH-FLOW | Hủy bỏ thao tác đăng nhập tại trang MockPass và quay lại màn hình chính | Luồng chức năng (Function Flow) | Đăng nhập Cổng Phụ huynh | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Trang MockPass đang mở | Nút Hủy bỏ (Cancel) | 3 | 1. Nhấn nút Đăng nhập Singpass.<br>2. Tại màn hình MockPass, nhấn nút Hủy bỏ (Cancel).<br>3. Quan sát màn hình trả về. | Tiến trình dừng an toàn; người dùng được đưa trở lại trang Đăng nhập ban đầu mà không phát sinh lỗi. |  | FLOW-AUTH-CANCEL; SAFE-RETURN |  | FLOW-AUTH-CANCEL; SAFE-RETURN | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-AUTH-09 | TS-AUTH-ERR | Xử lý khi dịch vụ xác thực công dân gián đoạn: Hiển thị thông báo thân thiện | Xử lý lỗi (Error Handling) | Đăng nhập Cổng Phụ huynh | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Cổng xác thực gặp sự cố mạng | Thao tác đăng nhập | 2 | 1. Thử đăng nhập khi cổng xác thực gián đoạn.<br>2. Quan sát phản hồi trên giao diện. | Màn hình không bị vỡ hoặc treo; xuất hiện thông báo: 'Dịch vụ xác thực tạm thời gián đoạn, vui lòng thử lại sau'. |  | ERR-AUTH-SERVICE-FAIL; GRACEFUL |  | ERR-AUTH-SERVICE-FAIL; GRACEFUL | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-AUTH-10 | TS-AUTH-ERR | Khóa nút Đăng nhập khi nhấp liên tiếp tránh gửi nhiều yêu cầu trùng lặp | Xử lý lỗi (Error Handling) | Đăng nhập Cổng Phụ huynh | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Nút Đăng nhập MockPass | Nhấp chuột liên tiếp 2 lần | 2 | 1. Nhấp nhanh liên tiếp vào nút Đăng nhập.<br>2. Quan sát phản hồi nút bấm. | Nút bấm lập tức chuyển trạng thái 'Đang xử lý...' và tạm khóa để ngăn việc gửi nhiều yêu cầu cùng lúc. |  | ERR-AUTH-DEBOUNCE; RATE-LIMIT |  | ERR-AUTH-DEBOUNCE; RATE-LIMIT | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

## 3. Locator từ Live DOM

| Tên | Selector | Nguồn recon |
| --- | --- | --- |
| Nút Đăng nhập Singpass MockPass | button:has-text('Singpass'), button:has-text('MockPass') | Giữa khung đăng nhập |
| Danh sách tài khoản mẫu | select, .persona-list | Màn hình xác thực MockPass |
| Nút Xác nhận Đăng nhập | button:has-text('Login'), button:has-text('Submit') | Màn hình MockPass |
| Nút Hủy bỏ | button:has-text('Cancel'), a:has-text('Cancel') | Màn hình MockPass |
| Thông báo lỗi | [role='alert'], .alert-danger | Đầu khung đăng nhập |

## 4. Fixtures

```json
{
  "fixture_reference": "01_parent_login_and_mockpass_data.json",
  "design_status": "Not Run",
  "result_fields": "Actual Result và Defect ID để trống phục vụ kiểm thử thực tế"
}
```

## 5. Truy vết và coverage

| ID | Pillar | Nguồn | Section |
| --- | --- | --- | --- |
| BR-CORE | BR | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/01_parent_login_and_mockpass.md | Quy tắc nghiệp vụ cốt lõi |
| AC-CORE | AC | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/01_parent_login_and_mockpass.md | Tiêu chí nghiệm thu chức năng |
| VAL-12 | Validation | 1_Nghiep_Vu_va_Specs/specs/HUONG_DAN_THIET_KE_TEST_CASE_UAT_5_PILLARS.md | Ma trận kiểm thử hợp lệ ô nhập liệu |
| FLOW-CORE | Flow | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/01_parent_login_and_mockpass.md | Luồng tương tác và chuyển đổi trạng thái |
| ERR-CORE | Error | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/01_parent_login_and_mockpass.md | Xử lý ngoại lệ và cảnh báo lỗi |

| Đối tượng | Lớp | Trạng thái | TC IDs | Lý do |
| --- | --- | --- | --- | --- |
| Quy tắc nghiệp vụ cốt lõi và phân quyền | BR | Applicable | TC-AUTH-01, TC-AUTH-02 |  |
| Tiêu chí nghiệm thu chức năng chính | AC | Applicable | TC-AUTH-03, TC-AUTH-04 |  |
| Kiểm tra tính hợp lệ dữ liệu ô nhập (Validation) | Validation | Applicable | TC-AUTH-05, TC-AUTH-06 |  |
| Luồng tương tác và chuyển trạng thái (Flow) | Flow | Applicable | TC-AUTH-07, TC-AUTH-08 |  |
| Xử lý lỗi và phản hồi cảnh báo (Error) | Error | Applicable | TC-AUTH-09, TC-AUTH-10 |  |

Kiểm tra cấu trúc không xác nhận đầy đủ nghiệp vụ hoặc chất lượng oracle.
