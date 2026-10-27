# BỘ ĐẶC TẢ TEST CASE ĐẦY ĐỦ VÀ CHI TIẾT - PHÂN HỆ FS08: MY DETAILS / PARENT PROFILE
## MOE SINGAPORE EDUSAVE E-SERVICE PORTAL (`http://localhost:5174/profile`)

> **Quy chuẩn ban hành**: Tuân thủ chuẩn `/combo-qa` (ISTQB / ISO/IEC/IEEE 29119-3 & Standard 10-Column Test Matrix).  
> **Nguyên tắc Invariant 6**: ZERO ASSUMPTIONS — 100% kịch bản, quy tắc biên, mã lỗi và dữ liệu đối soát trực tiếp từ FSD, Biên bản Quyết định nghiệp vụ và BSK Reconnaissance DOM thực tế.  
> **Nguyên tắc Invariant 7**: 9-Tier Failure Evaluation Framework (Client Health, Network/API, Visual, Actionability, Performance, A11y, Data Integrity, Security, Isolation).

---

## 1. THÔNG TIN NGHIỆP VỤ & TRUY VẾT HỆ THỐNG (TRACEABILITY MATRIX)

| Tiêu Chí | Nội Dung Đặc Tả |
| :--- | :--- |
| **Mã Chức Năng** | `FR-08.3` Cập nhật thông tin cá nhân cơ bản (My Details) |
| **Epic / Feature** | `EP-08` Parent Portal SingPass & Profile Management |
| **URL Kiểm Thử** | `http://localhost:5174/profile` (Port: 5174) |
| **Tài Liệu Căn Cứ** | • `specs/md/FS document/FS-08_Parent_Portal_SingPass_Profile.md` (FR-08.3, Mục 6, Phụ lục A & B)<br>• `specs/md/Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md` (Test Suite `TS-010: My Details`, `TC-R8-094` $\rightarrow$ `TC-R8-114`)<br>• `specs/md/MEETINGS_AND_DECISIONS_SUMMARY.md` (`D-20`, `D-28`) |
| **Tiêu Chí Nghiệm Thu (AC)** | `AC #10` (Read-only SingPass Identity & NRIC Masking)<br>`AC #14` (Lưu thông tin hợp lệ hiển thị Confirm Dialog & MSG-0807)<br>`AC #15` (Bắt lỗi định dạng SĐT MSG-0805 & Email MSG-0806)<br>`AC #16` (Trường bắt buộc không được bỏ trống MSG-0001)<br>`AC #17` (Lỗi hệ thống lưu DB trả về MSG-0808 giữ nguyên dữ liệu cũ)<br>`AC #18` (Residential Address chỉ đọc, không chỉnh sửa)<br>`AC #09` (Tất cả con $\ge 16$ tuổi khóa chế độ Edit, chỉ cho phép View) |
| **Quyết Định Đã Chốt** | • `D-20`: Residential Address lấy từ SingPass MyInfo, portal tuyệt đối không cung cấp input chỉnh sửa.<br>• `D-28`: Không gửi email thông báo cho phụ huynh khi cập nhật thông tin cá nhân. |
| **Bảng Mã Lỗi FSD** | • `MSG-0805`: *"Enter a mobile number in the correct format, like 9123 4567"*<br>• `MSG-0806`: *"Enter an email address in the correct format, like name@example.com"*<br>• `MSG-0807`: *"Your details have been updated."* (Success)<br>• `MSG-0808`: *"We could not update your details. Please try again."* (System Error 500)<br>• `MSG-0001`: *"Enter your <field>"* (Required field missing)<br>• `MSG-0003`: *"You do not have permission to view or edit this record."* (HTTP 403 Forbidden) |

---

## 2. BẢNG TRA CỨU LOCATOR XÁC MINH QUA BSK (BROWSER-SKILL RECONNAISSANCE)

