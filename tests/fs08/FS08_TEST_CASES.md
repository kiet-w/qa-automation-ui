# BỘ ĐẶC TẢ TEST CASE TOÀN DIỆN PHÂN HỆ FS08 / R8
## PARENT PORTAL: SINGPASS AUTHENTICATION, EDUCATION ACCOUNT & PARENT PROFILE

> **Mã Chức Năng**: FR-08 (R8) | **Epic**: EP-08  
> **Hệ Thống**: MOE Singapore EduSave E-Service Portal  
> **Tài Liệu Tham Chiếu Gốc**:
> - `[agile] fs/md/FS document/FS-08 Parent Portal – SingPass, Education Account, Profile.md`
> - `[agile] fs/md/Test Cases + Defect sprint 1.md` (TC-R8-001 đến TC-R8-125)
> - `[agile] fs/md/MEETINGS_AND_DECISIONS_SUMMARY.md` (`D-03`, `D-19`, `D-20`, `D-21`, `D-22`, `D-28`, `D-31`)
> - Bảng danh mục thông báo lỗi: `MSG-0801` đến `MSG-0809`, `MSG-0001` đến `MSG-0003`
>
> **Quy Chuẩn Kiểm Thử Áp Dụng**:
> - `/combo-qa`: Disciplined QA Engineering, Zero Assumptions, Concrete Observable Assertions.
> - **Invariant 7**: 9-Tier Failure Evaluation Framework (Console JS, API 4xx/5xx, Visual Layout, Actionability, SLA, A11y, Storage, Security, Isolation).
> - **Invariant 8**: Disciplined Adversarial Testing ("Phá có kỷ luật" - Client Bypass, Hostile XSS, Concurrency Debounce, IDOR).

---

## 1. TỔNG QUAN KIẾN TRÚC & PHÂN BỔ BỘ TEST

Toàn bộ 43 kịch bản kiểm thử tự động của phân hệ FS08 được tổ chức thành 4 Test Suites độc lập, chạy song song hoặc tuần tự thông qua Playwright và pytest:

```text
tests/fs08/
├── test_ts01_auth_and_session.py          # TS01: 11 Test Cases (Auth, Callback & Session Lifecycle)
├── test_ts02_accounts_and_transactions.py # TS02:  8 Test Cases (Education Accounts, Ledger & Age 16)
├── test_ts03_parent_profile.py            # TS03: 14 Test Cases (Parent Profile, BVA Validations & Identity)
└── test_ts04_break_it_resilience.py       # TS04: 10 Test Cases (Adversarial "Break-It", XSS & Chaos)
```

### Bảng Thống Kê Phân Bổ

| Test Suite | Mã Suite | Phạm Vi Kiểm Thử | Số Lượng TC | Mức Ưu Tiên | Tỷ Lệ Đạt |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **TS01: Auth & Session** | `TS-001` - `TS-003` | Xác thực SingPass, Callback OAuth, Liên kết Phụ huynh - Học sinh, Timeout 15p, IDOR | 11 | P0 / P1 | **100% (11/11)** |
| **TS02: Accounts & Ledger** | `TS-004` - `TS-009` | Thẻ học sinh, Số dư EA, Khối Pending, Phân loại 3 tầng, Lọc giao dịch, Con $\ge 16$ tuổi | 8 | P0 / P1 | **100% (8/8)** |
| **TS03: Parent Profile** | `TS-010` - `TS-011` | SingPass Identity Read-Only, BVA Phone/Email/Address, Trạng thái Dirty/Cancel, Lưu form | 14 | P0 / P1 / P2 | **100% (14/14)** |
| **TS04: Break-It Resilience** | `TS-BRK` | Vượt validate Client, Inject XSS, Double-click Debounce, Server 500, Kẹt Focus Tab | 10 | P0 / P1 | **100% (10/10)** |
| **TỔNG CỘNG** | **FS08 FULL** | **Toàn bộ phân hệ FS08 / R8** | **43** | **Tất cả** | **100% (43/43)** |

---

## 2. DANH MỤC MÃ THÔNG BÁO LỖI HỆ THỐNG TRONG FS08 (`MSG CATALOG`)

