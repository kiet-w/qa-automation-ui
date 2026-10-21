# Adversarial Testing Toolkit & AI Coding Directives (`tools/break_it`)

> **Triết lý cốt lõi**: *"Có, nên phá, nhưng phải có kỷ luật."*
> Một bộ test automation chỉ chạy "happy path" theo kiểu người dùng ngoan ngoãn sẽ bỏ sót đến 80% các lỗi nghiêm trọng nhất trong môi trường thực tế (server crash unhandled, lộ IDOR, double charge, validation bypass, WSoD trắng màn hình).
>
> **MANDATE CHO AI CODING AGENTS**:
> Khi nhận nhiệm vụ tạo automation test cho bất kỳ User Story, Form, API hay Module nào từ tài liệu spec `[agile] fs/md/`:
> 1. AI Coding **BẮT BUỘC** phải tạo song song:
>    - Bộ test chức năng chuẩn (`test_tsXX_...py`): Kiểm tra Acceptance Criteria (Happy & Negative Path chuẩn).
>    - Bộ test phá có kỷ luật (`test_tsXX_break_it.py` hoặc `tests/break_it/...`): Kiểm tra tính bền bỉ, chống tấn công, vượt rào cản client, và idempotency.
> 2. Mọi test phá phải được gắn decorator: `@pytest.mark.break_it`.
> 3. AI Coding sử dụng bộ công cụ và templates có sẵn ngay trong thư mục này (`tools/break_it/`).

---

## 1. Bảng Ánh Xạ Từ Test Case Thông Thường Sang Test Phá (Adversarial Derivation Matrix)

Khi đọc một Test Case bình thường trong tài liệu, AI Coding tra cứu bảng sau để tự động phái sinh (derive) các kịch bản phá tương ứng:

| Phần tử / Nghiệp vụ trong Test Case gốc | Kỹ thuật Phá cần phái sinh (`@pytest.mark.break_it`) | Helper sử dụng | Kỳ vọng (Oracle) |
| :--- | :--- | :--- | :--- |
| **Trường Text / Name / Input** | **Bypass Client**: Gỡ `maxlength`, gỡ `required`, ép chuỗi 10.000 ký tự qua React setter.<br>**Hostile Strings**: XSS, SQLi, SSTI, null byte, NFC vs NFD tiếng Việt, RTL Ả Rập. | `curricula.strip_client_constraints()`<br>`curricula.force_set_value(selector, val)`<br>`self.naughty_strings` | Server từ chối an toàn hoặc sanitize;<br>Không hiện `alert()` dialog;<br>`assert_no_horizontal_overflow()`. |
| **Trường Email / Phone / Postal** | **Malformed RFC**: Bơm email thiếu domain, ký tự lạ `@#$`, số điện thoại chữ, postal code 7 số. | `curricula.force_set_value(selector, val)` | Server từ chối đúng;<br>`Exceptor.expect_bug_if_accepted()`. |
| **Dropdown `<select>`** | **Schema Tampering**: Inject một `<option>` lạ không nằm trong danh mục DB rồi chọn và submit. | `curricula.inject_select_option(selector, val, label)` | Server chặn enum lạ, không sập 500 unhandled. |
| **Nút Submit / Save / Publish / Pay** | **Concurrency & Debounce**: Double click hoặc click liên tục vào nút thao tác.<br>**Idempotency**: Gửi 2 request Publish liên tiếp. | `locator.dblclick()`<br>`curricula.track_requests(url_pattern)` | Chỉ có duy nhất 1 HTTP request dispatch;<br>Không sinh duplicate charge hay record trùng. |
| **Trường Ẩn / Disabled / Readonly** | **Tampering & Force Click**: Sửa giá tiền/role trong thẻ `<input type="hidden">`; gỡ disabled của nút Submit chưa đủ điều kiện rồi click. | `curricula.set_hidden_field_value(selector, val)`<br>`curricula.enable_element(selector)` | Backend tính giá theo rule máy chủ, bỏ qua số bị client can thiệp. |
| **Thao tác gọi API / Sync** | **Network Chaos**: Giả lập server sập 500, ngắt mạng giữa chừng, mạng 3G chậm. | `curricula.mock_http_response("**/api/**", status=500)`<br>`curricula.simulate_network_failure("**/api/**")`<br>`curricula.set_network_conditions(latency=2000)` | UI hiển thị lỗi thân thiện (Alert/Toast);<br>Không White Screen of Death (WSoD);<br>Spinner không treo vô hạn. |
| **URL có ID bản ghi (`/students/{id}`)** | **IDOR (Phân quyền)**: Dùng session của phụ huynh A để request dữ liệu con của phụ huynh B qua `page.request`. | `self.page.request.get(f"/api/students/{other_id}/...")` | Trả HTTP 401, 403 hoặc 404 (tuyệt đối không lộ dữ liệu). |
| **File Upload (CCCD, Hóa đơn)** | **Malformed Fixtures**: Upload file 0-byte, 11MB, MIME giả mạo, file đuôi kép `.pdf.exe`. | `self.get_fixture_file("data/fixtures/oversized_11mb.pdf")` | Báo lỗi dung lượng/định dạng rõ ràng. |
| **Modal / Dialog / Wizard** | **A11y Boundary**: Dùng phím Tab 10 lần liên tiếp, bấm phím ESC để thoát. | `self.page.keyboard.press("Tab")`<br>`self.page.keyboard.press("Escape")` | Focus di chuyển tuần tự, không bị kẹt trong Focus Trap; ESC đóng được modal. |
| **Mọi kịch bản (All Tests)** | **Invisible Defect Oracle**: Giám sát lỗi ngầm trong suốt vòng đời test. | `Exceptor.expect_zero_js_errors(tech_snapshot)`<br>`self.assert_ui_health()` | 0 Uncaught JS Exceptions;<br>0 `console.error`;<br>0 Silent HTTP 4xx/5xx ngầm. |

