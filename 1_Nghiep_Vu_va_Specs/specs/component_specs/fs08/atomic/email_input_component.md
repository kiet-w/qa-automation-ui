# Component Specification: Email Input (Parent Profile)

## 1. Metadata & Selector

| Attribute | Specification |
| :--- | :--- |
| **Component Name** | `EmailInputComponent` |
| **Target Page / Route** | `/profile` (`ParentProfilePage` Edit Mode) |
| **Element Hierarchy** | Form field wrapper `<div>`, Label `<label>`, Input `<input>`, Error message `<p>` |
| **Input Tag** | `<input name="email" type="email" autocomplete="email" maxlength="150">` |
| **Visual State** | Edit Mode (kích hoạt sau khi bấm "Update details") |
| **Component Scope** | Nhập địa chỉ thư điện tử nhận thông báo liên quan đến hồ sơ |

### Playwright Live DOM Locators
```python
# Extracted from pages/fs08/parent_profile_page.py
INPUT_EMAIL = "input[name='email']"
EMAIL_LABEL = "label[for='email'], label:has-text('Email')"
FIELD_ERROR_LOCATOR = "input[name='email'] ~ p[role='alert'], input[name='email'] ~ p[class*='error']"
SAVE_CHANGES_BTN = "button:has-text('Save changes')"
```

---

## 2. Business Rules & Acceptance Criteria Traceability

| ID | Type | Description | Source Reference |
| :--- | :--- | :--- | :--- |
| **BR-08-02** | Business Rule | Parent can update their email address independently of other guardians. | `specs/md/FS document/FS-08_Parent_Portal_SingPass_Profile.md` |
| **BR-08-04** | Business Rule | **No Notification Email**: Do not send an email notification when contact details or mailing address are updated (per Architecture Decision D-28). | `specs/md/MEETINGS_AND_DECISIONS_SUMMARY.md` |
| **R8-AC11** | Acceptance Criteria | In Edit mode, Email is an editable text field. | `specs/md/Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md` |
| **R8-AC13** | Acceptance Criteria | Validate email format (RFC 5322) and maximum length of 150 characters. | `specs/md/Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md` |
| **MSG-0001** | System Message | Blank error message: *"Enter your email"*. | `specs/validation_rules/md/FS08_R8_Profile_Validation_Rule.md` |
| **MSG-0806** | System Message | Invalid format error message: *"Enter an email address in the correct format, like name@example.com"*. | `specs/validation_rules/md/FS08_R8_Profile_Validation_Rule.md` |

---

## 3. Ma trận 12 lớp Validation & UI Integrity

| Lớp (Layer) | Phân Loại Kiểm Thử | Dữ Liệu Đầu Vào (Input Vector) | Trạng Thái / Hành Vi UI Kỳ Vọng | Tiêu Chí Đạt (Pass Criteria) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Empty Required** | Để trống trường bắt buộc | `""` (xóa trắng ô email) | Kích hoạt lỗi bắt buộc `MSG-0001`. Ô có viền đỏ, cờ `aria-invalid="true"`. Chặn submit. | Thông báo: *"Enter your email"*. |
| **2. All Whitespace** | Toàn khoảng trắng (ASM-15) | `"               "` (15 spaces) | Tự động trim, coi như rỗng, kích hoạt lỗi `MSG-0001`. | Thông báo: *"Enter your email"*. |
| **3. Leading/Trailing Spaces** | Khoảng trắng đầu / cuối | `"  user@example.com  "` | Tự động trim trước khi gửi hoặc validate, không báo lỗi định dạng sai. | Chuẩn hóa thành `"user@example.com"`. |
| **4. BVA 149 Chars** | Độ dài biên dưới $Max-1$ | `"a"*137 + "@example.com"` (149 chars) | Hợp lệ, chấp nhận lưu, không báo lỗi độ dài. | Form hợp lệ, lưu thành công. |
| **5. BVA 150 Chars** | Đúng độ dài tối đa $Max$ | `"a"*138 + "@example.com"` (150 chars) | Hợp lệ, chấp nhận lưu thành công. | Form hợp lệ, không lỗi. |
| **6. BVA 151 Chars** | Vượt độ dài tối đa $Max+1$ | `"a"*139 + "@example.com"` (151 chars) | Bị chặn bởi `maxlength="150"` hoặc báo lỗi `MSG-0806`. | Ký tự 151 bị cắt hoặc kích hoạt `MSG-0806`. |
| **7. Missing @ or Domain** | Cú pháp thiếu thành phần | `"userexample.com"`, `"user@"`, `"@example.com"` | Kích hoạt lỗi cú pháp `MSG-0806`. Ô có viền đỏ, cờ `aria-invalid="true"`. | Thông báo: *"Enter an email address in the correct format, like name@example.com"*. |
| **8. Double @ or Invalid TLD** | Ký tự không hợp lệ | `"user@@example.com"`, `"user@com"`, `"user@domain..com"` | Kích hoạt lỗi cú pháp `MSG-0806`. | Thông báo: *"Enter an email address in the correct format, like name@example.com"*. |
| **9. Valid Special Patterns** | Ký tự mở rộng hợp lệ | `"user.name+tag@sub.domain.edu.sg"` | Chấp nhận hợp lệ theo chuẩn RFC 5322. | Không có thông báo lỗi. |
| **10. Security / XSS / SQLi** | Vector tấn công tiêm mã | `<script>alert(1)</script>@evil.com`, `' OR 1=1 --@test.com` | Xử lý an toàn dưới dạng text literal, từ chối hoặc mã hóa an toàn. | Báo lỗi `MSG-0806`, không thực thi script. |
| **11. i18n Leak & Visual Feedback** | Chống rò rỉ translation key | Mọi trường hợp email sai | ⛔ CẤM hiển thị `features.parentProfile.validation.emailInvalid`. Viền đỏ rõ nét, tự động biến mất khi sửa đúng. | Error text tự nhiên; `aria-invalid="false"` khi sửa đúng. |
| **12. Case Insensitivity & Reload** | Bảo toàn và chữ thường | Nhập `"User.Test@Domain.COM"`, Save -> Reload | Hệ thống chuẩn hóa lưu trữ an toàn, reload giữ nguyên email sau cập nhật. | Dữ liệu hiển thị chuẩn xác sau F5. |