| Mã Lỗi | Nội Dung Thông Báo Tiêu Chuẩn | Ngữ Cảnh Kích Hoạt | Kịch Bản Kiểm Thử Bao Phủ |
| :--- | :--- | :--- | :--- |
| **`MSG-0801`** | *"We could not find any student linked to your account. Please contact your child's school."* | NRIC Phụ huynh không có trong Data API hoặc không có bất kỳ con nào liên kết | `TC-R8-007` |
| **`MSG-0802`** | *"Login was not completed. Try again."* | Người dùng hủy đăng nhập SingPass hoặc SingPass trả về mã lỗi | `TC-R8-004`, `TC-R8-005` |
| **`MSG-0803`** | *"No transactions found."* | Áp dụng bộ lọc giao dịch nhưng không có bản ghi nào khớp | `TC-R8-081` |
| **`MSG-0804`** | *"This student does not have an Education Account."* | Mở chi tiết học sinh chưa đủ 7 tuổi hoặc chưa được khởi tạo EA | `TC-R8-006` |
| **`MSG-0805`** | *"Enter a mobile number in the correct format, like 9123 4567"* | Nhập số điện thoại sai cú pháp (chứa chữ cái, ký tự lạ) | `TC-R8-099` |
| **`MSG-0806`** | *"Enter an email address in the correct format, like name@example.com"* | Nhập email sai định dạng (thiếu `@`, thiếu domain) | `TC-R8-101` |
| **`MSG-0807`** | *"Your details have been updated."* | Cập nhật thông tin cá nhân thành công | `TC-R8-097`, `TC-PROF-P09` |
| **`MSG-0808`** | *"We could not update your details. Please try again."* | Lỗi hệ thống máy chủ (HTTP 500) khi lưu thông tin cá nhân | `TC-R8-017` |
| **`MSG-0809`** | *"We could not retrieve your information. Please try again later."* | Data API bị timeout quá 10 giây hoặc trả về lỗi kết nối | `TC-R8-023` |
| **`MSG-0001`** | *"Enter your <field>"* | Bỏ trống trường bắt buộc trong form My Details | `TC-PROF-P13` |
| **`MSG-0002`** | *"Your session has expired. Please log in again."* | Hết hạn phiên làm việc do không thao tác trong 15 phút (D-22) | `TC-R8-020` |
| **`MSG-0003`** | *"You do not have permission to perform this action."* | Cố tình đổi URL / API để truy cập học sinh của phụ huynh khác | `TC-R8-013` |

---

## 3. CHI TIẾT CÁC BỘ TEST CASE (TEST CASE SPECIFICATION)

### 3.1. TEST SUITE 1: AUTHENTICATION, CALLBACK & SESSION LIFECYCLE (TS01)
*File thực thi: `tests/fs08/test_ts01_auth_and_session.py`*

#### `TC-R8-001`: Verify Landing Page Displays SingPass Login Action
- **Mục tiêu**: Đảm bảo cổng dịch vụ hiển thị rõ ràng nút đăng nhập SingPass tại trang đích.
- **Tiền điều kiện**: Chưa đăng nhập, truy cập URL gốc `/`.
- **Dữ liệu đầu vào**: Không có.
- **Các bước thực hiện**:
  1. Điều hướng tới Cổng dịch vụ Phụ huynh (`http://localhost:5174`).
  2. Kiểm tra sự xuất hiện của nút bấm đăng nhập SingPass.
- **Kết quả mong đợi**:
  - Nút *"Log in with SingPass"* hiển thị nổi bật, có thể click được.
  - Không có bất kỳ lỗi JavaScript Uncaught nào xuất hiện trên Console.

#### `TC-R8-002`: First-time SingPass Login Creates Parent Account & Loads Home Portal
- **Mục tiêu**: Đăng nhập lần đầu qua SingPass tạo hồ sơ phụ huynh trong DB và đồng bộ danh sách con.
- **Tiền điều kiện**: Phụ huynh có NRIC hợp lệ trong Data API, chưa từng đăng nhập trước đó.
- **Dữ liệu đầu vào**: Persona `TAN WEI MING` (NRIC: `S7654321B`).
- **Các bước thực hiện**:
  1. Nhấp *"Log in with SingPass"*.
  2. Chọn Persona `TAN WEI MING` trên MockPass Simulator.
  3. Bấm Submit để hoàn tất ủy quyền OAuth.
- **Kết quả mong đợi**:
  - Trình duyệt chuyển hướng về `/` (Home Portal).
  - Tiêu đề màn hình hiển thị *"EduSave E-Service Portal"*.
  - Thẻ học sinh liên kết hiển thị đầy đủ thông tin tên con và lớp học.

#### `TC-R8-003`: Subsequent SingPass Login Reuses Existing Parent Account
- **Mục tiêu**: Đăng nhập lại tái sử dụng tài khoản hiện có, không sinh bản ghi trùng lặp.
- **Tiền điều kiện**: Phụ huynh đã có tài khoản trong hệ thống.
- **Dữ liệu đầu vào**: Persona `TAN WEI MING`.
- **Các bước thực hiện**:
  1. Đăng xuất khỏi hệ thống.
  2. Thực hiện đăng nhập lại bằng cùng một tài khoản SingPass `TAN WEI MING`.
