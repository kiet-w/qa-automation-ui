# Component Specification: Applicant Details - Part 1 (`f05-applicant-details`)

> **Module**: `f05` - FAS Paper Applications (Đơn giấy / Hardcopy Applications Offline)  
> **Component**: `applicant_details` (Review Application Screen - Part 1: Applicant)  
> **Source Spec**: `specs/md/FS document/FS-05_Hardcopy_Applications_Offline.md` (Mục 5, Mục 6 VR-F5-01, Mục 9 BR3, BR4) & `specs/validation_rules/md/R5_FAS_APPLICATION_Validation_Rules.md` (Màn C: C5 - C15, Màn D: VR-F5-01)  
> **Target Audience**: School User (School Admin)  

---

## 1. Metadata & Selector

- **Route URL / Access Path**: Admin Portal $\rightarrow$ Financial assistance $\rightarrow$ Upload applications $\rightarrow$ Review application (`/admin/fas/paper-applications/review/:id` or `#part-1-applicant`)
- **Container Element Tag**: `<fieldset id="part-1-applicant" data-testid="section-part-1-applicant" aria-labelledby="heading-part-1">`
- **Playwright Locators (BSK Standardized Convention)**:

| Element Name | HTML Tag / Type | Playwright Locator (BSK Convention) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Section Header** | `h3` | `page.locator("h3:has-text('Part 1 · Applicant')")` | Section 1 Title |
| **Applicant NRIC/FIN Input** | `input[type="text"]` | `page.locator("input[data-testid='input-applicant-nric'], input[name='applicant_nric']")` | Field C5; triggers auto-fill on blur/enter |
| **Applicant Full Name** | `input[type="text"]` | `page.locator("input[data-testid='input-applicant-fullname'], input[name='applicant_fullname']")` | Field C6; locked (`disabled="true"` / `readonly`) |
| **Applicant Date of Birth** | `input[type="text"]` | `page.locator("input[data-testid='input-applicant-dob'], input[name='applicant_dob']")` | Field C7; locked (`DD/MM/YYYY`) |
| **Applicant Gender** | `select` | `page.locator("select[data-testid='select-applicant-gender'], select[name='applicant_gender']")` | Field C8; options: Male, Female, Other |
| **Applicant Category** | `select` | `page.locator("select[data-testid='select-applicant-category'], select[name='applicant_category']")` | Field C9; SC, PR, ASEAN, Non-ASEAN |
| **Applicant Nationality/Race** | `select` | `page.locator("select[data-testid='select-applicant-nationality'], select[name='applicant_nationality']")` | Field C10; Chinese, Malay, Indian, Eurasian, Others |
| **Relationship to Child** | `select` | `page.locator("select[data-testid='select-applicant-relationship'], select[name='applicant_relationship']")` | Field C11; Father, Mother, Legal guardian, etc. |
| **Phone Number Input** | `input[type="tel"]` | `page.locator("input[data-testid='input-applicant-phone'], input[name='applicant_phone']")` | Field C12; digits only, max 10 digits |
| **Email Address Input** | `input[type="email"]` | `page.locator("input[data-testid='input-applicant-email'], input[name='applicant_email']")` | Field C13; RFC 5322 format, max 150 chars |
| **Residential Address** | `textarea / input` | `page.locator("textarea[data-testid='input-applicant-address'], textarea[name='applicant_address']")` | Field C14; max 255 chars |
| **Consider for SBFAS Checkbox** | `input[type="checkbox"]` | `page.locator("input[data-testid='cb-applicant-sbfas'], input[name='applicant_consider_sbfas']")` | Field C15; default checked (Yes) |
| **Confidence Highlight Badge** | `span.ocr-confidence` | `page.locator("span[data-testid^='ocr-uncertain-tag-']")` | Yellow highlight badge (`bg-yellow-100`) for low-confidence OCR fields |

---

## 2. BR / AC Traceability

