# Cổng Dịch vụ Phụ huynh EduSave — Hỗ trợ Tài chính FAS: Bước 3 - Đính kèm Tài liệu Minh chứng & Cam đoan (:5174) — Đặc tả Kiểm thử 5 Trụ Cột

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
| TC-FAS04-01 | TS-FAS04-BR | Bắt buộc chứng từ thu nhập: Phụ huynh phải đính kèm minh chứng cho thành viên có thu nhập | Quy tắc nghiệp vụ (BR) | FAS Bước 3: Đính kèm Tài liệu | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Thành viên gia đình có khai báo thu nhập | Khu vực tải tài liệu minh chứng | 2 | 1. Mở Bước 3 của hồ sơ FAS.<br>2. Kiểm tra danh sách các tài liệu bắt buộc phải nộp. | Hệ thống đánh dấu rõ các tệp bắt buộc (bảng lương, sao kê ngân hàng) tương ứng với từng thành viên có đi làm. |  | BR-FAS04-MANDATORY-DOCS; PROOF-OF-INCOME |  | BR-FAS04-MANDATORY-DOCS; PROOF-OF-INCOME | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS04-02 | TS-FAS04-BR | Tính pháp lý cam kết: Phụ huynh cam đoan chịu trách nhiệm pháp lý về tính xác thực của tài liệu | Quy tắc nghiệp vụ (BR) | FAS Bước 3: Đính kèm Tài liệu | S1 | High | Not Run | Nghiệp vụ | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Mục Cam kết tính trung thực | Ô cam kết pháp lý | 2 | 1. Đọc nội dung điều khoản cam kết.<br>2. Quan sát điều kiện ràng buộc pháp lý. | Nội dung khẳng định việc khai gian dối hoặc làm giả giấy tờ sẽ bị hủy bỏ hỗ trợ và xử lý theo pháp luật. |  | BR-FAS04-LEGAL-DECLARATION; COMPLIANCE |  | BR-FAS04-LEGAL-DECLARATION; COMPLIANCE | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### AC

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-FAS04-03 | TS-FAS04-AC | Khu vực tải tệp hỗ trợ kéo thả hoặc chọn tệp từ máy tính, hiển thị hướng dẫn rõ ràng | Tiêu chí nghiệm thu (AC) | FAS Bước 3: Đính kèm Tài liệu | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Màn hình Bước 3 | Vùng tải tệp (Dropzone) | 2 | 1. Kiểm tra khu vực tải tệp trên giao diện.<br>2. Quan sát các định dạng được chấp nhận. | Vùng tải tệp hiển thị trực quan; ghi rõ chấp nhận định dạng PDF, PNG, JPG với dung lượng tối đa 5MB mỗi tệp. |  | AC-FAS04-DROPZONE; DOM-STEP3 |  | AC-FAS04-DROPZONE; DOM-STEP3 | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS04-04 | TS-FAS04-AC | Tải tệp thành công hiển thị tên tệp, dung lượng, nút Xem trước và biểu tượng Thùng rác để xóa | Tiêu chí nghiệm thu (AC) | FAS Bước 3: Đính kèm Tài liệu | S2 | High | Not Run | Giao diện | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Đã chọn 1 tệp bảng lương hợp lệ | Tệp: bang_luong_thang_10.pdf (1.2MB) | 2 | 1. Tải lên tệp bảng lương hợp lệ.<br>2. Quan sát dòng tệp vừa được thêm. | Tên tệp hiển thị kèm dung lượng 1.2MB; nút 'Xem trước' và nút 'Xóa tệp' sẵn sàng hoạt động. |  | AC-FAS04-FILE-ITEM; FILE-MANAGEMENT |  | AC-FAS04-FILE-ITEM; FILE-MANAGEMENT | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

### Tech/UI

