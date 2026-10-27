# Component Specification: Household Members & Income - Part 3 (`f05-household-members`)

> **Module**: `f05` - FAS Paper Applications (Đơn giấy / Hardcopy Applications Offline)  
> **Component**: `household_members` (Review Application Screen - Part 3: Other family members & Household Summary)  
> **Source Spec**: `specs/md/FS document/FS-05_Hardcopy_Applications_Offline.md` (Mục 5, Mục 6, Mục 9 BR4, Mục 10 T7) & `specs/validation_rules/md/R5_FAS_APPLICATION_Validation_Rules.md` (Màn C: C19 - C20, Màn D: VR-F5-01, VR-F5-08)  
> **Target Audience**: School User (School Admin)  

---

## 1. Metadata & Selector

- **Route URL / Access Path**: Admin Portal $\rightarrow$ Financial assistance $\rightarrow$ Upload applications $\rightarrow$ Review application (`/admin/fas/paper-applications/review/:id` or `#part-3-household`)
- **Container Element Tag**: `<fieldset id="part-3-household" data-testid="section-part-3-household" aria-labelledby="heading-part-3">`
- **Playwright Locators (BSK Standardized Convention)**:

| Element Name | HTML Tag / Type | Playwright Locator (BSK Convention) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Section Header** | `h3` | `page.locator("h3:has-text('Part 3 · Other family members')")` | Section 3 Title |
| **Member Row Container** | `div / tr` | `page.locator("div[data-testid^='family-member-row-'], tr[data-testid^='family-member-row-']")` | Container for member $N$ |
| **Member Full Name** | `input[type="text"]` | `page.locator("input[data-testid^='input-member-fullname-']")` | Field C19; required if row added |
| **Member NRIC/FIN** | `input[type="text"]` | `page.locator("input[data-testid^='input-member-nric-']")` | Field C19; 9 chars checksum format |
| **Member Gender** | `select` | `page.locator("select[data-testid^='select-member-gender-']")` | Field C19; Male, Female, Other |
| **Add Member Button** | `button` | `page.locator("button[data-testid='btn-add-member'], button:has-text('+ Add member')")` | Field C20; adds optional member row |
| **Remove Member Button** | `button` | `page.locator("button[data-testid^='btn-remove-member-']")` | Deletes selected member row |
| **Household Size Display** | `span / div` | `page.locator("[data-testid='display-household-size']")` | Total members: 1 + children + other members |
| **Gross Household Income (GHI)** | `span / div` | `page.locator("[data-testid='display-gross-household-income'], [data-testid='display-ghi']")` | S$ #,##0.00 from Gov API |
| **Per Capita Income (PCI)** | `span / div` | `page.locator("[data-testid='display-per-capita-income'], [data-testid='display-pci']")` | S$ #,##0.00 (GHI / Size) |
| **Gov Income Source Badge** | `span.badge` | `page.locator("span:has-text('Government records (CPF)')")` | Notice that income is retrieved via API |

---

## 2. BR / AC Traceability

- **Functional Requirements**: `FS-05` Section 2 Step 3, Section 5 Part 3, Section 6, Section 9 BR4.
- **Business Rules (BR)**:
  - `BR-05-HH-01`: Phần thành viên gia đình khác là tùy chọn (có thể có 0 thành viên khác nếu hộ chỉ gồm người khai và các con).
  - `BR-05-HH-02`: **Không có ô nhập thu nhập trên mẫu đơn**. Thu nhập của người khai và từng thành viên gia đình được tra cứu tự động qua API dữ liệu Chính phủ (CPF / IRAS).
  - `BR-05-HH-03`: Công thức tính quy mô hộ gia đình (`Household size`):
    $$\text{Household Size} = 1\ (\text{Applicant}) + N_{\text{children}} + N_{\text{other members}}$$
  - `BR-05-HH-04`: Công thức tính thu nhập bình quân đầu người (`PCI`):
    $$\text{PCI} = \frac{\text{GHI}}{\text{Household Size}}$$
    (Hiển thị dạng tiền tệ Singapore `S$ #,##0.00`).
  - `BR-05-HH-05`: Nếu đã thêm một dòng thành viên gia đình, bắt buộc phải nhập đủ cả Họ tên và NRIC/FIN hợp lệ (`VR-F5-01`).
  - `BR-05-HH-06`: Tuyệt đối không được trùng NRIC giữa người khai, bất kỳ con nào, hoặc giữa các thành viên gia đình với nhau (`VR-F5-08`).
- **User Story Traceability**: `US-F5-04` (Quản lý danh sách thành viên hộ gia đình và tính toán tự động GHI / PCI).
- **Access Control (RBAC)**: Dành riêng cho School User (School Admin).

---

## 3. Ma trận 12 lớp Validation