- **Functional Requirements**: `FS-05` Section 2 Steps 2-3, Section 5 Part 1, Section 6 (Validation Rules), Section 9 (BR1, BR3, BR4).
- **Business Rules (BR)**:
  - `BR-05-03`: Khi nhập NRIC của người khai, họ tên, ngày sinh, giới tính, category, nationality, số điện thoại, email và địa chỉ được điền tự động từ hồ sơ phụ huynh và dữ liệu Chính phủ rồi khóa lại.
  - `BR-05-REL-01`: Quan hệ với con (`Relationship to child`) là trường bắt buộc, lấy từ đơn giấy hoặc do School Admin chọn theo khai báo phụ huynh.
  - `BR-05-SBFAS-01`: Trường "School-based FAS" đại diện cho "Also consider for SBFAS", mặc định là `Yes` (`checked = true`).
  - `VR-F5-01`: Thiếu bất kỳ trường bắt buộc nào trong Part 1 sẽ kích hoạt cảnh báo chặn `Complete: {danh sách trường thiếu}.` khi bấm `Review and submit`.
- **User Story Traceability**: `US-F5-02` (Xác nhận thông tin phụ huynh / người khai đơn giấy từ dữ liệu định danh).
- **Access Control (RBAC)**: Chỉ School User của trường học sinh đang theo học được quyền nhập và xem.

---

## 3. Ma trận 12 lớp Validation

| Lớp Kiểm Thử (12 Tầng) | Điều Kiện / Dữ Liệu Đầu Vào | Kỳ Vọng Giao Diện & Hành Vi Hệ Thống | Mã Lỗi / Phản Hồi Trực Quan |
| :--- | :--- | :--- | :--- |
| **1. Empty / Required** | Bỏ trống NRIC, Relationship, Phone, Email hoặc Address khi bấm `Review and submit`. | Bị chặn mở dialog Review; hiện thanh alert màu đỏ ở đầu trang liệt kê các trường thiếu. Input thiếu có `aria-invalid="true"` và viền đỏ `#D9383A`. | `Complete: Applicant NRIC, Relationship to child, Phone number (up to 10 digits), Email, Address.` |
| **2. Whitespace / Trim** | Nhập khoảng trắng đầu/cuối vào ô NRIC (ví dụ `" S1234567D "`) hoặc Phone (`" 91234567 "`). | Tự động trim khoảng trắng đầu/cuối trước khi gửi request và lưu vào CSDL. Nếu toàn khoảng trắng coi như rỗng. | Trường hợp rỗng: Báo lỗi `Complete: ...` |
| **3. BVA Phone Number** | • 7 chữ số (Min - 1)<br>• 8 chữ số (Chuẩn SG)<br>• 10 chữ số (Max boundary)<br>• 11 chữ số (Max + 1) | • 8 và 10 chữ số: Hợp lệ.<br>• Nhỏ hơn 8 chữ số hoặc lớn hơn 10 chữ số: Bị chặn. Chặn ký tự chữ hoặc dấu cách. | `Complete: Phone number (up to 10 digits).` hoặc `MSG-0805` |
| **4. BVA Email Address** | • Rỗng: Thiếu trường.<br>• 150 ký tự chuẩn email: Hợp lệ.<br>• 151 ký tự: Vượt giới hạn, chặn. | Trường email tuân thủ RFC 5322; tối đa 150 ký tự. | `Complete: Email.` hoặc `MSG-0806` |
| **5. NRIC/FIN Checksum** | Nhập NRIC sai cấu trúc (ví dụ: `12345678A`, `S1234567`, `A1234567B`, sai chữ cái kiểm tra). | Bị từ chối, không tra cứu được hồ sơ phụ huynh. | Báo lỗi không hợp lệ; trường bị viền đỏ. |
| **6. XSS / Script Injection** | Nhập payload vào Address: `<script>alert('xss')</script>`, `<b onmouseover=alert(1)>`, `'; DROP TABLE;`. | Text được escape an toàn khi render sang HTML, lưu dạng raw Unicode text trong DB; không execute script. | Render an toàn dạng chuỗi ký tự. |
| **7. Cross-Field Auto-Fill** | Nhập NRIC hợp lệ của phụ huynh đã có trong Gov/MyInfo dataset (ví dụ `S1234567A`). | Tự động điền Full Name, DOB, Gender, Category, Nationality; các trường này chuyển sang trạng thái disabled/locked (nền xám). | Trường hiển thị nền xám `#F3F4F6`, icon ổ khóa `🔒`. |
| **8. Duplicate NRIC Check** | Nhập NRIC người khai trùng với NRIC của con (Part 2) hoặc thành viên gia đình (Part 3). | Bị chặn khi bấm `Review and submit` với thông báo trùng lặp cụ thể. | `The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN.` |
| **9. Extended Controls (Dropdowns)** | Click chọn `Relationship to child` trong dropdown: Father, Mother, Legal guardian, Grandfather, Grandmother, Sibling, Uncle, Aunt, Cousin, Other. | Giá trị được ghi nhận chính xác; nếu chọn `Other` hoặc người giám hộ không phải cha/mẹ, không ảnh hưởng quyền nộp đơn. | Giá trị hiển thị đúng nhãn. |
| **10. UI Health & Highlight OCR** | Ô nhập liệu có độ tin cậy OCR thấp (`confidence < 0.85`). | Phần tử được bao viền vàng nhạt (`bg-yellow-100 border-yellow-400`) để nhắc School Admin xác minh lại với bản scan bên trái. | Highlight vàng cảnh báo. |
| **11. Pristine / Dirty States** | Thay đổi số điện thoại hoặc email so với giá trị ban đầu. | Kích hoạt cờ dirty form, nút `Save draft` sáng bật; nút `Discard` kích hoạt hộp thoại xác nhận hủy bỏ. | State chuyển sang dirty. |
| **12. Security & PII Protection** | NRIC hiển thị trên màn hình Review hoặc View application. | NRIC được hiển thị đầy đủ cho School Admin trong phiên nhập liệu hợp lệ, nhưng truyền qua HTTPS an toàn và không log thô vào client console. | Tuân thủ Invariant 7 về PII protection. |

