# 🎓 Bước 6: Cấu hình Gói Trợ cấp Trường SBFAS (UAT-SCH-02 & UAT-SCH-02-N1)

Thư mục chứa toàn bộ kịch bản tự động hóa, dữ liệu kiểm thử và công cụ thực thi trực quan trên trình duyệt (Headed Mode) cho **Bước 6: Cấu hình Gói Trợ cấp Trường SBFAS**.

---

## 📂 Cấu Trúc Thư Mục

```
step_06_sbfas_scheme_configuration/
├── data/
│   └── step_06_data.json         # Tập dữ liệu mẫu (Tier 1, Dates, Budget, GHI/PCI, Add fee, N1 Conflict)
├── evidence/                     # Thư mục lưu 9 ảnh chụp màn hình bằng chứng thực tế
├── README.md                     # Hướng dẫn chi tiết & thao tác chạy
├── run_step_06.py                # Script chạy tự động với HUD banner trực quan và highlight phần tử
└── STEP_06_REPORT.md             # Báo cáo nghiệm thu chi tiết kết quả chạy
```

---

## 🎯 Phạm Vi Nghiệp Vụ & Kiểm Thử

| Mã Kịch Bản | Tiêu Đề Nghiệp Vụ | Thao Tác Trọng Tâm | Kỳ Vọng Nghiệm Thu |
| :--- | :--- | :--- | :--- |
| **`UAT-SCH-02` (Phần 1)** | **Tạo & Xuất bản Đề án Tier 1** | Điền Wizard 4 bước: General, Eligibility, Subsidy Matrix, Review $\rightarrow$ Publish. | Cấp mã `SBF-xxxxx` tự động, chuyển trạng thái `Published`/`Active`, chuyển cấu hình sang Read-only. |
| **`UAT-SCH-02` (Phần 2)** | **Thêm Thành phần Phí vào Đề án đã Xuất bản** | Menu Actions `...` $\rightarrow$ `Add fee` $\rightarrow$ Chọn khoản phí mới & nhập % các khối lớp $\rightarrow$ `Add fee`. | Thành phần phí mới được bổ sung vào ma trận, các cột phí cũ giữ nguyên. |
| **`UAT-SCH-02-N1` (Lần 1)** | **Kiểm thử Tiêu cực Chặn Trùng Tên** | Nhập trùng tên `Tier 1` đã xuất bản $\rightarrow$ Bấm `Publish` ở Bước 4. | Chặn xuất bản, giữ nguyên giao diện Review, hiển thị Alert đỏ `Unable to create scheme: A scheme with this name already exists for this school.` |
| **`UAT-SCH-02-N1` (Lần 2)** | **Khôi phục Hợp lệ & Đổi Tên Tier 2** | Bấm Back về Bước 1, đổi tên thành `Tier 2` $\rightarrow$ Nhấn `Publish`. | Xuất bản thành công, danh sách hiển thị đồng thời cả 2 đề án `Tier 1` và `Tier 2`. |
| **Validation BVA** | **Kiểm tra Biên Ngày & Trần Thu nhập** | Thử ngày `Effective from` $\le$ `Open to` và bỏ trống ô `To *` của GHI/PCI. | Hệ thống chặn chuyển bước và kích hoạt cờ validation kèm cảnh báo tương ứng. |

---

## 🚀 Hướng Dẫn Chạy Trên Trình Duyệt Để Quan Sát (Headed Mode)

Chạy lệnh sau từ thư mục gốc dự án:

```bash
# Chạy trực quan có giao diện mở trình duyệt (slow-mo 600ms, giữ trình duyệt 15s sau khi hoàn tất)
.venv/bin/python automation-uat/step_06_sbfas_scheme_configuration/run_step_06.py --headed --slow-mo 600 --hold 15

# Hoặc chạy kiểm thử chuẩn Pytest
.venv/bin/python -m pytest tests/uat/test_uat_6_sbfas_scheme_configuration.py -v -n 0
```