| STT | Tên Thành Phần UI | Nhãn Hiển Thị | Selector / Locator BSK | Loại HTML | Trạng Thái / Ràng Buộc |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | **Full Name** | Full Name | `[data-testid="full-name"], dt:has-text("Full Name") + dd` | `<dd>/<span>` | Read-only tĩnh (SingPass MyInfo) |
| 2 | **Residential Address**| Residential address | `[data-testid="residential-address"], dt:has-text("Residential") + dd` | `<dd>/<span>` | Read-only tĩnh (`D-20`), không có input |
| 3 | **NRIC Masked** | NRIC / FIN | `[data-testid="nric"], dt:has-text("NRIC") + dd` | `<dd>/<span>` | Che mặt nạ định dạng `*****123F` |
| 4 | **Show NRIC Button** | Show NRIC | `button:has-text("Show NRIC")` | `<button>` | Bấm để hiện đầy đủ số NRIC |
| 5 | **Hide NRIC Button** | Hide NRIC | `button:has-text("Hide NRIC")` | `<button>` | Bấm để che lại số NRIC |
| 6 | **Update Details** | Update details | `button:has-text("Update details")` | `<button>` | Chuyển View Mode $\rightarrow$ Edit Mode |
| 7 | **Mobile Number** | Mobile Number * | `input[name="phoneNumber"]` | `<input type="tel">` | Bắt buộc, 8 số bắt đầu bằng 6, 8, 9 |
| 8 | **Email Address** | Email Address * | `input[name="email"]` | `<input type="email">`| Bắt buộc, chuẩn RFC 5322, $\le 150$ ký tự |
| 9 | **Mailing Block** | Block | `input[name="mailingBlock"]` | `<input type="text">` | Tùy chọn, tối đa 20 ký tự |
| 10 | **Mailing Street** | Street * | `input[name="mailingStreet"]` | `<input type="text">` | Bắt buộc, tối đa 100 ký tự |
| 11 | **Mailing Unit** | Unit | `input[name="mailingUnit"]` | `<input type="text">` | Tùy chọn, tối đa 20 ký tự |
| 12 | **Mailing Postal Code**| Postal code * | `input[name="mailingPostalCode"]` | `<input type="text">` | Bắt buộc, đúng 6 chữ số |
| 13 | **Mailing Country** | Country * | `input[name="mailingCountry"]` | `<input type="text">` | Bắt buộc, tối đa 100 ký tự |
| 14 | **Save Changes** | Save changes | `button[type="submit"]:has-text("Save changes")` | `<button>` | Disabled khi form chưa sửa (Pristine) |
| 15 | **Cancel Button** | Cancel | `button:has-text("Cancel")` | `<button>` | Hủy chỉnh sửa, khôi phục View Mode |
| 16 | **Pristine Hint** | Make a change... | `p:has-text("Make a change to enable saving.")` | `<p>` | Hiển thị khi chưa có thay đổi |
| 17 | **Confirm Dialog** | Confirm details | `div[role="alertdialog"]` | `<div>` | Modal xác nhận trước khi lưu DB |
| 18 | **Keep Editing Btn** | Keep editing | `div[role="alertdialog"] button:has-text("Keep editing")` | `<button>` | Đóng dialog, giữ nguyên dữ liệu đang sửa |
| 19 | **Confirm Save Btn** | Save changes | `div[role="alertdialog"] button:has-text("Save changes")` | `<button>` | Gửi mutation lưu vào Database |
| 20 | **Success Toast** | Details updated | `div[role="status"], div[role="alert"], div.toast` | `<div>` | Hiển thị `MSG-0807` màu xanh |

---

## 3. MA TRẬN TEST CASE TIÊU CHUẨN 10 CỘT (`COMBO-QA` DEFAULT SCHEMA)

