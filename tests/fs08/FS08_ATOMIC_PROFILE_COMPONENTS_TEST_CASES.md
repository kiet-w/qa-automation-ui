# BỘ ĐẶC TẢ TEST CASE ĐƠN COMPONENT (UI ATOMIC TESTS) PHÂN HỆ FS08 / R8
## MÀN HÌNH HỒ SƠ PHỤ HUYNH (PARENT PROFILE & MY DETAILS - HTTP://LOCALHOST:5174/PROFILE)

> **Mã Chức Năng**: FR-08.3 (Cập nhật thông tin cá nhân cơ bản) | **Epic**: EP-08  
> **Hệ Thống**: MOE Singapore EduSave E-Service Portal (`http://localhost:5174/profile`)  
> **Tài Liệu Tham Chiếu Gốc**:
> - `specs/md/FS document/FS-08_Parent_Portal_SingPass_Profile.md` (FR-08.3, Bảng trường Mục 6, Phụ lục A & B)
> - `specs/md/Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md` (Test Suite `TS-010: My Details`, `TC-R8-094` đến `TC-R8-111`)
> - Quyết định nghiệp vụ đã phê duyệt: `D-20` (Residential Address chỉ đọc từ Singpass), `D-28` (Không gửi email thông báo khi sửa thông tin)
> - Tiêu chí nghiệm thu FSD: `AC #14` (Sửa hợp lệ), `AC #15` (Bắt lỗi định dạng SĐT/Email), `AC #16` (Trường bắt buộc), `AC #18` (Residential address chỉ đọc)
> - Danh mục thông báo lỗi: `MSG-0805` (SĐT sai định dạng), `MSG-0806` (Email sai định dạng), `MSG-0807` (Lưu thành công), `MSG-0001` (Bỏ trống trường bắt buộc)
>
> **Quy Chuẩn Kiểm Thử Áp Dụng**:
> - **Triết lý Đơn Component (UI Atomic Testing)**: Kiểm thử độc lập từng component UI riêng biệt (1 ô input, 1 button, 1 dropdown, validate rỗng/biên/regex, dirty state) trước khi tích hợp vào luồng UAT.
> - **Reconnaissance First**: 100% selector được trinh sát từ DOM thật qua công cụ `tools/recon_bsk.py`, nghiêm cấm đọc code source hoặc đoán mò selector.
> - **Invariant 7**: Đánh giá kiểm thử 9 tầng (Technical Health, Console Errors, Visual Overflow, Actionability).

---

## 🔍 BẢNG TRA CỨU LOCATOR XÁC MINH QUA BSK (BROWSER-SKILL RECONNAISSANCE)

| Tên Phần Tử Component | Nhãn Hiển Thị Trên UI | Selector / ID Kỹ Thuật BSK | Loại Phần Tử HTML | Thuộc Tính Ràng Buộc |
| :--- | :--- | :--- | :--- | :--- |
| **Full Name** | Full Name | `[data-testid="full-name"], dt:has-text("Full Name") + dd` | `<dd> / <span>` | Read-only (SingPass) |
| **Residential Address** | Residential address | `[data-testid="residential-address"], dt:has-text("Residential") + dd` | `<dd> / <span>` | Read-only (D-20) |
| **NRIC Display** | NRIC / FIN | `[data-testid="nric"], dt:has-text("NRIC") + dd` | `<dd> / <span>` | Masked `*****123F` |
| **Show NRIC Button** | Show NRIC | `button:has-text("Show NRIC")` | `<button type="button">` | Toggle reveal NRIC |
| **Hide NRIC Button** | Hide NRIC | `button:has-text("Hide NRIC")` | `<button type="button">` | Toggle mask NRIC |
| **Update Details Button** | Update details | `button:has-text("Update details")` | `<button type="button">` | Chuyển View ➔ Edit Mode |
| **Mobile Number Input** | Mobile Number * | `input[name="phoneNumber"]` | `<input type="tel">` | Bắt buộc, 8 số (6/8/9) |
| **Email Address Input** | Email Address * | `input[name="email"]` | `<input type="email">` | Bắt buộc, RFC 5322, $\le 150$ ký tự |
| **Mailing Block Input** | Block | `input[name="mailingBlock"]` | `<input type="text">` | Tùy chọn, $\le 20$ ký tự |
| **Mailing Street Input** | Street | `input[name="mailingStreet"]` | `<input type="text">` | Bắt buộc, $\le 100$ ký tự |
| **Mailing Unit Input** | Unit | `input[name="mailingUnit"]` | `<input type="text">` | Tùy chọn, $\le 20$ ký tự |
| **Mailing Postal Code** | Postal code | `input[name="mailingPostalCode"]` | `<input type="text">` | Bắt buộc, đúng 6 chữ số |
| **Mailing Country Input**| Country | `input[name="mailingCountry"]` | `<input type="text">` | Bắt buộc, $\le 100$ ký tự |
| **Save Changes Button** | Save changes | `button:has-text("Save changes")` | `<button type="submit">` | Bị khóa khi chưa có thay đổi |
| **Cancel Button** | Cancel | `button:has-text("Cancel")` | `<button type="button">` | Hủy thay đổi, về View Mode |
| **Dirty State Hint** | Make a change to enable saving. | `p:has-text("Make a change to enable saving.")` | `<p>` | Hướng dẫn trạng thái dirty |
| **Inline Validation Alert** | Thông báo lỗi xác thực | `div[role="alert"], p[role="alert"], p[class*="error"]` | `<p> / <div>` | Hiển thị mã lỗi MSG |

