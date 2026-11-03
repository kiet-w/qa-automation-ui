# Cổng Dịch vụ Phụ huynh EduSave — Hỗ trợ Tài chính FAS: Bước 4 - Rà soát Hồ sơ & Nộp đơn Chính thức (:5174) — Đặc tả Kiểm thử 5 Trụ Cột

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
| TC-FAS05-01 | TS-FAS05-BR | Khóa hồ sơ sau khi nộp: Đơn FAS nộp chính thức chuyển trạng thái 'Đã nộp' và không được tự ý sửa | Quy tắc nghiệp vụ (BR) | FAS Bước 4: Rà soát & Nộp đơn | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Đơn FAS đã nộp thành công | Hồ sơ trên Cổng phụ huynh | 2 | 1. Hoàn tất nộp đơn FAS chính thức.<br>2. Mở lại hồ sơ từ danh sách đơn nộp. | Hồ sơ hiển thị huy hiệu 'Đã tiếp nhận' (SUBMITTED); toàn bộ các trường thông tin ở trạng thái khóa chỉnh sửa. |  | BR-FAS05-SUBMISSION-LOCK; IMMUTABLE-SUBMISSION |  | BR-FAS05-SUBMISSION-LOCK; IMMUTABLE-SUBMISSION | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS05-02 | TS-FAS05-BR | Sinh mã hồ sơ duy nhất: Mỗi lần nộp thành công sinh một Mã hồ sơ chuẩn để theo dõi tiến độ | Quy tắc nghiệp vụ (BR) | FAS Bước 4: Rà soát & Nộp đơn | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Hoàn tất nộp đơn | Mã số hồ sơ (Application ID) | 2 | 1. Nhấn nút Nộp đơn chính thức.<br>2. Quan sát màn hình xác nhận kết quả. | Hệ thống sinh Mã hồ sơ duy nhất (ví dụ: FAS-2026-08912); mã này được lưu vào hệ thống và gửi xác nhận qua SMS/Email. |  | BR-FAS05-APP-ID; TRACKING-KEY |  | BR-FAS05-APP-ID; TRACKING-KEY | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### AC

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-FAS05-03 | TS-FAS05-AC | Màn hình xem lại tổng hợp đầy đủ: Học sinh thụ hưởng, Nhân khẩu, Mức PCI và Các tệp đính kèm | Tiêu chí nghiệm thu (AC) | FAS Bước 4: Rà soát & Nộp đơn | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Đang ở Bước 4 | Trang Xem lại tổng thể | 2 | 1. Kiểm tra giao diện màn hình Bước 4.<br>2. Rà soát từng khối dữ liệu được tổng hợp. | Hiển thị đầy đủ, mạch lạc 4 phần thông tin tương ứng với 3 bước trước; có các nút Chỉnh sửa nhanh cho từng phần. |  | AC-FAS05-REVIEW-LAYOUT; DOM-STEP4 |  | AC-FAS05-REVIEW-LAYOUT; DOM-STEP4 | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS05-04 | TS-FAS05-AC | Màn hình thông báo nộp đơn thành công hiển thị huy hiệu xanh xác nhận và hướng dẫn các bước tiếp theo | Tiêu chí nghiệm thu (AC) | FAS Bước 4: Rà soát & Nộp đơn | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Nộp đơn thành công | Màn hình Thông báo kết quả | 2 | 1. Nhấn nút Nộp đơn.<br>2. Quan sát màn hình kết quả được mở ra. | Biểu tượng tích xanh nổi bật xuất hiện kèm dòng chữ: 'Đơn hỗ trợ tài chính đã được nộp thành công' và thời gian xử lý dự kiến. |  | AC-FAS05-SUCCESS-BANNER; CONFIRMATION |  | AC-FAS05-SUCCESS-BANNER; CONFIRMATION | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### Tech/UI

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-FAS05-05 | TS-FAS05-VAL | Bắt buộc tích chọn ô cam kết cuối cùng trước khi cho phép bấm nút 'Nộp đơn chính thức' | Kiểm tra hợp lệ (Validation) | FAS Bước 4: Rà soát & Nộp đơn | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Chưa tích cam đoan sự thật | Nút 'Nộp đơn chính thức' | 2 | 1. Để trống không tích ô cam kết sự thật.<br>2. Quan sát nút 'Nộp đơn chính thức'. | Nút Nộp đơn bị làm mờ (disabled); khi di chuột vào hiển thị nhắc nhở cần tích xác nhận cam đoan. |  | VAL-12 Lớp 1; FINAL-DECLARATION-GATE |  | VAL-12 Lớp 1; FINAL-DECLARATION-GATE | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS05-06 | TS-FAS05-VAL | Khóa nút Nộp đơn và hiển thị vòng xoay đang xử lý ngay sau khi nhấp chuột | Kiểm tra hợp lệ (Validation) | FAS Bước 4: Rà soát & Nộp đơn | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Đã tích cam kết | Nhấp nút 'Nộp đơn chính thức' | 2 | 1. Nhấn nút 'Nộp đơn chính thức'.<br>2. Quan sát phản ứng của nút bấm. | Nút lập tức chuyển chữ 'Đang gửi hồ sơ...' và vô hiệu hóa nhấp chuột để tránh gửi 2 lần. |  | VAL-12 Lớp 8; SUBMIT-IN-FLIGHT |  | VAL-12 Lớp 8; SUBMIT-IN-FLIGHT | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS05-07 | TS-FAS05-FLOW | Quy trình rà soát toàn diện, tích cam kết và nộp đơn thành công nhận mã biên nhận | Luồng chức năng (Function Flow) | FAS Bước 4: Rà soát & Nộp đơn | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Hồ sơ hợp lệ đầy đủ thông tin | Nút 'Nộp đơn chính thức' | 3 | 1. Rà soát thông tin tại các khối.<br>2. Tích chọn cam kết trung thực.<br>3. Nhấn 'Nộp đơn chính thức'. | Quy trình hoàn tất mỹ mãn; màn hình chuyển sang thông báo thành công kèm nút Tải bản sao đơn đã nộp (PDF). |  | FLOW-FAS05-SUBMIT-HAPPY; END-TO-END |  | FLOW-FAS05-SUBMIT-HAPPY; END-TO-END | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS05-08 | TS-FAS05-FLOW | Nhấp liên kết 'Chỉnh sửa' tại mục Nhân khẩu để quay lại sửa đổi dữ liệu Bước 2 | Luồng chức năng (Function Flow) | FAS Bước 4: Rà soát & Nộp đơn | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Màn hình Xem lại Bước 4 | Nút 'Chỉnh sửa' tại mục Nhân khẩu | 2 | 1. Nhấn nút Chỉnh sửa ở khối Nhân khẩu.<br>2. Kiểm tra màn hình được mở ra. | Hệ thống đưa người dùng quay lại đúng Bước 2; sau khi sửa xong nhấn Tiếp tục sẽ quay lại ngay Bước 4 rà soát. |  | FLOW-FAS05-EDIT-SHORTCUT; DEEP-NAV |  | FLOW-FAS05-EDIT-SHORTCUT; DEEP-NAV | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS05-09 | TS-FAS05-ERR | Ngăn chặn nhấp chuột liên tiếp nhiều lần gây trùng lặp gửi hồ sơ lên máy chủ | Xử lý lỗi (Error Handling) | FAS Bước 4: Rà soát & Nộp đơn | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Nút Nộp đơn chính thức | Nhấp đúp chuột thật nhanh 2 lần | 2 | 1. Nhấp nhanh liên tiếp 2 lần vào nút Nộp đơn.<br>2. Kiểm tra số lượng hồ sơ được tạo trên hệ thống. | Chỉ có duy nhất 1 bộ hồ sơ được tạo ra; yêu cầu nhấp thứ hai bị chặn an toàn bởi cơ chế chống trùng lặp. |  | ERR-FAS05-DEBOUNCE; IDEMPOTENCY |  | ERR-FAS05-DEBOUNCE; IDEMPOTENCY | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS05-10 | TS-FAS05-ERR | Xử lý khi máy chủ gián đoạn lúc gửi đơn: Giữ an toàn bản nháp và cho phép bấm gửi lại | Xử lý lỗi (Error Handling) | FAS Bước 4: Rà soát & Nộp đơn | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Mất kết nối máy chủ khi đang nộp | Nút 'Thử gửi lại' | 2 | 1. Mô phỏng lỗi máy chủ khi nhấn Nộp đơn.<br>2. Quan sát giao diện thông báo. | Hệ thống thông báo 'Gửi đơn chưa thành công do gián đoạn kết nối. Bản nháp của bạn đã được lưu an toàn' kèm nút Thử lại. |  | ERR-FAS05-SERVER-FAIL; DRAFT-SAFETY |  | ERR-FAS05-SERVER-FAIL; DRAFT-SAFETY | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

