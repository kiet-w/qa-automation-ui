# Component Specification: Children Applying - Part 2 (`f05-children-applying`)

> **Module**: `f05` - FAS Paper Applications (Đơn giấy / Hardcopy Applications Offline)  
> **Component**: `children_applying` (Review Application Screen - Part 2: Children applying)  
> **Source Spec**: `specs/md/FS document/FS-05_Hardcopy_Applications_Offline.md` (Mục 5, Mục 6, Mục 9 BR2, BR8, BR9, Mục 10 T3..T6, T13) & `specs/validation_rules/md/R5_FAS_APPLICATION_Validation_Rules.md` (Màn C: C16 - C18, Màn D: VR-F5-01 đến VR-F5-07)  
> **Target Audience**: School User (School Admin)  

---

## 1. Metadata & Selector

- **Route URL / Access Path**: Admin Portal $\rightarrow$ Financial assistance $\rightarrow$ Upload applications $\rightarrow$ Review application (`/admin/fas/paper-applications/review/:id` or `#part-2-children`)
- **Container Element Tag**: `<fieldset id="part-2-children" data-testid="section-part-2-children" aria-labelledby="heading-part-2">`
- **Playwright Locators (BSK Standardized Convention)**:

| Element Name | HTML Tag / Type | Playwright Locator (BSK Convention) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Section Header** | `h3` | `page.locator("h3:has-text('Part 2 · Children applying')")` | Section 2 Header |
| **Child Row Container** | `div / tr` | `page.locator("div[data-testid^='child-row-'], tr[data-testid^='child-row-']")` | Container for child block $N$ |
| **Child NRIC Input** | `input[type="text"]` | `page.locator("input[data-testid^='input-child-nric-']")` | Field C16; triggers MOE database lookup |
| **Child Full Name** | `input[type="text"]` | `page.locator("input[data-testid^='input-child-fullname-']")` | Field C17; auto-filled & locked |
| **Child Date of Birth** | `input[type="text"]` | `page.locator("input[data-testid^='input-child-dob-']")` | Field C17; auto-filled & locked (`DD/MM/YYYY`) |
| **Child Gender** | `input / select` | `page.locator("input[data-testid^='input-child-gender-']")` | Field C17; auto-filled & locked |
| **Child School** | `input[type="text"]` | `page.locator("input[data-testid^='input-child-school-']")` | Field C17; auto-filled current enrolled school |
| **Child Level** | `input[type="text"]` | `page.locator("input[data-testid^='input-child-level-']")` | Field C17; Primary / Secondary / Pre-University |
| **Child Grade** | `input[type="text"]` | `page.locator("input[data-testid^='input-child-grade-']")` | Field C17; P1–P6, S1–S5, PU1–PU3 |
| **Child Class** | `input[type="text"]` | `page.locator("input[data-testid^='input-child-class-']")` | Field C17; e.g. "Primary 3A" |
| **Add Child Button** | `button` | `page.locator("button[data-testid='btn-add-child'], button:has-text('+ Add child')")` | Field C18; adds new empty child row |
| **Remove Child Button** | `button` | `page.locator("button[data-testid^='btn-remove-child-']")` | Deletes row; disabled if only 1 child left |
| **Name Mismatch Warning** | `div.warning-note` | `page.locator("div[data-testid^='warn-name-mismatch-']")` | Non-blocking alert if scanned name differs |

---

## 2. BR / AC Traceability

- **Functional Requirements**: `FS-05` Section 2 Steps 2-5, Section 5 Part 2, Section 6 (VR-F5-02 đến VR-F5-07), Section 9 BR1, BR2, BR8, BR9.
- **Business Rules (BR)**:
  - `BR-05-CHILD-01`: Ít nhất một con trong danh sách nộp đơn (`At least one child is required`).
  - `BR-05-CHILD-02`: Mỗi con phải tồn tại trong cơ sở dữ liệu hồ sơ MOE (`Function 3 Enrolment`). Nếu không tìm thấy, hệ thống chặn đơn (`VR-F5-03`).
  - `BR-05-CHILD-03`: Giới hạn độ tuổi: Con phải từ đủ 7 đến dưới 17 tuổi (từ 7 đến 16 tuổi tại ngày nộp đơn). Đúng ngày sinh nhật 7 tuổi hợp lệ; đúng ngày sinh nhật 17 tuổi bị chặn (`VR-F5-04`).
  - `BR-05-CHILD-04`: Đơn duy nhất trong năm: Học sinh chưa từng có đơn FAS nào trong năm dương lịch hiện tại (bất kể trạng thái Pending, Approved, Rejected). Nếu đã có, hệ thống chặn đơn (`VR-F5-05`).
  - `BR-05-CHILD-05`: Phân quyền trường học: **Ít nhất một con trong đơn phải đang theo học tại trường của School User** đang thao tác (`VR-F5-06`). Nếu tất cả các con đều học trường khác, School User bị chặn không cho nộp.
  - `BR-05-CHILD-06`: Thời gian mở form: Chỉ được nộp khi hôm nay nằm trong khoảng `Form opens` – `Form closes` của scheme MOEFAS hoặc scheme SBFAS của trường con đang học (`VR-F5-07`).
