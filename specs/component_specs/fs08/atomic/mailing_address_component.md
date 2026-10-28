# Component Specification: Mailing Address Fields (Parent Profile)

## 1. Metadata & Selector

| Attribute | Specification |
| :--- | :--- |
| **Component Name** | `MailingAddressComponent` |
| **Target Page / Route** | `/profile` (`ParentProfilePage` Edit Mode) |
| **Element Hierarchy** | Form grid container `<div>`, Field groups `<div>`, Labels `<label>`, Inputs `<input>` |
| **Visual State** | Edit Mode (kích hoạt sau khi bấm "Update details") |
| **Component Scope** | Cụm trường địa chỉ gửi thư thay thế: Block, Street, Unit, Postal Code, Country |

### Playwright Live DOM Locators
```python
# Extracted from pages/fs08/parent_profile_page.py
INPUT_BLOCK = "input[name='mailingBlock']"
INPUT_STREET = "input[name='mailingStreet']"
INPUT_UNIT = "input[name='mailingUnit']"
INPUT_POSTAL = "input[name='mailingPostalCode']"
INPUT_COUNTRY = "input[name='mailingCountry']"

BLOCK_LABEL = "label[for='mailingBlock'], label:has-text('Block')"
STREET_LABEL = "label[for='mailingStreet'], label:has-text('Street')"
UNIT_LABEL = "label[for='mailingUnit'], label:has-text('Unit')"
POSTAL_LABEL = "label[for='mailingPostalCode'], label:has-text('Postal code')"
COUNTRY_LABEL = "label[for='mailingCountry'], label:has-text('Country')"
```

---

## 2. Business Rules & Acceptance Criteria Traceability

| ID | Type | Description | Source Reference |
| :--- | :--- | :--- | :--- |
| **BR-08-02** | Business Rule | Parent can specify an alternative Mailing Address for official correspondence. | `specs/md/FS document/FS-08_Parent_Portal_SingPass_Profile.md` |
| **D-20** | Architecture Decision | Singpass residential address is immutable; only mailing address can be customized. | `specs/md/MEETINGS_AND_DECISIONS_SUMMARY.md` |
| **R8-AC11** | Acceptance Criteria | In Edit mode, fields for Block, Street, Unit, Postal Code, and Country are rendered. | `specs/md/Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md` |
| **R8-AC15** | Acceptance Criteria | Validate required status: Street, Postal Code, and Country are required; Block and Unit are optional. | `specs/md/Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md` |
| **MSG-0001** | System Message | Blank required field error: *"Enter your <field>"* (e.g. *"Enter your mailing street"*). | `specs/validation_rules/md/FS08_R8_Profile_Validation_Rule.md` |

---

## 3. Ma trận 12 lớp Validation & UI Integrity Theo Từng Ô Địa Chỉ

### 3.1 Mailing Street (Bắt buộc, Tối đa 100 ký tự)
- **Empty / Whitespace (ASM-15)**: Nhập rỗng hoặc `"   "` -> Lỗi `MSG-0001`: *"Enter your mailing street"*.
- **BVA Max (99, 100, 101)**: 99 và 100 ký tự hợp lệ; 101 ký tự bị chặn bởi `maxlength="100"` hoặc báo lỗi vượt quá 100 ký tự.
- **Ký tự chấp nhận**: Chữ, số, ký tự địa chỉ thường gặp (`.`, `,`, `-`, `/`, `'`) như `"JURONG EAST STREET 21"`, `"ST. GEORGE'S ROAD"`.

### 3.2 Mailing Postal Code (Bắt buộc, Đúng 6 chữ số)
- **Empty / Whitespace**: Nhập rỗng hoặc khoảng trắng -> Lỗi `MSG-0001`: *"Enter your mailing postal code"*.
- **BVA Min/Max (5, 6, 7 chữ số)**:
  - 5 chữ số (`"60021"`): Báo lỗi không hợp lệ: *"Enter a valid 6-digit postal code."*
  - 6 chữ số (`"600210"`, `"018956"`): Hợp lệ (bảo toàn số 0 đứng đầu).
  - 7 chữ số (`"6002100"`): Bị chặn hoặc báo lỗi không hợp lệ.
- **Lẫn chữ hoặc ký tự**: `"60021A"`, `"600-210"` -> Bị từ chối.

### 3.3 Mailing Country (Bắt buộc, Tối đa 100 ký tự)
- **Empty / Whitespace**: Nhập rỗng -> Lỗi `MSG-0001`: *"Enter your mailing country"*.
- **BVA Max**: 100 ký tự hợp lệ; 101 ký tự bị từ chối hoặc chặn.
- **Mặc định**: `"SINGAPORE"`.

### 3.4 Mailing Block (Tùy chọn, Tối đa 20 ký tự)
- **Empty**: Để trống -> Hợp lệ (Cho phép lưu).
- **BVA Max (20, 21)**: 20 ký tự hợp lệ (ví dụ: `"Blk 123A"` hoặc `"12345678901234567890"`); 21 ký tự bị chặn bởi `maxlength="20"`.

### 3.5 Mailing Unit (Tùy chọn, Tối đa 20 ký tự)
- **Empty**: Để trống -> Hợp lệ.
- **Format Singapore**: Hỗ trợ định dạng `#05-12`, `#12-34A`, `Level 3`.
- **BVA Max (20, 21)**: 20 ký tự hợp lệ; 21 ký tự bị chặn bởi `maxlength="20"`.

