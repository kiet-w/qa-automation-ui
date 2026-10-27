# Feature: Curricula Adversarial & Resilience Testing (Break_It)

## 🔍 Locators đã xác minh qua BSK (Browser-Skill Reconnaissance)
| Tên Phần Tử | Nhãn Hiển Thị | Selector / ID Thực Tế | Kỹ Thuật Phá Tương Ứng |
| :--- | :--- | :--- | :--- |
| Ô nhập họ tên | Preferred name * | `#preferredName` | Strip `maxlength`, `force_fill` chuỗi XSS / Malformed |
| Nút Lưu thao tác | Save | `#saveBtn` | `dblclick` kiểm tra race condition, `strip_constraints` |
| Báo lỗi bắt buộc | This field is required. | `.error[data-for="preferredName"]` | Oracle: Server/Form phải chặn lỗi sau khi gỡ client constraints |
| Hộp thông báo thành công | Successfully saved | `#successBox` | Oracle: Không được xuất hiện khi submit payload lỗi |

---

## Scenario: TC-BRK-001 Strip Client Constraints and Verify Validation Defense @break_it @p0
| Step | Action | Target / Selector | Value | Expected / Assertion |
| :--- | :--- | :--- | :--- | :--- |
| 1 | open | curricula_trainer_account.html | | Form mở thành công |
| 2 | strip_constraints | | | Toàn bộ required, maxlength, disabled bị gỡ bỏ |
| 3 | click | #saveBtn | | Submit dữ liệu khi không còn rào cản client |
| 4 | assert_visible | .error[data-for="preferredName"] | | Hệ thống vẫn phải từ chối an toàn với thông báo lỗi |
| 5 | assert_not_visible | #successBox | | Không được lưu dữ liệu sai vào hệ thống |

## Scenario: TC-BRK-002 Force Set Malformed String and Double Click Save @break_it @concurrency
| Step | Action | Target / Selector | Value | Expected / Assertion |
| :--- | :--- | :--- | :--- | :--- |
| 1 | open | curricula_trainer_account.html | | Form mở thành công |
| 2 | force_fill | #preferredName | <script>alert("XSS")</script> | Bơm chuỗi độc hại qua prototype setter |
| 3 | dblclick | #saveBtn | | Double click nút Submit mô phỏng race condition |
| 4 | assert_no_console_errors | | | 0 Uncaught JS Exceptions trong runtime |

## Scenario: TC-BRK-003 Mobile Viewport and Overflow Integrity Check @break_it @layout
| Step | Action | Target / Selector | Value | Expected / Assertion |
| :--- | :--- | :--- | :--- | :--- |
| 1 | set_viewport | 375x667 | | Co giãn kích thước sang Mobile Viewport |
| 2 | open | curricula_trainer_account.html | | |
| 3 | assert_no_overflow | | | Không xuất hiện thanh cuộn ngang vỡ màn hình |
| 4 | assert_visible | #saveBtn | | Nút Save vẫn hiển thị và tương tác được |
