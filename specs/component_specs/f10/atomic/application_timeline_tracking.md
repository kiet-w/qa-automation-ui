# Component Specification: Application Timeline & Decision Tracking (`f10-timeline-tracking`)

> **Module**: `f10` - FAS Online Family Application Portal (Cổng Nộp Đơn FAS Phụ Huynh)  
> **Component**: `application_timeline_tracking` (My Applications: 4-Stage Timeline & Decision Outcome Cards)  
> **Source Spec**: `specs/md/FS document/FS-10_FAS_Family_Application_Portal.md` (Mục 9 My applications timeline, Mục 11 BR5, BR8, Mục 12 T9, T10, T11) & `specs/validation_rules/md/FS10_R10_FAS_Application_Validation (Draft).md`  
> **Target Audience**: Parent / Legal Guardian (Đăng nhập Singpass)  

---

## 1. Metadata & Selector

- **Route URL / Access Path**: e-Service Portal $\rightarrow$ Financial assistance $\rightarrow$ My applications (`/parent/fas/applications` hoặc `/parent/fas#my-applications`)
- **Container Element Tag**: `<section id="my-fas-applications" data-testid="section-application-timeline">`
- **Playwright Locators (BSK Standardized Convention)**:

| Element Name | HTML Tag / Type | Playwright Locator (BSK Convention) | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Applications Container** | `div` | `page.locator("div[data-testid='container-my-applications']")` | Wrapper for all application cards |
| **Family Card Header** | `div.card-header` | `page.locator("div[data-testid^='card-family-app-']")` | "Family application FAM-..." |
| **Child Application Item** | `div.child-item` | `page.locator("div[data-testid^='item-child-app-']")` | Per-child application block |
| **Status Badge** | `span.badge` | `page.locator("span[data-testid^='badge-status-']")` | "Under review", "Approved", "Rejected" |
| **Timeline Node 1: Submitted** | `li / div` | `page.locator("div[data-testid^='timeline-node-submitted-']")` | Stage 1: Submitted date |
| **Timeline Node 2: System Check**| `li / div` | `page.locator("div[data-testid^='timeline-node-syscheck-']")` | Stage 2: MOEFAS/SBFAS check |
| **Timeline Node 3: Review** | `li / div` | `page.locator("div[data-testid^='timeline-node-review-']")` | Stage 3: System or School review |
| **Timeline Node 4: Decision** | `li / div` | `page.locator("div[data-testid^='timeline-node-decision-']")` | Stage 4: Decision date / waiting |
| **Approved Outcome Box** | `div.alert-success`| `page.locator("div[data-testid^='outcome-box-approved-']")` | Subsidy details & effective date |
| **Rejected Outcome Box** | `div.alert-danger` | `page.locator("div[data-testid^='outcome-box-rejected-']")` | Rejection reason & SBFAS transfer note |

---

## 2. BR / AC Traceability

- **Functional Requirements**: `FS-10` Section 9 Timeline & Outcome, Section 11 BR5, BR8, Section 12 Scenarios T9, T10, T11.
- **Business Rules (BR)**:
  - `BR-10-TIME-01`: Gom nhóm theo đơn gia đình: Mỗi đơn gia đình hiển thị một thẻ tổng (`Family application FAM-YYYY-NNNNN`), ngày nộp, nguồn (`Online`), số thành viên trong hộ, và tổng thu nhập GHI.
  - `BR-10-TIME-02`: Đơn con độc lập: Mỗi con có một dòng/khối riêng với Application ID riêng, nhãn scheme dự kiến (`MOEFAS` hoặc `SBFAS`), và trạng thái xử lý.
  - `BR-10-TIME-03`: Hiển thị trạng thái thân thiện: Trạng thái kỹ thuật `Pending` **được hiển thị cho phụ huynh là `"Under review"`**.
  - `BR-10-TIME-04`: Chu trình 4 giai đoạn tiến trình (`4-Stage Timeline`):
    1. **1. Submitted**: Ngày nộp đơn thực tế.
    2. **2. System check**:
       - MOEFAS: `"MOEFAS · after the form closes on DD/MM/YYYY"` khi đang chờ form đóng; sau đó chuyển thành `"MOEFAS"`.
       - SBFAS: `"Sent to school (SBFAS)"`.
    3. **3. Review**:
       - MOEFAS: `"by the system (automatic)"`.
       - SBFAS: `"by {tên trường của con}"`.
    4. **4. Decision**: Ngày có kết quả chính thức hoặc chữ `"waiting"`.
  - `BR-10-TIME-05`: Khung kết quả Approved:
    - Hiển thị rõ: `"{MOEFAS | SBFAS Tier n} from DD/MM/YYYY. Fees reduced: ..."` hoặc `"Eligible fees will be reduced when issued."`.
  - `BR-10-TIME-06`: Khung kết quả Rejected:
    - Hiển thị lý do từ chối; nếu đơn đã được tự động chuyển sang trường xét SBFAS thì hiển thị thêm dòng: `"Now being considered for SBFAS ({id})"`.
  - `BR-10-TIME-07`: Thông báo Email (`BR8`): Phụ huynh nhận email tự động sau mỗi quyết định được ban hành.
