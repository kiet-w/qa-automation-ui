# Component Specification: Household & Income - Step 2 (`f10-household-income`)

> **Module**: `f10` - FAS Online Family Application Portal (Cổng Nộp Đơn FAS Phụ Huynh)  
> **Component**: `household_income` (Wizard Step 2: Household Members, CPF Income & Circumstances)  
> **Source Spec**: `specs/md/FS document/FS-10_FAS_Family_Application_Portal.md` (Mục 5 Bước 2, Mục 11 BR3, Mục 12 T3) & `specs/validation_rules/md/FS10_R10_FAS_Application_Validation (Draft).md`  
> **Target Audience**: Parent / Legal Guardian (Đăng nhập Singpass)  

---

## 1. Metadata & Selector

- **Route URL / Access Path**: e-Service Portal $\rightarrow$ Financial assistance $\rightarrow$ Apply for FAS $\rightarrow$ Step 2 (`/parent/fas/apply/step-2`)
- **Container Element Tag**: `<section id="fas-wizard-step-2" data-testid="wizard-step-2-household">`
- **Playwright Locators (BSK Standardized Convention)**:

| Element Name | HTML Tag / Type | Playwright Locator (BSK Convention) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Step 2 Container** | `div` | `page.locator("div[data-testid='step-container-household']")` | Step 2 wrapper |
| **Auto-Income Help Notice** | `div.alert-info` | `page.locator("div:has-text('Income is retrieved automatically from Government records (CPF)')")` | Statutory notice on income |
| **Household Members Table** | `table` | `page.locator("table[data-testid='table-household-members']")` | Member data grid |
| **Applicant Row (You)** | `tr` | `page.locator("tr[data-testid='row-member-applicant'], tr:has-text('(you)')")` | Locked applicant row |
| **Spouse Row** | `tr` | `page.locator("tr[data-testid='row-member-spouse'], tr:has-text('(spouse)')")` | Auto-added & locked if linked |
| **Children Row** | `tr` | `page.locator("tr[data-testid^='row-member-child-']")` | Read-only children from Step 1 |
| **Add Family Member Button** | `button` | `page.locator("button[data-testid='btn-add-family-member'], button:has-text('+ Add family member')")` | Adds empty member row |
| **Member Name Input** | `input[type="text"]` | `page.locator("input[data-testid^='input-member-name-']")` | Required for added member |
| **Member NRIC Input** | `input[type="text"]` | `page.locator("input[data-testid^='input-member-nric-']")` | Required 9 chars checksum |
| **Member Gender Select** | `select` | `page.locator("select[data-testid^='select-member-gender-']")` | Male, Female, Other |
| **Member Has Income Select** | `select / radio` | `page.locator("select[data-testid^='select-member-has-income-']")` | Yes / No selection |
| **Remove Member Link** | `button / a` | `page.locator("button[data-testid^='btn-remove-member-']")` | Deletes self-added member row |
| **Gross Household Income (GHI)** | `span` | `page.locator("[data-testid='display-ghi-step2']")` | S$ #,##0.00 from Gov CPF |
| **Household Size Display** | `span` | `page.locator("[data-testid='display-household-size-step2']")` | Total headcount |
| **Per Capita Income (PCI)** | `span` | `page.locator("[data-testid='display-pci-step2']")` | S$ #,##0.00 (GHI / Size) |
| **Income Trend Select** | `select` | `page.locator("select[data-testid='select-income-trend'], select[name='income_trend']")` | Stable, Dropped >30%, Unemployed |
| **Assistance History Select** | `select` | `page.locator("select[data-testid='select-assistance-history'], select[name='assistance_history']")` | Never, <3mo, 4-12mo, 13-24mo |
| **Single Parent Checkbox** | `input[type="checkbox"]` | `page.locator("input[data-testid='cb-single-parent']")` | Circumstances flag |
| **Disabled Member Checkbox** | `input[type="checkbox"]` | `page.locator("input[data-testid='cb-disabled-member']")` | Circumstances flag |
| **Child Under 6 Checkbox** | `input[type="checkbox"]` | `page.locator("input[data-testid='cb-child-under-6']")` | Circumstances flag |
| **Step 2 Continue Button** | `button` | `page.locator("button[data-testid='btn-step2-continue'], button:has-text('Continue')")` | Disabled if member incomplete |