---

## 4. Error Handling & Visual Feedback

- **Standard Messages**:
  - Thiếu trường bắt buộc: `"Complete: {danh sách trường thiếu}."` (Ví dụ: `"Complete: Applicant NRIC, Relationship to child, Phone number (up to 10 digits), Email, Address."`)
  - Trùng lặp NRIC: `"The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN."`
  - Sai định dạng điện thoại: `"Enter a mobile number in the correct format, like 9123 4567"` (`MSG-0805`)
  - Sai định dạng email: `"Enter an email address in the correct format, like name@example.com"` (`MSG-0806`)
- **Visual Cues**:
  - Ghi chú đỏ ở đầu trang (`div.bg-red-50.border-red-500.text-red-700`) cuộn lên đầu màn hình khi có lỗi.
  - Ô nhập liệu lỗi có thuộc tính `aria-invalid="true"` và viền đỏ `border-red-600`.

---

## 5. JSON Fixtures Data Payload

```json
{
  "valid_applicant_payload": {
    "applicantNric": "S7512345Z",
    "fullName": "Tan Ah Seng",
    "dateOfBirth": "12/05/1975",
    "gender": "Male",
    "category": "Singapore Citizen",
    "nationality": "Chinese",
    "relationshipToChild": "Father",
    "phone": "91234567",
    "email": "ahseng.tan@example.com",
    "address": "Blk 123 Ang Mo Kio Ave 4 #08-12, Singapore 560123",
    "alsoConsiderSbfas": true
  },
  "bva_phone_boundary_10_digits": {
    "applicantNric": "S8012345B",
    "relationshipToChild": "Mother",
    "phone": "6591234567",
    "email": "valid.boundary@domain.org",
    "address": "Blk 456 Jurong West St 42 #05-88, Singapore 640456",
    "alsoConsiderSbfas": false
  },
  "invalid_missing_fields_payload": {
    "applicantNric": "",
    "relationshipToChild": "",
    "phone": "",
    "email": "",
    "address": "",
    "expectedErrorString": "Complete: Applicant NRIC, Relationship to child, Phone number (up to 10 digits), Email, Address."
  },
  "duplicate_nric_payload": {
    "applicantNric": "T0812345A",
    "relationshipToChild": "Father",
    "conflictingChildNric": "T0812345A",
    "expectedErrorMessage": "The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN."
  },
  "xss_address_payload": {
    "applicantNric": "S7812345C",
    "address": "<script>alert('xss_audit')</script>Blk 789 Bedok Reservoir #01-01"
  }
}
```