---

## 📋 MA TRẬN KỊCH BẢN KIỂM THỬ ĐƠN COMPONENT (ATOMIC TEST MATRIX)

| Mã Kịch Bản | Phân Loại Component | Mục Tiêu & Kỹ Thuật Kiểm Thử | Traceability Gốc | Mức Ưu Tiên |
| :--- | :--- | :--- | :--- | :---: |
| **`TC-ATM-01`** | SingPass Identity Component | Xác minh tính bất biến (Read-only) của Full Name & Residential Address | `TC-R8-094`, `TC-R8-095`, `D-20` | **P0 / Smoke** |
| **`TC-ATM-02`** | NRIC Mask Toggle Component | Kiểm tra nút toggle ẩn/hiện NRIC (`Show NRIC` $\leftrightarrow$ `Hide NRIC`) | `TC-R8-094`, `BR-08-09.1` | **P0 / Smoke** |
| **`TC-ATM-03`** | Transition Buttons Component| Chuyển đổi trạng thái View Mode $\leftrightarrow$ Edit Mode qua nút Update & Cancel | `TC-R8-096`, `AC #14` | **P0** |
| **`TC-ATM-04`** | Save Button Component State | Cơ chế khóa Dirty State: Nút Save bị vô hiệu hóa khi form chưa thay đổi | `TC-R8-096`, `AC #14` | **P1** |
| **`TC-ATM-05`** | Mobile Number Input Component | Phân vùng tương đương (EP): Chấp nhận SĐT Singapore hợp lệ (đầu 6, 8, 9) | `TC-R8-098`, `BR-08-09.1` | **P0 / Smoke** |
| **`TC-ATM-06`** | Mobile Number Input Component | Phân tích giá trị biên (BVA): Bắt lỗi SĐT sai định dạng / chứa ký tự lạ (`MSG-0805`) | `TC-R8-099`, `MSG-0805` | **P0** |
| **`TC-ATM-07`** | Email Address Input Component | Kiểm tra xác thực cú pháp RFC 5322 (thiếu `@`, thiếu domain) (`MSG-0806`) | `TC-R8-101`, `MSG-0806` | **P0** |
| **`TC-ATM-08`** | Required Fields Component | Ngăn chặn lưu trường bắt buộc ở trạng thái rỗng (`MSG-0001` Architecture) | `TC-R8-103`, `AC #16` | **P1** |
| **`TC-ATM-09`** | Mailing Address Sub-Components| Ràng buộc trường tùy chọn (Block, Unit) và trường bắt buộc (Street, Postal) | `TC-R8-105`, `TC-R8-108` | **P1** |
| **`TC-ATM-10`** | Non-Functional Layout & Health| Tiêu chuẩn Invariant 7: 0 lỗi Console Uncaught JS và không vỡ Layout cuộn ngang | `Invariant 7`, `WCAG 2.1` | **P0** |