| TC_ID | Module / Feature | Test Title / Objective | Preconditions | Test Data | Steps to Execute | Expected Observable Result | Technique | Suite | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :-: |
| `TC-R8-094` | My Details | Verify SingPass verified identity fields are strictly read-only and NRIC is masked | Phụ huynh FA đã đăng nhập Singpass, mở trang `/profile` | NRIC: `S****123F`, Name: `TAN WEI MING` | 1. Mở trang `/profile`<br>2. Kiểm tra các trường Họ tên, NRIC, Địa chỉ cư trú | Họ tên, NRIC, Residential Address không có thẻ `<input>` nào; NRIC hiển thị dạng che `*****123F`; xuất hiện nút "Show NRIC" | UI / Security | Smoke | **P1** |
| `TC-R8-095` | My Details | Verify residential address cannot be edited per Decision D-20 | Phụ huynh FA đăng nhập; trang ở View/Edit Mode | Residential: `Blk 123 Ang Mo Kio Ave 3...` | 1. Mở trang `/profile`<br>2. Bấm "Update details"<br>3. Tìm trường Residential Address | Không có ô input cho địa chỉ cư trú; dòng thông báo D-20 hiển thị rõ ràng: *"Residential address is maintained via Government Digital Services and cannot be edited in this portal."* | UI / Spec | Smoke | **P1** |
| `TC-R8-096` | My Details | Verify the API ignores or rejects changes to read-only fields (Tampering Prevention) | Token phiên của FA; giả lập request PUT `/api/parent/profile` | Payload chứa `fullName: "HACKED"`, `nric: "S9999999Z"` | 1. Bắt request update profile<br>2. Bơm thêm trường `fullName` và `nric`<br>3. Gửi payload lên server | Backend từ chối hoặc bỏ qua hoàn toàn các trường read-only; DB giữ nguyên họ tên và NRIC ban đầu | Security / API | Sprint | **P1** |
| `TC-R8-097` | My Details | Verify saving valid phone, email and mailing address with Confirm Dialog (MSG-0807) | Phụ huynh FA đăng nhập, đang ở Edit Mode | `phone="98887777"`, `email="fa.new@example.sg"`, `street="Verde Walk"`, `postal="650009"` | 1. Nhập các giá trị hợp lệ<br>2. Bấm "Save changes"<br>3. Trên dialog bấm "Save changes"<br>4. Reload trang | Hiển thị Toast thành công `MSG-0807`: *"Your details have been updated."*; Dữ liệu mới tồn tại sau reload; Không gửi email thông báo (D-28) | Functional / E2E | Sprint | **P1** |
| `TC-R8-098` | My Details | Verify mobile numbers starting with 6, 8, and 9 are accepted (Singapore EP Valid) | Edit Mode đang mở | EP1: `61234567`<br>EP2: `81234567`<br>EP3: `91234567` | 1. Lần lượt nhập từng số điện thoại hợp lệ<br>2. Bấm "Save changes"<br>3. Xác nhận trên dialog | Nút Save kích hoạt (`disabled=false`); cả 3 đầu số đều lưu thành công với `MSG-0807` | EP (Valid) | Smoke | **P1** |
| `TC-R8-099` | My Details | Verify invalid mobile numbers are rejected with MSG-0805 | Edit Mode đang mở | `71234567`, `51234567`, `9123456` (7 số), `912345678` (9 số), `9123abcd`, `+6591234567` | 1. Lần lượt nhập các số không hợp lệ<br>2. Blur ô input hoặc bấm Lưu | Hiển thị lỗi xác thực `MSG-0805`: *"Enter a mobile number in the correct format, like 9123 4567"*; Nút Save bị vô hiệu hóa hoặc dialog bị chặn | BVA / Regex | Regression | **P1** |
| `TC-R8-100` | My Details | Verify a mobile number entered with space is sanitized and accepted | Edit Mode đang mở | `phoneNumber = "9123 4567"` | 1. Nhập `9123 4567`<br>2. Bấm "Save changes" và xác nhận lưu | Hệ thống chấp nhận lưu với `MSG-0807`; dữ liệu lưu trong DB và hiển thị View Mode được chuẩn hóa thành `91234567` (hoặc định dạng hiển thị chuẩn) | Boundary / Robustness | Sprint | **P2** |
| `TC-R8-101` | My Details | Verify invalid email formats are rejected with MSG-0806 | Edit Mode đang mở | `nameexample.com`, `name@`, `@example.com`, `name@example`, `name @example.com` | 1. Lần lượt nhập từng chuỗi email sai RFC 5322<br>2. Kiểm tra thông báo lỗi | Hiển thị inline error `MSG-0806`: *"Enter an email address in the correct format, like name@example.com"*; Hệ thống chặn không cho lưu | EP (Invalid) | Regression | **P1** |
| `TC-R8-102` | My Details | Verify email length boundary of 150 characters (BVA 2-Point) | Edit Mode đang mở | 150 chars: `a`*138 + `@example.com`<br>151 chars: `a`*139 + `@example.com` | 1. Nhập email 150 ký tự $\rightarrow$ Lưu<br>2. Nhập email 151 ký tự $\rightarrow$ Lưu | Chuỗi 150 ký tự: Lưu thành công với `MSG-0807`; Chuỗi 151 ký tự: Bị chặn bởi `maxlength="150"` hoặc báo lỗi | BVA (2-Point) | Sprint | **P2** |
| `TC-R8-103` | My Details | Verify each blank required field shows MSG-0001 or prevents saving | Edit Mode đang mở | Xóa trống: `phoneNumber`, `email`, `mailingStreet`, `mailingPostalCode`, `mailingCountry` | 1. Xóa rỗng từng trường bắt buộc<br>2. Bấm Save changes | Xuất hiện thông báo lỗi `MSG-0001` (ví dụ: *"Enter your email"*); nút Save changes bị khóa vô hiệu hóa; không gửi request rỗng lên server | Robustness | Regression | **P1** |
| `TC-R8-104` | My Details | Verify whitespace-only input is treated as blank | Edit Mode đang mở | `mailingStreet = " "` (khoảng trắng) | 1. Nhập khoảng trắng vào trường Street<br>2. Blur ô input | Hệ thống tự động trim và coi là để trống; kích hoạt validation lỗi `MSG-0001` cho trường bắt buộc | Boundary / Edge | Sprint | **P2** |
| `TC-R8-105` | My Details | Verify optional mailing block and unit can be left blank | Edit Mode đang mở | `mailingBlock = ""`, `mailingUnit = ""`; các trường khác hợp lệ | 1. Xóa trống Block và Unit<br>2. Bấm Lưu và xác nhận | Lưu thành công với `MSG-0807`; View Mode hiển thị dấu gạch ngang hoặc ẩn mục Block/Unit mà không sập giao diện | EP (Valid Optional) | Sprint | **P3** |
| `TC-R8-106` | My Details | Verify mailing block and unit length boundary of 20 characters | Edit Mode đang mở | 20 chars: `"B"*20`<br>21 chars: `"B"*21` | 1. Nhập 20 ký tự vào Block/Unit $\rightarrow$ Lưu<br>2. Nhập 21 ký tự vào Block/Unit $\rightarrow$ Lưu | 20 ký tự được lưu thành công; 21 ký tự bị cắt ngắn tại 20 ký tự bởi `maxlength="20"` hoặc báo lỗi | BVA (2-Point) | Sprint | **P3** |
| `TC-R8-107` | My Details | Verify mailing street and country length boundary of 100 characters | Edit Mode đang mở | 100 chars: `"S"*100`<br>101 chars: `"S"*101` | 1. Nhập 100 ký tự $\rightarrow$ Lưu<br>2. Nhập 101 ký tự $\rightarrow$ Lưu | 100 ký tự được lưu thành công; 101 ký tự bị chặn/cắt ngắn tại 100 ký tự bởi `maxlength="100"` | BVA (2-Point) | Sprint | **P3** |
| `TC-R8-108` | My Details | Verify mailing postal code must be exactly 6 digits (Singapore Format) | Edit Mode đang mở | Hợp lệ: `650009`<br>Không hợp lệ: `65000` (5 số), `6500091` (7 số), `65A009` | 1. Thử nhập từng giá trị vào Postal code<br>2. Kiểm tra lưu | Chỉ chấp nhận đúng 6 chữ số; các trường hợp 5 số, 7 số hoặc chứa chữ cái bị chặn lưu và hiển thị cảnh báo lỗi | BVA / Regex | Regression | **P2** |
| `TC-R8-109` | My Details | Verify backend 500 error shows MSG-0808 and retains baseline data | Edit Mode đang mở; Mock API `/api/parent/profile` trả về HTTP 500 | `phoneNumber = "98887777"` (SĐT cũ là `91234567`) | 1. Sửa SĐT thành `98887777`<br>2. Bấm Save changes $\rightarrow$ Confirm Save<br>3. Quan sát giao diện & reload | Hiển thị thông báo lỗi `MSG-0808`: *"We could not update your details. Please try again."*; Sau khi reload, số điện thoại vẫn giữ nguyên giá trị cũ `91234567` | Resilience / Chaos | Regression | **P1** |
| `TC-R8-110` | My Details | Verify My details is strictly view-only when all children are age 16+ | Phụ huynh PE đăng nhập; tất cả con (E1: 16t, E2: 17t) đều $\ge 16$ | Tài khoản phụ huynh PE | 1. Đăng nhập PE<br>2. Mở `/profile` | Nút "Update details" hoàn toàn biến mất hoặc bị ẩn; màn hình chỉ ở chế độ View tĩnh; gọi API update trả về 403 Forbidden | Decision Table | Sprint | **P1** |
| `TC-R8-111` | My Details | Verify My details is editable when at least one child is under age 16 | Phụ huynh PB đăng nhập; có con B1: 16t, con B2: 14t (< 16) | Tài khoản phụ huynh PB | 1. Đăng nhập PB<br>2. Mở `/profile` | Nút "Update details" hiển thị bình thường; bấm vào mở được Edit Mode và lưu thông tin thành công | Decision Table | Sprint | **P1** |
| `TC-R8-112` | My Details | Verify a parent cannot update another parent's profile via API (IDOR / BOLA Prevention) | Phụ huynh FA đăng nhập; lấy được Profile ID của phụ huynh MA | Target ID: `MA_PROFILE_ID` | 1. Dùng token của FA gửi API update với ID của MA<br>2. Kiểm tra response và hồ sơ MA | Request bị từ chối với HTTP 403 Forbidden hoặc `MSG-0003`: *"You do not have permission to view or edit this record."*; Hồ sơ MA không đổi | Security (IDOR) | Sprint | **P1** |
| `TC-R8-113` | My Details | Verify father's profile update does not alter mother's separate profile details | Cả Cha (FA) và Mẹ (MA) liên kết chung con | FA cập nhật số điện thoại mới: `98887777` | 1. FA đăng nhập và lưu số điện thoại mới<br>2. Đăng xuất FA, đăng nhập MA vào `/profile` | Hồ sơ cá nhân của MA giữ nguyên số điện thoại riêng của MA, không bị ảnh hưởng bởi thay đổi của FA | Data Isolation | Sprint | **P2** |
| `TC-R8-114` | My Details | Verify script input in mailing fields is safely sanitized (XSS Prevention) | Edit Mode đang mở | `mailingStreet = "<script>alert('XSS')</script>"` | 1. Nhập chuỗi script vào Street<br>2. Bấm Lưu và xác nhận<br>3. Reload trang `/profile` | Không có hộp thoại popup alert nào bị kích hoạt; chuỗi script được mã hóa an toàn (HTML Entity Escaped) hiển thị dạng text thường | Security (XSS) | Regression | **P1** |
| `TC-ATM-02` | My Details | Verify NRIC masking toggle button switches between Show and Hide state | View Mode đang mở trên `/profile` | NRIC: `*****123F` $\leftrightarrow$ `S1234123F` | 1. Kiểm tra ban đầu: NRIC che, nút nhãn "Show NRIC"<br>2. Click "Show NRIC"<br>3. Kiểm tra NRIC hiện, nút nhãn "Hide NRIC"<br>4. Click "Hide NRIC" | NRIC ẩn/hiện mượt mà; nhãn nút đổi tương ứng; không gây giật layout CLS | UI Atomic | Smoke | **P1** |
| `TC-ATM-03` | My Details | Verify mode transition buttons (Update details and Cancel) restore clean baseline | View Mode trên `/profile` | Nhập tạm SĐT `97776666` | 1. Bấm "Update details" (Mở Edit)<br>2. Gõ thay đổi dữ liệu<br>3. Bấm "Cancel" | Quay lại View Mode; dữ liệu gõ dở bị hủy bỏ; không lưu vào state/DB | UI Atomic | Smoke | **P1** |
| `TC-ATM-04` | My Details | Verify Save button pristine & dirty state gatekeeper | Vừa mở Edit Mode qua Update details | Form chưa thay đổi (Pristine) | 1. Mở Edit Mode<br>2. Kiểm tra trạng thái nút Save và dòng hint<br>3. Gõ 1 ký tự vào SĐT<br>4. Xóa ký tự đó về nguyên bản | Khi form chưa sửa: Nút Save `disabled=true`, hiển thị dòng *"Make a change to enable saving."*; Khi sửa: Nút Save sáng `disabled=false` | UI State Gate | Sprint | **P2** |
| `TC-INT-01` | My Details | Verify Confirm Dialog 'Keep editing' button retains dirty form data | Đã mở Edit Mode, nhập dữ liệu hợp lệ mới | SĐT mới: `98887777` | 1. Nhập SĐT mới<br>2. Bấm "Save changes" $\rightarrow$ Mở dialog<br>3. Bấm nút "Keep editing" trên dialog | Dialog đóng lại; form vẫn giữ nguyên ở Edit Mode với số `98887777`; không gửi API lưu | Multi-Component | Sprint | **P2** |
| `TC-NFR-01` | My Details | Verify Non-Functional Layout Integrity, Zero Console Crash & Accessibility (Invariant 7) | Mở `/profile` trên Desktop (1280x720) và Mobile Viewport | DOM cây component | 1. Quét Console logs trong suốt vòng đời chuyển tab View $\leftrightarrow$ Edit<br>2. Kiểm tra thanh cuộn ngang `overflow-x`<br>3. Kiểm tra bàn phím Tab order | 0 Uncaught JS Exceptions; không xuất hiện thanh cuộn ngang (`scrollWidth === clientWidth`); tỷ lệ tương phản đạt chuẩn WCAG AA $\ge 4.5:1$ | Non-Functional | Smoke | **P1** |

