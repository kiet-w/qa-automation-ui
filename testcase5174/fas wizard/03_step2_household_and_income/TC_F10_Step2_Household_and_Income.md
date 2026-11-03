# Cổng Dịch vụ Phụ huynh EduSave — Hỗ trợ Tài chính FAS: Bước 2 - Nhân khẩu & Kê khai Thu nhập GHI/PCI (:5174) — Đặc tả Kiểm thử 5 Trụ Cột

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
| TC-FAS03-01 | TS-FAS03-BR | Tự động tính thu nhập chuẩn: Tính Tổng thu nhập gia đình (GHI) và Bình quân đầu người (PCI) | Quy tắc nghiệp vụ (BR) | FAS Bước 2: Kê khai Thu nhập | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Kê khai các thành viên có thu nhập | Thu nhập của cha và mẹ | 2 | 1. Khai thu nhập của cha ($2,000) và mẹ ($1,000) trong gia đình 4 người.<br>2. Quan sát ô GHI và PCI. | Hệ thống tự động tính: GHI = $3,000.00 SGD; PCI = $750.00 SGD ($3,000 / 4 người) theo đúng công thức quy định. |  | BR-FAS03-PCI-FORMULA; AUTO-CALC |  | BR-FAS03-PCI-FORMULA; AUTO-CALC | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS03-02 | TS-FAS03-BR | Kê khai nhân khẩu: Bắt buộc kê khai đầy đủ các thành viên sống chung cùng hộ để tính chính xác PCI | Quy tắc nghiệp vụ (BR) | FAS Bước 2: Kê khai Thu nhập | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Thêm các thành viên gia đình | Danh sách thành viên | 2 | 1. Thêm từng thành viên gia đình vào biểu mẫu.<br>2. Quan sát chỉ số Tổng số nhân khẩu. | Tổng nhân khẩu cập nhật tương ứng với từng thành viên được thêm; làm căn cứ tính toán mức hỗ trợ công bằng. |  | BR-FAS03-HOUSEHOLD-INTEGRITY; HEADCOUNT |  | BR-FAS03-HOUSEHOLD-INTEGRITY; HEADCOUNT | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### AC

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-FAS03-03 | TS-FAS03-AC | Biểu mẫu cho phép thêm mới thành viên: Họ tên, NRIC, Mối quan hệ, Nghề nghiệp và Thu nhập | Tiêu chí nghiệm thu (AC) | FAS Bước 2: Kê khai Thu nhập | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Màn hình Bước 2 | Biểu mẫu Thêm thành viên | 2 | 1. Nhấn nút 'Thêm thành viên'.<br>2. Kiểm tra các trường thông tin trong form. | Hiển thị đầy đủ các ô nhập: Họ và tên, Số NRIC, Mối quan hệ (Cha/Mẹ/Anh/Chị/Em), Tình trạng việc làm và Thu nhập tháng. |  | AC-FAS03-ADD-MEMBER-FORM; DOM-STEP2 |  | AC-FAS03-ADD-MEMBER-FORM; DOM-STEP2 | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS03-04 | TS-FAS03-AC | Khung tóm tắt tự động cập nhật mức GHI và PCI tức thì ngay khi chỉnh sửa thu nhập | Tiêu chí nghiệm thu (AC) | FAS Bước 2: Kê khai Thu nhập | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Đã có danh sách 3 thành viên | Sửa ô Thu nhập của 1 thành viên | 2 | 1. Sửa mức thu nhập của thành viên từ $1,000 thành $1,500.<br>2. Quan sát bảng tóm tắt bên cạnh. | Tổng thu nhập GHI và mức PCI lập tức cập nhật giá trị mới một cách mượt mà mà không giật màn hình. |  | AC-FAS03-REACTIVE-SUMMARY; INSTANT-UPDATE |  | AC-FAS03-REACTIVE-SUMMARY; INSTANT-UPDATE | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### Tech/UI

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-FAS03-05 | TS-FAS03-VAL | Báo lỗi viền đỏ khi để trống Họ tên hoặc Mối quan hệ của thành viên được thêm | Kiểm tra hợp lệ (Validation) | FAS Bước 2: Kê khai Thu nhập | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Form thêm thành viên | Họ tên để trống, chọn quan hệ Cha | 2 | 1. Để trống ô Họ tên và nhấn Thêm.<br>2. Quan sát phản hồi của form. | Ô Họ tên hiển thị viền đỏ cảnh báo: 'Vui lòng nhập họ và tên của thành viên gia đình'. |  | VAL-12 Lớp 1; MANDATORY-FIELD |  | VAL-12 Lớp 1; MANDATORY-FIELD | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS03-06 | TS-FAS03-VAL | Kiểm tra ô Thu nhập tháng: Chặn nhập số âm hoặc ký tự đặc biệt | Kiểm tra hợp lệ (Validation) | FAS Bước 2: Kê khai Thu nhập | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Form thêm thành viên | Thu nhập nhập '-500' | 2 | 1. Nhập số âm '-500' vào ô Thu nhập hàng tháng.<br>2. Quan sát phản hồi. | Ô nhập chặn số âm và báo lỗi: 'Thu nhập hàng tháng không thể là số âm (tối thiểu là $0 nếu không đi làm)'. |  | VAL-12 Lớp 3; POSITIVE-INCOME |  | VAL-12 Lớp 3; POSITIVE-INCOME | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS03-07 | TS-FAS03-FLOW | Quy trình thêm đầy đủ thành viên gia đình, kiểm tra PCI và nhấn Tiếp tục sang Bước 3 | Luồng chức năng (Function Flow) | FAS Bước 2: Kê khai Thu nhập | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Kê khai hoàn tất các thành viên | Nút 'Tiếp tục' | 3 | 1. Thêm đầy đủ thông tin cha, mẹ, học sinh.<br>2. Đọc kết quả tính toán PCI.<br>3. Nhấn nút Tiếp tục. | Hệ thống ghi nhận toàn bộ thông tin nhân khẩu và chuyển tiếp suôn sẻ sang Bước 3: Đính kèm tài liệu minh chứng. |  | FLOW-FAS03-COMPLETE-PROCEED; WIZARD-STEP |  | FLOW-FAS03-COMPLETE-PROCEED; WIZARD-STEP | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS03-08 | TS-FAS03-FLOW | Xóa một thành viên nhập nhầm kèm hộp thoại hỏi lại an toàn trước khi xóa | Luồng chức năng (Function Flow) | FAS Bước 2: Kê khai Thu nhập | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Đang có 4 thành viên trong danh sách | Nút Xóa tại dòng thành viên | 2 | 1. Nhấn biểu tượng thùng rác tại dòng thành viên nhập nhầm.<br>2. Nhấn 'Xác nhận xóa' trên hộp thoại. | Dòng thành viên biến mất ngay lập tức; tổng số nhân khẩu và chỉ số PCI được tính toán lại chính xác. |  | FLOW-FAS03-DELETE-MEMBER; CONFIRM-MODAL |  | FLOW-FAS03-DELETE-MEMBER; CONFIRM-MODAL | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS03-09 | TS-FAS03-ERR | Cảnh báo khi tổng số nhân khẩu nhỏ hơn số lượng học sinh thụ hưởng đã chọn ở Bước 1 | Xử lý lỗi (Error Handling) | FAS Bước 2: Kê khai Thu nhập | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Bước 1 chọn 2 con; Bước 2 chỉ khai 1 người | Nhấn nút Tiếp tục | 2 | 1. Để số lượng thành viên ít hơn số con đã chọn ở Bước 1.<br>2. Nhấn Tiếp tục. | Hệ thống chặn lại và cảnh báo: 'Tổng số nhân khẩu không thể nhỏ hơn số lượng học sinh thụ hưởng trong đơn'. |  | ERR-FAS03-HEADCOUNT-CONFLICT; INTEGRITY |  | ERR-FAS03-HEADCOUNT-CONFLICT; INTEGRITY | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS03-10 | TS-FAS03-ERR | Hiển thị lưu ý cảnh báo nhẹ nếu mức thu nhập PCI vượt mức trần xét duyệt hỗ trợ | Xử lý lỗi (Error Handling) | FAS Bước 2: Kê khai Thu nhập | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Mức PCI tính ra $1,500 (trên mức trần $1,100) | Khung tóm tắt PCI | 2 | 1. Nhập thu nhập khiến mức PCI vượt trần tiêu chuẩn.<br>2. Quan sát khung tóm tắt. | Xuất hiện hộp lưu ý màu vàng: 'Mức PCI hiện tại cao hơn tiêu chuẩn thông thường. Đơn của bạn sẽ cần nhà trường xem xét đặc biệt'. |  | ERR-FAS03-PCI-EXCEEDED-NOTE; ADVISORY |  | ERR-FAS03-PCI-EXCEEDED-NOTE; ADVISORY | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

