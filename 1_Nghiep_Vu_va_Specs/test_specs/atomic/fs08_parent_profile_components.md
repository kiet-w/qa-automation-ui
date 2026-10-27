# Feature: FS-08 Parent Profile & Personal Details Management (Atomic UI Components)

> **Mô tả nghiệp vụ**: Kiểm thử UI Unit Test cho từng ĐƠN COMPONENT độc lập trên màn hình Thông tin Phụ huynh (`http://localhost:5174/profile`).  
> **Căn cứ đặc tả & truy vết**:
> - Tài liệu FSD: `specs/md/FS document/FS-08_Parent_Portal_SingPass_Profile.md` (FR-08.3 Cập nhật thông tin cá nhân cơ bản)
> - Quy định nghiệp vụ: `BR-08-01.4` (Dữ liệu SingPass chỉ đọc), `BR-08-09.1` (Validate SĐT & Email)
> - Tiêu chí nghiệm thu: `AC #14` (Sửa thông tin), `AC #15` (Bắt lỗi định dạng), `AC #16` (Bắt buộc), `AC #18` (Residential address chỉ đọc)
> - Quyết định nghiệp vụ đã chốt: `D-20` (Residential Address chỉ đọc từ Singpass), `D-28` (Không gửi email khi sửa thông tin)
> - Bảng mã lỗi FSD Phụ lục B: `MSG-0805` (Format phone), `MSG-0806` (Format email), `MSG-0001` (Bỏ trống trường bắt buộc)

---

## 🔍 Locators đã xác minh qua BSK (Browser-Skill Reconnaissance)
| Tên Phần Tử | Nhãn Hiển Thị | Selector / ID Thực Tế | Loại Phần Tử |
| :--- | :--- | :--- | :--- |
| Ngôn ngữ | English / Vietnamese | `select` | `<select>` |
| Nút Đăng xuất | Log out | `button:has-text("Log out")` | `<button type="button">` |
| Mobile Menu | ☰ | `button:has-text("☰")` | `<button type="button">` |
| Hiện NRIC | Show NRIC | `button:has-text("Show NRIC")` | `<button type="button">` |
| Ẩn NRIC | Hide NRIC | `button:has-text("Hide NRIC")` | `<button type="button">` |
| Nút Cập nhật | Update details | `button:has-text("Update details")` | `<button type="button">` |
| Ô nhập SĐT | Mobile Number * | `input[name="phoneNumber"]` | `<input type="tel">` |
| Ô nhập Email | Email Address * | `input[name="email"]` | `<input type="email">` |
| Ô nhập Block | Block | `input[name="mailingBlock"]` | `<input>` |
| Ô nhập Street | Street | `input[name="mailingStreet"]` | `<input>` |
| Ô nhập Unit | Unit | `input[name="mailingUnit"]` | `<input>` |
| Ô nhập Mã bưu chính | Postal code | `input[name="mailingPostalCode"]` | `<input>` |
| Ô nhập Quốc gia | Country | `input[name="mailingCountry"]` | `<input>` |
| Nút Lưu | Save changes | `button:has-text("Save changes")` | `<button type="submit">` |
| Nút Hủy | Cancel | `button:has-text("Cancel")` | `<button type="button">` |

---

## Scenario: TC-ATM-FS08-01 Singpass Identity Component Read-Only Verification @smoke @p0 @atomic
- Open: http://localhost:5174/profile
- Assert: "SINGPASS VERIFIED IDENTITY (READ-ONLY)" is visible
- Assert: "Residential address is maintained via Government Digital Services and cannot be edited in this portal." is visible
- Assert: "NGUYEN VAN MINH" is visible
- Assert: input[name="fullName"] is not visible
- Assert: input[name="residentialAddress"] is not visible

## Scenario: TC-ATM-FS08-02 NRIC Masking and Reveal Toggle Button Component @smoke @p0 @atomic
- Open: http://localhost:5174/profile
- Assert: button:has-text("Show NRIC") is visible
- Click: button:has-text("Show NRIC")
- Assert: button:has-text("Hide NRIC") is visible
- Click: button:has-text("Hide NRIC")
- Assert: button:has-text("Show NRIC") is visible

## Scenario: TC-ATM-FS08-03 Mode Transition Buttons Component (Update Details and Cancel) @p0 @atomic
- Open: http://localhost:5174/profile
- Click: button:has-text("Update details")
- Assert: input[name="phoneNumber"] is visible
- Assert: input[name="email"] is visible
- Click: button:has-text("Cancel")
- Assert: button:has-text("Update details") is visible

## Scenario: TC-ATM-FS08-04 Save Changes Button Pristine and Dirty State Gatekeeper @p1 @atomic
- Open: http://localhost:5174/profile
- Click: button:has-text("Update details")
- Assert: button:has-text("Save changes") is disabled
- Assert: "Make a change to enable saving." is visible

## Scenario: TC-ATM-FS08-05 Mobile Number Component Valid Singapore Format @smoke @p0 @atomic
- Open: http://localhost:5174/profile
- Click: button:has-text("Update details")
- Fill: input[name="phoneNumber"] with "98765432"
- Assert: button:has-text("Save changes") is enabled

## Scenario: TC-ATM-FS08-06 Mobile Number Component Empty Validation State @p1 @atomic
- Open: http://localhost:5174/profile
- Click: button:has-text("Update details")
- Fill: input[name="phoneNumber"] with ""
- Assert: button:has-text("Save changes") is disabled

## Scenario: TC-ATM-FS08-07 Email Address Component RFC 5322 Format Validation Error @p0 @atomic
- Open: http://localhost:5174/profile
- Click: button:has-text("Update details")
- Fill: input[name="email"] with "invalid-email-address"
- Click: button:has-text("Save changes")
- Assert: "Enter a valid email address." is visible

## Scenario: TC-ATM-FS08-08 Mailing Address Sub-Components Visibility and Constraints @p1 @atomic
| Step | Action | Target / Selector | Value | Expected / Assertion |
| :--- | :--- | :--- | :--- | :--- |
| 1 | open | http://localhost:5174/profile | | Mở trang hồ sơ phụ huynh |
| 2 | click | button:has-text("Update details") | | Chuyển sang Edit Mode |
| 3 | assert_visible | input[name="mailingBlock"] | | Ô Block hiển thị |
| 4 | assert_visible | input[name="mailingStreet"] | | Ô Street hiển thị |
| 5 | assert_visible | input[name="mailingUnit"] | | Ô Unit hiển thị |
| 6 | assert_visible | input[name="mailingPostalCode"] | | Ô Postal code hiển thị |
| 7 | assert_visible | input[name="mailingCountry"] | | Ô Country hiển thị |
| 8 | click | button:has-text("Cancel") | | Thoát Edit Mode |

## Scenario: TC-ATM-FS08-09 UI Technical Health and Layout Integrity Non-Functional Check @p0 @atomic
- Open: http://localhost:5174/profile
- Assert: Title contains "EduFAMS"
- Assert: "My Profile" is visible
- Assert: no_console_errors
- Assert: no_overflow
