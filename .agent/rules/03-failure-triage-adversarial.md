# RULE MODULE 03: 9-TIER FAILURE EVALUATION & ADVERSARIAL TESTING ("PHÁ CÓ KỶ LUẬT")
> **Mục đích**: Áp dụng khi phân tích nguyên nhân test fail (triage), đánh giá sức khỏe toàn diện UI và viết bộ test resilience/chaos (`@pytest.mark.break_it`) thuộc coverage mandate của Invariant 7.
> **Trọng tâm**: 9 Tầng tiêu chí kích hoạt test FAIL, Triage Matrix, và 6 nhóm kỹ thuật phá có kỷ luật kèm bộ helper methods.

> [!IMPORTANT]
> **Safety, execution & path contract**: Chỉ thực hiện adversarial testing trên môi trường QA/Staging nội bộ được User cho phép. AI không tự chạy pytest hoặc break-it scripts theo Invariant 11. Code/tài liệu luôn dùng canonical paths (`tests/`, `pages/`, `data/`, `reports/`); ba folder đánh số chỉ là navigation views bằng symlink.

### Invariant 7: 9-Tier UI Automation Failure Evaluation Framework (Beyond AC & Business Rules)
> **Nguyên tắc cốt lõi**: Một bài test UI không chỉ verify kết quả đầu ra của nghiệp vụ (AC/Business Rules), mà phải là một **màng lọc toàn diện về độ ổn định kỹ thuật (Technical Health), trải nghiệm người dùng (UX/Visual), hiệu năng (SLA), khả năng tiếp cận (Accessibility), và tính toàn vẹn của hệ thống (System Integrity)**.
> Khi đánh giá một kịch bản kiểm thử là **FAIL**, bài test phải kiểm tra và kích hoạt FAIL trên cả 9 tầng tiêu chí sau:

```text
                              BỘ TIÊU CHÍ ĐÁNH GIÁ TEST FAIL
 ┌───────────────────────────┼───────────────────────────┐
 ▼                           ▼                           ▼
[1] TẦNG RUNTIME CLIENT     [2] TẦNG NETWORK & API      [3] TẦNG VISUAL & LAYOUT
 - Uncaught JS Exception     - HTTP 4xx/5xx ngầm         - Element overlap / Z-index
 - Framework Crash (WSoD)    - Failed Asset / 404 Chunk  - Layout Clipping / Overflow
 - Memory Leaks              - GraphQL/REST silent fail  - Broken Images / Fonts
 ┌───────────────────────────┼───────────────────────────┐
 ▼                           ▼                           ▼
[4] TẦNG ACTIONABILITY      [5] TẦNG HIỆU NĂNG & SLA    [6] TẦNG ACCESSIBILITY (A11Y)
 - Pointer-events Disabled   - TTI / LCP vượt ngưỡng     - Focus Trap (Kẹt phím Tab)
 - Element Stale / Detached  - Long Task Freeze UI       - Contrast Ratio < 4.5:1
 - Spinner Treo Vô Hạn       - Action Latency > 3000ms   - Missing ARIA / Labels
 ┌───────────────────────────┼───────────────────────────┐
 ▼                           ▼                           ▼
[7] TẦNG DỮ LIỆU NGOẠI VI   [8] TẦNG BẢO MẬT GIAO DIỆN  [9] TẦNG IDEMPOTENCY & ISOLATION
 - File tải về 0 Bytes       - PII rò rỉ trong DOM       - Data Collision (Chạy song song)
 - Corrupted Excel/PDF       - Mixed Content (HTTP/HTTPS)- Test Leaks (Không dọn dẹp)
 - LocalStorage Malformed    - Token lộ trong URL        - Flaky do Race Condition
```

#### Chi tiết 9 Tầng Tiêu Chí Kích Hoạt Test FAIL:
1. **Tầng Runtime & Console Logs (Client-side Health)**:
   - *FAIL khi*: Xuất hiện Uncaught JS Exceptions (`TypeError`, `ReferenceError`), Promise Rejection chưa xử lý, hoặc sập cây component React/Vue (White Screen of Death - WSoD).