---

## 2. Các Công Cụ Có Sẵn Trong Thư Mục Này

### A. CLI Scaffolder: `scaffold_break_it.py`
Tự động sinh khung test `@pytest.mark.break_it` đầy đủ 6 dimensions cho bất kỳ module hoặc Page Object nào:
```bash
# Ví dụ sinh bộ test phá cho form Học phí (Fees) hoặc Curricula
python3 tools/break_it/scaffold_break_it.py \
    --module fs03_fees \
    --page-class FeePublicationPage \
    --page-module pages.fs03.fee_publication_page \
    --output tests/fs03/test_ts05_fee_publication_break_it.py
```

### B. Mẫu Code Snippets: `test_templates.py`
Chứa các function templates hoàn chỉnh, chuẩn PEP-8, kế thừa `BaseTest`, tích hợp sẵn `self.step()`, `Exceptor`, và video recording. AI Coding có thể copy trực tiếp hoặc import để sử dụng.

### C. Công Cụ Kiểm Tra Độ Phủ: `audit_coverage.py`
Quét toàn bộ thư mục `tests/` để đánh giá xem module nào đã có test functional nhưng chưa có kịch bản phá `@pytest.mark.break_it`:
```bash
python3 tools/break_it/audit_coverage.py
```

---

## 3. Bộ 6 Câu Hỏi Đánh Giá Kết Quả Khi Phá (The 6 Oracle Questions)
Mỗi bài test phá do AI tạo ra **BẮT BUỘC** phải xác minh đủ 6 câu hỏi chất lượng sau:
1. **Server có từ chối đúng không?** (Nếu bypass client thành công mà server chấp nhận dữ liệu sai -> `Exceptor.expect_bug_if_accepted()` kích hoạt BUG).
2. **Thông báo lỗi có rõ ràng không?** (Hiển thị đúng trường vi phạm, không vỡ layout).
3. **Có lỗi 5xx, sập JS hoặc rò rỉ stack trace không?** (`Exceptor.expect_zero_js_errors()`).
4. **Có dữ liệu rác/mồ côi lưu vào DB không?** (Khi fail thì DB phải rollback toàn vẹn).
5. **Người dùng có thoát lỗi và làm lại được không?** (UI không đơ, spinner không quay vĩnh viễn qua `assert_no_hanging_spinners()`).
6. **Có hành vi trùng lặp không?** (Double click nút thanh toán/publish không tạo 2 charge).

---

## 4. Năm Quy Tắc Phòng Ngừa Test Nhiễu (Anti-Noise Protocols)
1. **Marker `@pytest.mark.break_it` là bắt buộc**: Tách biệt hoàn toàn khỏi Smoke suite chạy nhanh.
2. **Kỳ vọng dựa trên Spec (Evidence-First)**: Nếu spec không nói rõ hành vi khi nhập chuỗi 10.000 ký tự, assert hệ thống reject hoặc không vỡ layout; không tự đoán string thông báo lỗi. Gắn nhãn `[SPEC GAP]` nếu thiếu quy định.
3. **UUID độc lập**: Mỗi record tạo trong test phá phải có UUID/timestamp riêng và có teardown dọn sạch.
4. **Chỉ test hệ thống nội bộ**: Tuyệt đối không bắn payload XSS/SQLi vào bên thứ ba (Bing, Google, YouTube).
5. **Tránh False Positive**: Nếu script JS bypass được client mà backend chặn đứng -> **ĐÂY LÀ TEST PASS** (hệ thống an toàn), không được đánh fail.
