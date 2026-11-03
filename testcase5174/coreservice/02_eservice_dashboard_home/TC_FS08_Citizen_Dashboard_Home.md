# Cổng Dịch vụ Phụ huynh EduSave — Trang chủ Dịch vụ Công dân & Số dư Quỹ EduSave (:5174) — Đặc tả Kiểm thử 5 Trụ Cột

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
| TC-DSH-01 | TS-DSH-BR | Cô lập thông tin con: Phụ huynh chỉ xem thông tin các con ruột và con nuôi hợp pháp | Quy tắc nghiệp vụ (BR) | Trang chủ Phụ huynh | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Phụ huynh Tan Ah Teck đã đăng nhập | Hồ sơ 2 người con | 2 | 1. Đăng nhập vào Cổng phụ huynh.<br>2. Kiểm tra danh sách thẻ học sinh trên Trang chủ. | Chỉ hiển thị đúng 2 học sinh thuộc gia đình ông Tan Ah Teck; tuyệt đối không hiển thị học sinh gia đình khác. |  | BR-DSH-TENANCY; FAMILY-ISOLATION |  | BR-DSH-TENANCY; FAMILY-ISOLATION | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-DSH-02 | TS-DSH-BR | Quy định số dư EduSave: Chỉ học sinh mang quốc tịch Singapore mới có tài khoản EduSave | Quy tắc nghiệp vụ (BR) | Trang chủ Phụ huynh | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Học sinh quốc tịch Singapore | Thẻ học sinh con | 2 | 1. Quan sát thẻ học sinh mang quốc tịch Singapore.<br>2. Kiểm tra khu vực hiển thị số dư EduSave. | Số dư hiển thị chuẩn xác (ví dụ: $240.00 SGD); nếu con là quốc tịch nước ngoài thì ghi rõ 'Không áp dụng Quỹ EduSave'. |  | BR-DSH-EDUSAVE-ELIGIBLE; CITIZEN-ONLY |  | BR-DSH-EDUSAVE-ELIGIBLE; CITIZEN-ONLY | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### AC

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-DSH-03 | TS-DSH-AC | Trang chủ hiển thị đầy đủ thẻ các con, số dư tài khoản và các nút dịch vụ nhanh | Tiêu chí nghiệm thu (AC) | Trang chủ Phụ huynh | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Đã đăng nhập thành công | Giao diện Trang chủ | 2 | 1. Đăng nhập vào hệ thống.<br>2. Kiểm tra các khu vực nội dung trên Trang chủ. | Hiển thị đầy đủ lời chào phụ huynh, danh sách thẻ học sinh, số dư EduSave và các nút Thanh toán học phí, Nộp đơn FAS. |  | AC-DSH-LAYOUT; DOM-HOME |  | AC-DSH-LAYOUT; DOM-HOME | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-DSH-04 | TS-DSH-AC | Chuyển đổi linh hoạt giữa các con để xem học phí và tình hình học vụ tương ứng | Tiêu chí nghiệm thu (AC) | Trang chủ Phụ huynh | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Gia đình có từ 2 con trở lên | Thẻ chọn học sinh | 2 | 1. Nhấp chọn thẻ của người con thứ hai.<br>2. Quan sát thông tin hiển thị bên dưới. | Thông tin lớp học, trường học và danh sách học phí tự động cập nhật khớp chính xác với người con thứ hai. |  | AC-DSH-SWITCH-CHILD; DYNAMIC-CARD |  | AC-DSH-SWITCH-CHILD; DYNAMIC-CARD | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### Tech/UI

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-DSH-05 | TS-DSH-VAL | Hiển thị định dạng tiền tệ chuẩn Đô-la Singapore có dấu phân cách hàng nghìn | Kiểm tra hợp lệ (Validation) | Trang chủ Phụ huynh | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Học sinh có số dư trên $1,000 | Số dư tài khoản | 2 | 1. Quan sát cách hiển thị các con số tiền tệ trên màn hình.<br>2. Kiểm tra ký hiệu tiền tệ và dấu chấm phẩy. | Số tiền hiển thị chuẩn định dạng Singapore (ví dụ: '$1,250.00 SGD'), dễ đọc và trực quan. |  | VAL-12 Lớp 4; CURRENCY-FORMAT |  | VAL-12 Lớp 4; CURRENCY-FORMAT | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-DSH-06 | TS-DSH-VAL | Nhãn trạng thái công nợ học phí hiển thị đúng màu sắc trực quan theo quy định | Kiểm tra hợp lệ (Validation) | Trang chủ Phụ huynh | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Học sinh có học phí chưa đóng | Huy hiệu trạng thái (Badge) | 2 | 1. Kiểm tra nhãn trạng thái các khoản phí trên thẻ học sinh.<br>2. Quan sát màu sắc biểu thị. | Khoản phí chưa đóng hiển thị màu cam/đỏ 'Chưa thanh toán'; khoản đã đóng hiển thị màu xanh lá 'Đã thanh toán'. |  | VAL-12 Lớp 6; STATUS-BADGE |  | VAL-12 Lớp 6; STATUS-BADGE | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-DSH-07 | TS-DSH-FLOW | Nhấp chọn nút Đóng học phí từ thẻ con chuyển tiếp chính xác vào màn hình Thanh toán | Luồng chức năng (Function Flow) | Trang chủ Phụ huynh | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Thẻ học sinh có công nợ | Nút 'Đóng học phí' | 2 | 1. Nhấp vào nút 'Đóng học phí' trên thẻ con.<br>2. Kiểm tra trang đích được mở ra. | Hệ thống chuyển thẳng vào trang Thanh toán học phí của đúng người con đã chọn, sẵn sàng thao tác. |  | FLOW-DSH-PAY; ROUTE-NAV |  | FLOW-DSH-PAY; ROUTE-NAV | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-DSH-08 | TS-DSH-FLOW | Nhấp chọn nút Nộp đơn FAS chuyển tiếp chính xác vào quy trình Đơn hỗ trợ tài chính | Luồng chức năng (Function Flow) | Trang chủ Phụ huynh | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Thanh dịch vụ nhanh | Nút 'Nộp đơn FAS' | 2 | 1. Nhấp vào nút 'Nộp đơn FAS' trên Trang chủ.<br>2. Quan sát màn hình tiếp theo. | Hệ thống chuyển vào màn hình Giới thiệu chính sách FAS, hiển thị rõ ràng điều kiện xét duyệt. |  | FLOW-DSH-FAS; ROUTE-NAV |  | FLOW-DSH-FAS; ROUTE-NAV | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-DSH-09 | TS-DSH-ERR | Hiển thị thông báo khi học sinh chưa có công nợ học phí phát sinh trong tháng | Xử lý lỗi (Error Handling) | Trang chủ Phụ huynh | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Học sinh không nợ học phí | Khu vực Học phí cần đóng | 2 | 1. Chọn học sinh đã đóng đủ toàn bộ học phí.<br>2. Quan sát khu vực công nợ học phí. | Hiển thị thông báo thân thiện kèm biểu tượng nhẹ nhàng: 'Tuyệt vời! Hiện tại con không có khoản học phí nào cần đóng'. |  | ERR-DSH-EMPTY-FEE; EMPTY-STATE |  | ERR-DSH-EMPTY-FEE; EMPTY-STATE | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-DSH-10 | TS-DSH-ERR | Xử lý tải lại trang khi mạng chập chờn: Hiển thị nút 'Thử lại' không vỡ giao diện | Xử lý lỗi (Error Handling) | Trang chủ Phụ huynh | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Mất kết nối mạng ngắt quãng | Nút 'Tải lại trang' | 2 | 1. Mở Trang chủ trong lúc mạng gián đoạn.<br>2. Nhấn nút Thử lại sau khi mạng ổn định. | Trang chủ tải lại bình thường, các thẻ học sinh và số dư tài khoản hiển thị đầy đủ, không lỗi giao diện. |  | ERR-DSH-RELOAD; RESILIENCE |  | ERR-DSH-RELOAD; RESILIENCE | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

