# 📂 Bước 7: Thẩm Định & Phê Duyệt Đơn Trợ Cấp SBFAS (UAT-SCH-03, UAT-SCH-03-N1 & UAT-035)

> **Mô đun**: `Financial Management` / `FAS Assessment`  
> **Target URL**: `https://admin.20-255-158-192.sslip.io/fas-applications` & `/moe-hq/fas-applications`  
> **Vai trò**: Cán bộ trường School Reviewer (`staff1@IAM.edu.vn`) & Cấp Bộ MOE HQ Observer (`admin@IAM.edu.vn`)  
> **Tiêu chuẩn kiểm thử**: Pure Black-Box Testing / ISTQB Foundation & ISO/IEC/IEEE 29119-3  

---

## 📌 Tổng Quan Kịch Bản Nghiệp Vụ

Bộ kiểm thử Bước 7 kiểm chứng trọn vẹn 4 chặng thẩm định và ra quyết định hỗ trợ tài chính cho học sinh trường Rosyth Primary School:
1. **Tìm kiếm & Lọc hồ sơ (`7.1`)**: Tìm kiếm và lọc danh sách theo `Pending School Review`, xác nhận học sinh Ethan Rahman (`APP-01004`).
2. **Thẩm định Tài chính Hộ gia đình (`7.2`)**: Kiểm tra tổng thu nhập $\text{GHI} = \$4,400.00 /month$, nhân khẩu $4$, và thu nhập bình quân $\text{PCI} = \$1,100.00 /month$. Rule Engine quốc gia chuyển hồ sơ về cấp trường xử lý (`Evaluating at school level.`). Nút `View documents` khả dụng xem chứng từ trực tuyến.
3. **Phê duyệt SBFAS Tier 1 (`7.3` — `UAT-SCH-03`)**: Gói trợ cấp trường Tier 1 (100% Fee Waiver) và Comment `"Eligible"`.
4. **Từ chối & Cổng Kiểm soát BVA (`7.4` — `UAT-SCH-03-N1`)**: Bắt buộc chọn Lý do VÀ nhập Remarks tối thiểu 15 ký tự. 14 ký tự bị khóa `disabled`; 15 ký tự được kích hoạt `enabled`.
5. **Ranh giới Phân quyền & Tính Bất biến (`Phần 4` — `UAT-035`)**: Cách ly dữ liệu liên trường (Cross-School Boundary) và Quyền hạn MOE HQ chỉ có quyền xem (Read-only, 0 nút Approve/Reject).

---

## 🚀 Hướng Dẫn Thực Thi

### 1. Chạy Trực Quan Trên Màn Hình (Visual Headed Mode với Live HUD Banner)
Chạy script độc lập mở trình duyệt trực tiếp, làm nổi bật phần tử và hiển thị HUD banner từng bước:
```bash
.venv/bin/python automation-uat/step_07_fas_assessment/run_step_07.py --headed --slow-mo 700 --hold 5
```

### 2. Chạy Bằng Pytest Suite (100% Chế độ Headed)
```bash
.venv/bin/pytest tests/uat/test_uat_7_fas_assessment.py -n 1 --headed -v
```

---

## 📁 Cấu Trúc Thư Mục Lưu Trữ

```
automation-uat/step_07_fas_assessment/
├── data/
│   └── step_07_data.json         # Dữ liệu tài khoản, hồ sơ học sinh và tham số validation
├── evidence/                     # Ảnh chụp màn hình độ phân giải cao tại 9 checkpoint
│   ├── cp01_school_login.png
│   ├── cp02_fas_applications_list.png
│   ├── cp03_filter_pending_row.png
│   ├── cp04_household_financials_review.png
│   ├── cp05_documents_and_beneficiaries.png
│   ├── cp06_approval_status_confirmed.png
│   ├── cp07_rejection_validation_gate.png
│   ├── cp08_cross_school_isolation.png
│   └── cp09_moe_hq_read_only.png
├── README.md                     # Tài liệu hướng dẫn sử dụng và nghiệp vụ
├── STEP_07_REPORT.md             # Báo cáo tổng hợp chi tiết kết quả thực thi
└── run_step_07.py                # Script chạy tự động hóa visual runner với HUD
```