---

## 📝 CHI TIẾT KỊCH BẢN KIỂM THỬ ĐƠN COMPONENT

### `TC-ATM-01`: SingPass Identity Component Strictly Read-Only
- **Mục tiêu**: Đảm bảo họ tên và địa chỉ cư trú lấy từ SingPass là bất biến, không thể sửa đổi trên giao diện người dùng theo Quyết định `D-20`.
- **Tiền điều kiện**: Phụ huynh đã đăng nhập, đang ở trang `/profile` (View Mode).
- **Các bước thực hiện**:
  1. Kiểm tra sự xuất hiện của tiêu đề thẻ *"SINGPASS VERIFIED IDENTITY (READ-ONLY)"*.
  2. Kiểm tra dòng hướng dẫn pháp lý: *"Residential address is maintained via Government Digital Services and cannot be edited in this portal."*.
  3. Kiểm tra DOM không tồn tại bất kỳ thẻ `<input>` nào có tên `fullName` hoặc `residentialAddress`.
- **Kết quả kỳ vọng**:
  - Không có trường nhập liệu nào cho họ tên và địa chỉ cư trú.
  - Thông tin hiển thị rõ ràng dưới dạng văn bản tĩnh (read-only text).

### `TC-ATM-02`: NRIC Masking & Reveal Toggle Button Component
- **Mục tiêu**: Kiểm tra component nút bấm ẩn/hiện số NRIC.
- **Tiền điều kiện**: Đang ở màn hình Hồ sơ Phụ huynh.
- **Các bước thực hiện**:
  1. Kiểm tra trạng thái ban đầu: NRIC được che mặt nạ dạng `*****123F`, nút bấm hiển thị nhãn *"Show NRIC"*.
  2. Click vào nút *"Show NRIC"*.
  3. Kiểm tra nhãn nút bấm chuyển thành *"Hide NRIC"*.
  4. Click vào nút *"Hide NRIC"*.
  5. Kiểm tra nhãn nút bấm quay trở lại *"Show NRIC"*.
- **Kết quả kỳ vọng**: Nút chuyển đổi trạng thái mượt mà, bảo vệ dữ liệu PII người dùng.

### `TC-ATM-03`: Mode Transition Buttons (Update details & Cancel)
- **Mục tiêu**: Kiểm tra component chuyển đổi giao diện giữa chế độ Xem và chế độ Chỉnh sửa.
- **Tiền điều kiện**: Trang `/profile` đang ở View Mode.
- **Các bước thực hiện**:
  1. Bấm nút *"Update details"*.
  2. Kiểm tra xuất hiện form chỉnh sửa với các ô input `phoneNumber`, `email`.
  3. Bấm nút *"Cancel"*.
  4. Kiểm tra thoát khỏi form chỉnh sửa, quay trở lại View Mode ban đầu.
- **Kết quả kỳ vọng**: Trạng thái giao diện thay đổi chính xác, không lưu dữ liệu rác khi bấm Cancel.

### `TC-ATM-04`: Save Changes Button Pristine & Dirty State Gatekeeper
- **Mục tiêu**: Đảm bảo nút "Save changes" luôn bị vô hiệu hóa khi người dùng chưa thực hiện bất kỳ thay đổi nào trên form.
- **Tiền điều kiện**: Vừa mở Edit Mode qua nút Update details.
- **Các bước thực hiện**:
  1. Kiểm tra trạng thái của nút *"Save changes"*.
  2. Kiểm tra sự xuất hiện của dòng hướng dẫn: *"Make a change to enable saving."*.
- **Kết quả kỳ vọng**: Nút *"Save changes"* có thuộc tính `disabled = true`, ngăn chặn gửi request vô nghĩa lên server.

### `TC-ATM-05`: Mobile Number Input - Valid Singapore Format Acceptance
- **Mục tiêu**: Kiểm tra ô nhập Mobile Number chấp nhận các số điện thoại 8 chữ số bắt đầu bằng 6, 8, hoặc 9 per FS-08.
- **Tiền điều kiện**: Form đang ở Edit Mode.
- **Các bước thực hiện**:
  1. Nhập số điện thoại hợp lệ: `98765432`.
  2. Kiểm tra trạng thái nút *"Save changes"*.