2. **Tầng Mạng & API Tích Hợp (Network & Silent Failures)**:
   - *FAIL khi*: Có bất kỳ request background sync/API trả về HTTP 4xx/5xx ngầm mà UI không hiển thị thông báo lỗi; asset chunks/CSS/images bị 404; CORS bị trình duyệt block; API treo > 30s không timeout; hoặc API 200 trả về payload `errors: [...]` nhưng UI hiển thị màn hình trống.
3. **Tầng Hiển Thị, Layout & Trải Nghiệm Thị Giác (Visual & Layout Integrity)**:
   - *FAIL khi*: Element bị overlap/che khuất bởi sticky header/backdrop modal (Z-Index Conflict); xuất hiện thanh cuộn ngang ngoài ý muốn (`overflow-x: auto/scroll`); text/số tiền quan trọng bị cắt mất (`ellipsis`) mà không có tooltip; ảnh `<img>` vỡ kích thước 0x0 (`naturalWidth === 0`) hoặc font icon biến thành ô vuông (`tofu characters: □`).
4. **Tầng Tương Tác & Trạng Thái Phần Tử (Element Actionability & DOM State)**:
   - *FAIL khi*: Element bị kẹt animation/vị trí không ổn định; `pointer-events: none` vô hiệu thao tác người dùng; biểu tượng Spinner loading / Skeleton quay vô tận không tự tắt sau timeout (ví dụ: > 5s); hoặc nút bấm không disable sau click đầu tiên dẫn tới duplicate submission.
5. **Tầng Hiệu Năng & Độ Trễ Giao Diện (Performance & SLA Thresholds)**:
   - *FAIL khi*: Vi phạm Core Web Vitals (LCP > 2.5s, CLS > 0.1, INP > 200ms); Action Latency từ khi click Submit đến phản hồi đầu tiên > 1.5s (hoặc > 3s theo SLA module); JS Heap memory leak tăng liên tục không giải phóng sau các lượt navigation SPA.
6. **Tầng Khả Năng Tiếp Cận & Khả Dụng (Accessibility & Usability - WCAG 2.1)**:
   - *FAIL khi*: Kẹt bàn phím (Keyboard Focus Trap) trong modal/dropdown không thoát được bằng `Tab`/`Esc`; mất khung viền Focus Indicator; trật tự Tab lộn xộn; hoặc vi phạm Axe-core nghiêm trọng (Tỉ lệ tương phản màu < 4.5:1, icon button thiếu `aria-label`).
7. **Tầng Dữ Liệu Ngoại Vi & Lưu Trữ Client (Client Storage & I/O Integrity)**:
   - *FAIL khi*: File export/download có kích thước 0 Bytes, file `.xlsx`/`.pdf` bị corrupt hoặc thực chất là trang lỗi HTML trá hình; dữ liệu LocalStorage không parse được JSON (`Malformed JSON`); Cookie phiên thiếu cờ `SameSite`/`Secure`.
8. **Tầng Bảo Mật Bề Mặt Giao Diện (Client-Side Security)**:
   - *FAIL khi*: Rò rỉ PII (mật khẩu, OTP, CCCD/NRIC) dạng plain-text trong DOM attributes (`data-nric`, `data-value`) hoặc trên URL query string; cho phép phản xạ XSS injection (`<script>`, `<img onerror>`); cảnh báo Mixed Content HTTP trên trang HTTPS.
9. **Tầng Ổn Định & Cô Lập Môi Trường (Test Harness, Isolation & Flakiness)**:
   - *FAIL khi*: Vi phạm tính Idempotency (chạy lần 1 pass, lần 2 fail do không rollback/cleanup data); xung đột chạy song song (Parallel Collision do dùng chung tài khoản/bản ghi); Flaky do race condition giữa frontend navigate và backend DB persist.

