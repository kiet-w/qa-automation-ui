# 💥 EduFAMS Destructive & Vulnerability Testing Suite

Bộ kiểm thử thâm nhập, phá hủy và kiểm tra biên cực đoan cho toàn bộ hệ thống EduFAMS (Steps 1 – 8).
Được thiết kế theo tiêu chuẩn `/combo-qa` và triển khai theo phương pháp `/combo-code` với sự tham gia của các Subagents chuyên trách.

## Cấu Trúc Các Phân Vùng Phá Hủy (Attack Zones)
- **Zone 1 (`zone1_financial_ledger_tests.py`):** Phá hủy tài chính, công nợ, trừ âm ví Edusave, nợ 0 đồng, double-billing (Bước 5 & 8).
- **Zone 2 (`zone2_sbfas_fas_tests.py`):** Phá hủy ma trận trợ cấp, ngân sách quỹ, hồi tố duyệt đơn, biên từ chối 14/15 ký tự (Bước 6 & 7).
- **Zone 3 (`zone3_fees_batches_tests.py`):** Đảo ngược ngày hiệu lực, trùng lặp biểu phí, batch thiếu feeComponentId (Bước 4 & 5).
- **Zone 4 (`zone4_rbac_viewas_tests.py`):** Lách luật kiểm toán Reason bằng khoảng trắng, SQLi/XSS, rò rỉ quyền liên trường (Bước 1, 2 & 3).

## Trình Điều Khiển Trực Quan
- **`run_master_destructive_suite.py`**: Chạy toàn bộ 25 ca test phá hủy có Live HUD banner trên trình duyệt thực tế.