## 3. Locator từ Live DOM

| Tên | Selector | Nguồn recon |
| --- | --- | --- |
| Khối thông tin Học sinh thụ hưởng | .review-students, [data-testid='review-students'] | Bước 4 Xem lại |
| Khối thông tin Nhân khẩu & Thu nhập | .review-household, [data-testid='review-household'] | Bước 4 Xem lại |
| Khối tài liệu đính kèm | .review-documents, [data-testid='review-documents'] | Bước 4 Xem lại |
| Ô tích cam kết nộp đơn | input[type='checkbox'][name*='finalConfirm' i] | Cuối trang Bước 4 |
| Nút Nộp đơn chính thức | button:has-text('Submit Application'), button:has-text('Nộp đơn') | Cuối trang Bước 4 |

## 4. Fixtures

```json
{
  "fixture_reference": "05_step4_review_and_submission_data.json",
  "design_status": "Not Run",
  "result_fields": "Actual Result và Defect ID để trống phục vụ kiểm thử thực tế"
}
```

## 5. Truy vết và coverage

| ID | Pillar | Nguồn | Section |
| --- | --- | --- | --- |
| BR-CORE | BR | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/05_step4_review_and_submission.md | Quy tắc nghiệp vụ cốt lõi |
| AC-CORE | AC | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/05_step4_review_and_submission.md | Tiêu chí nghiệm thu chức năng |
| VAL-12 | Validation | 1_Nghiep_Vu_va_Specs/specs/HUONG_DAN_THIET_KE_TEST_CASE_UAT_5_PILLARS.md | Ma trận kiểm thử hợp lệ ô nhập liệu |
| FLOW-CORE | Flow | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/05_step4_review_and_submission.md | Luồng tương tác và chuyển đổi trạng thái |
| ERR-CORE | Error | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/05_step4_review_and_submission.md | Xử lý ngoại lệ và cảnh báo lỗi |

| Đối tượng | Lớp | Trạng thái | TC IDs | Lý do |
| --- | --- | --- | --- | --- |
| Quy tắc nghiệp vụ cốt lõi và phân quyền | BR | Applicable | TC-FAS05-01, TC-FAS05-02 |  |
| Tiêu chí nghiệm thu chức năng chính | AC | Applicable | TC-FAS05-03, TC-FAS05-04 |  |
| Kiểm tra tính hợp lệ dữ liệu ô nhập (Validation) | Validation | Applicable | TC-FAS05-05, TC-FAS05-06 |  |
| Luồng tương tác và chuyển trạng thái (Flow) | Flow | Applicable | TC-FAS05-07, TC-FAS05-08 |  |
| Xử lý lỗi và phản hồi cảnh báo (Error) | Error | Applicable | TC-FAS05-09, TC-FAS05-10 |  |

Kiểm tra cấu trúc không xác nhận đầy đủ nghiệp vụ hoặc chất lượng oracle.