#### Bảng Ma Trận Phân Loại Nguyên Nhân Khi Test Fail (Triage Matrix):
| Phân Loại Thất Bại | Biểu Hiện | Trách Nhiệm Xử Lý |
| :--- | :--- | :--- |
| **Product Defect (Lỗi Nghiệp vụ)** | AC không đạt, tính sai tiền, chuyển sai trạng thái dữ liệu. | **Dev Backend / BA** |
| **Frontend Defect (Lỗi Giao diện ngầm)** | Vỡ layout, console error, WSoD, nút bị che z-index, HTTP 500 ngầm. | **Dev Frontend / UI Designer** |
| **Performance / SLA Defect** | Trang tải > 5s, spinner quay vô tận, lag đơ giao diện. | **Dev Team / DevOps** |
| **Accessibility Defect** | Không thao tác được bằng bàn phím, kẹt focus, vi phạm WCAG. | **UI/UX & Frontend** |
| **Automation Defect (Script kém)** | Dùng hardcoded sleep, selector sai, không dọn test data rác, flaky. | **QA Automation Engineer** |
| **Infrastructure Defect** | Môi trường test sập, mạng chập chờn, browser crash OOM (Out of Memory). | **DevOps / CI-CD Admin** |

#### Quy Chuẩn Áp Dụng Cho Từng Module Cụ Thể:
- Mọi phân hệ nghiệp vụ (`fs08`, `f01`, `fs03`, `fs09`...) phải ánh xạ các tiêu chí Applicable vào coverage matrix tại `testcases/<module>/<ticket>/`; không tạo một đường dẫn tài liệu song song ngoài cấu trúc chuẩn.
- Mọi giá trị timeout, regex, mã lỗi, endpoint, trạng thái giao diện trong tài liệu module phải trích xuất 100% từ tài liệu gốc (`[Agile] FS.md`, Decisions D-xx, Message catalogs), **TUYỆT ĐỐI KHÔNG ĐƯỢC GIẢ ĐỊNH (ZERO ASSUMPTIONS)**.

### Disciplined Adversarial & Edge Case Testing ("Phá Có Kỷ Luật" - Resilience & Chaos Quality Gate)
> **Triết lý cốt lõi**: **"Có, nên phá, nhưng phải có kỷ luật."** Một bộ automation chỉ chạy "happy path" như một người dùng ngoan ngoãn sẽ bỏ sót phần lớn các lỗi nghiêm trọng nhất (server crash, mất tính toàn vẹn dữ liệu, rò rỉ IDOR, double-charging, validation bypass).
> Automation testing phải chủ động thử thách tính bền bỉ của hệ thống bằng các kỹ thuật phá có chủ đích, tách biệt rạch ròi khỏi smoke regression, và thực hiện nghiêm ngặt trên môi trường QA/Staging nội bộ.

#### 1. Ba Tầng Thực Hiện Phá:
| Tầng Kiểm Thử | Công Cụ & Kỹ Thuật | Phát Hiện Bug Gì | Chi Phí & Độ Ổn Định |
| :--- | :--- | :--- | :--- |
| **API Trực Tiếp** *(Khuyên dùng nhiều nhất)* | `page.request` / `APIRequestContext` với payload sai, thiếu token, sai role. | Server thiếu validate, vỡ logic phân quyền, crash database unhandled. | Rất rẻ, cực nhanh, 100% ổn định. |
| **UI Bypass (Client Validation Stripping)** | Dùng JS gỡ bỏ ràng buộc DOM (`strip_client_constraints`), ép giá trị qua React setter (`force_set_value`). | Backend ỷ lại validate ở client, server không chặn payload độc. | Vừa phải, độ ổn định cao. |
| **UI Hành Vi Bất Thường** | Double-click nút submit, click liên tục, rớt mạng, back/refresh giữa chừng, mở đa tab. | UI vỡ state, race condition, trùng lặp giao dịch (duplicate charge), spinner treo. | Vừa phải, cần kỹ thuật debounce. |