- **User Story Traceability**: `US-F10-07` (Phụ huynh theo dõi tiến trình xét duyệt và kết quả trợ cấp của các con trên timeline).
- **Access Control (RBAC)**: Chỉ phụ huynh của học sinh.

---

## 3. Ma trận 12 lớp Validation

| Lớp Kiểm Thử (12 Tầng) | Điều Kiện / Dữ Liệu Đầu Vào | Kỳ Vọng Giao Diện & Hành Vi Hệ Thống | Mã Lỗi / Phản Hồi Trực Quan |
| :--- | :--- | :--- | :--- |
| **1. Under Review State Display** | Đơn vừa nộp thành công, đang ở trạng thái Pending. | Trạng thái hiển thị là `"Under review"` (nhãn màu cam nhạt); timeline sáng ở bước 1 Submitted và bước 2 System check đang chờ. | Badge: `Under review` |
| **2. Timeline Waiting Notice (T9)** | Đơn MOEFAS đang chờ form nộp đơn đóng (ví dụ đóng vào 31/12/2026). | Node 2 hiển thị rõ ràng thông điệp chờ: `"MOEFAS · after the form closes on 31/12/2026"`. Node 4 hiển thị `"waiting"`. | Timeline giải thích thời gian chờ rõ ràng. |
| **3. Auto-Approved MOEFAS Display (T9)** | Form đóng vào 31/12/2026, hệ thống tự động duyệt đơn vào ngày 01/01/2027. | Timeline sáng cả 4 node xanh lá; xuất hiện khung Approved: `"MOEFAS from 01/01/2027. Eligible fees will be reduced when issued."`. | Khung xanh lá hiển thị trợ cấp. |
| **4. Direct SBFAS Referral for PR (T10)** | Con là Singapore PR, đơn nộp xong được chuyển thẳng cho trường xét SBFAS. | Node 2 hiển thị `"Sent to school (SBFAS)"`; Node 3 hiển thị `"by {School Name}"`; phụ huynh biết rõ trường đang thụ lý. | Minh bạch đơn vị thẩm định. |
| **5. Approved SBFAS with Tier (T11)** | Trường học xét duyệt SBFAS cấp Tier 2 có hiệu lực từ 01/02/2027. | Khung kết quả hiển thị cụ thể cấp tier trường ban hành: `"SBFAS Tier 2 from 01/02/2027. Fees reduced: 75% standard miscellaneous fees."`. | Thể hiện đúng tên Tier trường cấp. |
| **6. MOEFAS Rejection & SBFAS Forward** | Con trượt điều kiện MOEFAS do PCI cao hơn trần, nhưng có tick `Also consider SBFAS = Yes`. | Đơn MOEFAS chuyển sang Rejected; hiển thị thông báo chuyển tiếp kèm link: `"Now being considered for SBFAS (APP-2026-00412-S)"`. | Thông báo chuyển tiếp mượt mà. |
| **7. Final Direct Rejection** | Con không đạt chuẩn MOEFAS và phụ huynh không chọn SBFAS. | Timeline kết thúc tại Decision Rejected; hiển thị lý do: `"Not eligible for MOEFAS"` kèm ghi chú chi tiết. | Lý do rõ ràng, minh bạch. |
| **8. Multi-Child Split Status Card** | Đơn gia đình có 2 con: Con 1 đã được duyệt MOEFAS, Con 2 là SBFAS vẫn đang chờ trường xét. | Thẻ gia đình hiển thị độc lập trạng thái của từng con: Con 1 có khung Approved xanh lá, Con 2 có timeline đang dừng ở bước Review trường học. | Phân tách trạng thái độc lập từng con. |
| **9. Email Dispatch Verification** | Ngay khi quyết định (Approved hoặc Rejected) được cập nhật trên timeline. | Hệ thống tự động gửi email thông báo kết quả đến địa chỉ email đã đăng ký của phụ huynh (`BR8`). | Gửi email thông báo chuẩn xác. |
| **10. UI Health & Stepper Contrast** | Kiểm tra hiển thị thanh tiến trình 4 bước (Horizontal Stepper). | Các node đã hoàn thành có nền xanh lá kèm icon checkmark `✓`; node đang chờ có vòng tròn viền đứt nét; đường nối có độ tương phản cao; 0 console errors. | Đạt chuẩn Invariant 7 UI Health. |
| **11. Mobile Stepper Responsiveness** | Mở trang theo dõi đơn trên màn hình điện thoại (viewport 360px). | Thanh tiến trình tự động chuyển từ dạng ngang sang dạng danh sách dọc (`vertical stepper`), không bị đè chữ; đọc dễ dàng. | Responsive stepper hoàn hảo. |
| **12. Real-time Refresh Polling / Webhook** | Trường học phê duyệt đơn SBFAS trên Admin Portal. | Trang My applications của phụ huynh tự động cập nhật kết quả mới nhất khi reload hoặc qua cơ chế auto-poll mà không cần đăng xuất. | Dữ liệu đồng bộ tức thời. |

