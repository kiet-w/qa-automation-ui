# Cổng Dịch vụ Phụ huynh EduSave — Hỗ trợ Tài chính FAS: Bước 1 - Chọn Học sinh Thụ hưởng (:5174) — Đặc tả Kiểm thử 5 Trụ Cột

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
| TC-FAS02-01 | TS-FAS02-BR | Quy định thụ hưởng: Chỉ học sinh quốc tịch Singapore mới được chọn nộp đơn FAS | Quy tắc nghiệp vụ (BR) | FAS Bước 1: Chọn Học sinh | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Gia đình có con quốc tịch Singapore và quốc tịch khác | Danh sách các con | 2 | 1. Mở Bước 1 của đơn FAS.<br>2. Quan sát ô tích chọn của từng người con. | Học sinh quốc tịch Singapore có ô tích chọn hoạt động bình thường; con quốc tịch khác bị vô hiệu hóa kèm ghi chú rõ ràng. |  | BR-FAS02-CITIZEN-RULE; ELIGIBLE-CHILD |  | BR-FAS02-CITIZEN-RULE; ELIGIBLE-CHILD | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS02-02 | TS-FAS02-BR | Nộp đơn gộp nhiều con: Cho phép chọn đồng thời nhiều người con trong cùng một hồ sơ gia đình | Quy tắc nghiệp vụ (BR) | FAS Bước 1: Chọn Học sinh | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Gia đình có 2 con đều là công dân Singapore | Ô tích chọn từng con | 3 | 1. Tích chọn người con thứ nhất.<br>2. Tích chọn tiếp người con thứ hai.<br>3. Quan sát danh sách thụ hưởng. | Cả 2 con đều được ghi nhận vào danh sách thụ hưởng chung của bộ hồ sơ FAS gia đình. |  | BR-FAS02-MULTI-CHILD; FAMILY-BUNDLE |  | BR-FAS02-MULTI-CHILD; FAMILY-BUNDLE | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### AC

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-FAS02-03 | TS-FAS02-AC | Danh sách học sinh hiển thị đầy đủ: Họ tên, NRIC che bảo mật, Trường, Khối lớp và Hộp chọn | Tiêu chí nghiệm thu (AC) | FAS Bước 1: Chọn Học sinh | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Đang ở Bước 1 | Bảng danh sách các con | 2 | 1. Kiểm tra cấu trúc hiển thị danh sách các con.<br>2. Rà soát thông tin trên từng thẻ học sinh. | Thông tin trường lớp và mã số học sinh hiển thị chuẩn xác; số NRIC được che bảo mật đúng quy định an toàn thông tin. |  | AC-FAS02-LIST-VIEW; DOM-STEP1 |  | AC-FAS02-LIST-VIEW; DOM-STEP1 | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS02-04 | TS-FAS02-AC | Thanh tiến trình hiển thị rõ ràng người dùng đang ở Bước 1 trong tổng số 4 bước nộp đơn | Tiêu chí nghiệm thu (AC) | FAS Bước 1: Chọn Học sinh | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Thanh tiến trình Wizard (Stepper) | Trạng thái Bước 1 | 2 | 1. Quan sát thanh tiến trình ở đầu trang.<br>2. Kiểm tra chỉ số bước. | Bước 1 được đánh dấu nổi bật với nhãn 'Chọn học sinh thụ hưởng'; các bước sau hiển thị ở trạng thái chờ. |  | AC-FAS02-STEPPER; PROGRESS-UI |  | AC-FAS02-STEPPER; PROGRESS-UI | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### Tech/UI

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-FAS02-05 | TS-FAS02-VAL | Báo lỗi ngăn chặn khi không chọn bất kỳ học sinh nào mà bấm nút 'Tiếp tục' | Kiểm tra hợp lệ (Validation) | FAS Bước 1: Chọn Học sinh | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Chưa tích chọn con nào | Nút 'Tiếp tục' | 2 | 1. Để trống không tích chọn học sinh nào.<br>2. Nhấn nút 'Tiếp tục' sang Bước 2. | Hệ thống chặn chuyển bước và hiển thị cảnh báo: 'Vui lòng chọn ít nhất một học sinh thụ hưởng để tiếp tục'. |  | VAL-12 Lớp 1; MANDATORY-STUDENT |  | VAL-12 Lớp 1; MANDATORY-STUDENT | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS02-06 | TS-FAS02-VAL | Vô hiệu hóa ô tích chọn đối với học sinh không mang quốc tịch Singapore kèm chú thích | Kiểm tra hợp lệ (Validation) | FAS Bước 1: Chọn Học sinh | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Học sinh quốc tịch Thường trú nhân (PR) | Thẻ học sinh PR | 2 | 1. Di chuột vào thẻ của học sinh PR.<br>2. Quan sát ô chọn và thông báo đi kèm. | Ô tích chọn bị khóa làm mờ (disabled); xuất hiện dòng giải thích: 'Chỉ áp dụng cho công dân Singapore'. |  | VAL-12 Lớp 6; DISABLED-STATE |  | VAL-12 Lớp 6; DISABLED-STATE | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS02-07 | TS-FAS02-FLOW | Tích chọn học sinh đủ điều kiện và nhấn 'Tiếp tục' chuyển sang Bước 2 | Luồng chức năng (Function Flow) | FAS Bước 1: Chọn Học sinh | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Tích chọn 1 học sinh hợp lệ | Nút 'Tiếp tục' | 3 | 1. Tích chọn học sinh.<br>2. Nhấn nút 'Tiếp tục'.<br>3. Quan sát màn hình tiếp theo. | Hệ thống lưu trữ học sinh đã chọn vào hồ sơ nháp và chuyển sang Bước 2: Kê khai thông tin hộ gia đình. |  | FLOW-FAS02-PROCEED; STEP-TRANSITION |  | FLOW-FAS02-PROCEED; STEP-TRANSITION | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS02-08 | TS-FAS02-FLOW | Nhấn nút 'Lưu bản nháp & Thoát' cho phép quay lại hoàn thiện sau mà không mất dữ liệu | Luồng chức năng (Function Flow) | FAS Bước 1: Chọn Học sinh | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Đã chọn học sinh thụ hưởng | Nút 'Lưu bản nháp & Thoát' | 2 | 1. Nhấn nút 'Lưu bản nháp & Thoát'.<br>2. Quay lại Cổng phụ huynh sau đó mở lại đơn. | Lựa chọn học sinh trước đó được phục hồi nguyên vẹn; phụ huynh không cần phải chọn lại từ đầu. |  | FLOW-FAS02-SAVE-DRAFT; DRAFT-PERSIST |  | FLOW-FAS02-SAVE-DRAFT; DRAFT-PERSIST | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS02-09 | TS-FAS02-ERR | Cảnh báo khi học sinh được chọn đã có đơn FAS đang được nhà trường thụ lý | Xử lý lỗi (Error Handling) | FAS Bước 1: Chọn Học sinh | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Học sinh đã nộp đơn trước đó | Thao tác chọn học sinh | 2 | 1. Chọn học sinh đã có đơn đang xét duyệt.<br>2. Nhấn Tiếp tục. | Hệ thống hiển thị cảnh báo: 'Học sinh này đã có đơn FAS đang được thụ lý, không thể tạo thêm đơn mới'. |  | ERR-FAS02-DUPLICATE-STUDENT; POLICY-CHECK |  | ERR-FAS02-DUPLICATE-STUDENT; POLICY-CHECK | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS02-10 | TS-FAS02-ERR | Xử lý khi danh sách học sinh bị gián đoạn tải dữ liệu: Hiển thị nút 'Tải lại danh sách' | Xử lý lỗi (Error Handling) | FAS Bước 1: Chọn Học sinh | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Mất kết nối máy chủ khi tải danh sách | Nút 'Tải lại' | 2 | 1. Mô phỏng sự cố tải dữ liệu danh sách học sinh.<br>2. Nhấn nút Tải lại sau khi có mạng. | Hệ thống tải lại danh sách học sinh thành công, hiển thị đầy đủ thẻ các con mà không cần tải lại toàn bộ trang. |  | ERR-FAS02-FETCH-FAIL; RETRY-ACTION |  | ERR-FAS02-FETCH-FAIL; RETRY-ACTION | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