---

## 2. BR / AC Traceability

- **Functional Requirements**: `FS-10` Section 5 Step 2, Section 11 BR3, Section 12 Scenario T3.
- **Business Rules (BR)**:
  - `BR-10-INC-01`: **Thu nhập chỉ lấy tự động từ dữ liệu Chính phủ (CPF / IRAS)**. Phụ huynh tuyệt đối không cần nhập số tiền thu nhập hay nộp bảng lương (payslip) (`BR3`).
  - `BR-10-INC-02`: Thành viên cố định: Phụ huynh nộp đơn (`you`) và người phối ngẫu (`spouse` - nếu có liên kết trong hồ sơ công dân) được tự động thêm vào bảng và khóa lại.
  - `BR-10-INC-03`: Các con đã chọn ở Bước 1 hiển thị trong bảng ở chế độ chỉ đọc.
  - `BR-10-INC-04`: Thành viên gia đình tự thêm: Có thể thêm các thành viên khác đang sống cùng nhà. Nếu đã thêm thành viên, **bắt buộc phải có đầy đủ Họ tên và NRIC/FIN hợp lệ**.
  - `BR-10-INC-05`: Nút `Continue` **bị khóa (disabled)** khi còn bất kỳ thành viên gia đình tự thêm nào chưa có Họ tên hoặc chưa có NRIC/FIN (`Scenario T3`).
  - `BR-10-INC-06`: Các trường hoàn cảnh hộ gia đình (`Household circumstances`: thu nhập 12 tháng, lịch sử nhận trợ cấp, hộ đơn thân, khuyết tật, con dưới 6 tuổi) được thu thập để chuyển cho mô hình Machine Learning / Rule-based chấm điểm tại Chức năng 4 (F4 ML Risk & Recommendation).
- **User Story Traceability**: `US-F10-03` (Khai báo hộ gia đình và ghi nhận thu nhập tự động qua CPF).
- **Access Control (RBAC)**: Chỉ phụ huynh đăng nhập qua Singpass.

---

## 3. Ma trận 12 lớp Validation

