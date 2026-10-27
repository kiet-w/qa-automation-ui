# FS08: Parent Portal — SingPass, Education Account, Profile

## 1. Phân Hệ Tổng Quan
- **Mã phân hệ**: `FS08` (Requirement R8)
- **Tên nghiệp vụ**: Parent Portal – SingPass, Education Account, Profile
- **Đường dẫn ứng dụng**: `http://localhost:5174/profile`
- **Đối tượng sử dụng**: Phụ huynh / Người giám hộ học sinh (xác thực qua Singpass)
- **Mục tiêu**: Quản lý thông tin định danh bất biến từ Singpass (Full Name, NRIC/FIN, Residential Address) và cho phép phụ huynh tự cập nhật thông tin liên hệ (Mobile, Email) cùng Địa chỉ gửi thư thay thế (Mailing Address) một cách an toàn, độc lập.

---

## 2. Mục Lục Đặc Tả Thành Phần Đơn Lẻ (Atomic Component Specs)

Tất cả các tài liệu thành phần đơn lẻ tuân thủ cấu trúc 5 phần chuẩn hóa (Metadata & Selector, BR/AC Traceability, Ma trận 12 lớp validation, Error Handling & Visual Feedback, JSON Fixtures Data Payload):

| Component File | Tên Thành Phần & Chức Năng | Route & Selector Chính | BR / AC Traceability |
| :--- | :--- | :--- | :--- |
| [`singpass_identity_component.md`](./atomic/singpass_identity_component.md) | **Singpass Identity & NRIC Masking**: Hiển thị họ tên, địa chỉ thường trú và NRIC có che mặc định (`*****123F`) kèm nút toggle Show/Hide NRIC (CLS = 0). | `/profile`<br>`dt:has-text('NRIC') + dd`<br>`button:has-text('Show NRIC')` | `BR-08-03`<br>`D-20`<br>`R8-AC01`, `AC05`, `AC06`, `AC14` |
| [`mobile_input_component.md`](./atomic/mobile_input_component.md) | **Mobile Number Input**: Ô nhập số điện thoại Singapore 8 chữ số, bắt đầu bằng 6, 8, hoặc 9. Tự động trim khoảng trắng (ASM-15). | `/profile` (Edit Mode)<br>`input[name='phoneNumber']` | `BR-08-02`<br>`R8-AC11`, `AC12`<br>`MSG-0001`, `MSG-0805` |
| [`email_input_component.md`](./atomic/email_input_component.md) | **Email Input**: Ô nhập địa chỉ email theo chuẩn RFC 5322, tối đa 150 ký tự, kiểm tra BVA 149/150/151. | `/profile` (Edit Mode)<br>`input[name='email']` | `BR-08-02`, `BR-08-04`<br>`D-28`<br>`R8-AC11`, `AC13`<br>`MSG-0001`, `MSG-0806` |
| [`mailing_address_component.md`](./atomic/mailing_address_component.md) | **Mailing Address Fields**: Cụm trường địa chỉ gửi thư gồm Block (tùy chọn, max 20), Street (bắt buộc, max 100), Unit (tùy chọn, max 20), Postal Code (bắt buộc, 6 số), Country (bắt buộc, max 100). | `/profile` (Edit Mode)<br>`input[name='mailingStreet']`<br>`input[name='mailingPostalCode']` | `BR-08-02`<br>`D-20`<br>`R8-AC11`, `AC15`<br>`MSG-0001` |

---

## 3. Mục Lục Đặc Tả Luồng Tích Hợp (Integration Flow Specs)

Các tài liệu luồng tích hợp tuân thủ cấu trúc 5 phần chuẩn hóa (Flow Metadata, Inter-Component Dependencies, Step-by-Step Function Flow, State Machine & Transitions, Exception & Error Handling):