| ID | Scenario ID | Title | Test Suite | Page | Severity | Priority | Execution Status | Test Type | Environment | Preconditions | Test Data | Steps Test | Test Steps | Expected Result | Actual Result | Assumption Ref | Defect ID | Traceability | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-FAS04-05 | TS-FAS04-VAL | Chặn tải lên tệp không đúng định dạng (chỉ chấp nhận PDF, PNG, JPG; chặn file exe, zip) | Kiểm tra hợp lệ (Validation) | FAS Bước 3: Đính kèm Tài liệu | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Vùng tải tệp | Tệp không đúng định dạng: 'tai_lieu.zip' | 2 | 1. Thử kéo thả tệp .zip hoặc .exe vào vùng tải.<br>2. Quan sát thông báo của hệ thống. | Hệ thống từ chối nhận tệp và hiển thị cảnh báo: 'Định dạng tệp không hợp lệ. Vui lòng chỉ tải tệp PDF, PNG hoặc JPG'. |  | VAL-12 Lớp 4; MIME-TYPE-CHECK |  | VAL-12 Lớp 4; MIME-TYPE-CHECK | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS04-06 | TS-FAS04-VAL | Báo lỗi ngăn chặn khi dung lượng tệp vượt quá mức trần tối đa 5MB quy định | Kiểm tra hợp lệ (Validation) | FAS Bước 3: Đính kèm Tài liệu | S2 | High | Not Run | Kiểm thử nhập liệu | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Vùng tải tệp | Tệp ảnh dung lượng lớn: 'anh_sao_ke.png' (8MB) | 2 | 1. Tải lên tệp có dung lượng 8MB.<br>2. Quan sát phản hồi của hệ thống. | Hệ thống chặn tải lên và cảnh báo: 'Dung lượng tệp vượt quá giới hạn tối đa cho phép (5MB). Vui lòng giảm kích thước tệp'. |  | VAL-12 Lớp 2; FILE-SIZE-BVA |  | VAL-12 Lớp 2; FILE-SIZE-BVA | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS04-07 | TS-FAS04-FLOW | Tải lên đầy đủ tài liệu, tích chọn cam kết tính trung thực và nhấn Tiếp tục sang Bước 4 | Luồng chức năng (Function Flow) | FAS Bước 3: Đính kèm Tài liệu | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Tất cả tài liệu yêu cầu đã tải xong | Tích cam kết và nhấn 'Tiếp tục' | 3 | 1. Tải đầy đủ minh chứng thu nhập.<br>2. Tích vào ô cam kết trung thực.<br>3. Nhấn nút Tiếp tục. | Hệ thống lưu trữ các tệp đính kèm an toàn và chuyển tiếp thẳng vào Bước 4: Rà soát & Nộp đơn. |  | FLOW-FAS04-UPLOAD-PROCEED; WIZARD-NAV |  | FLOW-FAS04-UPLOAD-PROCEED; WIZARD-NAV | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS04-08 | TS-FAS04-FLOW | Xóa một tệp đính kèm tải nhầm và tải lên tệp mới thay thế | Luồng chức năng (Function Flow) | FAS Bước 3: Đính kèm Tài liệu | S2 | High | Not Run | Luồng chức năng | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Đã có 1 tệp đính kèm | Thao tác Xóa và Tải lại | 2 | 1. Nhấn biểu tượng thùng rác để xóa tệp nhầm.<br>2. Chọn tệp mới đúng từ máy tính để tải lên. | Tệp cũ được gỡ bỏ ngay lập tức; tệp mới tải lên thành công và hiển thị ngay ngắn trên danh sách. |  | FLOW-FAS04-REPLACE-FILE; REPLACEMENT |  | FLOW-FAS04-REPLACE-FILE; REPLACEMENT | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS04-09 | TS-FAS04-ERR | Cảnh báo khi nhấn Tiếp tục mà chưa đính kèm đủ chứng từ thu nhập bắt buộc | Xử lý lỗi (Error Handling) | FAS Bước 3: Đính kèm Tài liệu | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Chưa tải minh chứng thu nhập của Cha | Nút 'Tiếp tục' | 2 | 1. Bỏ qua không tải minh chứng thu nhập.<br>2. Nhấn nút Tiếp tục. | Hệ thống chặn lại và cảnh báo màu đỏ: 'Vui lòng đính kèm chứng từ minh chứng thu nhập cho thành viên có đi làm'. |  | ERR-FAS04-MISSING-DOCS; REQUIREMENT |  | ERR-FAS04-MISSING-DOCS; REQUIREMENT | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |
| TC-FAS04-10 | TS-FAS04-ERR | Xử lý sự cố mạng bị ngắt quãng trong quá trình tải tệp lên máy chủ: Cho phép tải lại | Xử lý lỗi (Error Handling) | FAS Bước 3: Đính kèm Tài liệu | S2 | High | Not Run | Xử lý lỗi | Môi trường kiểm thử UAT Cổng Dịch vụ Phụ huynh EduSave | Mạng chập chờn khi tệp đang tải | Tiến trình tải tệp | 2 | 1. Mô phỏng rớt mạng khi thanh phần trăm đang chạy.<br>2. Quan sát thông báo lỗi. | Hệ thống thông báo 'Tải tệp không thành công do sự cố mạng' kèm nút 'Thử lại' để phụ huynh bấm tải lại nhanh chóng. |  | ERR-FAS04-UPLOAD-INTERRUPT; RETRY |  | ERR-FAS04-UPLOAD-INTERRUPT; RETRY | Chụp ảnh màn hình minh chứng các bước và kết quả thực tế khi kiểm thử. |

