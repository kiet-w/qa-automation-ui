from pathlib import Path

def update_md():
    base_dir = Path("/home/baudui/automation-ui/testcases/fs08/fs08-parent-profile")
    table_file = base_dir / "table_19col.md"
    out_file = base_dir / "TC_FS08_Parent_Profile.md"

    with open(table_file, "r", encoding="utf-8") as f:
        table_content = f.read()

    md_content = """# BỘ ĐẶC TẢ TEST CASE CHUẨN GOOGLE SHEET (19 CỘT) — FS08: MY DETAILS / PARENT PROFILE
## MOE SINGAPORE EDUSAVE E-SERVICE PORTAL (`http://localhost:5174/profile`)

> **Quy chuẩn Format**: Bám sát 100% định dạng bảng tính Google Sheet Tender AvePoint:  
> [Google Sheet Reference (gid=1612531667)](https://docs.google.com/spreadsheets/d/1ViSPLgggDsBI13SCPjfO_i0QoyUXy35A/edit?gid=1612531667#gid=1612531667)
> 
> **File Excel Đi Kèm**: [`TC_FS08_Parent_Profile.xlsx`](TC_FS08_Parent_Profile.xlsx)  
> **Nguyên tắc Invariant 6**: Zero Assumptions — 100% kịch bản, quy tắc biên, mã lỗi đối soát trực tiếp từ FSD, Quyết định `D-20`/`D-28` và DOM thật từ BSK.  
> **Mục tiêu**: Làm tài liệu Single Source of Truth cho **AI Coding Agents** tự động đọc và sinh test automation Playwright/pytest mà không bị lệch chuẩn.

---

## 1. MA TRẬN TEST CASE ĐẦY ĐỦ 19 CỘT CHUẨN GOOGLE SHEET

""" + table_content + """

---

## 2. BẢNG LOCATOR BSK ĐÃ XÁC MINH TRÊN LIVE DOM (BSK RECON LOCATORS)

AI Coding Agent BẮT BUỘC sử dụng các locator đã trinh sát thực tế này từ `tools/recon_bsk.py` và [`ParentProfilePage`](file:///home/baudui/automation-ui/pages/fs08/parent_profile_page.py):

| Tên Phần Tử | Selector Playwright Chuẩn | Loại Element | Ràng Buộc / Ghi Chú Kỹ Thuật |
| :--- | :--- | :--- | :--- |
| **Tiêu đề trang** | `h1:has-text('My Profile'), h2:has-text('My Profile')` | `<h1> / <h2>` | Hiển thị tiêu đề trang profile |
| **Full Name** | `dt:has-text('Full Name') + dd, [data-testid='full-name']` | `<dd> / <span>` | Read-only tĩnh, lấy từ SingPass MyInfo |
| **Residential Address** | `dt:has-text('Residential') + dd, [data-testid='residential-address']` | `<dd> / <span>` | Read-only tĩnh theo Quyết định `D-20` (Không có thẻ input) |
| **NRIC Display** | `dt:has-text('NRIC') + dd, [data-testid='nric']` | `<dd> / <span>` | Mặc định che mặt nạ dạng `*****123F` |
| **Show NRIC Button** | `button:has-text("Show NRIC")` | `<button>` | Bấm để hiện đầy đủ số NRIC |
| **Hide NRIC Button** | `button:has-text("Hide NRIC")` | `<button>` | Bấm để che lại số NRIC |
| **Update Details Button** | `button:has-text("Update details")` | `<button>` | Chuyển View Mode -> Edit Mode |
| **Mobile Number Input** | `input[name="phoneNumber"]` | `<input type="tel">` | Bắt buộc, 8 chữ số đầu 6, 8, 9 |
| **Email Address Input** | `input[name="email"]` | `<input type="email">` | Bắt buộc, RFC 5322, <= 150 ký tự |
| **Mailing Block Input** | `input[name="mailingBlock"]` | `<input type="text">` | Tùy chọn, tối đa 20 ký tự |
| **Mailing Street Input** | `input[name="mailingStreet"]` | `<input type="text">` | Bắt buộc, tối đa 100 ký tự |
| **Mailing Unit Input** | `input[name="mailingUnit"]` | `<input type="text">` | Tùy chọn, tối đa 20 ký tự |
| **Mailing Postal Code** | `input[name="mailingPostalCode"]` | `<input type="text">` | Bắt buộc, đúng 6 chữ số Singapore |
| **Mailing Country Input**| `input[name="mailingCountry"]` | `<input type="text">` | Bắt buộc, tối đa 100 ký tự |
| **Pristine State Hint** | `p:has-text("Make a change to enable saving.")` | `<p>` | Hiển thị khi form chưa có thay đổi |
| **Save Changes Button** | `button[type="submit"]:has-text("Save changes")` | `<button>` | `disabled=true` khi chưa sửa (Pristine) |
| **Cancel Button** | `button:has-text("Cancel")` | `<button>` | Hủy thay đổi, hoàn nguyên View Mode |
| **Confirm Dialog** | `div[role="alertdialog"]` | `<div>` | Modal xác nhận trước khi gọi mutation API |
| **Dialog Keep Editing** | `div[role="alertdialog"] button:has-text("Keep editing")` | `<button>` | Đóng modal, giữ nguyên form dirty |
| **Dialog Confirm Save** | `div[role="alertdialog"] button:has-text("Save changes")` | `<button>` | Gửi mutation lưu dữ liệu vào DB |
| **Inline Error Alert** | `div[role="alert"], p[role="alert"], p[class*="error"]` | `<p> / <div>` | Hiển thị mã lỗi validation (`MSG-0805`, `MSG-0806`, `MSG-0001`) |
| **Success Toast** | `div[role="status"], div[role="alert"], div.toast` | `<div>` | Hiển thị thông báo `MSG-0807` màu xanh |

---

## 3. FIXTURE DỮ LIỆU KIỂM THỬ (TEST DATA FIXTURES)

```json
{
  "valid_baseline": {
    "fullName": "TAN WEI MING",
    "nric": "S1234123F",
    "phoneNumber": "91234567",
    "email": "weiming.tan@example.sg",
    "mailingBlock": "Blk 123",
    "mailingStreet": "Ang Mo Kio Ave 3",
    "mailingUnit": "#08-1234",
    "mailingPostalCode": "560123",
    "mailingCountry": "Singapore"
  },
  "valid_mutation": {
    "phoneNumber": "98887777",
    "email": "fa.new@example.sg",
    "mailingBlock": "Blk 9",
    "mailingStreet": "Verde Walk",
    "mailingUnit": "#02-01",
    "mailingPostalCode": "650009",
    "mailingCountry": "Singapore"
  },
  "phone_ep_valid": ["61234567", "81234567", "91234567"],
  "phone_ep_invalid": ["71234567", "51234567", "9123456", "912345678", "9123abcd", "+6591234567"],
  "email_invalid_syntax": ["nameexample.com", "name@", "@example.com", "name@example", "name @example.com"],
  "bva_boundaries": {
    "email_150": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@example.com",
    "email_151": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@example.com",
    "block_20": "BBBBBBBBBBBBBBBBBBBB",
    "block_21": "BBBBBBBBBBBBBBBBBBBBB",
    "street_100": "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
    "street_101": "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
    "postal_valid": "650009",
    "postal_invalid": ["65000", "6500091", "65A009"]
  },
  "security_payloads": {
    "xss_script": "<script>alert('XSS')</script>",
    "tampering_readonly": {
      "fullName": "HACKED_NAME",
      "nric": "S9999999Z",
      "residentialAddress": "HACKED_RESIDENTIAL"
    }
  }
}
```

---

## 4. HƯỚNG DẪN THỰC THI CHO AI CODING AGENTS

Khi thực hiện sinh code kiểm thử tự động, AI Agent tuân thủ các quy tắc sau:
1. **Thư mục thực thi**: Luôn đứng tại thư mục gốc `/home/baudui/automation-ui` (KHÔNG ĐƯỢC `cd copy`).
2. **Kế thừa Page Object**: Import và sử dụng trực tiếp [`ParentProfilePage`](file:///home/baudui/automation-ui/pages/fs08/parent_profile_page.py).
3. **Phân loại file test**:
   * **Đơn Component**: `tests/fs08/fs08-parent-profile/test_atomic_parent_profile_components.py`
   * **Giữa Nhiều Component / Form <-> API**: `tests/fs08/fs08-parent-profile/test_integration_parent_profile_components.py`
   * **UAT / Security / Multi-Child**: `tests/fs08/test_ts03_parent_profile.py`
4. **Lệnh chạy kiểm thử chuẩn**:
   * `.venv/bin/pytest tests/fs08/fs08-parent-profile/ -v`
   * Báo cáo ExtentReport & Video tại: `reports/fs08/fs08-parent-profile/execution_report.html`
"""

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[+] Successfully written {out_file}")

if __name__ == "__main__":
    update_md()