---

## 4. CHI TIẾT TỪNG KỊCH BẢN THỰC THI (STEP-BY-STEP SPECIFICATIONS)

### 📌 Nhóm 1: Kiểm thử Đơn Component & UI State (Atomic UI Units)

#### `TC-ATM-01` / `TC-R8-094`: SingPass Identity Read-Only & NRIC Toggle
* **Mục tiêu**: Đảm bảo các thông tin định danh cá nhân lấy từ SingPass (Full Name, NRIC, Residential Address) có thuộc tính chỉ đọc (read-only), không có ô input để chỉnh sửa theo quy định bảo mật chính phủ.
* **Tiền điều kiện**: Phụ huynh FA đăng nhập thành công vào hệ thống, đang ở URL `http://localhost:5174/profile`.
* **Dữ liệu kiểm thử**: Hồ sơ phụ huynh FA (Tên: `NGUYEN VAN MINH` hoặc `TAN WEI MING`, NRIC: `S****123F`).
* **Các bước thực hiện**:
  1. Kiểm tra sự hiện diện của khối thẻ thông tin SingPass: `h2:has-text("Singpass verified identity")` hoặc `[data-testid="full-name"]`.
  2. Tìm kiếm các phần tử input cho Họ tên (`input[name="fullName"]`) và Địa chỉ cư trú (`input[name="residentialAddress"]`).
  3. Kiểm tra số NRIC ban đầu đang hiển thị ở trạng thái che giấu ký tự (`*****123F`).
  4. Bấm vào nút `button:has-text("Show NRIC")`.
  5. Bấm vào nút `button:has-text("Hide NRIC")`.
