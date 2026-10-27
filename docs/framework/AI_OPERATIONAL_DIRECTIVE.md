# CHỈ THỊ HÀNH ĐỘNG DÀNH CHO AI: KHI ĐƯỢC YÊU CẦU TEST BẤT KỲ URL NÀO

> **Áp dụng cho mọi prompt dạng**:  
> `unit test cho cái trang này http://localhost:5174/profile /combo-qa thực hiện đầy đủ và chi tiết`

---

## 🚫 2 ĐIỀU CẤM KỴ TUYỆT ĐỐI (ZERO VIOLATIONS)

1. **CẤM PHÂN TÍCH SOURCE CODE**:
   - Tuyệt đối **KHÔNG** mở thư mục `copy/` hoặc các file `.tsx`, `.jsx`, `.ts`, `.js` của ứng dụng để tìm selector, ID hay suy diễn logic!
   - QA Automation là kiểm thử **Black-box 100% trên giao diện người dùng**. Mọi suy đoán từ code đều vi phạm nguyên tắc Zero Assumptions.
2. **BSK KHÔNG PHẢI TEST RUNNER**:
   - BSK **CHỈ CÓ MỘT VAI TRÒ DUY NHẤT LÀ SCAN LOCATOR / INSPECT DOM**.
   - Tuyệt đối **KHÔNG** dùng lệnh BSK (`bsk click`, `bsk type`, `bsk eval`) để chạy test case! Việc thực thi kiểm thử thuộc về **Playwright Python (`md_runner.py`)**.

---

## 🧭 QUY TRÌNH 4 BƯỚC CHUẨN MỰC BẮT BUỘC AI PHẢI LÀM

### Bước 1: Trinh sát DOM bằng BSK để lấy Selector thật
Chạy ngay lệnh sau trên terminal (thay thế URL mục tiêu):
```bash
python3 tools/recon_bsk.py --url http://localhost:5174/profile
```
Hoặc dùng session BSK để snapshot cây Accessibility:
```bash
SESSION=$(bsk session start --browser dfdc1a70 --json | jq -r .session_id)
bsk navigate "http://localhost:5174/profile" --session "$SESSION"
bsk snapshot --session "$SESSION"
bsk session stop "$SESSION"
```
👉 Kết quả thu được là cây DOM thực tế (Ví dụ: `button "Sign in with Singpass"`).

---

### Bước 2: AI lấy bảng Locator từ BSK và viết kịch bản Markdown (.md)
Tùy vào từ khóa trong yêu cầu của người dùng, tạo file `.md` vào đúng 1 trong 4 thư mục:

| Yêu cầu của người dùng | Thư mục lưu file | Loại kiểm thử | Bản chất kỹ thuật & Nhãn Tag |
| :--- | :--- | :--- | :--- |
| **"Unit test"** trên UI | `test_specs/atomic/<feature>.md` | **ĐƠN COMPONENT** | Kiểm tra riêng 1 component độc lập: validate rỗng, regex, maxlength, disabled (`@smoke @p0 @atomic`) |
| **"Integration test"** | `test_specs/integration/<feature>.md` | **TƯƠNG TÁC GIỮA CÁC COMPONENT** | • **1 Comp ➔ 1 Comp**: Chọn Country A ➔ hiện Input B<br>• **1 Comp ➔ Nhiều Comp**: Tick "Chọn tất cả" ➔ tick 10 dòng + bật nút<br>• **Form 🔁 API**: Bắt payload, mock status 200/400/500 (`@integration @api`) |
| **"UAT / Luồng dài"** | `test_specs/uat/<feature>.md` | **HÀNH TRÌNH NGƯỜI DÙNG** | Đi xuyên suốt nhiều màn hình/trang, giữ session liên tục (`@uat @journey`) |
| **"Break_It / Phá"** | `test_specs/break_it/<feature>.md` | **THỬ THÁCH ĐỘ BỀN** | Gỡ client constraints, double-click, XSS, 500 chaos (`@break_it`) |

**Cấu trúc mẫu của file `.md`**:
```markdown
# Feature: Tên Tính Năng Cần Test

## 🔍 Locators đã xác minh qua BSK (Browser-Skill Reconnaissance)
| Tên Phần Tử | Nhãn Hiển Thị | Selector / ID Thực Tế | Loại Phần Tử |
| :--- | :--- | :--- | :--- |
| Nút Đăng nhập Singpass | Sign in with Singpass | `button:has-text("Sign in with Singpass")` | `<button>` |

---

## Scenario: TC-001 Kiểm tra hiển thị nút đăng nhập Singpass @smoke @p0 @atomic
| Step | Action | Target / Selector | Value | Expected / Assertion |
| :--- | :--- | :--- | :--- | :--- |
| 1 | open | http://localhost:5174/profile | | Tự động chuyển tới trang đăng nhập |
| 2 | assert_visible | button:has-text("Sign in with Singpass") | | Nút đăng nhập hiển thị đầy đủ |
| 3 | assert_no_console_errors | | | 0 lỗi đỏ runtime trong console |
```

---

### Bước 3: Thực thi kịch bản bằng Playwright Python Engine
Chạy engine Playwright Python của dự án:
```bash
# Chạy toàn bộ
python3 md_runner.py

# Hoặc chỉ chạy riêng file vừa tạo
python3 md_runner.py test_specs/atomic/<feature>.md
```
👉 Playwright sẽ tự động:
- Auto-wait thông minh
- Thao tác click, fill, assert
- Quay video WebM HD từng bài test
- Chụp ảnh màn hình khi có lỗi

---

### Bước 4: Trình bày kết quả và báo cáo cho người dùng
Báo cáo HTML 1 trang đã được tự động sinh tại:
- [reports/uat/bao_cao_tinh_gon.html](file:///home/baudui/automation-ui/reports/uat/bao_cao_tinh_gon.html)

AI thông báo kết quả gồm:
- Số lượng test case đã chạy, Pass/Fail.
- Thời gian chạy (giây).
- Link mở video WebM và báo cáo HTML.
