# Feature: Curricula UI 🔁 API Integration & Contract Verification

## 🔍 Locators đã xác minh qua BSK (Browser-Skill Reconnaissance)
| Tên Phần Tử | Nhãn Hiển Thị | Selector / ID Thực Tế | Loại Tích Hợp |
| :--- | :--- | :--- | :--- |
| Ô nhập họ tên | Preferred name * | `#preferredName` | Bắn dữ liệu lên endpoint `/api/trainers` |
| Nút Lưu thao tác | Save | `#saveBtn` | Kích hoạt HTTP POST request |
| Hộp thông báo thành công | Successfully saved | `#successBox` | Hiển thị khi API trả về HTTP 200 OK |
| Báo lỗi bắt buộc | This field is required. | `.error[data-for="preferredName"]` | Hiển thị khi API trả về HTTP 400 Bad Request |

---

## Scenario: TC-INT-001 Verify UI Resilience on Backend API Error 500 @integration @api
| Step | Action | Target / Selector | Value | Expected / Assertion |
| :--- | :--- | :--- | :--- | :--- |
| 1 | open | curricula_trainer_account.html | | Form mở thành công |
| 2 | mock_status | **/api/** | 500 | Giả lập toàn bộ API Backend sập HTTP 500 |
| 3 | fill | #preferredName | Dr. Robert Oppenheimer | Điền dữ liệu hợp lệ |
| 4 | click | #saveBtn | | Bấm Submit khi server đang lỗi |
| 5 | assert_visible | #saveBtn | | Giao diện không bị White Screen of Death (WSoD) |
| 6 | assert_no_console_errors | | | Không phát sinh unhandled crash trong console |

## Scenario: TC-INT-002 Verify UI Contract on Mocked API Success 200 @integration @contract
| Step | Action | Target / Selector | Value | Expected / Assertion |
| :--- | :--- | :--- | :--- | :--- |
| 1 | open | curricula_trainer_account.html | | Form mở thành công |
| 2 | mock_response | **/api/trainers** | {"status": "success", "id": "TR-2026-001"} | Giả lập API Backend phản hồi thành công JSON |
| 3 | fill | #preferredName | Dr. Alan Turing | |
| 4 | click | #saveBtn | | Submit dữ liệu |
| 5 | assert_visible | #saveBtn | | Nút Save vẫn hoạt động ổn định |
| 6 | assert_no_console_errors | | | 0 lỗi đỏ runtime trong console |
