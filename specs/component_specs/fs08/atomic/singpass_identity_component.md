# Component Specification: Singpass Identity & NRIC Masking (Parent Profile)

## 1. Metadata & Selector

| Attribute | Specification |
| :--- | :--- |
| **Component Name** | `SingpassIdentityComponent` |
| **Target Page / Route** | `/profile` (`ParentProfilePage`) |
| **Element Hierarchy** | Profile summary card `<article>`, Definition list `<dl>`, Action buttons `<button>` |
| **Visual State** | View Mode & Edit Mode (Always present at top of profile) |
| **Component Scope** | Read-only identity attributes synced from Singpass (Full Name, NRIC/FIN, Residential Address) & Masking Toggle |

### Playwright Live DOM Locators
```python
# Extracted directly from pages/fs08/parent_profile_page.py
PROFILE_HEADING = "h1:has-text('My Profile'), h2:has-text('My Profile')"
FULL_NAME_VAL = "dt:has-text('Full Name') + dd"
NRIC_VAL = "dt:has-text('NRIC') + dd"
RESIDENTIAL_ADDRESS_VAL = "dt:has-text('Residential') + dd"
SHOW_NRIC_BTN = "button:has-text('Show NRIC')"
HIDE_NRIC_BTN = "button:has-text('Hide NRIC')"
UPDATE_DETAILS_BTN = "button:has-text('Update details')"
```

---

## 2. Business Rules & Acceptance Criteria Traceability

| ID | Type | Description | Source Reference |
| :--- | :--- | :--- | :--- |
| **BR-08-03** | Business Rule | **Singpass Immutability**: Full Name, NRIC, and Residential Address are authoritative from Singpass (MyInfo) and **STRICTLY READ-ONLY**. Users cannot edit them in the portal. Any change must be done via Singpass / ICA. | `specs/md/FS document/FS-08_Parent_Portal_SingPass_Profile.md` |
| **D-20** | Architecture Decision | Residential Address is retrieved from Singpass and is immutable; parents can only provide an alternative Mailing Address. | `specs/md/MEETINGS_AND_DECISIONS_SUMMARY.md` |
| **R8-AC01** | Acceptance Criteria | Successfully authenticate via Singpass and view parent profile details. | `specs/md/Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md` |
| **R8-AC05** | Acceptance Criteria | Read-only identity fields must be displayed as text/definition terms, without editable input fields. | `specs/md/Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md` |
| **R8-AC06** | Acceptance Criteria | NRIC must be masked by default (`*****123F`). Clicking "Show NRIC" reveals the full 9-character NRIC; button text toggles to "Hide NRIC". | `specs/md/Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md` |
| **R8-AC14** | Acceptance Criteria | Clicking "Hide NRIC" returns NRIC to masked format (`*****123F`) and button text back to "Show NRIC". | `specs/md/Test Cases/TC_R8_Parent_Portal_SingPass_Profile.md` |

---

## 3. Ma trận 12 lớp Validation & UI Integrity