### Bảng Tổng Hợp 12 Lớp Kiểm Thử Cho Toàn Cụm Mailing Address:
| Lớp (Layer) | Phân Loại | Kịch Bản & Input Vector | Trạng Thái UI Kỳ Vọng | Tiêu Chí Đạt |
| :--- | :--- | :--- | :--- | :--- |
| **1. Required Empty** | Bắt buộc để trống | Để trống Street, Postal Code, Country | Hiển thị 3 lỗi riêng biệt bên dưới từng trường: `MSG-0001`. | Cả 3 ô đều có viền đỏ. |
| **2. Optional Empty** | Tùy chọn để trống | Block="", Unit="" | Form hợp lệ, cho phép Save thành công. | Không sinh lỗi cho Block/Unit. |
| **3. Whitespace Trim** | Khoảng trắng toàn phần | Nhập `"   "` vào Postal Code | Trim sạch -> Kích hoạt `MSG-0001` cho Postal Code. | Báo lỗi bắt buộc. |
| **4. Leading Zeros** | Bảo toàn số 0 | Postal Code = `"018956"` | Lưu chính xác `"018956"`, không ép kiểu mất số 0 thành `18956`. | Reload hiển thị đủ 6 số. |
| **5. BVA Postal Code** | Biên độ dài Postal | 5 số vs 6 số vs 7 số | Chỉ chấp nhận đúng 6 số. | 5 số hoặc 7 số bật `aria-invalid`. |
| **6. BVA Street/Country**| Biên độ dài tối đa | Street: 100 vs 101 ký tự | 100 ký tự lưu thành công; 101 bị chặn. | Form an toàn, không tràn. |
| **7. BVA Block/Unit** | Biên độ dài tối đa | Block/Unit: 20 vs 21 ký tự | 20 ký tự hợp lệ; 21 bị chặn. | `maxlength="20"` hoạt động. |
| **8. Singapore Unit Hash**| Ký tự đặc biệt Unit | `"#05-12"`, `"#12-34A"` | Chấp nhận ký tự `#`, `-`. | Lưu thành công. |
| **9. Forbidden Symbols** | Ký tự cấm | `< > { } ;` trong địa chỉ | Bị từ chối hoặc mã hóa an toàn, không phá vỡ DOM. | An toàn, không vỡ UI. |
| **10. XSS Injection** | Bảo mật tiêm mã | `<script>alert(1)</script>` | Hiển thị dạng chuỗi plain text, không thực thi script. | Sanitized hoàn toàn. |
| **11. i18n & Feedback** | Chống rò rỉ raw key | Mọi trường hợp lỗi địa chỉ | ⛔ Không hiển thị raw key `features.parentProfile.*`. | Error text tự nhiên. |
| **12. Multi-line Paste** | Dán nhiều dòng | Dán địa chỉ 3 dòng có ký tự xuống dòng | Tự động loại bỏ newline hoặc chuẩn hóa thành 1 dòng. | Không làm gãy giao diện. |

---

## 4. Error Handling & Visual Feedback

| Trường | Tình Huống Kích Hoạt | Mã Lỗi Chuẩn | Nội Dung Thông Báo Bắt Buộc | Trạng Thái DOM |
| :--- | :--- | :--- | :--- | :--- |
| `mailingStreet` | Để trống | `MSG-0001` | *"Enter your mailing street"* | `aria-invalid="true"`, viền đỏ |
| `mailingPostalCode` | Để trống | `MSG-0001` | *"Enter your mailing postal code"* | `aria-invalid="true"`, viền đỏ |
| `mailingPostalCode` | Khác 6 chữ số / lẫn chữ | Format Error | *"Enter a valid 6-digit postal code."* | `aria-invalid="true"`, viền đỏ |
| `mailingCountry` | Để trống | `MSG-0001` | *"Enter your mailing country"* | `aria-invalid="true"`, viền đỏ |
| `mailingBlock` | Vượt quá 20 ký tự | Length Error | *"Enter no more than 20 characters."* | `aria-invalid="true"`, viền đỏ |
| `mailingUnit` | Vượt quá 20 ký tự | Length Error | *"Enter no more than 20 characters."* | `aria-invalid="true"`, viền đỏ |

---

## 5. JSON Fixtures Data Payload

```json
{
  "mailing_address_fixtures": {
    "valid_full_payload": {
      "mailingBlock": "210",
      "mailingStreet": "JURONG EAST STREET 21",
      "mailingUnit": "05-12",
      "mailingPostalCode": "600210",
      "mailingCountry": "SINGAPORE"
    },
    "valid_minimal_optional_blank": {
      "mailingBlock": "",
      "mailingStreet": "ORCHARD BOULEVARD",
      "mailingUnit": "",
      "mailingPostalCode": "248641",
      "mailingCountry": "SINGAPORE"
    },
    "leading_zero_postal": {
      "mailingBlock": "1",
      "mailingStreet": "RAFFLES LINK",
      "mailingUnit": "#02-01",
      "mailingPostalCode": "039393",
      "mailingCountry": "SINGAPORE"
    },
    "boundary_max_lengths": {
      "block_20": "BLOCK 1234567890ABCD",
      "street_100": "A very long street name that reaches exactly one hundred characters in total length for testing 1234",
      "unit_20": "UNIT #12-34567890ABC",
      "country_100": "REPUBLIC OF SINGAPORE OFFICIAL MAILING JURISDICTION ZONE A1 TESTING BOUNDARY REACHING 100 CHARACTERS"
    },
    "invalid_cases": {
      "postal_5_digits": "60021",
      "postal_letters": "60021A",
      "street_empty": "",
      "country_empty": ""
    }
  }
}
```
