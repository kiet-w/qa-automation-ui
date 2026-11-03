# Step 05: Đợt Thu Phí & Xuất Bản Công Nợ (Fee Batches & Publication)

> **Mô đun:** `Financial Management` / `Fee Batches & Student Charges`  
> **Kịch bản UAT:** `UAT-021` (Preview and publish fees once) & `UAT-MOE-01` (Publish fee publication batch)  
> **Target:** `https://admin.20-255-158-192.sslip.io` & `https://eservice.20-255-158-192.sslip.io`  

---

## 🚀 1. Lệnh Thực Thi Trực Quan (Headed Browser Mode)

Chạy runner trực tiếp có hiển thị cửa sổ trình duyệt, thanh HUD thông báo nổi và chớp sáng (highlight) các nút thao tác:

```bash
DISPLAY=:0 .venv/bin/python automation-uat/step_05_fee_batches_and_publication/run_step_05.py --headed --slow-mo 600 --hold 30
```

Các tham số tùy chọn:
- `--headed`: Bật giao diện trình duyệt trực quan.
- `--slow-mo 600`: Làm chậm mỗi thao tác 600ms để người dùng theo dõi rõ nét.
- `--hold 30`: Giữ trình duyệt mở trong 30 giây sau khi chạy xong để quan sát kết quả cuối cùng.
- `--url`: Địa chỉ Admin Portal (mặc định: `https://admin.20-255-158-192.sslip.io`).
- `--eservice-url`: Địa chỉ Parent Portal (mặc định: `https://eservice.20-255-158-192.sslip.io`).

---

## 📋 2. 8 Checkpoints Nghiệp Vụ Được Kiểm Chứng

1. **CP-01:** Prerequisite Warning khi mở `/fee-batches/new` thiếu tham số `feeComponentId`.
2. **CP-02:** Tạo Thành phần phí & Biểu phí Fixed Amount $100.00 SGD làm nguồn phát hành.
3. **CP-03:** Bấm nút *'Publish batch from this Fee Component'* chuyển tiếp sang form tạo đợt thu.
4. **CP-04:** BVA Validation ngày tháng (`Period end < Period start` hoặc `Period start` trong quá khứ).
5. **CP-05:** Tạo Đợt Thu Phí Hợp Lệ ở trạng thái **`Draft`**.
6. **CP-06:** Kiểm tra Student Charge Preview cho học sinh Liam Pham & Tiêu chí Âm tính (**Negative Oracle**: Preview không sinh nợ thật).
7. **CP-07:** Xuất Bản Đợt Phí (Publish) $\rightarrow$ **`Completed`** $\rightarrow$ Ghi nhận bản ghi nợ chính thức **`POSTED`**.
8. **CP-08:** Mở Cổng Phụ huynh E-Service Singpass (Pham Van Duc) kiểm chứng hiển thị học sinh và ví học vụ sẵn sàng bàn giao cho Gavin (**`UAT-PAR-01`**).