## 3. Locator từ Live DOM

| Tên | Selector | Nguồn recon |
| --- | --- | --- |
| Danh sách thẻ học sinh | .student-card, [data-testid='student-card'] | Khu vực trung tâm Trang chủ |
| Ô số dư EduSave | .edusave-balance, [data-testid='edusave-balance'] | Trên thẻ học sinh |
| Nút Đóng học phí | button:has-text('Pay'), a:has-text('Pay') | Dưới thẻ học sinh |
| Nút Nộp đơn FAS | button:has-text('FAS'), a:has-text('FAS') | Khu vực dịch vụ nổi bật |
| Lời chào phụ huynh | h1, h2, .welcome-header | Đầu trang chủ |

## 4. Fixtures

```json
{
  "fixture_reference": "02_eservice_dashboard_home_data.json",
  "design_status": "Not Run",
  "result_fields": "Actual Result và Defect ID để trống phục vụ kiểm thử thực tế"
}
```

## 5. Truy vết và coverage

| ID | Pillar | Nguồn | Section |
| --- | --- | --- | --- |
| BR-CORE | BR | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/02_eservice_dashboard_home.md | Quy tắc nghiệp vụ cốt lõi |
| AC-CORE | AC | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/02_eservice_dashboard_home.md | Tiêu chí nghiệm thu chức năng |
| VAL-12 | Validation | 1_Nghiep_Vu_va_Specs/specs/HUONG_DAN_THIET_KE_TEST_CASE_UAT_5_PILLARS.md | Ma trận kiểm thử hợp lệ ô nhập liệu |
| FLOW-CORE | Flow | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/02_eservice_dashboard_home.md | Luồng tương tác và chuyển đổi trạng thái |
| ERR-CORE | Error | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/02_eservice_dashboard_home.md | Xử lý ngoại lệ và cảnh báo lỗi |

| Đối tượng | Lớp | Trạng thái | TC IDs | Lý do |
| --- | --- | --- | --- | --- |
| Quy tắc nghiệp vụ cốt lõi và phân quyền | BR | Applicable | TC-DSH-01, TC-DSH-02 |  |
| Tiêu chí nghiệm thu chức năng chính | AC | Applicable | TC-DSH-03, TC-DSH-04 |  |
| Kiểm tra tính hợp lệ dữ liệu ô nhập (Validation) | Validation | Applicable | TC-DSH-05, TC-DSH-06 |  |
| Luồng tương tác và chuyển trạng thái (Flow) | Flow | Applicable | TC-DSH-07, TC-DSH-08 |  |
| Xử lý lỗi và phản hồi cảnh báo (Error) | Error | Applicable | TC-DSH-09, TC-DSH-10 |  |

Kiểm tra cấu trúc không xác nhận đầy đủ nghiệp vụ hoặc chất lượng oracle.