| Lớp Kiểm Thử (12 Tầng) | Điều Kiện / Dữ Liệu Đầu Vào | Kỳ Vọng Giao Diện & Hành Vi Hệ Thống | Mã Lỗi / Phản Hồi Trực Quan |
| :--- | :--- | :--- | :--- |
| **1. Empty / Optional Section** | Không thêm bất kỳ thành viên gia đình nào (0 other members). | Hợp lệ! Quy mô hộ gia đình bằng $1 + N_{\text{children}}$. Không bị chặn nộp. | Không có lỗi; cho phép đi tiếp. |
| **2. Incomplete Member Row** | Bấm `+ Add member` nhưng để trống ô Họ tên hoặc NRIC khi bấm `Review and submit`. | Bị chặn mở dialog Review; báo lỗi thiếu trường Họ tên hoặc NRIC của thành viên. | `Complete: Family members (name and NRIC).` |
| **3. Whitespace / Trim** | Nhập Họ tên và NRIC có khoảng trắng thừa `" S8812345A "`. | Tự động trim khoảng trắng đầu/cuối trước khi kiểm tra định dạng và gọi API. | Xử lý hợp lệ sau khi trim. |
| **4. Member NRIC Checksum** | Nhập NRIC thành viên sai cấu trúc hoặc sai checksum (ví dụ: `S1234`, `G12345678`, `ABCXYZ`). | Bị từ chối; báo lỗi định dạng NRIC/FIN không hợp lệ. | Báo lỗi NRIC sai định dạng. |
| **5. Duplicate with Applicant** | Nhập NRIC thành viên gia đình trùng với NRIC người khai ở Part 1. | Bị chặn khi bấm `Review and submit` với thông báo trùng lặp cụ thể. | `The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN.` |
| **6. Duplicate with Child** | Nhập NRIC thành viên gia đình trùng với NRIC của một đứa trẻ ở Part 2. | Bị chặn khi bấm `Review and submit`. | `The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN.` |
| **7. Duplicate between Members** | Nhập 2 thành viên gia đình có cùng một số NRIC. | Bị chặn khi bấm `Review and submit`. | `The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN.` |
| **8. Dynamic Metric Re-calculation** | Thêm 1 thành viên gia đình mới (ví dụ bà nội / Grandmother). | Quy mô hộ gia đình (`Household size`) tăng ngay lập tức thêm 1. GHI cộng thêm thu nhập từ CPF của thành viên mới; PCI tự động tính lại ngay trên UI. | Cập nhật real-time `Household size`, `GHI`, `PCI`. |
| **9. Zero Income Representation** | Thành viên gia đình (ví dụ con nhỏ dưới 6 tuổi, người nội trợ) không có thu nhập CPF. | Hệ thống ghi nhận thu nhập là `S$ 0.00`, vẫn cộng vào Household size để giảm PCI (hỗ trợ xét duyệt FAS thuận lợi hơn). | Hiển thị `S$ 0.00`, PCI giảm hợp lý. |
| **10. Currency Formatting Standards** | Giá trị GHI = $2500$, Size = 4 $\rightarrow$ PCI = $625$. | Định dạng tiền tệ đúng chuẩn ISO/MOE: `S$ 2,500.00` và `S$ 625.00`. | Căn đúng chuẩn `S$ #,##0.00`. |
| **11. Extended Controls (Removal)** | Bấm nút `Remove` ở một dòng thành viên gia đình đã nhập. | Dòng thành viên bị xóa hoàn toàn khỏi DOM; Household size giảm đi 1; GHI và PCI được tính toán lại ngay lập tức. | Cập nhật state mượt mà, 0 console errors. |
| **12. API Mock Resilience** | API tra cứu thu nhập Chính phủ gặp lỗi timeout hoặc không phản hồi. | Hệ thống hiển thị trạng thái `Income pending retrieval` hoặc fallback an toàn, không làm crash giao diện web. | Toast cảnh báo hoặc retry indicator. |

---

## 4. Error Handling & Visual Feedback

- **Standard Messages**:
  - Thiếu tên hoặc NRIC thành viên: `"Complete: Family members (name and NRIC)."`
  - Trùng lặp NRIC: `"The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN."`
- **Visual Cues**:
  - Ghi chú đỏ ở đầu trang Review application liệt kê lỗi khi submit không đạt.
  - Ô Họ tên hoặc NRIC chưa điền bị viền đỏ `#D9383A` và `aria-invalid="true"`.
  - Khung tóm tắt hộ gia đình (`Household summary`) có nền xám nhạt bo góc, hiển thị rõ huy hiệu `"Income from Government records (CPF)"`.

---

## 5. JSON Fixtures Data Payload

```json
{
  "valid_household_with_members": {
    "familyMembers": [
      {
        "fullName": "Lim Geok Choo",
        "nric": "S5012345D",
        "gender": "Female",
        "relationship": "Grandmother",
        "monthlyIncome": 0.00
      },
      {
        "fullName": "Tan Ah Boon",
        "nric": "S7712345E",
        "gender": "Male",
        "relationship": "Uncle",
        "monthlyIncome": 1200.00
      }
    ],
    "calculatedMetrics": {
      "applicantIncome": 1800.00,
      "childrenCount": 2,
      "otherMembersCount": 2,
      "totalHouseholdSize": 5,
      "grossHouseholdIncome": 3000.00,
      "perCapitaIncome": 600.00,
      "formattedGhi": "S$ 3,000.00",
      "formattedPci": "S$ 600.00"
    }
  },
  "valid_zero_other_members": {
    "familyMembers": [],
    "calculatedMetrics": {
      "applicantIncome": 2200.00,
      "childrenCount": 1,
      "otherMembersCount": 0,
      "totalHouseholdSize": 2,
      "grossHouseholdIncome": 2200.00,
      "perCapitaIncome": 1100.00
    }
  },
  "invalid_incomplete_member_payload": {
    "familyMembers": [
      {
        "fullName": "Incomplete Member",
        "nric": "",
        "gender": "Male"
      }
    ],
    "expectedErrorMessage": "Complete: Family members (name and NRIC)."
  },
  "duplicate_nric_member_conflict": {
    "applicantNric": "S7512345Z",
    "memberNric": "S7512345Z",
    "expectedErrorMessage": "The same NRIC/FIN appears twice. The applicant, each child and each family member must have a different NRIC/FIN."
  }
}
```
