# BÁO CÁO TỔNG HỢP LỖI (DEFECT AUDIT REPORT)
**Module**: FS-08 Parent Portal (SingPass, Education Account, Profile)  
**Màn hình kiểm thử**: `My Profile` (`http://localhost:5174/profile`)  
**Tài liệu tham chiếu chuẩn**:
- FSD: [`specs/md/FS document/FS-08 Parent Portal – SingPass, Education Account, Profile.md`](file:///home/baudui/automation-ui/specs/md/FS%20document/FS-08%20Parent%20Portal%20–%20SingPass,%20Education%20Account,%20Profile.md) (Quy định MSG-0001, MSG-0805, MSG-0806, độ dài và các trường bắt buộc).
- Test Case Matrix: [`specs/md/Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md`](file:///home/baudui/automation-ui/specs/md/Test%20Cases/TC_R8_Parent_Portal_SingPass_Profile.md) (TC-R8-099, TC-R8-103, TC-R8-124).
- Tiêu chuẩn định dạng: AvePoint / Jira 15-field Enterprise Defect Logging Schema (`combo-qa` Format B).
- File Word đính kèm: [`Defect_Report_EduSave_Profile_FS08.docx`](./Defect_Report_EduSave_Profile_FS08.docx).

---

## 1. Bảng Tổng Hợp Lỗi (Defect Executive Summary Table)

| # | Mã Bug | Tóm tắt lỗi (Summary) | Thành phần (Component) | Mức độ nghiêm trọng (Severity) | Độ ưu tiên (Priority) | Trạng thái (Status) |
| :-: | :--- | :--- | :--- | :-: | :-: | :-: |
| **1** | `BUG-R8-001` | Lộ mã định danh i18n raw key `features.parentProfile.validation.mobileInvalid` thay vì câu thông báo lỗi cho người dùng | My Profile (Contact Form) | **S2 - Major** | **High** | Open / Pending Review |
| **2** | `BUG-R8-002` | Thiếu inline validation cảnh báo khi để trống trường bắt buộc `Street` và `Country` (vi phạm MSG-0001) | My Profile (Mailing Address) | **S2 - Major** | **High** | Open / Pending Review |
| **3** | `BUG-R8-003` | Nút hamburger "Open navigation" trên Navbar bị đè z-index / không mở rộng menu điều hướng ở giao diện mobile responsive | Navigation Bar (Responsive Header) | **S3 - Normal** | **Medium** | Open / Pending Review |

---

## 2. Chi Tiết Từng Lỗi (15-Field Enterprise Defect Records)

### Bug #1 — Lộ mã raw key `features.parentProfile.validation.mobileInvalid` khi nhập sai định dạng Mobile Number

| Field Name | Specification / Value |
| :--- | :--- |
| **Project** | EduFAMS E-Service Portal |
| **Issue Type** | Bug |
| **Summary** | Mobile Number validation displays raw untranslated i18n translation key `features.parentProfile.validation.mobileInvalid` instead of user-friendly error message |
| **Priority** | High |
| **Component** | My Profile (`Contact Information` section) |
| **Affected Version** | Web Client SIT v1.0.0 (Port 5174) |
| **Fix Version** | Sprint 1 / Next Release |
| **Assignee** | Frontend Team / Unassigned |
| **Reviewer** | QA Team (`combo-qa`) |
| **Due Date** | 25-Oct-2026 |
| **Description** | Khi người dùng nhập số điện thoại sai định dạng (ví dụ `12` hoặc không đủ 8 chữ số bắt đầu bằng 6, 8, 9), hệ thống render trực tiếp chuỗi key bản địa hóa thô `features.parentProfile.validation.mobileInvalid`. Điều này gây khó hiểu nghiêm trọng cho người dùng cuối (End-User Confusion), vi phạm nguyên tắc bảo mật thông tin nội bộ giao diện và vi phạm quy định thông báo lỗi trong FSD FS-08. |
| **Steps to Reproduce** | 1. Truy cập `http://localhost:5174/profile` và đăng nhập bằng Singpass test citizen.<br>2. Nhấn nút **"Update details"** để mở form chỉnh sửa.<br>3. Tại trường **"Mobile Number"**, xóa và nhập giá trị không hợp lệ: `12`.<br>4. Blur khỏi ô nhập hoặc quan sát thông báo lỗi hiển thị ngay dưới trường. |
| **Expected Result** | Hệ thống hiển thị câu thông báo lỗi chuẩn nghiệp vụ theo FSD FS-08 (Mã `MSG-0805`):<br>`"Enter a mobile number in the correct format, like 9123 4567"`. |
| **Actual Result** | Hệ thống hiển thị chuỗi text kỹ thuật thô: `features.parentProfile.validation.mobileInvalid`. |
| **Attachment** | [`evidence_bug1_bug2_form_validation.png`](./evidence_bug1_bug2_form_validation.png) (Textbox Mobile Number kèm alert `features.parentProfile.validation.mobileInvalid`). |

---

### Bug #2 — Thiếu thông báo lỗi khi để trống các trường bắt buộc `Street` và `Country` trong Mailing Address

| Field Name | Specification / Value |
| :--- | :--- |
| **Project** | EduFAMS E-Service Portal |
| **Issue Type** | Bug |
| **Summary** | Mailing Address mandatory fields (`Street`, `Country`) do not show required field validation error (`MSG-0001`) when left blank |
| **Priority** | High |
| **Component** | My Profile (`Mailing Address` section) |
| **Affected Version** | Web Client SIT v1.0.0 (Port 5174) |
| **Fix Version** | Sprint 1 / Next Release |
| **Assignee** | Frontend Team / Unassigned |
| **Reviewer** | QA Team (`combo-qa`) |
| **Due Date** | 25-Oct-2026 |
| **Description** | Theo FSD FS-08 (Bảng quy định thuộc tính trường mục 5) và Test Case `TC-R8-103`: Các trường `Street`, `Postal code`, `Country`, `Mobile number`, `Email` là các trường **bắt buộc (Mandatory = Có)**; chỉ riêng `Block` và `Unit` là tùy chọn. Khi người dùng xóa rỗng `Street` hoặc `Country`, hệ thống hoàn toàn im lặng, không hiển thị bất kỳ cảnh báo lỗi validation inline nào dưới các ô nhập này. |
| **Steps to Reproduce** | 1. Truy cập `http://localhost:5174/profile` và nhấn **"Update details"**.<br>2. Xóa toàn bộ nội dung trong ô **"Street"** thành rỗng `""`.<br>3. Xóa toàn bộ nội dung trong ô **"Country"** thành rỗng `""`.<br>4. Nhấn nút **"Save changes"** hoặc blur ra ngoài form. |
| **Expected Result** | Hệ thống phải kích hoạt kiểm tra bắt buộc và hiển thị thông báo lỗi `MSG-0001` (hoặc thông báo inline yêu cầu nhập dữ liệu) dưới trường `Street` và `Country` tương tự như Email / Mobile. |
| **Actual Result** | Không có bất kỳ cảnh báo lỗi inline nào hiển thị dưới ô `Street` và `Country`. Hệ thống không phản hồi trực quan cho người dùng biết hai trường này đang vi phạm điều kiện bắt buộc. |
| **Attachment** | [`evidence_bug1_bug2_form_validation.png`](./evidence_bug1_bug2_form_validation.png) (Không có alert container dưới Street và Country). |

---

### Bug #3 — Nút hamburger "Open navigation" bị lỗi hiển thị / tương tác trên mobile responsive viewport

| Field Name | Specification / Value |
| :--- | :--- |
| **Project** | EduFAMS E-Service Portal |
| **Issue Type** | Bug |
| **Summary** | Mobile Navbar navigation drawer / dropdown does not expand properly when clicking "Open navigation" button at mobile viewports |
| **Priority** | Medium |
| **Component** | Header Navigation Bar (Responsive Layout) |
| **Affected Version** | Web Client SIT v1.0.0 (Port 5174) |
| **Fix Version** | Sprint 1 / UI Polish |
| **Assignee** | Frontend Team / UI/UX |
| **Reviewer** | QA Team (`combo-qa`) |
| **Due Date** | 27-Oct-2026 |
| **Description** | Khi co màn hình về kích thước thiết bị di động (Mobile Viewport 375x812 hoặc 498x669), thanh menu desktop được thu gọn thành nút icon hamburger `Open navigation`. Tuy nhiên, khi nhấp vào nút này, drawer / menu trượt điều hướng không mở ra hoặc bị che khuất / đè layout, dẫn đến người dùng trên thiết bị di động không thể truy cập các menu điều hướng chính (`Home`, `Transactions`, `FAS Application`, `Fees & Payments`). |
| **Steps to Reproduce** | 1. Mở trang `http://localhost:5174/profile` trên viewport màn hình điện thoại (chiều rộng <= 500px).<br>2. Quan sát header: Menu ngang bị ẩn, xuất hiện nút hamburger có `aria-label="Open navigation"`.<br>3. Nhấn vào nút **"Open navigation"** (`button[aria-label='Open navigation']`).<br>4. Quan sát phản hồi hiển thị của menu. |
| **Expected Result** | Menu điều hướng dạng drawer (hoặc accordion dropdown) phải bung mở mượt mà, hiển thị đầy đủ danh sách liên kết và cho phép người dùng chuyển trang hoặc đóng menu bằng phím `Esc`/nút đóng (tuân thủ `TC-R8-124` về khả năng sử dụng trên di động). |
| **Actual Result** | Menu không bung mở tương tác đúng chuẩn trên màn hình nhỏ; người dùng bị kẹt tại trang hiện tại và không thể điều hướng sang các phân hệ khác. |
| **Attachment** | [`evidence_bug3_mobile_navbar.png`](./evidence_bug3_mobile_navbar.png) (Nút hamburger hiện diện nhưng không mở được menu điều hướng). |
