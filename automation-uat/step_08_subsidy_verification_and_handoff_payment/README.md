# 📂 Bước 8: Kiểm Tra Kết Quả Giảm Trừ & Bàn Giao Thanh Toán (Kent ➔ Gavin / UAT-PAR-01)

> **Mô đun**: `Fees and payments` & `FAS assessment` (Giao thoa Kent R03 ➔ Gavin R09)  
> **Target URLs**:  
>   - Admin Portal: `https://admin.20-255-158-192.sslip.io` (`/fee-batches`, `/student-management/STU-001`, `/education-accounts`)  
>   - Parent E-Service Portal: `https://eservice.20-255-158-192.sslip.io` (`/accounts/STU-001/pay`, `/invoices`)  
> **Vai trò**: School Admin Kent (`admin@IAM.edu.vn`) & Parent Tester Gavin (Pham Van Duc / Singpass `S7654321B`)  
> **Tiêu chuẩn kiểm thử**: Pure Black-Box Testing / ISTQB Foundation & ISO/IEC/IEEE 29119-3  

---

## 📌 Tổng Quan Kịch Bản Nghiệp Vụ

Bộ kiểm thử Bước 8 kiểm chứng trọn vẹn quy trình đối soát cấn trừ trợ cấp và chu trình bàn giao thanh toán phụ huynh (End-to-End Cycle):
1. **Kiểm tra Cổng Trường (Admin Portal)**:
   - Sổ nợ (Student Ledger) và danh sách đợt phí (`/fee-batches`): Trạng thái Fee Batch đạt `Published`/`Completed`.
   - Bản ghi nợ (Student Charge): Chuyển trạng thái sang `PARTIALLY_SUBSIDIZED` (nếu miễn 60%) hoặc `SUBSIDIZED_PAID` (nếu miễn 100%).
   - Audit Link: Liên kết tham chiếu trực tiếp đến mã đề án trợ cấp (`SBF-01015 - Tier 1`) và mã đơn duyệt.
2. **Kiểm tra trực quan Cổng Dịch vụ Phụ huynh (E-Service Portal)**:
   - Đăng nhập Singpass chọn `S7654321B - PHAM VAN DUC`.
   - Truy cập chi tiết tài khoản học vụ con Liam Pham (`EDU-01001`), xác nhận NRIC che `*****854C` và số dư ví EA ban đầu `SGD 500.00`.
   - Bảng đối soát nợ học phí (`/accounts/STU-001/pay`): Đối chiếu các trường `Gross amount` (SGD 100.00), `Subsidy` (SGD 60.00), `Amount due / Net amount` (SGD 40.00).
3. **Biên Bản Bàn Giao Kiểm Thử (UAT Handoff Dossier to Gavin)**:
   - Đóng gói đủ 4 khối fixtures: Học sinh (Liam Pham / STU-001), Phụ huynh (`S7654321B`), Ví Edusave EA (EDU-01001, balance SGD 500.00), Khoản phí (Gross SGD 100, Net SGD 40).
   - Kích hoạt chốt chặn **Gate G1 Passed**.
4. **Gavin Thực Thi Ca Kiểm Thử UAT-PAR-01**:
   - Chọn khoản phí cần thanh toán (Net amount SGD 40.00).
   - Chọn phương thức thanh toán: `Education Account` (EA only).
   - Màn hình Review & Authorize: Xác nhận số tiền trừ ví EA SGD 40.00, số tiền Online SGD 0.00.
   - Nhấn `Authorize & pay`: Giao dịch thành công, số dư ví EA giảm xuống `SGD 460.00`, trạng thái hóa đơn chuyển `PAID`.
5. **Chốt Chặn An Toàn (Safety Gates G2 & G3)**:
   - **Gate G2 (Idempotency)**: Không bị trừ trùng tiền ví Edusave (No double debit).
   - **Gate G3 (Receipt Integrity)**: Phiếu thu xuất ra thể hiện rõ: Tiền gốc SGD 100.00, Miễn giảm SBFAS SGD 60.00, Thực thu SGD 40.00.

---

## 🚀 Hướng Dẫn Thực Thi

### 1. Chạy Trực Quan Trên Màn Hình (Visual Headed Mode với Live HUD Banner)
Chạy script độc lập mở trình duyệt trực tiếp, làm nổi bật phần tử và hiển thị HUD banner từng bước:
```bash
.venv/bin/python automation-uat/step_08_subsidy_verification_and_handoff_payment/run_step_08.py --headed --slow-mo 800 --hold 5
```

### 2. Chạy Bằng Pytest Suite
```bash
.venv/bin/pytest tests/uat/test_uat_8_subsidy_verification_and_handoff_payment.py -v
```

---

## 📁 Cấu Trúc Thư Mục Lưu Trữ

```
automation-uat/step_08_subsidy_verification_and_handoff_payment/
├── data/
│   └── step_08_data.json                  # Dữ liệu fixtures học sinh, phụ huynh, ví EA và kịch bản thanh toán
├── evidence/                              # Ảnh chụp màn hình độ phân giải cao tại 11 checkpoint
│   ├── 01_admin_fee_batches.png           # Checkpoint 1: Danh sách Fee Batches trạng thái Published
│   ├── 01_admin_student_detail.png        # Checkpoint 2: Hồ sơ học sinh Liam Pham & Ledger Admin
│   ├── 02_eservice_dashboard_wallets.png  # Checkpoint 3: Thẻ ví Edusave trên E-Service Dashboard
│   ├── 02_eservice_account_detail.png     # Checkpoint 4: Chi tiết tài khoản EDU-01001, NRIC che *****854C
│   ├── 02_eservice_charges_subsidy_table.png # Checkpoint 5: Bảng đối soát nợ Gross, Subsidy, Net
│   ├── 03_handoff_dossier_ready.png       # Checkpoint 6: Hồ sơ bàn giao Handoff Dossier Gate G1
│   ├── 04_gavin_charge_selected.png       # Checkpoint 7: Chọn khoản phí thanh toán
│   ├── 04_gavin_payment_methods.png       # Checkpoint 8: Chọn phương thức thanh toán Education Account
│   ├── 04_gavin_review_and_authorize.png  # Checkpoint 9: Màn hình Review & Authorize
│   ├── 04_gavin_payment_success.png       # Checkpoint 10: Thông báo thanh toán thành công (PAID)
│   └── 05_gate_g3_receipt.png             # Checkpoint 11: Phiếu thu điện tử đối soát 3 nguồn tiền
├── README.md                              # Tài liệu hướng dẫn sử dụng và nghiệp vụ
├── STEP_08_REPORT.md                      # Báo cáo tổng hợp chi tiết kết quả thực thi
└── run_step_08.py                         # Script visual runner với live HUD banner
```