#### 2. Sáu Nhóm Kỹ Thuật Phá Toàn Diện (6 Adversarial Dimensions):
```text
                  6 NHÓM KỸ THUẬT PHÁ ("PHÁ CÓ KỶ LUẬT")
 ┌───────────────────────────┼───────────────────────────┐
 ▼                           ▼                           ▼
[A] DỮ LIỆU ĐẦU VÀO ĐỘC     [B] VƯỢT VALIDATE PHÍA CLIENT[C] THỜI GIAN & ĐỒNG THỜI
 - Biên: min-1, max+1        - Gỡ novalidate/required    - Double click Submit/Publish
 - Ký tự đặc biệt, Null Byte - force_set_value qua React - Network throttle/offline CDP
 - Naughty Strings / XSS / SQL- inject_select_option lạ  - Mock HTTP 500/502/Timeout
 ┌───────────────────────────┼───────────────────────────┐
 ▼                           ▼                           ▼
[D] LUỒNG & PHÂN QUYỀN      [E] GIAO DIỆN & TIẾP CẬN    [F] PHÁT HIỆN NGẦM (ORACLE)
 - IDOR qua URL / API params - Viewport hẹp, Zoom 200%   - Bắt mọi Uncaught JS Error
 - Role thấp gọi URL Admin   - Bàn phím Tab, kẹt focus   - Silent HTTP 4xx/5xx
 - Idempotency (gọi 2 lần)   - Không vỡ layout / scroll  - Không lộ Stack Trace / PII
```

- **Nhóm A: Dữ Liệu Đầu Vào (Nhập như người thật & Hostile Strings)**:
  - **Biên**: `min - 1`, `min`, `max`, `max + 1` (độ dài chuỗi, số lượng, tuổi học sinh, hạn mức số tiền).
  - **Rỗng & Khoảng trắng**: Chuỗi rỗng, chỉ gồm dấu cách (`   `), tab (`\t`), xuống dòng (`\n\r`), khoảng trắng đầu/cuối chuỗi.
  - **Ký tự đặc biệt & Unicode**: `' " < > & % \ /`, null byte (`\0`), emoji (`🚀🔥`), tiếng Việt đủ 2 chuẩn tổ hợp & dựng sẵn (NFC vs NFD), chữ Ả Rập RTL (`اللغة العربية`), chữ tượng hình CJK.
  - **Chuỗi cực dài**: Bơm chuỗi 10.000 ký tự vào các trường text/name nơi DB giới hạn VARCHAR(255).
  - **Số học**: Số âm, số 0, số mũ khoa học (`1e5`), sai số floating-point (`0.1 + 0.2`), dấu phẩy vs dấu chấm thập phân (`1.000,50`), số nguyên cực lớn vượt tràn bộ đệm.
  - **Ngày tháng biên**: 29/02 năm không nhuận, 31/04, ngày tương lai xa (`2099-12-31`), ngày quá cũ (`1800-01-01`), đổi múi giờ qua nửa đêm.
  - **Payload tấn công (Escape Check)**: XSS (`<script>alert(1)</script>`, `<img src=x onerror=alert(1)>`), SQL Injection (`' OR 1=1--`), SSTI (`{{7*7}}`), CSV Formula Injection (`=1+1`).
  - **File Upload dị dạng**: File sai định dạng MIME, file 0-byte, file vượt 10MB (`oversized_11mb.pdf`), file đuôi kép (`invoice.pdf.exe`). Dùng sẵn tại `data/fixtures/`.
- **Nhóm B: Vượt Kiểm Tra Phía Client (Client-Side Constraint Bypass)**:
  - Gọi `curricula.strip_client_constraints()` để xóa sạch `novalidate`, `required`, `maxlength`, `pattern`, `min`, `max`, `disabled`, `readonly`.
  - Dùng `curricula.force_set_value(selector, val)`: Ép giá trị thông qua property descriptor setter gốc và bắn synthetic events (`input`, `change`) tương thích hoàn hảo với React, Vue và Angular.
  - Dùng `curricula.inject_select_option(selector, val)`: Thêm một option lạ không nằm trong danh mục vào thẻ `<select>` rồi submit để ép server validate enum.
  - Dùng `curricula.enable_element(selector)` để bật các nút bị disabled/ẩn rồi click.
  - Dùng `curricula.set_hidden_field_value(selector, val)` để can thiệp các trường ẩn (giá tiền, role, CSRF token).