* **Kết quả kỳ vọng**:
  - `page.locator('input[name="fullName"]').count() === 0`.
  - `page.locator('input[name="residentialAddress"]').count() === 0`.
  - NRIC ban đầu được che mặt nạ; sau bước 4 số NRIC hiển thị rõ ràng và nút đổi thành `"Hide NRIC"`; sau bước 5 NRIC được che lại và nút quay về `"Show NRIC"`.

#### `TC-ATM-04`: Save Changes Button Pristine & Dirty State Gatekeeper
* **Mục tiêu**: Đảm bảo nút "Save changes" luôn bị vô hiệu hóa (`disabled`) khi người dùng chưa thực hiện bất kỳ thay đổi nào trên form, nhằm tránh việc kích hoạt request API vô nghĩa.
* **Tiền điều kiện**: Form hồ sơ đang được mở ở chế độ Chỉnh sửa (Edit Mode).
* **Các bước thực hiện**:
  1. Ngay khi bấm "Update details", quan sát trạng thái của nút `button:has-text("Save changes")`.
  2. Kiểm tra dòng chỉ dẫn: `p:has-text("Make a change to enable saving.")`.
  3. Thay đổi 1 chữ số trong ô `input[name="phoneNumber"]`.
  4. Quan sát lại trạng thái nút "Save changes".