- **User Story Traceability**: `US-F5-03` (Thêm và đối chiếu hồ sơ học sinh nộp đơn FAS).
- **Access Control (RBAC)**: School User chỉ được nộp đơn nếu có ít nhất 1 học sinh thuộc danh sách ghi danh của trường mình.

---

## 3. Ma trận 12 lớp Validation

| Lớp Kiểm Thử (12 Tầng) | Điều Kiện / Dữ Liệu Đầu Vào | Kỳ Vọng Giao Diện & Hành Vi Hệ Thống | Mã Lỗi / Phản Hồi Trực Quan |
| :--- | :--- | :--- | :--- |
| **1. Empty / Required** | Bỏ trống hoàn toàn danh sách con (0 trẻ) khi bấm `Review and submit`. | Bị chặn mở dialog Review; hiện lỗi bắt buộc có ít nhất 1 con. | `Complete: At least one child.` |
| **2. Empty NRIC of Child** | Thêm 1 hàng con nhưng để trống ô NRIC của trẻ thứ $N$. | Bị chặn mở dialog Review; báo rõ số thứ tự dòng con thiếu NRIC. | `Child {n}: enter the NRIC/FIN.` |
| **3. Non-Existent MOE Record** | Nhập NRIC không tồn tại trong CSDL học sinh MOE (ví dụ `T1599999Z`). | Hệ thống tra cứu thất bại; không tự điền được trường nào; báo lỗi chặn nộp. | `Child {n}: no student with NRIC/FIN {nric} in MOE records.` |
| **4. BVA Age Limit (7 to 16)** | • Trẻ 6 tuổi 364 ngày (Dưới 7 tuổi)<br>• Đúng ngày sinh nhật 7 tuổi<br>• Trẻ 16 tuổi 364 ngày<br>• Đúng ngày sinh nhật 17 tuổi (17 tuổi) | • Dưới 7 tuổi: Bị chặn.<br>• 7 đến 16 tuổi: Hợp lệ.<br>• 17 tuổi: Bị chặn. | `{tên} must be 7 to 16 years old (now {tuổi}).` |
| **5. Duplicate Application This Year** | Con đã nộp đơn FAS trong năm 2026 (ví dụ đơn `APP-2026-00123`, trạng thái `Pending` hoặc `Approved`). | Hệ thống chặn không cho nộp thêm đơn thứ hai trong năm. | `{tên} already has an application this year ({id}, {status}).` |
| **6. Cross-School Enrolment Check** | School User thuộc trường Tiểu học Bedok Green nhập đơn cho 2 con nhưng cả 2 đều học tại Trường Tiểu học Ang Mo Kio. | Bị chặn nộp do vi phạm quyền hạn trường học. | `At least one child must be enrolled at {trường}.` |
| **7. Cross-School Mixed Enrolment** | Con 1 học tại Bedok Green (trường của user), Con 2 học tại Temasek Secondary (trường khác). | Hợp lệ! Hệ thống chấp nhận đơn gia đình liên trường; đơn của Con 2 sẽ tự động phân luồng về Temasek Secondary nếu vào diện SBFAS. | Hợp lệ, đi tiếp tới bước Review. |
| **8. Form Closed Check** | Ngày nộp đơn nằm ngoài khoảng Form Opens – Form Closes của MOEFAS và SBFAS của trường con. | Bị chặn nộp; hiển thị ngày mở form tiếp theo (nếu đã công bố). | `{tên}: the FAS application form is closed (next opens DD/MM/YYYY).` hoặc `{tên}: the FAS application form is closed.` |
| **9. Duplicate NRIC within Form** | • Nhập 2 con cùng 1 NRIC.<br>• Nhập NRIC con trùng với NRIC người khai hoặc thành viên gia đình (Part 3). | Hệ thống phát hiện trùng lặp NRIC trong cùng hồ sơ gia đình và chặn lại. | `The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN.` |
| **10. Name Discrepancy Tolerance** | Tên trên bản scan đơn giấy (OCR đọc được) khác nhẹ với tên chính thức trong CSDL MOE (ví dụ "Aisha Binte Mohd" vs "Aisha Bte Mohammad"). | Không chặn nộp đơn! Hệ thống hiển thị ghi chú cảnh báo màu vàng cho biết MOE sẽ thấy cảnh báo sai lệch dữ liệu. | Alert banner vàng: "Name mismatch with MOE records: MOE HQ will see a discrepancy flag." |
| **11. Extended Controls (Add/Remove)** | Bấm `+ Add child` khi đang có 1 con. Sau đó bấm nút `Remove` ở con thứ 2. | Thêm dòng con mới thành công. Khi chỉ còn 1 con duy nhất, nút `Remove` bị disable để đảm bảo luôn có ít nhất 1 con. | Thêm/xóa dòng mượt mà, DOM cập nhật tức thì. |
| **12. UI Health & Auto-Derivation** | Khi tra cứu NRIC con thành công. | Cột `Level` tự động suy ra từ `Grade` (P1–P6 $\rightarrow$ Primary; S1–S5 $\rightarrow$ Secondary; PU1–PU3 $\rightarrow$ Pre-University). Toàn bộ ô tự điền hiển thị nền xám khóa. | Auto-derived Level chính xác 100%. |