- **Nhóm C: Thời Gian, Đồng Thời & Hỏng Hóc Mạng (Timing & Concurrency Chaos)**:
  - **Double Click / Rapid Submit**: Dùng `locator.dblclick()` hoặc click liên tiếp. Kết hợp `curricula.track_requests(url_pattern)` để assert số lượng HTTP dispatch chính xác là 1 (chặn duplicate submission).
  - **Mô phỏng lỗi máy chủ & ngắt mạng**: Dùng `curricula.mock_http_response("**/api/**", status=500)` hoặc `curricula.simulate_network_failure("**/api/**")`. UI phải hiển thị thông báo lỗi thân thiện, không được sập trắng trang (WSoD) hay treo vô hạn.
  - **Thắt nút cổ chai mạng (CDP Throttling)**: Dùng `curricula.set_network_conditions(latency=2000, download_throughput=50_000)` để kiểm tra độ ổn định trên mạng 3G/chậm.
- **Nhóm D: Luồng Nghiệp Vụ & Phân Quyền (Flow & Authorization Tampering)**:
  - **IDOR (Insecure Direct Object Reference)**: Dùng `self.page.request.get(f"/api/students/{other_student_id}/charges")` để chứng minh phụ huynh A không thể xem hóa đơn của con phụ huynh B (phải trả HTTP 401, 403, hoặc 404).
  - **Role Escalation**: Thử dùng phiên của School Clerk để truy cập trang MOE HQ Admin `/admin/fees` (phải bị từ chối truy cập).
  - **Idempotency**: Submit một hành động tài chính (Publish Fee / Process Payment) 2 lần liên tiếp không được sinh 2 bản ghi trừ tiền trùng lặp.
- **Nhóm E: Giao Diện & Khả Năng Tiếp Cận (Viewport & A11y Boundaries)**:
  - Thử nghiệm trên Viewport hẹp (Mobile 375x667) và kiểm tra không có thanh cuộn ngang ngoài ý muốn (`assert_no_horizontal_overflow`).
  - Thao tác thuần bàn phím (Keyboard Tab Navigation): Focus phải di chuyển tuần tự qua các input mà không bị kẹt trong Focus Trap (`test_tc_brk_006`).
- **Nhóm F: Phát Hiện Ngầm Toàn Diện (Passive Technical Oracle)**:
  - Mọi kịch bản phá đều phải kích hoạt kiểm tra kỹ thuật ở bước cuối:
    `Exceptor.expect_zero_js_errors(tech_snapshot)` và `self.assert_ui_health()`.
    Tuyệt đối không để sót bất kỳ Uncaught JS Exception hay console error nào trong runtime.

#### 3. Bộ 6 Câu Hỏi Đánh Giá Kết Quả Khi Phá (The 6 Oracle Questions):
Khi một bài test phá chạy xong, nó phải trả lời và xác minh đầy đủ 6 câu hỏi chất lượng sau:
1. **Server có từ chối đúng không?** Khi bypass client, backend phải từ chối payload sai (`Exceptor.expect_bug_if_accepted(snapshot)`).
2. **Thông báo lỗi có rõ ràng, đúng spec không?** Error message phải hiển thị đúng trường vi phạm, không báo chung chung hay vỡ layout.
3. **Có lỗi 5xx, sập JS hoặc rò rỉ stack trace không?** Mọi lỗi phải được bọc an toàn, không lộ đường dẫn nội bộ máy chủ ra màn hình.
4. **Có dữ liệu rác/dữ liệu hỏng bị lưu vào cơ sở dữ liệu không?** Nếu request fail, DB không được phép tạo bản ghi mồ côi (dirty state).
5. **Người dùng có thoát lỗi và thao tác lại được không?** UI không được rơi vào trạng thái tê liệt (freeze), spinner không được treo vĩnh viễn.
6. **Có hành vi trùng lặp (Duplicate action) không?** Double click hoặc submit đồng thời tuyệt đối không sinh 2 giao dịch song song.