- **Kết quả kỳ vọng**: Nút *"Save changes"* tự động kích hoạt `disabled = false`, form sẵn sàng để lưu.

### `TC-ATM-06`: Mobile Number Input - Invalid Formats Rejection (MSG-0805)
- **Mục tiêu**: Kiểm tra ô nhập Mobile Number từ chối số điện thoại không hợp lệ (< 8 chữ số hoặc chứa chữ cái).
- **Tiền điều kiện**: Form đang ở Edit Mode.
- **Các bước thực hiện**:
  1. Nhập số không hợp lệ: `9123abcd` hoặc `12345`.
  2. Bấm Lưu hoặc kiểm tra validate.
- **Kết quả kỳ vọng**: Hệ thống từ chối lưu, giữ nút Save ở trạng thái vô hiệu hoặc hiển thị thông báo lỗi `MSG-0805`: *"Enter a mobile number in the correct format, like 9123 4567"*.

### `TC-ATM-07`: Email Address Input - RFC 5322 Syntax Error (MSG-0806)
- **Mục tiêu**: Kiểm tra ô nhập Email từ chối các chuỗi không tuân thủ chuẩn RFC 5322.
- **Tiền điều kiện**: Form đang ở Edit Mode.
- **Các bước thực hiện**:
  1. Nhập email sai: `invalid-email-address` (thiếu `@`, thiếu tên miền).
  2. Bấm nút *"Save changes"*.
- **Kết quả kỳ vọng**:
  - Xuất hiện thông báo lỗi `MSG-0806` / inline alert: *"Enter a valid email address."* (hoặc *"Enter an email address in the correct format, like name@example.com"*).
  - Hộp thoại lưu xác nhận bị chặn lại, không gửi request lên server.

### `TC-ATM-08`: Required Fields Empty Prevention (MSG-0001 Architecture)
- **Mục tiêu**: Kiểm tra việc xóa trắng trường bắt buộc (SĐT, Email) bị hệ thống ngăn chặn.
- **Tiền điều kiện**: Form đang ở Edit Mode.
- **Các bước thực hiện**:
  1. Xóa sạch ô nhập số điện thoại (`fill("")`).
  2. Kiểm tra trạng thái nút Lưu.
- **Kết quả kỳ vọng**: Nút *"Save changes"* lập tức bị vô hiệu hóa (`disabled = true`), ngăn người dùng submit payload rỗng.

### `TC-ATM-09`: Mailing Address Sub-Components Visibility & Limits
- **Mục tiêu**: Kiểm tra sự hiện diện đầy đủ và thuộc tính của các trường địa chỉ nhận thư.
- **Tiền điều kiện**: Form đang ở Edit Mode.
- **Các bước thực hiện**:
  1. Kiểm tra sự hiện diện của trường Block (`input[name="mailingBlock"]`).
  2. Kiểm tra sự hiện diện của trường Street (`input[name="mailingStreet"]`).
  3. Kiểm tra sự hiện diện của trường Unit (`input[name="mailingUnit"]`).
  4. Kiểm tra sự hiện diện của trường Postal code (`input[name="mailingPostalCode"]`).
  5. Kiểm tra sự hiện diện của trường Country (`input[name="mailingCountry"]`).
- **Kết quả kỳ vọng**: Toàn bộ 5 trường địa chỉ hiển thị chính xác, sẵn sàng tiếp nhận tương tác.

### `TC-ATM-10`: UI Technical Health & Layout Integrity (Invariant 7)
- **Mục tiêu**: Kiểm tra sức khỏe kỹ thuật của giao diện người dùng theo Invariant 7.
- **Tiền điều kiện**: Mở trang `/profile`.
- **Kết quả kỳ vọng**:
  - Tiêu đề trang chứa `"EduFAMS"`.
  - Tiêu đề chính `"My Profile"` hiển thị rõ ràng.
  - Số lượng lỗi Uncaught JS Exception trong Console bằng 0.
  - Không xuất hiện thanh cuộn ngang ngoài ý muốn (`document.documentElement.scrollWidth <= document.documentElement.clientWidth`).