---

## 4. Error Handling & Visual Feedback

- **Standard Messages**:
  - Không có con nào: `"Complete: At least one child."`
  - Thiếu NRIC con: `"Child {n}: enter the NRIC/FIN."`
  - Không tìm thấy học sinh: `"Child {n}: no student with NRIC/FIN {nric} in MOE records."`
  - Sai độ tuổi: `"{tên} must be 7 to 16 years old (now {tuổi})."`
  - Trùng đơn trong năm: `"{tên} already has an application this year ({id}, {status})."`
  - Không thuộc trường user: `"At least one child must be enrolled at {trường}."`
  - Form đóng: `"{tên}: the FAS application form is closed (next opens DD/MM/YYYY)."`
  - Trùng lặp NRIC: `"The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN."`
- **Visual Cues**:
  - Thẻ đỏ thông báo lỗi cố định ở đỉnh trang Review (`div[role="alert"]`).
  - Ô NRIC sai có viền đỏ `#D9383A`, tự động focus hoặc cuộn tới vị trí lỗi.

---

## 5. JSON Fixtures Data Payload

```json
{
  "valid_two_children_payload": [
    {
      "childIndex": 1,
      "nric": "T1412345B",
      "fullName": "Tan Mei Ling",
      "dateOfBirth": "15/03/2014",
      "gender": "Female",
      "school": "Bedok Green Primary School",
      "level": "Primary",
      "grade": "P6",
      "className": "Primary 6 Compassion",
      "eaNumber": "EA-2014-00123"
    },
    {
      "childIndex": 2,
      "nric": "T1798765C",
      "fullName": "Tan Jun Jie",
      "dateOfBirth": "20/08/2017",
      "gender": "Male",
      "school": "Bedok Green Primary School",
      "level": "Primary",
      "grade": "P3",
      "className": "Primary 3 Honesty",
      "eaNumber": "EA-2017-00456"
    }
  ],
  "invalid_scenarios": {
    "age_ineligible_17": {
      "nric": "T0912345A",
      "fullName": "Tan Wei Kang",
      "dateOfBirth": "25/10/2009",
      "calculatedAge": 17,
      "expectedMessage": "Tan Wei Kang must be 7 to 16 years old (now 17)."
    },
    "duplicate_application_this_year": {
      "nric": "T1412345B",
      "fullName": "Tan Mei Ling",
      "existingApplicationId": "APP-2026-00412",
      "existingStatus": "Pending",
      "expectedMessage": "Tan Mei Ling already has an application this year (APP-2026-00412, Pending)."
    },
    "not_enrolled_in_user_school": {
      "userSchool": "Bedok Green Primary School",
      "childrenSchools": ["Ang Mo Kio Primary School"],
      "expectedMessage": "At least one child must be enrolled at Bedok Green Primary School."
    },
    "form_closed_scenario": {
      "childName": "Tan Jun Jie",
      "nextOpenDate": "01/11/2026",
      "expectedMessage": "Tan Jun Jie: the FAS application form is closed (next opens 01/11/2026)."
    },
    "student_not_found": {
      "nric": "T1999999Z",
      "childIndex": 1,
      "expectedMessage": "Child 1: no student with NRIC/FIN T1999999Z in MOE records."
    }
  }
}
```