| Lớp (Layer) | Phân Loại Kiểm Thử | Dữ Liệu Đầu Vào (Input Vector) | Trạng Thái / Hành Vi UI Kỳ Vọng | Tiêu Chí Đạt (Pass Criteria) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Empty / Default** | Trạng thái hiển thị mặc định | Page mount sau khi Singpass login | NRIC hiển thị masked dạng `*****123F` (5 dấu `*`, 3 số cuối, 1 chữ cái cuối). Nút hiển thị `Show NRIC`. | Text chứa `*****`, nút có nhãn `Show NRIC`. |
| **2. Toggle Show** | Tương tác người dùng | Click `button:has-text('Show NRIC')` | NRIC hiển thị đầy đủ 9 ký tự (ví dụ: `S7654321B`). Nhãn nút đổi ngay sang `Hide NRIC`. | Text khớp regex `^[STFGMO]\d{7}[A-Z]$`. |
| **3. Toggle Hide** | Tương tác đảo chiều | Click `button:has-text('Hide NRIC')` | NRIC lập tức hoàn nguyên về định dạng che `*****321B`. Nhãn nút hoàn nguyên `Show NRIC`. | NRIC được che lại, nút đổi thành `Show NRIC`. |
| **4. Immutability** | Ngăn chặn can thiệp DOM | Cố tình kiểm tra thuộc tính input | Toàn bộ 3 trường (Full Name, NRIC, Residential Address) không render dưới dạng `<input>` hoặc `<textarea>`, mà là `<dd>` thuần. | Locator `input[name='nric']` hoặc `input[name='fullName']` trả về count = 0. |
| **5. Form State Impact** | Trạng thái Dirty/Pristine | Click "Show NRIC" hoặc "Hide NRIC" | Hành động toggle NRIC **KHÔNG** làm bẩn form (Form pristine). Nút "Save changes" (nếu ở Edit mode) không bị kích hoạt ngoài ý muốn. | Trạng thái dirty không thay đổi khi toggle NRIC. |
| **6. Cumulative Layout Shift (CLS)** | Sức khỏe UI & Trải nghiệm | Toggle qua lại giữa Show và Hide NRIC | Chiều cao hoặc độ rộng phần tử không bị co giật gây xô lệch layout lân cận (`CLS = 0`). | Không xuất hiện layout shift trên container. |
| **7. Persistence Integrity** | Bảo toàn trạng thái khi Reload | Đang ở trạng thái "Show NRIC" -> Bấm F5 reload trang | Sau khi tải lại trang, NRIC **BẮT BUỘC** tự động che lại về mặc định an toàn (`*****123F`). Không lưu trạng thái unmasked vào localStorage/session. | NRIC hiển thị `*****` sau khi reload. |
| **8. Accessibility & Screen Reader** | WCAG 2.1 AA Compliance | Kiểm tra thuộc tính ARIA | Nút toggle có `aria-label` hoặc tên rõ ràng: "Show NRIC" / "Hide NRIC". Có `aria-expanded` hoặc `aria-pressed` chỉ báo trạng thái. | Hỗ trợ bàn phím `Space` / `Enter`. |
| **9. Multi-session Privacy** | Bảo mật PII Client-Side | Chuyển tab hoặc logout Singpass | Thông tin NRIC không lộ trong DOM ẩn, không bị lưu vào global JavaScript window object. | Window scope sạch PII không được mã hóa. |
| **10. Address Formatting** | Hiển thị địa chỉ thường trú | Address từ Singpass payload | Hiển thị đầy đủ Block, Street, Unit, Postal Code chuẩn Singapore: `BLK 123 BISHAN ST 12 #05-12 SINGAPORE 570123`. | Hiển thị dạng text liền mạch, không gãy hàng sai quy tắc. |
| **11. Stress Toggle** | Phá có kỷ luật / Debounce | Click liên tục 10 lần vào nút Show/Hide | Giao diện phản hồi mượt mà, không sinh lỗi JavaScript Console, trạng thái cuối cùng khớp với số lần chẵn/lẻ. | 0 Console errors, trạng thái xác định. |
| **12. Multi-role Uniformity** | Phân quyền người dùng | Citizen vs PR vs Foreigner | Format che NRIC/FIN áp dụng nhất quán: 1 chữ cái đầu + 5 dấu sao + 3 số + 1 chữ cái cuối (ví dụ `*****123A`). | Đúng chuẩn Singapore NRIC/FIN masking policy. |

---

## 4. Error Handling & Visual Feedback

- **Chỉ báo lỗi hệ thống**: Trường danh tính Singpass là dữ liệu được cung cấp từ IdP Singpass / MockPass. Trường hợp API hồ sơ lỗi không tải được dữ liệu, trang hiển thị alert toàn cục:
  - Mã thông báo: `MSG-0808`
  - Nội dung: *"We could not update your details. Please try again."* hoặc *"Unable to load your profile details."*
- **Quy chuẩn thông báo**:
  - ⛔ **CẤM hiển thị raw key**: Tuyệt đối không hiển thị `features.parentProfile.identity.*` hoặc `undefined`.
  - **Visual Indicator**: Dữ liệu hiển thị với kiểu chữ `font-medium text-gray-900`, nhãn `text-sm text-gray-500`.
  - Nút toggle sử dụng biến thể secondary/ghost button, có focus ring chuẩn WCAG khi điều hướng bằng bàn phím.

---

## 5. JSON Fixtures Data Payload

```json
{
  "singpass_identity_fixtures": {
    "default_masked": {
      "full_name": "TAN WEI MING",
      "nric_masked": "*****321B",
      "nric_unmasked": "S7654321B",
      "residential_address": "BLK 210 JURONG EAST STREET 21 #05-12 SINGAPORE 600210",
      "expected_button_text": "Show NRIC"
    },
    "secondary_parent": {
      "full_name": "NGUYEN VAN MINH",
      "nric_masked": "*****123F",
      "nric_unmasked": "S7890123F",
      "residential_address": "BLK 105 BISHAN STREET 12 #10-45 SINGAPORE 570105",
      "expected_button_text": "Show NRIC"
    },
    "fin_holder": {
      "full_name": "K. SHANMUGAM",
      "nric_masked": "*****345H",
      "nric_unmasked": "G9012345H",
      "residential_address": "12 ORCHARD BOULEVARD #15-01 SINGAPORE 248641",
      "expected_button_text": "Show NRIC"
    }
  }
}
```