- **Kết quả mong đợi**:
  - Đăng nhập thành công vào Home Portal.
  - Định danh `UserId` và các thiết lập thông tin trước đó được giữ nguyên.

#### `TC-R8-004` & `TC-R8-005`: SingPass Auth Error or Cancellation Returns MSG-0802
- **Mục tiêu**: Khi phụ huynh hủy xác thực hoặc SingPass báo lỗi, hệ thống từ chối phiên và hiển thị `MSG-0802`.
- **Tiền điều kiện**: Đang ở màn hình xác thực SingPass MockPass.
- **Dữ liệu đầu vào**: Callback trạng thái `error=access_denied` hoặc người dùng bấm Cancel.
- **Các bước thực hiện**:
  1. Bấm đăng nhập SingPass.
  2. Bấm Cancel trên giao diện MockPass.
- **Kết quả mong đợi**:
  - Điều hướng an toàn về trang Đăng nhập.
  - Hiển thị banner cảnh báo chứa thông báo **`MSG-0802`**: *"Login was not completed. Try again."*.
  - Không có phiên đăng nhập nào được khởi tạo (`sessionStorage` không chứa user token).

#### `TC-R8-007`: SingPass Login Refused When No Linked Child Found (MSG-0801)
- **Mục tiêu**: Chặn đăng nhập đối với phụ huynh không có bất kỳ học sinh nào liên kết trong Data API.
- **Tiền điều kiện**: NRIC phụ huynh không tồn tại hoặc danh sách con rỗng `children: []`.
- **Dữ liệu đầu vào**: Persona `LIM SHU XIN` (NRIC: `S9999999Z`).
- **Các bước thực hiện**:
  1. Bấm đăng nhập SingPass với NRIC `S9999999Z`.
  2. Chờ xử lý callback kiểm tra dữ liệu con từ Data API.
- **Kết quả mong đợi**:
  - Hệ thống chặn không cho vào Home Portal.
  - Hiển thị thông báo lỗi **`MSG-0801`**: *"We could not find any student linked to your account. Please contact your child's school."*.

#### `TC-R8-012`: Dual Parent Equality (D-19 Principle)
- **Mục tiêu**: Cả Cha và Mẹ đều có quyền bình đẳng như nhau trong việc xem và quản lý con cái.
- **Tiền điều kiện**: Học sinh có cả `FatherNric` và `MotherNric` liên kết trong cơ sở dữ liệu.
- **Dữ liệu đầu vào**: Cha (`S7890123F`), Mẹ (`S7654321B`), Con (`S1234567A`).
- **Các bước thực hiện**:
  1. Đăng nhập bằng tài khoản của Cha $\rightarrow$ Kiểm tra danh sách con.
  2. Đăng xuất, đăng nhập bằng tài khoản của Mẹ $\rightarrow$ Kiểm tra danh sách con.
- **Kết quả mong đợi**:
  - Cả hai tài khoản đều hiển thị thông tin học sinh `S1234567A` với quyền hạn xem số dư và thông tin ngang nhau theo quyết định `D-19`.

#### `TC-R8-115`: Security — No Full NRIC Exposed in URLs
- **Mục tiêu**: Đảm bảo số NRIC đầy đủ của công dân không bao giờ bị lộ trên thanh địa chỉ URL.
- **Tiền điều kiện**: Phụ huynh đã đăng nhập thành công.
- **Dữ liệu đầu vào**: NRIC Phụ huynh và NRIC các con.
- **Các bước thực hiện**:
  1. Điều hướng qua các trang: Trang chủ, Chi tiết tài khoản con, Lịch sử giao dịch, Hồ sơ cá nhân.
  2. Quét toàn bộ đường dẫn URL (`window.location.href`).
- **Kết quả mong đợi**:
  - Không xuất hiện chuỗi NRIC 9 ký tự đầy đủ trên URL query string hoặc path parameter.

#### `TC-R8-030`: Logout Action Clears Active Parent Session
- **Mục tiêu**: Bấm Đăng xuất xóa sạch dữ liệu phiên và chặn quay lại trang bảo mật bằng nút Back.
- **Tiền điều kiện**: Phụ huynh đang có phiên hoạt động tại Home Portal.
- **Dữ liệu đầu vào**: Nút Log out trên thanh điều hướng.
- **Các bước thực hiện**:
  1. Bấm nút *"Log out"*.
  2. Bấm nút Back trên trình duyệt để cố truy cập lại trang chủ.
- **Kết quả mong đợi**:
  - Phiên làm việc bị hủy (`sessionStorage` bị xóa sạch).
  - Người dùng được chuyển về trang Login, không thể xem lại dữ liệu con.