* **Kết quả kỳ vọng**:
  - Tại bước 1: Nút "Save changes" có thuộc tính `disabled` hoặc `is_disabled() == True`. Dòng hint xuất hiện.
  - Tại bước 4: Nút "Save changes" lập tức chuyển sang trạng thái kích hoạt (`is_enabled() == True`), dòng hint biến mất.

---

### 📌 Nhóm 2: Kiểm thử Xác Thực Dữ Liệu & Giá Trị Biên (Validation & BVA/EP)

#### `TC-R8-098` & `TC-R8-099`: Mobile Number Format Acceptance & Rejection (`MSG-0805`)
* **Mục tiêu**: Xác thực nghiêm ngặt số điện thoại di động Singapore (8 chữ số, bắt đầu bằng 6, 8, hoặc 9) theo tiêu chuẩn FSD Section 6 & BR-08-09.1.
* **Phân vùng tương đương (EP)**:
  - *Hợp lệ*: 8 số bắt đầu bằng 6 (ví dụ: `61234567`), 8 (ví dụ: `81234567`), hoặc 9 (ví dụ: `91234567`).
  - *Không hợp lệ*: Đầu số khác (ví dụ: `71234567`, `51234567`), độ dài thiếu/thừa (7 số: `9123456`, 9 số: `912345678`), chứa chữ cái (`9123abcd`), có tiền tố quốc gia (`+6591234567`).
