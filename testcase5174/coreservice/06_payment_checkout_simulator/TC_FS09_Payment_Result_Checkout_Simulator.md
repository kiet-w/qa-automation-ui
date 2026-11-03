# Cổng Dịch vụ Phụ huynh EduSave — Cổng Mô phỏng Thanh toán & Biên lai Điện tử (:5174 / :5176) — Đặc tả Kiểm thử 5 Trụ Cột

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
| TC-CHK-01 | TS-CHK-BR | Tính xác thực biên lai: Giao dịch thành công phải sinh Mã biên nhận duy nhất và trừ công nợ | Quy tắc nghiệp vụ (BR) | Kết quả Thanh toán | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Thanh toán thành công qua cổng thanh toán | Mã biên nhận giao dịch | 2 | 1. Hoàn tất thanh toán trên màn hình mô phỏng.<br>2. Quan sát thông tin trên Biên lai kết quả. | Hệ thống ghi nhận Mã biên lai chuẩn duy nhất (ví dụ: REC-2026-9812); khoản học phí được chuyển trạng thái 'Đã thanh toán'. |  | BR-CHK-IDEMPOTENCY; RECEIPT-GEN |  | BR-CHK-IDEMPOTENCY; RECEIPT-GEN | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-CHK-02 | TS-CHK-BR | Bảo toàn công nợ khi hủy thanh toán: Hủy giao dịch tại cổng giữ nguyên trạng thái nợ của học sinh | Quy tắc nghiệp vụ (BR) | Mô phỏng Thanh toán | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Đang ở cổng thanh toán mô phỏng | Thao tác Hủy giao dịch | 2 | 1. Tại cổng thanh toán, nhấn nút 'Hủy bỏ thanh toán'.<br>2. Quay lại kiểm tra danh sách học phí của con. | Công nợ học phí của con giữ nguyên trạng thái chưa đóng; số dư tài khoản EduSave không bị trừ tiền. |  | BR-CHK-CANCEL-REVERSAL; ZERO-SIDE-EFFECT |  | BR-CHK-CANCEL-REVERSAL; ZERO-SIDE-EFFECT | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### AC

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-CHK-03 | TS-CHK-AC | Màn hình xác nhận hiển thị chi tiết: Tên học sinh, Các khoản phí, Tổng tiền và nút Xác nhận | Tiêu chí nghiệm thu (AC) | Xác nhận Thanh toán | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Đã chọn xong các khoản phí | Màn hình Xem lại & Xác nhận | 2 | 1. Mở màn hình Xác nhận thanh toán.<br>2. Rà soát các thông tin được tóm tắt. | Thông tin học sinh, danh sách khoản thu, số tiền trừ EduSave và số tiền thanh toán trực tuyến hiển thị rõ ràng, chuẩn xác. |  | AC-CHK-REVIEW-PAGE; DOM-CHECKOUT |  | AC-CHK-REVIEW-PAGE; DOM-CHECKOUT | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-CHK-04 | TS-CHK-AC | Màn hình kết quả hiển thị biểu tượng chữ V xanh 'Thanh toán thành công' kèm nút Tải biên lai | Tiêu chí nghiệm thu (AC) | Kết quả Thanh toán | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Giao dịch thanh toán hoàn tất | Màn hình Thông báo kết quả | 2 | 1. Hoàn tất quy trình thanh toán.<br>2. Quan sát màn hình kết quả thông báo. | Biểu tượng tích xanh nổi bật xuất hiện kèm dòng chữ 'Thanh toán thành công'; nút 'Tải biên lai PDF' sẵn sàng hoạt động. |  | AC-CHK-SUCCESS-BANNER; DOM-RESULT |  | AC-CHK-SUCCESS-BANNER; DOM-RESULT | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### Tech/UI

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-CHK-05 | TS-CHK-VAL | Khóa nút 'Xác nhận thanh toán' ngay sau khi nhấp chuột để ngăn trừ tiền lặp lại | Kiểm tra hợp lệ (Validation) | Xác nhận Thanh toán | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Màn hình Xác nhận | Nhấp chuột vào nút Xác nhận | 2 | 1. Nhấp nút 'Xác nhận & Thanh toán'.<br>2. Quan sát trạng thái hiển thị của nút. | Nút chuyển trạng thái 'Đang xử lý...' và làm mờ ngay lập tức; không cho phép nhấp tiếp lần thứ hai. |  | VAL-12 Lớp 8; DEBOUNCE-LOCK |  | VAL-12 Lớp 8; DEBOUNCE-LOCK | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-CHK-06 | TS-CHK-VAL | Hiển thị phân bổ dòng tiền chuẩn xác khi thanh toán kết hợp (EduSave + Cổng trực tuyến) | Kiểm tra hợp lệ (Validation) | Xác nhận Thanh toán | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Khoản phí $100: Trừ $40 EduSave, $60 Trực tuyến | Bảng cơ cấu thanh toán | 2 | 1. Kiểm tra dòng phân bổ trừ Quỹ EduSave ($40.00 SGD).<br>2. Kiểm tra dòng thanh toán qua PayNow ($60.00 SGD). | Tổng hai dòng phân bổ cộng lại khớp chính xác 100% với tổng số tiền học phí $100.00 SGD. |  | VAL-12 Lớp 4; RECONCILIATION |  | VAL-12 Lớp 4; RECONCILIATION | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-CHK-07 | TS-CHK-FLOW | Luồng thanh toán mô phỏng thành công trọn vẹn từ bước xác nhận đến xuất biên lai | Luồng chức năng (Function Flow) | Mô phỏng Thanh toán | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Môi trường Sandbox thanh toán | Chọn kết quả mô phỏng 'Thành công' | 3 | 1. Tại cổng mô phỏng, chọn trạng thái 'Thành công (Success)'.<br>2. Nhấn nút Xác nhận thanh toán.<br>3. Nhận biên lai trên Cổng phụ huynh. | Hệ thống tự động chuyển tiếp về Cổng phụ huynh, hiển thị biên lai thành công và nút quay về Trang chủ. |  | FLOW-CHK-HAPPY-PATH; END-TO-END |  | FLOW-CHK-HAPPY-PATH; END-TO-END | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-CHK-08 | TS-CHK-FLOW | Nhấn nút 'Quay lại' tại màn hình xác nhận để điều chỉnh danh sách khoản phí cần đóng | Luồng chức năng (Function Flow) | Xác nhận Thanh toán | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Màn hình Xác nhận thanh toán | Nút 'Quay lại' (Back) | 2 | 1. Nhấn nút Quay lại từ màn hình Xác nhận.<br>2. Kiểm tra màn hình Danh sách học phí. | Quay về trang chọn học phí thành công; các khoản phí đã chọn trước đó vẫn được giữ nguyên trạng thái tích chọn. |  | FLOW-CHK-BACK-RETAIN; STATE-RETENTION |  | FLOW-CHK-BACK-RETAIN; STATE-RETENTION | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-CHK-09 | TS-CHK-ERR | Mô phỏng thanh toán thất bại (Ngân hàng từ chối/Hết tiền): Báo lỗi rõ ràng và có nút Thử lại | Xử lý lỗi (Error Handling) | Mô phỏng Thanh toán | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Cổng mô phỏng thanh toán | Chọn kết quả 'Thất bại (Failed)' | 2 | 1. Chọn mô phỏng thất bại tại cổng thanh toán.<br>2. Quan sát thông báo khi quay về Cổng phụ huynh. | Màn hình hiển thị dấu X đỏ kèm thông báo: 'Thanh toán không thành công (Ngân hàng từ chối). Vui lòng thử lại'. |  | ERR-CHK-PAYMENT-FAILED; RECOVERY |  | ERR-CHK-PAYMENT-FAILED; RECOVERY | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-CHK-10 | TS-CHK-ERR | Xử lý hết thời gian chờ tại cổng thanh toán (Timeout): Cảnh báo phiên giao dịch hết hạn | Xử lý lỗi (Error Handling) | Mô phỏng Thanh toán | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Quá thời gian thanh toán quy định | Mô phỏng Timeout | 2 | 1. Giữ phiên thanh toán vượt quá thời gian cho phép.<br>2. Quay lại ứng dụng. | Giao diện cảnh báo: 'Phiên thanh toán đã hết hạn vì lý do an toàn. Vui lòng thực hiện lại giao dịch'. |  | ERR-CHK-TIMEOUT; SESSION-SAFETY |  | ERR-CHK-TIMEOUT; SESSION-SAFETY | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