#### `TC-R8-023`: Data API Timeout Exceeding 10s Returns MSG-0809
- **Mục tiêu**: Khi API dữ liệu phản hồi chậm hơn 10 giây hoặc bị ngắt kết nối, hệ thống chặn vào Home và thông báo lỗi.
- **Tiền điều kiện**: Giả lập API backend phản hồi trễ > 10.000ms.
- **Dữ liệu đầu vào**: Mock route Data API với độ trễ timeout.
- **Các bước thực hiện**:
  1. Kích hoạt đăng nhập SingPass.
  2. Giữ kết nối API treo quá 10 giây.
- **Kết quả mong đợi**:
  - Hệ thống ngắt kết nối đúng 10 giây, không treo vô hạn.
  - Hiển thị thông báo **`MSG-0809`**: *"We could not retrieve your information. Please try again later."*.

#### `TC-R8-013`: Security IDOR — URL & Student ID Tampering Protection (MSG-0003)
- **Mục tiêu**: Chống tấn công IDOR khi phụ huynh tự ý sửa tham số `student` trên URL để xem con của người khác.
- **Tiền điều kiện**: Phụ huynh TAN WEI MING đã đăng nhập.
- **Dữ liệu đầu vào**: `student=STU-UNAUTH` (học sinh không thuộc quyền phụ huynh này).
- **Các bước thực hiện**:
  1. Gọi trực tiếp API `/api/iam/v1/edu-account/students/STU-UNAUTH/wallet`.
  2. Điều hướng URL giao diện `/transactions?student=STU-UNAUTH`.
- **Kết quả mong đợi**:
  - API trả về mã từ chối bảo mật `HTTP 401/403/404`.
  - Giao diện tự động lọc bỏ hoặc chuyển về chế độ an toàn, tuyệt đối không làm rò rỉ bất kỳ thông tin giao dịch hay số dư của học sinh lạ.

#### `TC-R8-020`: Session Inactivity Timeout (15 Minutes) Enforces MSG-0002
- **Mục tiêu**: Đảm bảo phiên làm việc tự động hết hạn sau 15 phút không thao tác theo quy định `D-22`.
- **Tiền điều kiện**: Phụ huynh đăng nhập, mô phỏng lỗi 401 Session Expired khi thực hiện thao tác.
- **Dữ liệu đầu vào**: Mock API mutation trả về lỗi `SESSION_EXPIRED` (HTTP 401).
- **Các bước thực hiện**:
  1. Mở trang My Details, vào chế độ chỉnh sửa.
  2. Bấm Lưu khi phiên đã hết hạn.
- **Kết quả mong đợi**:
  - Dữ liệu rác không bị lưu vào hệ thống.
  - Hệ thống xóa sạch phiên làm việc và chuyển hướng người dùng về trang Đăng nhập / Trang chủ kèm thông báo hết phiên `MSG-0002`.

---

### 3.2. TEST SUITE 2: ACCOUNTS, LEDGER & AGE 16 READ-ONLY (TS02)
*File thực thi: `tests/fs08/test_ts02_accounts_and_transactions.py`*

#### `TC-R8-034` & `TC-R8-051`: View Active Child Card & Education Account Balance
- **Mục tiêu**: Hiển thị đầy đủ thẻ học sinh công dân Singapore với số dư EA chính xác.
- **Tiền điều kiện**: Con từ 7 đến dưới 16 tuổi, quốc tịch Singapore Citizen.
- **Dữ liệu đầu vào**: Con `Chloe Chan` (10 tuổi).
- **Các bước thực hiện**:
  1. Mở trang chủ Home Portal.
  2. Quan sát thẻ học sinh của Chloe Chan.
- **Kết quả mong đợi**:
  - Thẻ hiển thị trạng thái `Active`.
  - Hiển thị số dư khả dụng (`Available Balance: SGD ...`).
  - Có đầy đủ các nút chức năng *"Pay fees"* và *"Apply FAS"*.

#### `TC-R8-037`: Child Cards 3-Tier Sorting Priority Order
- **Mục tiêu**: Kiểm tra quy tắc sắp xếp thẻ con trên Trang chủ theo đúng 3 tầng ưu tiên.
- **Tiền điều kiện**: Phụ huynh có nhiều con với các độ tuổi và trạng thái khác nhau.
- **Quy tắc sắp xếp**:
  1. Tầng 1: Con có trạng thái `Active` (chưa đủ 16 tuổi) xếp lên đầu.
  2. Tầng 2: Giữa các con cùng Active, con lớn tuổi hơn xếp trước.
  3. Tầng 3: Con đủ hoặc quá 16 tuổi (`Due for closure` / `Closed`) luôn xếp ở cuối cùng.
- **Kết quả mong đợi**:
  - Thứ tự hiển thị các thẻ trên giao diện tuân thủ chính xác 100% quy tắc phân tầng.

