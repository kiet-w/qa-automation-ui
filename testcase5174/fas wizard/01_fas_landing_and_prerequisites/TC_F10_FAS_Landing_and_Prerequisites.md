# Cổng Dịch vụ Phụ huynh EduSave — Hỗ trợ Tài chính FAS: Giới thiệu & Điều kiện Tiêu chuẩn (:5174) — Đặc tả Kiểm thử 5 Trụ Cột

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
| TC-FAS01-01 | TS-FAS01-BR | Tiêu chuẩn hỗ trợ FAS: Chỉ áp dụng cho học sinh quốc tịch Singapore đạt chuẩn thu nhập | Quy tắc nghiệp vụ (BR) | Giới thiệu Chính sách FAS | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Hồ sơ học sinh | Chính sách FAS Bộ Giáo dục | 2 | 1. Mở trang Giới thiệu chính sách FAS.<br>2. Đọc quy định đối tượng được hưởng chính sách. | Quy định nêu rõ chính sách dành cho công dân Singapore có thu nhập hộ gia đình (GHI/PCI) dưới mức trần quy định. |  | BR-FAS01-ELIGIBILITY; POLICY-RULE |  | BR-FAS01-ELIGIBILITY; POLICY-RULE | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS01-02 | TS-FAS01-BR | Quy định một hồ sơ duy nhất: Mỗi năm học chỉ nộp một bộ đơn chung cho các con trong gia đình | Quy tắc nghiệp vụ (BR) | Giới thiệu Chính sách FAS | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Gia đình đã có đơn FAS đang xử lý | Nút 'Bắt đầu nộp đơn' | 2 | 1. Đăng nhập tài khoản gia đình đã nộp đơn FAS năm nay.<br>2. Quan sát trạng thái trên màn hình giới thiệu. | Hệ thống hiển thị trạng thái hồ sơ đang xử lý kèm mã đơn; không cho phép nộp thêm một đơn trùng lặp. |  | BR-FAS01-ONE-APP-PER-YEAR; SINGLE-ACTIVE |  | BR-FAS01-ONE-APP-PER-YEAR; SINGLE-ACTIVE | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### AC

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-FAS01-03 | TS-FAS01-AC | Hiển thị đầy đủ thông tin quyền lợi FAS (Học phí, Đồng phục, Bữa ăn) và điều kiện tham gia | Tiêu chí nghiệm thu (AC) | Giới thiệu Chính sách FAS | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Màn hình Giới thiệu FAS | Nội dung quyền lợi chính sách | 2 | 1. Mở màn hình Giới thiệu chương trình FAS.<br>2. Kiểm tra các mục thông tin giới thiệu. | Các khối thông tin quyền lợi hỗ trợ (miễn giảm học phí, trợ cấp sách vở, đồng phục) hiển thị rõ ràng, trực quan. |  | AC-FAS01-OVERVIEW; DOM-FAS-LANDING |  | AC-FAS01-OVERVIEW; DOM-FAS-LANDING | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS01-04 | TS-FAS01-AC | Nút 'Bắt đầu nộp đơn hỗ trợ' nổi bật, dẫn thẳng vào Bước 1 của quy trình làm đơn | Tiêu chí nghiệm thu (AC) | Giới thiệu Chính sách FAS | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Gia đình chưa nộp đơn năm nay | Nút 'Bắt đầu nộp đơn' | 2 | 1. Kiểm tra vị trí và khả năng nhấp của nút Bắt đầu.<br>2. Nhấp vào nút. | Hệ thống chuyển tiếp nhanh chóng vào Bước 1 của quy trình Wizard nộp đơn hỗ trợ tài chính. |  | AC-FAS01-START-BTN; ROUTE-STEP1 |  | AC-FAS01-START-BTN; ROUTE-STEP1 | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### Tech/UI

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-FAS01-05 | TS-FAS01-VAL | Bắt buộc tích chọn ô cam kết đã hiểu rõ điều kiện trước khi mở quy trình nộp đơn | Kiểm tra hợp lệ (Validation) | Giới thiệu Chính sách FAS | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Chưa tích ô cam kết | Nút 'Bắt đầu nộp đơn' | 2 | 1. Để trống không tích ô cam kết.<br>2. Thử nhấn nút 'Bắt đầu nộp đơn'. | Nút Bắt đầu bị khóa mờ hoặc hiển thị cảnh báo: 'Vui lòng xác nhận đã đọc và hiểu điều kiện chương trình'. |  | VAL-12 Lớp 1; CHECKBOX-GATE |  | VAL-12 Lớp 1; CHECKBOX-GATE | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS01-06 | TS-FAS01-VAL | Kiểm tra định dạng liên kết tải tài liệu hướng dẫn quy chuẩn chính sách dạng PDF | Kiểm tra hợp lệ (Validation) | Giới thiệu Chính sách FAS | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Liên kết 'Tải tài liệu hướng dẫn' | Tệp tài liệu FAS.pdf | 2 | 1. Rà soát liên kết tải hướng dẫn trên trang.<br>2. Kiểm tra định dạng tệp đính kèm. | Liên kết trỏ đúng tới tệp tài liệu hướng dẫn chính thức định dạng PDF có thể xem và tải về dễ dàng. |  | VAL-12 Lớp 4; PDF-LINK |  | VAL-12 Lớp 4; PDF-LINK | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS01-07 | TS-FAS01-FLOW | Đọc hướng dẫn, tích cam kết hiểu rõ tiêu chuẩn và bắt đầu nộp đơn thành công | Luồng chức năng (Function Flow) | Giới thiệu Chính sách FAS | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Phụ huynh chuẩn bị nộp đơn | Tích cam kết và bấm Bắt đầu | 3 | 1. Đọc nội dung hướng dẫn trên trang.<br>2. Tích vào ô xác nhận cam kết.<br>3. Nhấn 'Bắt đầu nộp đơn'. | Hệ thống chuyển trạng thái trơn tru, hiển thị giao diện Bước 1: Chọn học sinh thụ hưởng. |  | FLOW-FAS01-START; ONBOARDING |  | FLOW-FAS01-START; ONBOARDING | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS01-08 | TS-FAS01-FLOW | Tải về tài liệu hướng dẫn chi tiết về chính sách hỗ trợ tài chính để nghiên cứu | Luồng chức năng (Function Flow) | Giới thiệu Chính sách FAS | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Tài liệu hướng dẫn | Nút 'Tải hướng dẫn (PDF)' | 2 | 1. Nhấn vào nút 'Tải hướng dẫn (PDF)'.<br>2. Kiểm tra tiến trình tải về của trình duyệt. | Tệp PDF được tải về thành công; nội dung trình bày chuẩn chỉ, không bị lỗi font chữ. |  | FLOW-FAS01-DOWNLOAD; ATTACHMENT |  | FLOW-FAS01-DOWNLOAD; ATTACHMENT | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS01-09 | TS-FAS01-ERR | Cảnh báo khi cổng nộp đơn đang trong thời gian bảo trì hoặc đóng kỳ tiếp nhận | Xử lý lỗi (Error Handling) | Giới thiệu Chính sách FAS | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Thời điểm ngoài kỳ tiếp nhận đơn | Thao tác nộp đơn | 2 | 1. Truy cập trang nộp đơn ngoài khung thời gian quy định.<br>2. Quan sát thông báo trên màn hình. | Xuất hiện banner thông báo: 'Kỳ nộp đơn hỗ trợ FAS năm học hiện tại chưa mở hoặc đã kết thúc. Vui lòng liên hệ nhà trường'. |  | ERR-FAS01-CLOSED-WINDOW; SCHEDULE-CHECK |  | ERR-FAS01-CLOSED-WINDOW; SCHEDULE-CHECK | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS01-10 | TS-FAS01-ERR | Xử lý tải trang khi kết nối mạng yếu: Nội dung văn bản hướng dẫn vẫn hiển thị đầy đủ | Xử lý lỗi (Error Handling) | Giới thiệu Chính sách FAS | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Kết nối mạng chập chờn | Tải trang giới thiệu | 2 | 1. Mở trang giới thiệu trong điều kiện mạng yếu.<br>2. Quan sát khả năng hiển thị. | Toàn bộ văn bản hướng dẫn và các tiêu chuẩn chính sách được tải về nguyên vẹn, không bị đứt đoạn giao diện. |  | ERR-FAS01-OFFLINE-CACHE; RESILIENCE |  | ERR-FAS01-OFFLINE-CACHE; RESILIENCE | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