## 3. Locator từ Live DOM

| Tên | Selector | Nguồn recon |
| --- | --- | --- |
| Nút Thêm thành viên | button:has-text('Add Member'), button:has-text('Thêm thành viên') | Đầu danh sách thành viên |
| Ô nhập Họ và tên thành viên | input[name*='memberName' i] | Form thêm thành viên |
| Ô nhập Thu nhập hàng tháng | input[name*='income' i] | Form thêm thành viên |
| Hộp chọn Mối quan hệ | select[name*='relation' i] | Form thêm thành viên |
| Khung tóm tắt GHI và PCI | .income-summary, [data-testid='income-summary'] | Bên phải hoặc cuối Bước 2 |

## 4. Fixtures

```json
{
  "fixture_reference": "03_step2_household_and_income_data.json",
  "design_status": "Not Run",
  "result_fields": "Actual Result và Defect ID để trống phục vụ kiểm thử thực tế"
}
```

## 5. Truy vết và coverage

| ID | Pillar | Nguồn | Section |
| --- | --- | --- | --- |
| BR-CORE | BR | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/03_step2_household_and_income.md | Quy tắc nghiệp vụ cốt lõi |
| AC-CORE | AC | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/03_step2_household_and_income.md | Tiêu chí nghiệm thu chức năng |
| VAL-12 | Validation | 1_Nghiep_Vu_va_Specs/specs/HUONG_DAN_THIET_KE_TEST_CASE_UAT_5_PILLARS.md | Ma trận kiểm thử hợp lệ ô nhập liệu |
| FLOW-CORE | Flow | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/03_step2_household_and_income.md | Luồng tương tác và chuyển đổi trạng thái |
| ERR-CORE | Error | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/03_step2_household_and_income.md | Xử lý ngoại lệ và cảnh báo lỗi |

| Đối tượng | Lớp | Trạng thái | TC IDs | Lý do |
| --- | --- | --- | --- | --- |
| Quy tắc nghiệp vụ cốt lõi và phân quyền | BR | Applicable | TC-FAS03-01, TC-FAS03-02 |  |
| Tiêu chí nghiệm thu chức năng chính | AC | Applicable | TC-FAS03-03, TC-FAS03-04 |  |
| Kiểm tra tính hợp lệ dữ liệu ô nhập (Validation) | Validation | Applicable | TC-FAS03-05, TC-FAS03-06 |  |
| Luồng tương tác và chuyển trạng thái (Flow) | Flow | Applicable | TC-FAS03-07, TC-FAS03-08 |  |
| Xử lý lỗi và phản hồi cảnh báo (Error) | Error | Applicable | TC-FAS03-09, TC-FAS03-10 |  |

Kiểm tra cấu trúc không xác nhận đầy đủ nghiệp vụ hoặc chất lượng oracle.