## 3. Locator từ Live DOM

| Tên | Selector | Nguồn recon |
| --- | --- | --- |
| Thẻ chọn học sinh | .student-select-card, [data-testid='student-select-card'] | Khu vực danh sách học sinh |
| Hộp tích chọn học sinh | input[type='checkbox'] | Trên thẻ từng học sinh |
| Thanh tiến trình Bước 1 | .stepper, [aria-label*='step' i] | Đầu biểu mẫu nộp đơn |
| Nút Tiếp tục | button:has-text('Next'), button:has-text('Tiếp tục') | Cuối màn hình Bước 1 |
| Nút Lưu bản nháp | button:has-text('Save Draft'), button:has-text('Lưu nháp') | Dưới cùng biểu mẫu |

## 4. Fixtures

```json
{
  "fixture_reference": "02_step1_student_selection_data.json",
  "design_status": "Not Run",
  "result_fields": "Actual Result và Defect ID để trống phục vụ kiểm thử thực tế"
}
```

## 5. Truy vết và coverage

| ID | Pillar | Nguồn | Section |
| --- | --- | --- | --- |
| BR-CORE | BR | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/02_step1_student_selection.md | Quy tắc nghiệp vụ cốt lõi |
| AC-CORE | AC | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/02_step1_student_selection.md | Tiêu chí nghiệm thu chức năng |
| VAL-12 | Validation | 1_Nghiep_Vu_va_Specs/specs/HUONG_DAN_THIET_KE_TEST_CASE_UAT_5_PILLARS.md | Ma trận kiểm thử hợp lệ ô nhập liệu |
| FLOW-CORE | Flow | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/02_step1_student_selection.md | Luồng tương tác và chuyển đổi trạng thái |
| ERR-CORE | Error | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/02_step1_student_selection.md | Xử lý ngoại lệ và cảnh báo lỗi |

| Đối tượng | Lớp | Trạng thái | TC IDs | Lý do |
| --- | --- | --- | --- | --- |
| Quy tắc nghiệp vụ cốt lõi và phân quyền | BR | Applicable | TC-FAS02-01, TC-FAS02-02 |  |
| Tiêu chí nghiệm thu chức năng chính | AC | Applicable | TC-FAS02-03, TC-FAS02-04 |  |
| Kiểm tra tính hợp lệ dữ liệu ô nhập (Validation) | Validation | Applicable | TC-FAS02-05, TC-FAS02-06 |  |
| Luồng tương tác và chuyển trạng thái (Flow) | Flow | Applicable | TC-FAS02-07, TC-FAS02-08 |  |
| Xử lý lỗi và phản hồi cảnh báo (Error) | Error | Applicable | TC-FAS02-09, TC-FAS02-10 |  |

Kiểm tra cấu trúc không xác nhận đầy đủ nghiệp vụ hoặc chất lượng oracle.