#### 4. Quy Tắc Để Không Thành Đống Test Nhiễu (Anti-Noise Protocols):
1. **Tách biệt bằng Marker `@pytest.mark.break_it`**: Mọi bài test phá phải được gắn decorator `@pytest.mark.break_it` (đã khai báo trong `pytest.ini`). Không đưa test phá vào bộ smoke chạy nhanh; chỉ chạy theo lịch định kỳ hoặc trước đợt release.
2. **Kỳ vọng phải dựa trên Spec (Evidence-First)**: Nếu tài liệu spec chưa quy định hành vi cho ô dữ liệu đó, bắt buộc gắn ghi chú `[SPEC GAP]` và đối soát với BA/PO, tuyệt đối không tự bịa expected outcome.
3. **Mỗi lần chạy là một dữ liệu độc lập (UUID Isolated)**: Sinh UUID/Timestamp động cho mỗi bản ghi test và luôn có teardown dọn sạch để không làm ô nhiễm môi trường QA.
4. **Phạm vi an toàn**: Tuyệt đối KHÔNG chạy payload tấn công, fuzzing, hay script phá lên các dịch vụ bên ngoài của bên thứ ba (Bing, Google, YouTube). Chỉ thực thi trên trang app nội bộ được phân quyền (`curricula`, `portal`, `admin`).
5. **Tránh False Positives**:
   - Nếu test bypass bằng JS thành công và server chặn đứng trả về lỗi hợp lệ: **ĐÂY LÀ TEST PASS** (hệ thống an toàn), không được báo fail.
   - Nếu test fail do selector bị vỡ hoặc script test viết sai: Đây là **Automation Defect**, không phải bug của sản phẩm.

#### 5. Bảng Phương Thức & Helpers Chuẩn Có Sẵn Để AI Coding Sử Dụng:
| Helper Method | Vị Trí Cung Cấp | Mục Đích Sử Dụng |
| :--- | :--- | :--- |
| `curricula.force_set_value(selector, value)` | `BasePage` | Gán giá trị input trực tiếp qua React/Vue prototype setter và bắn event. |
| `curricula.strip_client_constraints(container)` | `BasePage` | Xóa bỏ `novalidate`, `required`, `pattern`, `disabled` trên toàn form. |
| `curricula.inject_select_option(selector, val, label)`| `BasePage` | Bơm option lạ vào dropdown để test schema validation của server. |
| `curricula.enable_element(selector)` | `BasePage` | Bật các nút/input đang bị `disabled`, xóa bỏ `pointer-events: none`. |
| `curricula.set_hidden_field_value(selector, val)` | `BasePage` | Can thiệp trực tiếp giá trị của trường ẩn (`input[type="hidden"]`). |
| `curricula.set_network_conditions(offline, latency)` | `BasePage` | Mô phỏng mạng chậm, rớt mạng qua giao thức CDP Chromium. |
| `curricula.track_requests(url_pattern, method)` | `BasePage` | Giám sát số lượt request HTTP để verify idempotency / double-click. |
| `self.naughty_strings` | `BaseTest` | Truy cập nhanh kho payload độc hại `data/naughty_strings.json`. |
| `Exceptor.expect_bug_if_accepted(snapshot)` | `core.Exceptor` | Bắt lỗi nếu hệ thống chấp nhận dữ liệu sai (Validation Bypass Bug). |
| `Exceptor.expect_zero_js_errors(tech_snapshot)` | `core.Exceptor` | Verify 100% không có Uncaught Exception hay console.error ngầm. |
| `self.assert_ui_health()` | `BaseTest` | Kiểm tra toàn diện Tier 1 (Runtime) và Tier 2 (Silent HTTP failures). |
| `self.assert_no_horizontal_overflow()` | `BaseTest` | Kiểm tra trang không bị vỡ layout tràn ngang màn hình (Tier 3). |

---

---