| Lớp Kiểm Thử (12 Tầng) | Điều Kiện / Dữ Liệu Đầu Vào | Kỳ Vọng Giao Diện & Hành Vi Hệ Thống | Mã Lỗi / Phản Hồi Trực Quan |
| :--- | :--- | :--- | :--- |
| **1. Incomplete Member Lock** | Bấm `+ Add family member` nhưng để trống ô Họ tên hoặc NRIC (Scenario T3). | Nút `Continue` bị khóa ngay lập tức (`disabled="true"`). Không cho phép sang Bước 3. | Nút chuyển xám mờ; trường trống viền đỏ. |
| **2. Valid Complete Member** | Điền đủ Họ tên `"Tan Ah Kow"` và NRIC `"S5512345F"`. | Nút `Continue` tự động bật sáng; hệ thống truy vấn CPF và cộng thêm thu nhập vào GHI nếu có. | Nút `Continue` sáng bật. |
| **3. Duplicate NRIC with Parent** | Thêm thành viên gia đình có NRIC trùng với NRIC phụ huynh đăng nhập. | Bị chặn; hiện thông báo lỗi ngay dưới ô NRIC của thành viên. | `This NRIC / FIN is already used in this application.` |
| **4. Duplicate NRIC with Child** | Thêm thành viên có NRIC trùng với một đứa trẻ đã chọn ở Bước 1. | Bị chặn với thông báo trùng NRIC. | `This NRIC / FIN is already used in this application.` |
| **5. NRIC/FIN Checksum Format** | Nhập NRIC thành viên sai cấu trúc (ví dụ: `S123456`, `12345678A`, `ABC`). | Trường hiển thị lỗi định dạng, yêu cầu nhập đúng chuẩn NRIC Singapore. | `Enter a valid NRIC / FIN, like S1234567D.` |
| **6. Dynamic Headcount Calculation** | Hộ gồm: Phụ huynh (1) + 2 con (2) + Thêm 1 bà ngoại (1). | Chỉ số `Household size` hiển thị tự động bằng 4. Khi bấm `Remove` bà ngoại, size giảm về 3. | Cập nhật real-time. |
| **7. PCI Computation Accuracy** | GHI = $3,000.00$, Household size = 4 $\rightarrow$ PCI = $750.00$. | Hiển thị chính xác định dạng tiền tệ `S$ 3,000.00` và `S$ 750.00`. | Căn đúng chuẩn `S$ #,##0.00`. |
| **8. Circumstances Radio / Selects** | Chọn: Thu nhập `"Dropped more than 30%"`, Trợ cấp `"Never / more than 2 years"`, tick `"Single parent"`. | Các cờ dữ liệu được ghi nhận vào payload của đơn để F4 ML engine phân loại mức độ rủi ro (Low / Medium / High Risk). | Lưu chính xác các cờ hoàn cảnh. |
| **9. Auto-Fill Read-Only Protection** | Cố tình can thiệp sửa giá trị thu nhập CPF của phụ huynh trên giao diện. | Ô thu nhập có thuộc tính `readonly="true"`; server chỉ tin cậy giá trị lấy từ API nội bộ Chính phủ. | Dữ liệu thu nhập được bảo vệ tuyệt đối. |
| **10. UI Health & Dynamic Row Adding** | Thêm liên tiếp 5 thành viên gia đình khác trên màn hình điện thoại di động. | Bảng cuộn mượt mà; các nút `Remove` tách biệt rõ ràng, không gây bấm nhầm; 0 console errors. | Đạt chuẩn Invariant 7 UI Health. |
| **11. Pristine / Dirty Detection** | Thay đổi lựa chọn trong dropdown xu hướng thu nhập. | Kích hoạt cờ dirty form, cho phép lưu nháp qua nút `Save draft & exit`. | State chuyển sang dirty. |
| **12. Zero Income Representation** | Thành viên hoặc phụ huynh làm nội trợ, thất nghiệp, thu nhập CPF = 0. | Hiển thị giá trị `S$ 0.00`; thành viên vẫn được tính vào mẫu số của PCI để hạ thấp thu nhập bình quân. | Hiển thị `S$ 0.00` chuẩn xác. |

---

## 4. Error Handling & Visual Feedback

- **Standard Messages**:
  - Thiếu NRIC thành viên: `MSG-0001` - `"Enter the family member's NRIC / FIN"`
  - Thiếu tên thành viên: `MSG-0001` - `"Enter the family member's full name"`
  - Trùng lặp NRIC: `"This NRIC / FIN is already used in this application."`
  - Sai định dạng NRIC: `"Enter a valid NRIC / FIN, like S1234567D."`
- **Visual Cues**:
  - Hàng thành viên thiếu thông tin có viền đỏ bao quanh; con trỏ tự động focus vào ô trống đầu tiên khi phụ huynh cố bấm Continue.

---

## 5. JSON Fixtures Data Payload

```json
{
  "step2_valid_payload": {
    "applicant": {
      "name": "Mdm Noor Aisha",
      "nric": "S8212345E",
      "grossMonthlyIncome": 1600.00
    },
    "spouse": null,
    "childrenApplying": [
      { "name": "Nurul Huda Binte Mohd", "nric": "T1456789A", "income": 0.00 },
      { "name": "Muhammad Danial Bin Mohd", "nric": "T1856789B", "income": 0.00 }
    ],
    "otherFamilyMembers": [
      {
        "fullName": "Mariam Binte Osman",
        "nric": "S5212345A",
        "gender": "Female",
        "hasIncome": false,
        "grossMonthlyIncome": 0.00
      }
    ],
    "circumstances": {
      "incomeTrend": "Dropped more than 30%",
      "recentAssistance": "Never / more than 2 years",
      "isSingleParent": true,
      "hasDisabledMember": false,
      "hasChildUnder6": false
    },
    "summaryMetrics": {
      "householdSize": 4,
      "grossHouseholdIncome": 1600.00,
      "perCapitaIncome": 400.00
    }
  },
  "step2_incomplete_member_payload": {
    "otherFamilyMembers": [
      { "fullName": "Incomplete Member", "nric": "" }
    ],
    "isContinueDisabled": true
  }
}
```