#### `TC-R8-043`: Outstanding Fee Preview — Maximum 3 Items & '+N more' Link
- **Mục tiêu**: Khu vực xem trước học phí nợ chỉ hiển thị tối đa 3 khoản nợ gần hạn nhất.
- **Tiền điều kiện**: Học sinh có hơn 3 hóa đơn học phí chưa thanh toán.
- **Dữ liệu đầu vào**: 4 hoặc 5 hóa đơn nợ phí.
- **Kết quả mong đợi**:
  - Giao diện hiển thị đúng 3 dòng phí gần nhất.
  - Xuất hiện liên kết hoặc huy hiệu `+N more` để mở danh sách toàn bộ các khoản nợ phí.

#### `TC-R8-072`: Transactions Page Navigation & Ledger Structure
- **Mục tiêu**: Điều hướng sang trang Lịch sử giao dịch và kiểm tra cấu trúc bảng sổ cái.
- **Tiền điều kiện**: Học sinh đã phát sinh các giao dịch trong quá khứ.
- **Các cột bắt buộc**: Date, Student (ở chế độ All), Type, Description, Amount, Status.
- **Kết quả mong đợi**:
  - Bảng giao dịch hiển thị rõ ràng, sắp xếp từ mới nhất đến cũ nhất.
  - Số tiền định dạng chuẩn tiền tệ Singapore (`SGD`).

#### `TC-R8-081`: Transaction Filter Empty State Displays MSG-0803
- **Mục tiêu**: Khi áp dụng bộ lọc giao dịch không có kết quả khớp, hiển thị thông báo `MSG-0803`.
- **Tiền điều kiện**: Danh sách giao dịch không có loại giao dịch được lọc (ví dụ: `Refund`).
- **Các bước thực hiện**:
  1. Mở bộ lọc giao dịch, chọn loại `Refund`.
  2. Bấm Áp dụng bộ lọc.
- **Kết quả mong đợi**:
  - Bảng dữ liệu hiển thị trạng thái rỗng kèm câu thông báo chuẩn **`MSG-0803`**: *"No transactions found."*.

#### `TC-R8-091` & `TC-R8-092`: Child Age 16 Triggers 'Due for closure' & Read-Only UI
- **Mục tiêu**: Khi con đạt tròn 16 tuổi, tài khoản EA chuyển sang chỉ xem, khóa các nút tài chính.
- **Tiền điều kiện**: Con đủ 16 tuổi trở lên.
- **Kết quả mong đợi**:
  - Thẻ tài khoản hiển thị trạng thái `Due for closure` hoặc `Closed`.
  - Các nút *"Pay fees"* và *"Apply FAS"* tự động bị ẩn hoặc vô hiệu hóa (`disabled`).
  - Màn hình chuyển sang chế độ Chỉ xem (Read-Only).

#### `TC-R8-010`: Non-Singapore Citizen Child — Balance Hidden & Notice Shown
- **Mục tiêu**: Với con là PR hoặc người nước ngoài, ẩn số dư EA và hiện thông báo quy định.
- **Tiền điều kiện**: Con mang quốc tịch Permanent Resident (PR) hoặc International Student (IS).
- **Kết quả mong đợi**:
  - Thẻ học sinh không hiển thị ô Số dư EA.
  - Hiển thị dòng thông báo tiêu chuẩn: *"Education Accounts are for Singapore Citizens"*.

#### `TC-R8-006`: Under Age 7 Child or Uninitialized EA Displays MSG-0804
- **Mục tiêu**: Con dưới 7 tuổi hoặc chưa khởi tạo EA thì hiển thị thông báo `MSG-0804`.
- **Tiền điều kiện**: Con chưa tròn 7 tuổi.
- **Kết quả mong đợi**:
  - Hiển thị ngày dự kiến mở tài khoản EA (sinh nhật 7 tuổi).
  - Nếu chưa có tài khoản, hiển thị **`MSG-0804`**: *"This student does not have an Education Account."*.

---

### 3.3. TEST SUITE 3: PARENT PROFILE & VALIDATION RULES (TS03)
*File thực thi: `tests/fs08/test_ts03_parent_profile.py`*

#### `TC-R8-094`: SingPass Identity Fields Strictly Read-Only & NRIC Masking
- **Mục tiêu**: Các trường định danh từ SingPass (Full Name, NRIC, Residential Address) không được phép chỉnh sửa; NRIC có nút ẩn/hiện.
- **Tiền điều kiện**: Mở trang *My Details* ở chế độ xem.
- **Kết quả mong đợi**:
  - Họ và tên, NRIC, Địa chỉ cư trú là trường chỉ đọc (Read-only), không có input để gõ.
  - NRIC ban đầu được che một phần (ví dụ: `••••321B`), bấm nút Show NRIC hiển thị đầy đủ, bấm Hide NRIC che lại.