---

## 4. Error Handling & Visual Feedback

- **Standard Messages**:
  - Đang chờ form đóng: `"MOEFAS · after the form closes on DD/MM/YYYY"`
  - Chuyển tiếp SBFAS: `"Now being considered for SBFAS ({id})"`
  - Trợ cấp MOEFAS: `"MOEFAS from DD/MM/YYYY. Eligible fees will be reduced when issued."`
  - Trợ cấp SBFAS: `"SBFAS Tier {n} from DD/MM/YYYY. Fees reduced: ..."`
- **Visual Cues**:
  - Node hoàn thành: Xanh lá đậm (`bg-emerald-600 text-white`).
  - Node đang chờ: Xám nhạt viền vàng cam (`border-amber-400 bg-amber-50 text-amber-800`).
  - Huy hiệu `Under review`: Nền vàng cam ấm áp (`bg-amber-100 text-amber-800 font-medium`).

---

## 5. JSON Fixtures Data Payload

```json
{
  "timeline_moefas_waiting_mock": {
    "familyApplicationId": "FAM-2026-00045",
    "submittedAt": "26/10/2026",
    "source": "Online",
    "childApplications": [
      {
        "childName": "Nurul Huda Binte Mohd",
        "applicationId": "APP-2026-00501",
        "scheme": "MOEFAS",
        "status": "Pending",
        "displayStatus": "Under review",
        "timeline": {
          "step1Submitted": "26/10/2026",
          "step2SystemCheck": "MOEFAS · after the form closes on 31/12/2026",
          "step3Review": "by the system (automatic)",
          "step4Decision": "waiting"
        }
      }
    ]
  },
  "timeline_sbfas_approved_mock": {
    "familyApplicationId": "FAM-2026-00045",
    "childApplications": [
      {
        "childName": "Muhammad Danial Bin Mohd",
        "applicationId": "APP-2026-00502",
        "scheme": "SBFAS",
        "status": "Approved",
        "displayStatus": "Approved",
        "decision": {
          "schemeName": "SBFAS Tier 1",
          "effectiveFrom": "01/01/2027",
          "feeReductionText": "100% standard and second-tier miscellaneous fees waived.",
          "decidedBy": "Tampines Primary School"
        }
      }
    ]
  }
}
```