* **Các bước thực hiện**:
  1. Nhập lần lượt các giá trị hợp lệ $\rightarrow$ Kiểm tra form cho phép lưu.
  2. Nhập các giá trị không hợp lệ $\rightarrow$ Blur ô input hoặc bấm Save changes.
* **Kết quả kỳ vọng**:
  - Các số hợp lệ: Form chấp nhận và mở khóa nút lưu.
  - Các số không hợp lệ: Hiển thị thông báo lỗi inline chuẩn FSD `MSG-0805`: *"Enter a mobile number in the correct format, like 9123 4567"*. Hệ thống từ chối lưu.

#### `TC-R8-101` & `TC-R8-102`: Email Syntax RFC 5322 & Length Limit (150 Characters)
* **Mục tiêu**: Kiểm tra định dạng cú pháp email và giới hạn tối đa 150 ký tự.
* **Dữ liệu kiểm thử**:
  - Cú pháp sai: `nameexample.com`, `name@`, `@example.com`, `name@example`, `name @example.com`.
  - Biên độ dài: 150 ký tự (`"a"*138 + "@example.com"`) và 151 ký tự (`"a"*139 + "@example.com"`).
* **Kết quả kỳ vọng**:
  - Cú pháp sai: Hiển thị lỗi `MSG-0806`: *"Enter an email address in the correct format, like name@example.com"*.
  - 150 ký tự: Được chấp nhận lưu.
  - 151 ký tự: Bị chặn hoặc bị cắt ngắn ở 150 ký tự theo thuộc tính `maxlength="150"`.

#### `TC-R8-103` & `TC-R8-104`: Required Fields Blank & Whitespace-Only Prevention (`MSG-0001`)
* **Mục tiêu**: Ngăn chặn người dùng bỏ trống hoặc chỉ nhập khoảng trắng vào 5 trường bắt buộc (`phoneNumber`, `email`, `mailingStreet`, `mailingPostalCode`, `mailingCountry`).
* **Kết quả kỳ vọng**:
  - Hiển thị thông báo lỗi `MSG-0001` (ví dụ: *"Enter your email"*, *"Enter your street"*, v.v.).
  - Nút Save changes bị vô hiệu hóa hoặc form chặn không cho submit.

---

### 📌 Nhóm 3: Kiểm thử Tích Hợp Giữa Nhiều Component & API (Integration & Dialog)

#### `TC-R8-097` & `TC-INT-01`: Form Submission $\rightarrow$ Confirm Dialog Workflow
* **Mục tiêu**: Kiểm thử luồng tương tác giữa Form nhập liệu, Hộp thoại xác nhận (`alertdialog`), và Toast thông báo sau khi API phản hồi.
* **Các bước thực hiện**:
  1. Ở Edit Mode, sửa số điện thoại thành `98887777`.
  2. Bấm nút "Save changes" trên form.
  3. Kiểm tra sự xuất hiện của Modal Dialog: `div[role="alertdialog"]`.
  4. Bấm nút "Keep editing" trên dialog $\rightarrow$ Xác minh dialog đóng, form vẫn giữ nguyên `98887777`.
  5. Bấm lại "Save changes" trên form $\rightarrow$ Bấm tiếp "Save changes" trên dialog.
* **Kết quả kỳ vọng**:
  - Hộp thoại hiển thị đúng vai trò `alertdialog` và có tiêu đề xác nhận.
  - Nút "Keep editing" không làm mất dữ liệu vừa gõ.
  - Nút "Save changes" trên dialog kích hoạt request mutation, hiển thị Toast xanh `MSG-0807`: *"Your details have been updated."*, đưa giao diện trở lại View Mode với số điện thoại mới.