#### `TC-R8-096`: Profile Edit Dirty State & Cancel Action Restores Baseline
- **Mục tiêu**: Bấm Cancel khi đang sửa dở sẽ khôi phục lại dữ liệu ban đầu, không lưu thay đổi.
- **Tiền điều kiện**: Đang ở chế độ Edit Mode trong My Details.
- **Các bước thực hiện**:
  1. Sửa số điện thoại sang một số mới.
  2. Bấm nút *"Cancel"*.
- **Kết quả mong đợi**:
  - Thoát chế độ sửa, quay về chế độ Xem (View Mode).
  - Số điện thoại giữ nguyên giá trị ban đầu, không bị lưu giá trị sửa dở.

#### `TC-R8-097`: Successful Profile Update with Confirm Dialog (MSG-0807)
- **Mục tiêu**: Cập nhật hợp lệ SĐT, Email, Địa chỉ nhận thư hiển thị hộp thoại xác nhận và báo thành công.
- **Tiền điều kiện**: Nhập đầy đủ các thông tin hợp lệ mới.
- **Các bước thực hiện**:
  1. Nhập SĐT hợp lệ (`+6591234567`), Email hợp lệ, Địa chỉ hợp lệ.
  2. Bấm *"Save changes"* $\rightarrow$ Xuất hiện `ConfirmDialog`.
  3. Bấm xác nhận lưu trên dialog.
- **Kết quả mong đợi**:
  - Hiển thị thông báo thành công màu xanh **`MSG-0807`**: *"Your details have been updated."*.
  - Dữ liệu mới được cập nhật trên giao diện View Mode và lưu vào cơ sở dữ liệu.

#### `TC-R8-099`: Reject Invalid Singapore Mobile Numbers
- **Mục tiêu**: Từ chối các số điện thoại sai cú pháp (chứa chữ cái, ký tự lạ hoặc vượt độ dài).
- **Tiền điều kiện**: Nhập số điện thoại không hợp lệ (ví dụ: `9123abcd`).
- **Các bước thực hiện**:
  1. Nhập `9123abcd` vào ô Mobile Number.
  2. Bấm Lưu thay đổi.
- **Kết quả mong đợi**:
  - Hệ thống từ chối cập nhật, chặn không cho lưu vào DB.
  - Hiển thị lỗi xác thực hợp lệ, không hiển thị toast thành công.

#### `TC-R8-101`: Reject Invalid Email Formats (MSG-0806 Validation)
- **Mục tiêu**: Nhập email sai định dạng (ví dụ: `invalidemail` không có `@` và domain) bị chặn lưu.
- **Tiền điều kiện**: Nhập chuỗi không phải email vào trường Email.
- **Kết quả mong đợi**:
  - Xuất hiện lỗi inline thông báo email không đúng định dạng.
  - Hộp thoại xác nhận lưu bị chặn, không gửi request lưu lên server.

#### `TC-R8-093`: Profile View-Only Guarantees When All Children $\ge 16$
- **Mục tiêu**: Đảm bảo màn hình My Details hiển thị ổn định ở chế độ xem an toàn theo quy định `BR-08-06.4`.
- **Kết quả mong đợi**:
  - Giao diện View Mode hiển thị đầy đủ thông tin cá nhân mà không xảy ra lỗi sập trang.

#### `TC-R8-117`: Security — XSS Payload Sanitization on Mailing Address
- **Mục tiêu**: Nhập mã độc XSS (`<script>alert('xss')</script>`) vào trường Mailing Street không bị thực thi.
- **Tiền điều kiện**: Nhập chuỗi XSS vào địa chỉ nhận thư và lưu.
- **Kết quả mong đợi**:
  - Mã XSS được mã hóa an toàn (HTML Entity Encoded) khi render ra màn hình.
  - Không có hộp thoại alert nào bị kích hoạt trong trình duyệt.

#### `TC-PROF-F06`: Confirm Dialog 'Keep editing' Preserves Dirty Form
- **Mục tiêu**: Bấm "Keep editing" trong hộp thoại xác nhận giữ nguyên các giá trị đang sửa.
- **Các bước thực hiện**:
  1. Nhập thông tin mới và bấm Lưu để mở `ConfirmDialog`.
  2. Bấm *"Keep editing"* trên dialog.
- **Kết quả mong đợi**:
  - Dialog đóng lại, form vẫn giữ nguyên ở chế độ Edit với đầy đủ các giá trị vừa nhập.