## 3. Locator từ Live DOM

| Tên | Selector | Nguồn recon |
| --- | --- | --- |
| Nút Xác nhận & Thanh toán | button:has-text('Confirm'), button:has-text('Xác nhận') | Màn hình xác nhận |
| Nút Quay lại | button:has-text('Back'), a:has-text('Quay lại') | Đầu hoặc cuối màn hình xác nhận |
| Biểu tượng Thanh toán thành công | .success-icon, [data-testid='success-icon'] | Màn hình kết quả |
| Mã số biên lai | .receipt-number, [data-testid='receipt-number'] | Trên biên lai kết quả |
| Nút Tải biên lai PDF | button:has-text('Download Receipt'), a:has-text('Tải biên lai') | Màn hình kết quả |

## 4. Fixtures

```json
{
  "fixture_reference": "06_payment_checkout_simulator_data.json",
  "design_status": "Not Run",
  "result_fields": "Actual Result và Defect ID để trống phục vụ kiểm thử thực tế"
}
```

## 5. Truy vết và coverage

| ID | Pillar | Nguồn | Section |
| --- | --- | --- | --- |
| BR-CORE | BR | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/06_payment_checkout_simulator.md | Quy tắc nghiệp vụ cốt lõi |
| AC-CORE | AC | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/06_payment_checkout_simulator.md | Tiêu chí nghiệm thu chức năng |
| VAL-12 | Validation | 1_Nghiep_Vu_va_Specs/specs/HUONG_DAN_THIET_KE_TEST_CASE_UAT_5_PILLARS.md | Ma trận kiểm thử hợp lệ ô nhập liệu |
| FLOW-CORE | Flow | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/06_payment_checkout_simulator.md | Luồng tương tác và chuyển đổi trạng thái |
| ERR-CORE | Error | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/06_payment_checkout_simulator.md | Xử lý ngoại lệ và cảnh báo lỗi |

| Đối tượng | Lớp | Trạng thái | TC IDs | Lý do |
| --- | --- | --- | --- | --- |
| Quy tắc nghiệp vụ cốt lõi và phân quyền | BR | Applicable | TC-CHK-01, TC-CHK-02 |  |
| Tiêu chí nghiệm thu chức năng chính | AC | Applicable | TC-CHK-03, TC-CHK-04 |  |
| Kiểm tra tính hợp lệ dữ liệu ô nhập (Validation) | Validation | Applicable | TC-CHK-05, TC-CHK-06 |  |
| Luồng tương tác và chuyển trạng thái (Flow) | Flow | Applicable | TC-CHK-07, TC-CHK-08 |  |
| Xử lý lỗi và phản hồi cảnh báo (Error) | Error | Applicable | TC-CHK-09, TC-CHK-10 |  |

Kiểm tra cấu trúc không xác nhận đầy đủ nghiệp vụ hoặc chất lượng oracle.