---

## 4. Error Handling & Visual Feedback

| Tình Huống Kích Hoạt | Mã Lỗi Chuẩn | Nội Dung Thông Báo Bắt Buộc | Trạng Thái DOM & Style |
| :--- | :--- | :--- | :--- |
| Để trống hoặc chỉ có khoảng trắng | `MSG-0001` | *"Enter your email"* | `aria-invalid="true"`, `class*="error"`, viền đỏ hiển thị dưới ô input. |
| Sai cú pháp RFC 5322 (thiếu @, thiếu domain) | `MSG-0806` | *"Enter an email address in the correct format, like name@example.com"* | `aria-invalid="true"`, `class*="error"`, viền đỏ. |
| Độ dài vượt quá 150 ký tự | `MSG-0806` | *"Enter an email address in the correct format, like name@example.com"* | `aria-invalid="true"`, `class*="error"`, viền đỏ. |
| Sửa lại email hợp lệ | N/A | Tự động xóa thông báo lỗi (Auto-dismissed) | `aria-invalid="false"`, xóa bỏ class lỗi, viền trở lại màu trung tính. |

---

## 5. JSON Fixtures Data Payload

```json
{
  "email_input_fixtures": {
    "valid_cases": [
      { "id": "EML-VAL-01", "input": "tan.wei.ming@example.com", "description": "Standard email" },
      { "id": "EML-VAL-02", "input": "chloe.chan+school@sub.moe.edu.sg", "description": "Subdomain and plus tagging" },
      { "id": "EML-VAL-03", "input": "user_name.123@domain-co.com", "description": "Alphanumeric with dots and hyphens" },
      { "id": "EML-VAL-04", "input": "  trimmed.user@example.com  ", "description": "Email with leading/trailing spaces" }
    ],
    "boundary_cases": {
      "bva_149": "a78901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567@example.com",
      "bva_150": "ab78901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567@example.com",
      "bva_151": "abc78901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567@example.com"
    },
    "empty_cases": [
      { "id": "EML-EMP-01", "input": "", "expected_code": "MSG-0001", "expected_msg": "Enter your email" },
      { "id": "EML-EMP-02", "input": "        ", "expected_code": "MSG-0001", "expected_msg": "Enter your email" }
    ],
    "invalid_format_cases": [
      { "id": "EML-INV-01", "input": "plainaddress", "expected_code": "MSG-0806" },
      { "id": "EML-INV-02", "input": "@missingusername.com", "expected_code": "MSG-0806" },
      { "id": "EML-INV-03", "input": "user@.com.sg", "expected_code": "MSG-0806" },
      { "id": "EML-INV-04", "input": "user@example..com", "expected_code": "MSG-0806" },
      { "id": "EML-INV-05", "input": "user@@example.com", "expected_code": "MSG-0806" }
    ],
    "security_cases": [
      { "id": "EML-SEC-01", "input": "<script>alert(1)</script>@test.com", "expected_code": "MSG-0806" },
      { "id": "EML-SEC-02", "input": "' OR '1'='1' --@test.com", "expected_code": "MSG-0806" }
    ]
  }
}
```