#### `TC-R8-109`: Fault Injection - Backend 500 System Error Resilience (`MSG-0808`)
* **Mục tiêu**: Kiểm tra khả năng xử lý sự cố khi API backend trả về HTTP 500 trong lúc lưu hồ sơ.
* **Tiền điều kiện**: Sử dụng Playwright Route Mock để chặn endpoint cập nhật profile và trả về status `500 Internal Server Error`.
* **Kết quả kỳ vọng**:
  - Giao diện không bị crash trắng trang (White Screen of Death).
  - Hiển thị thông báo lỗi hệ thống `MSG-0808`: *"We could not update your details. Please try again."*.
  - Sau khi reload trang, toàn bộ thông tin trong DB vẫn giữ nguyên giá trị cũ ban đầu.

---

### 📌 Nhóm 4: Quy Tắc Ràng Buộc Nghiệp Vụ & An Toàn Bảo Mật (Business Rules & Security)

#### `TC-R8-110` & `TC-R8-111`: Quy Tắc Độ Tuổi Con $\ge 16$ Tuổi Khóa Chế Độ Chỉnh Sửa
* **Mục tiêu**: Kiểm tra nghiệp vụ `FR-08.3 Precondition` & `AC #09`:
  - Khi TẤT CẢ các con của phụ huynh đều từ 16 tuổi trở lên: Màn hình Profile bị khóa ở chế độ View-only, ẩn nút "Update details", API từ chối cập nhật.
  - Khi có ÍT NHẤT 1 con dưới 16 tuổi: Nút "Update details" hiển thị bình thường, cho phép chỉnh sửa.
* **Dữ liệu kiểm thử**:
  - Phụ huynh PE: Con E1 (16 tuổi), Con E2 (17 tuổi) $\rightarrow$ Khóa chỉnh sửa.
  - Phụ huynh PB: Con B1 (16 tuổi), Con B2 (14 tuổi) $\rightarrow$ Mở chỉnh sửa.

#### `TC-R8-112`: Chống Tấn Công IDOR / BOLA Giữa Các Phụ Huynh
* **Mục tiêu**: Đảm bảo phụ huynh A (FA) không thể can thiệp hoặc sửa đổi hồ sơ của phụ huynh B (MA) thông qua việc can thiệp API endpoint.
* **Kết quả kỳ vọng**: Request bị backend từ chối với mã lỗi HTTP `403 Forbidden` hoặc `MSG-0003`: *"You do not have permission to view or edit this record."*.

#### `TC-R8-114`: Phòng Chống Tấn Công XSS Trên Các Trường Nhập Liệu
* **Mục tiêu**: Nhập mã độc JavaScript `<script>alert('xss')</script>` hoặc `<img src=x onerror=alert(1)>` vào trường `mailingStreet`.
* **Kết quả kỳ vọng**: Dữ liệu được mã hóa an toàn (HTML Entity Escaped) khi lưu và hiển thị lại; tuyệt đối không có popup script nào được kích hoạt.

---

## 5. ĐÁNH GIÁ THẤT BẠI 9 TẦNG (9-TIER FAILURE EVALUATION GATES)

Bất kỳ kịch bản kiểm thử nào trên màn hình Profile đều sẽ bị đánh dấu **FAIL** ngay lập tức nếu vi phạm 1 trong 9 tầng sau:
1. **Client Runtime**: Xuất hiện bất kỳ lỗi Uncaught JS Exception (`TypeError`, `ReferenceError`) nào trong DevTools Console.
2. **Network Silent Fails**: Có request background API trả về HTTP 4xx/5xx hoặc asset CSS/JS bị 404 mà không được UI xử lý.
3. **Visual & Layout**: Giao diện xuất hiện thanh cuộn ngang ngoài ý muốn (`overflow-x`), nút bấm bị che khuất bởi Header (Z-Index).
4. **Actionability**: Nút bấm bị vô hiệu hóa bởi `pointer-events: none` sai lệch, Spinner loading quay vô tận quá 5s.
5. **Performance & SLA**: Độ trễ từ khi bấm Save đến khi có phản hồi vượt quá 3.0s; rò rỉ bộ nhớ JS Heap.
6. **Accessibility (A11y)**: Kẹt phím Tab trong Confirm Dialog, tỷ lệ tương phản màu chữ thông báo < 4.5:1.
7. **Client Storage**: Dữ liệu lưu trong LocalStorage/SessionStorage bị sai cấu trúc hoặc không parse được JSON.
8. **UI Security**: Lộ PII (số NRIC nguyên vẹn không che mặt nạ) trong thuộc tính DOM hoặc URL query string.
9. **Idempotency**: Test không thể chạy lặp lại nhiều lần do không rollback/cleanup dữ liệu kiểm thử.
