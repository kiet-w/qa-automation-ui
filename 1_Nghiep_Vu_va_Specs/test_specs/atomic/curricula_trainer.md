# Feature: Curricula Trainer Account Management

## 🔍 Locators đã xác minh qua BSK (Browser-Skill Reconnaissance)
| Tên Phần Tử | Nhãn Hiển Thị | Selector / ID Thực Tế | Loại Phần Tử |
| :--- | :--- | :--- | :--- |
| Ô nhập họ tên | Preferred name * | `#preferredName` | `<input type="text">` |
| Nút Lưu | Save | `#saveBtn` | `<button class="primary">` |
| Nút Hủy | Cancel | `#cancelBtn` | `<button>` |
| Tiêu đề form | Personal information | `.section-title` | `<div>` |
| Báo lỗi bắt buộc | This field is required. | `.error[data-for="preferredName"]` | `<div>` |

---

## Scenario: TC-001 Verify Form Validation on Empty Submit @smoke @p0
- Open: curricula_trainer_account.html
- Assert: Title contains "Curricula - Create Trainer Account"
- Assert: "Personal information" is visible
- Click: #saveBtn
- Assert: "This field is required." is visible

## Scenario: TC-002 Preferred Name Input and Boundary State @regression @p1
| Step | Action | Target / Selector | Value | Expected / Assertion |
| :--- | :--- | :--- | :--- | :--- |
| 1 | open | curricula_trainer_account.html | | Title contains "Curricula" |
| 2 | fill | #preferredName | Master John Doe | |
| 3 | assert | #preferredName | | is visible |
| 4 | assert | #cancelBtn | | is enabled |
| 5 | click | #cancelBtn | | |