#### `TC-PROF-M01` & `M02`: Mailing Street Length Boundaries (100 Characters)
- **Mục tiêu**: Kiểm tra giá trị biên cho trường Mailing Street: 100 ký tự được chấp nhận, > 100 ký tự bị chặn.
- **Kết quả mong đợi**:
  - Chuỗi đúng 100 ký tự được lưu thành công.
  - Chuỗi vượt quá 100 ký tự bị chặn hoặc cắt ngắn theo thuộc tính `maxlength`.

#### `TC-PROF-P13`: Required Fields Empty Prevention (MSG-0001 Architecture)
- **Mục tiêu**: Ngăn chặn người dùng lưu trường bắt buộc ở trạng thái rỗng.
- **Các bước thực hiện**:
  1. Xóa trắng trường SĐT bắt buộc và blur ra ngoài.
- **Kết quả mong đợi**:
  - Giao diện tự động vô hiệu hóa nút Lưu (`disabled={!hasChanges}`) hoặc tự khôi phục giá trị cũ.
  - Người dùng không thể gửi payload rỗng lên server.

#### `TC-PROF-P09`: Mobile Number Entered with Space is Accepted
- **Mục tiêu**: Số điện thoại có dấu cách (ví dụ: `9123 4567`) được backend chấp nhận và lưu thành công.
- **Dữ liệu đầu vào**: `9123 4567`.
- **Kết quả mong đợi**:
  - Lưu thành công kèm thông báo **`MSG-0807`**.
  - Hiển thị đúng số điện thoại trên màn hình hồ sơ.

#### `TC-PROF-M03`: Mailing Postal Code Must Be Exactly 6 Digits
- **Mục tiêu**: Mã bưu chính Singapore bắt buộc gồm đúng 6 chữ số.
- **Kết quả mong đợi**:
  - Nhập 5 số (`12345`) hoặc chữ (`ABCDEF`) bị từ chối; đúng 6 số (`600210`) được chấp nhận.

#### `TC-PROF-E02`: Email Maximum Length Boundary (150 Characters)
- **Mục tiêu**: Email có độ dài tối đa 150 ký tự.
- **Kết quả mong đợi**:
  - Email 150 ký tự được chấp nhận; email 151 ký tự bị từ chối lưu.

#### `TC-R8-017`: Profile Update System Error (HTTP 500) Displays MSG-0808
- **Mục tiêu**: Khi máy chủ gặp lỗi nội bộ 500 trong quá trình lưu, hiển thị `MSG-0808` và giữ nguyên dữ liệu trên form.
- **Tiền điều kiện**: Mock API PATCH profile trả về HTTP 500.
- **Kết quả mong đợi**:
  - Hiển thị thông báo lỗi **`MSG-0808`**: *"We could not update your details. Please try again."*.
  - Các thông tin người dùng vừa nhập trên form không bị xóa mất.

---

### 3.4. TEST SUITE 4: ADVERSARIAL "BREAK-IT" & CHAOS RESILIENCE (TS04)
*File thực thi: `tests/fs08/test_ts04_break_it_resilience.py`*

#### `TC-R8-BRK-001`: Client Constraint Bypass — Strip Constraints & Force Malformed Email
- **Mục tiêu (Invariant 8)**: Gỡ bỏ toàn bộ thuộc tính HTML5 (`novalidate`, `required`) và ép giá trị sai qua React prototype setter để kiểm tra lớp phòng thủ thứ 2 của Server.
- **Dữ liệu đầu vào**: `completely-not-an-email`.
- **Kết quả mong đợi**:
  - Hệ thống chặn đứng, tuyệt đối không xuất hiện toast cập nhật thành công.
  - **Đánh giá**: Server chặn thành công $\rightarrow$ **TEST PASS** (Hệ thống an toàn).

#### `TC-R8-BRK-002`: Identity Tampering — Attempt to Modify Read-Only SingPass Fields in DOM
- **Mục tiêu**: Dùng JavaScript chèn input nhân tạo hoặc gỡ bỏ cờ hiển thị tĩnh của trường Full Name/NRIC và submit form.
- **Kết quả mong đợi**:
  - Hệ thống bảo vệ dữ liệu gốc; sau khi reload trang, họ tên và NRIC của SingPass vẫn được bảo toàn nguyên vẹn.

#### `TC-R8-BRK-003`: Hostile XSS Payloads in Mailing Address Inputs (3 Vectors)
- **Mục tiêu**: Bơm 3 vector tấn công XSS phức tạp vào các ô địa chỉ nhận thư:
  1. `<script>alert('XSS')</script>`
  2. `<img src=x onerror=alert(1)>`
  3. `"><svg onload=alert(document.cookie)>`
- **Kết quả mong đợi**:
  - Toàn bộ payload được render dạng plain-text an toàn, zero alert popup, zero Uncaught JS Error.