| Integration Flow File | Tên Luồng Nghiệp Vụ & Quy Trình | Vai Trò & Điều Kiện Tiên Quyết | Trạng Thái Chuyển Đổi Chính |
| :--- | :--- | :--- | :--- |
| [`parent_profile_update_flow.md`](./integration/parent_profile_update_flow.md) | **Parent Profile Update & Confirm Dialog**: Chuyển đổi View $\leftrightarrow$ Edit mode, quản lý trạng thái Pristine $\leftrightarrow$ Dirty, kích hoạt hộp thoại xác nhận modal `alertdialog`, xử lý mutation lưu và thông báo toast `MSG-0807`. | Phụ huynh có con $< 16$ tuổi đăng nhập qua Singpass | `VIEW_MODE`<br>➔ `EDIT_MODE_DIRTY`<br>➔ `CONFIRM_DIALOG_OPEN`<br>➔ `SUBMITTING`<br>➔ `TOAST_SUCCESS` |
| [`child_age_access_control_flow.md`](./integration/child_age_access_control_flow.md) | **Child Age Access Control & Independence**: Khóa chế độ chỉ xem (Read-Only Lockout) khi tất cả các con $\ge 16$ tuổi (`BR-08-01`), cho phép sửa khi có ít nhất 1 con $< 16$ tuổi, đảm bảo tính độc lập giữa hồ sơ Cha và Mẹ (`BR-08-02`), ngăn chặn tấn công BOLA/IDOR (`MSG-0003`). | Phụ huynh với các nhóm tuổi con cái khác nhau | `PARENT_ALL_GE_16`<br>➔ `VIEW_MODE_LOCKED`<br>`PARENT_ACTIVE_UNDER_16`<br>➔ `VIEW_MODE_EDITABLE` |
| [`singpass_child_authorization_flow.md`](./integration/singpass_child_authorization_flow.md) | **SingPass Auth & Child Guardianship Authorization (UAT-005)**: Xác thực SingPass, liệt kê chính xác các con hợp pháp, kiểm soát chống truy cập chéo IDOR qua URL/API và cô lập phiên làm việc hoàn toàn giữa 2 phụ huynh. | Phụ huynh A và Phụ huynh B đăng nhập MockPass | `ANONYMOUS`<br>➔ `PARENT_A_AUTH`<br>➔ `IDOR_BLOCKED`<br>➔ `SESSION_FLUSHED`<br>➔ `PARENT_B_AUTH` |

---

## 4. Bảng Tra Cứu Mã Thông Báo Hệ Thống (Error Catalog)

| Mã Lỗi | Nội Dung Thông Báo Chuẩn | Ngữ Cảnh Kích Hoạt | Quy Định UI Feedback |
| :--- | :--- | :--- | :--- |
| `MSG-0001` | *"Enter your <field>"* (vd: *"Enter your mobile number"*, *"Enter your email"*) | Để trống hoặc nhập toàn khoảng trắng vào ô bắt buộc | `aria-invalid="true"`, viền đỏ, auto-dismiss khi nhập đúng |
| `MSG-0801` | *"No Edu Account linked with for this parent"* | Phụ huynh hợp lệ nhưng không có con nào liên kết trong DB | Banner cảnh báo tại trang chủ / trang hồ sơ |
| `MSG-0805` | *"Enter a mobile number in the correct format, like 9123 4567"* | Sai cú pháp số ĐT: khác 8 số, ký tự lạ, đầu số khác 6, 8, 9 | `aria-invalid="true"`, viền đỏ |
| `MSG-0806` | *"Enter an email address in the correct format, like name@example.com"* | Sai định dạng RFC 5322 hoặc vượt quá 150 ký tự | `aria-invalid="true"`, viền đỏ |
| `MSG-0807` | *"Your details have been updated."* | Cập nhật hồ sơ thành công | Toast thông báo xanh lá góc trên màn hình |
| `MSG-0808` | *"We could not update your details. Please try again."* | Lỗi API 500 hoặc mất kết nối khi lưu | Alert bên trong hộp thoại xác nhận, không đóng modal |
