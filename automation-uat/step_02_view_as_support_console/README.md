# Phân Hệ UAT: Bước 2: Giả Lập Vai Trò Cán Bộ Trường Qua "View As" (/support-console)

Tài liệu ghi nhận chi tiết kịch bản, bộ định vị, công cụ thực thi trực quan (Visual Headed Automation) và báo cáo kiểm thử cho **Bước 2: View As Support Console** của Cổng Quản trị EduFAMS.

---

## 📌 1. Thông Tin Phiên Kiểm Thử

| Thông Tin | Giá Trị Chi Tiết |
| :--- | :--- |
| **Hạng Mục UAT** | **Bước 2: Giả Lập Vai Trò Cán Bộ Trường Qua "View As"** |
| **Môi Trường Target** | `https://admin.20-255-158-192.sslip.io` |
| **URL Chức Năng** | `/support-console` |
| **Vai Trò Đăng Nhập** | **Quản trị viên Bộ Giáo dục (MOEHQ / System Admin)** |
| **Tài Khoản Test** | `admin@IAM.edu.vn` |
| **Chế Độ Chạy** | Headed Browser (Hiển thị trực tiếp trên màn hình với Live HUD & Pacing `slow_mo=500ms`) |
| **Trạng Thái** | ✅ **HOÀN THÀNH TOÀN BỘ (8/8 Checkpoints PASS)** |

---

## 🚀 2. Hướng Dẫn Chạy Nhanh

```bash
# Chạy trực quan có giao diện trình duyệt và HUD trực tiếp:
.venv/bin/python automation-uat/step_02_view_as_support_console/run_step_02_tests.py --url https://admin.20-255-158-192.sslip.io --headed --slow-mo 500

# Chạy chế độ headless nền:
.venv/bin/python automation-uat/step_02_view_as_support_console/run_step_02_tests.py --url https://admin.20-255-158-192.sslip.io

# Chạy thông qua Pytest UAT suite:
pytest tests/uat/test_uat_2_view_as_support_console.py -v
```

---

## 📂 3. Cấu Trúc Thành Phần

- **`run_step_02_tests.py`**: Trình chạy test độc lập có Live HUD banner, làm nổi bật phần tử và tự động chụp 8 ảnh bằng chứng.
- **`STEP_02_REPORT.md`**: Báo cáo tổng hợp chi tiết kết quả thực thi 8 checkpoint.
- **`evidence/`**: Thư mục lưu trữ ảnh chụp màn hình minh chứng tại từng thời điểm kiểm toán.
- **`data/step_02_test_data.json`**: Tập dữ liệu test mẫu (Persona, User, BVA boundaries, Security payloads).