## 3. Locator từ Live DOM

| Tên | Selector | Nguồn recon |
| --- | --- | --- |
| Vùng kéo thả tải tệp | .dropzone, input[type='file'] | Khu vực tải tệp tài liệu |
| Danh sách tệp đã tải lên | .file-list, [data-testid='file-list'] | Dưới vùng tải tệp |
| Nút Xem trước tệp | button:has-text('Preview'), a:has-text('Xem') | Trên từng dòng tệp |
| Nút Xóa tệp | button:has-text('Delete'), button[aria-label*='delete' i] | Trên từng dòng tệp |
| Ô tích cam kết trung thực | input[type='checkbox'][name*='declaration' i] | Cuối Bước 3 |

## 4. Fixtures

```json
{
  "fixture_reference": "04_step3_documents_and_declaration_data.json",
  "design_status": "Not Run",
  "result_fields": "Actual Result và Defect ID để trống phục vụ kiểm thử thực tế"
}
```

## 5. Truy vết và coverage

| ID | Pillar | Nguồn | Section |
| --- | --- | --- | --- |
| BR-CORE | BR | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/04_step3_documents_and_declaration.md | Quy tắc nghiệp vụ cốt lõi |
| AC-CORE | AC | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/04_step3_documents_and_declaration.md | Tiêu chí nghiệm thu chức năng |
| VAL-12 | Validation | 1_Nghiep_Vu_va_Specs/specs/HUONG_DAN_THIET_KE_TEST_CASE_UAT_5_PILLARS.md | Ma trận kiểm thử hợp lệ ô nhập liệu |
| FLOW-CORE | Flow | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/04_step3_documents_and_declaration.md | Luồng tương tác và chuyển đổi trạng thái |
| ERR-CORE | Error | 1_Nghiep_Vu_va_Specs/specs/ui_bsk/localhost-5174/04_step3_documents_and_declaration.md | Xử lý ngoại lệ và cảnh báo lỗi |

| Đối tượng | Lớp | Trạng thái | TC IDs | Lý do |
| --- | --- | --- | --- | --- |
| Quy tắc nghiệp vụ cốt lõi và phân quyền | BR | Applicable | TC-FAS04-01, TC-FAS04-02 |  |
| Tiêu chí nghiệm thu chức năng chính | AC | Applicable | TC-FAS04-03, TC-FAS04-04 |  |
| Kiểm tra tính hợp lệ dữ liệu ô nhập (Validation) | Validation | Applicable | TC-FAS04-05, TC-FAS04-06 |  |
| Luồng tương tác và chuyển trạng thái (Flow) | Flow | Applicable | TC-FAS04-07, TC-FAS04-08 |  |
| Xử lý lỗi và phản hồi cảnh báo (Error) | Error | Applicable | TC-FAS04-09, TC-FAS04-10 |  |

Kiểm tra cấu trúc không xác nhận đầy đủ nghiệp vụ hoặc chất lượng oracle.