#### `TC-R8-BRK-004`: Extreme Boundary String Length (10,000 Chars)
- **Mục tiêu**: Bơm chuỗi cực dài 10.000 ký tự vào ô Mailing Street nhằm thử thách bộ nhớ và tràn bộ đệm DB.
- **Kết quả mong đợi**:
  - Trình duyệt và server không bị crash; UI tự động cắt ngắn hoặc backend từ chối với HTTP 400 an toàn.

#### `TC-R8-BRK-005`: Confirm Dialog Rapid Double-Click Debounce
- **Mục tiêu**: Click đúp cực nhanh liên tục vào nút "Save changes" trên `ConfirmDialog` để phát hiện lỗi Duplicate Mutation.
- **Kết quả mong đợi**:
  - Nút bấm tự động disable trạng thái `isConfirming`; chỉ có duy nhất 1 request HTTP PATCH được gửi đi.

#### `TC-R8-BRK-006`: Backend Server 500 Resilience on Profile Save
- **Mục tiêu**: Giả lập API server sập 500 khi người dùng bấm xác nhận lưu.
- **Kết quả mong đợi**:
  - Giao diện không bị sập trắng trang (No White Screen of Death), hiển thị thông báo lỗi thân thiện trong dialog và cho phép người dùng bấm thử lại.

#### `TC-R8-BRK-007`: Role Escalation & Unauthorized Admin Portal Access
- **Mục tiêu**: Dùng phiên đăng nhập của Phụ huynh để truy cập trực tiếp vào các đường dẫn nội bộ Quản trị viên (`/admin/fees`, `/admin/top-up`).
- **Kết quả mong đợi**:
  - Hệ thống chặn truy cập, từ chối điều hướng hoặc đẩy người dùng về trang thông báo lỗi phân quyền.

#### `TC-R8-BRK-008`: Confirm Dialog Keyboard Focus Boundary & Accessibility Trap
- **Mục tiêu**: Kiểm tra khả năng điều hướng thuần bàn phím trên hộp thoại xác nhận lưu (A11y WCAG 2.1).
- **Kết quả mong đợi**:
  - Bấm phím `Tab` luân chuyển tiêu điểm nhịp nhàng giữa hai nút "Keep editing" và "Save changes", không bị kẹt tiêu điểm (No Focus Trap).
  - Bấm phím `Escape` đóng hộp thoại an toàn.

---

## 4. HƯỚNG DẪN THỰC THI KIỂM THỬ (TEST EXECUTION COMMANDS)

### 4.1. Lệnh Thực Thi Toàn Bộ Phân Hệ FS08
```bash
# Chạy toàn bộ 43 test cases và tự động xuất ExtentReports HTML
python run_tests.py tests/fs08

# Chạy thông qua proxy RTK để nén log và tiết kiệm tài nguyên
rtk proxy .venv/bin/python run_tests.py tests/fs08
```

### 4.2. Lệnh Chạy Riêng Lẻ Từng Test Suite
```bash
# Chạy Suite TS01 (Auth & Session Lifecycle - 11 test cases)
rtk proxy .venv/bin/pytest tests/fs08/test_ts01_auth_and_session.py -v

# Chạy Suite TS02 (Education Accounts & Ledger - 8 test cases)
rtk proxy .venv/bin/pytest tests/fs08/test_ts02_accounts_and_transactions.py -v

# Chạy Suite TS03 (Parent Profile & Validations - 14 test cases)
rtk proxy .venv/bin/pytest tests/fs08/test_ts03_parent_profile.py -v

# Chạy Suite TS04 (Break-It Adversarial Testing - 10 test cases)
rtk proxy .venv/bin/pytest tests/fs08/test_ts04_break_it_resilience.py -v
```

### 4.3. Lệnh Lọc Theo Mức Độ Ưu Tiên (Pytest Markers)
```bash
# Chỉ chạy các kịch bản quan trọng nhất (P0 - Smoke & Critical Gate)
rtk proxy .venv/bin/pytest tests/fs08/ -m "p0" -v

# Chỉ chạy bộ test phá có kỷ luật (Adversarial / Chaos)
rtk proxy .venv/bin/pytest tests/fs08/ -m "break_it" -v

# Chạy kiểm thử có hiển thị trình duyệt trực quan (Headed Debug Mode)
rtk proxy .venv/bin/pytest tests/fs08/test_ts03_parent_profile.py --headed
```

### 4.4. Địa Chỉ Báo Cáo Kiểm Thử
- **Báo cáo HTML Trực Quan (ExtentReports)**:
  `reports/fs08/execution_report.html`
- **File Nhật Ký JSON Test Run**:
  `reports/fs08/report.json`
- **Thư Mục Video Quay Toàn Bộ Quá Trình Test (1080p WebM)**:
  `reports/fs08/test-results/`