## 3. Locator từ Live DOM

| Tên | Selector | Nguồn recon |
| --- | --- | --- |
| Ô tích cam kết hiểu rõ điều kiện | input[type='checkbox'] | Cuối trang giới thiệu FAS |
| Nút Bắt đầu nộp đơn | button:has-text('Apply'), button:has-text('Bắt đầu') | Dưới cùng trang giới thiệu |
| Liên kết tải tài liệu PDF | a[href*='.pdf' i] | Khung tài liệu tham khảo |
| Khung tóm tắt quyền lợi chính sách | .benefits-grid, [data-testid='fas-benefits'] | Trung tâm trang giới thiệu |
| Banner thông báo trạng thái kỳ nộp | .alert, [role='alert'] | Đầu trang |

## 4. Fixtures

```json
{
  "fixture_reference": "01_fas_landing_and_prerequisites_data.json",
  "design_status": "Not Run",
  "result_fields": "Actual Result và Defect ID để trống phục vụ kiểm thử thực tế"
}
```

## 5. Truy vết và coverage

| ID | Pillar | Nguồn | Section |
| --- | --- | --- | --- |
| BR-CORE | BR | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/01_fas_landing_and_prerequisites.md | Quy tắc nghiệp vụ cốt lõi |
| AC-CORE | AC | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/01_fas_landing_and_prerequisites.md | Tiêu chí nghiệm thu chức năng |
| VAL-12 | Validation | 1_Nghiep_Vu_va_Specs/specs/HUONG_DAN_THIET_KE_TEST_CASE_UAT_5_PILLARS.md | Ma trận kiểm thử hợp lệ ô nhập liệu |
| FLOW-CORE | Flow | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/01_fas_landing_and_prerequisites.md | Luồng tương tác và chuyển đổi trạng thái |
| ERR-CORE | Error | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/01_fas_landing_and_prerequisites.md | Xử lý ngoại lệ và cảnh báo lỗi |

| Đối tượng | Lớp | Trạng thái | TC IDs | Lý do |
| --- | --- | --- | --- | --- |
| Quy tắc nghiệp vụ cốt lõi và phân quyền | BR | Applicable | TC-FAS01-01, TC-FAS01-02 |  |
| Tiêu chí nghiệm thu chức năng chính | AC | Applicable | TC-FAS01-03, TC-FAS01-04 |  |
| Kiểm tra tính hợp lệ dữ liệu ô nhập (Validation) | Validation | Applicable | TC-FAS01-05, TC-FAS01-06 |  |
| Luồng tương tác và chuyển trạng thái (Flow) | Flow | Applicable | TC-FAS01-07, TC-FAS01-08 |  |
| Xử lý lỗi và phản hồi cảnh báo (Error) | Error | Applicable | TC-FAS01-09, TC-FAS01-10 |  |

Kiểm tra cấu trúc không xác nhận đầy đủ nghiệp vụ hoặc chất lượng oracle.
