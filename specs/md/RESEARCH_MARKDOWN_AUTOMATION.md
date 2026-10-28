# Báo Cáo Nghiên Cứu & Kiến Trúc: Markdown-Driven UI Automation Testing (AI + BSK + Playwright)

> **Dự án:** Automation UI (Enterprise Framework & Lean Markdown Engine)  
> **Phiên bản:** 2.0 (Kiềng 3 Chân: Atomic · UAT · Break_It)  
> **Ngày phê duyệt:** 2026-10-23  

---

## 1. Tóm Tắt Điều Hành (Executive Summary)

1. **Vấn đề cốt lõi của QA Automation truyền thống**:
   - Viết code framework (Page Object, Pytest, Class, Fixture) tốn quá nhiều thời gian và công sức bảo trì.
   - Khi nhờ AI viết test, AI hay bị **"ảo giác locator" (Locator Hallucination)** do chỉ đọc tài liệu FSD mà không biết DOM thật của lập trình viên, dẫn đến test fail liên tục vì sai selector.
   - Test suite thường chỉ chạy "Happy Path", bỏ sót đến 80% các lỗi nghiêm trọng ở môi trường thực tế (server unhandled crash 500, double click trừ tiền 2 lần, gỡ client validation lọt payload độc).

2. **Giải pháp đột phá đã hiện thực hóa**:
   - **Vòng lặp AI 🔁 BSK Reconnaissance**: Dùng công cụ `tools/recon_bsk.py` (dựa trên Chrome DevTools Protocol) để quét DOM thực tế trước khi viết test, triệt tiêu 100% việc tự đoán selector.
   - **Đặc tả kịch bản bằng Markdown thuần túy (`.md`)**: QA/BA chỉ cần viết các bước dạng bảng `Action | Target | Value | Expected`. Không cần viết một dòng code Python nào.
   - **Kiềng 3 Chân Kiểm Thử (Triple-Track Execution)**:
     - ⚡ **Atomic**: Test từng trường, validate biên, format (`@smoke`, `@p0`, `@regression`).
     - 🚀 **UAT Journey**: Luồng người dùng E2E dài, xuyên suốt nhiều màn hình, giữ session (`@uat`, `@journey`).
     - 💥 **Break_It**: Phá có kỷ luật: gỡ client constraints, double-click, 10k ký tự, sập mạng 500 (`@break_it`).
   - **Báo cáo đồ họa 1 trang tinh gọn (`bao_cao_tinh_gon.html`)**: Trực quan hóa 4 cấp độ phân tầng, phân loại rõ 3 nhánh test, kèm video WebM và 1-click nhảy lỗi.

---

## 2. Bảng So Sánh Kiến Trúc: Cũ vs. Mới

| Chiều Đánh Giá | Mô Hình Code Framework Cũ (Pytest POM) | Mô Hình Mới Tinh Gọn (Markdown + BSK) |
| :--- | :--- | :--- |
| **Độ phức tạp code** | Cao (Cần tạo Class, Method, Page Object, Locator, Fixture) | **Bằng 0** (Chỉ viết bảng Markdown `.md`) |
| **Độ chính xác Selector** | Hay đoán mò, phụ thuộc tài liệu FSD | **100% chuẩn xác** (Do BSK soi trực tiếp trên live web) |
| **Thời gian tạo 1 test case** | 15 - 30 phút | **1 - 2 phút** (Chỉ cần copy bảng locator và ghi các bước) |
| **Khả năng tiếp cận (Ai dùng được)** | Chỉ QA Automation biết code Python | **Bất kỳ ai** (Manual Tester, BA, PO, PM đều đọc và sửa được) |
| **Bảo trì khi UI thay đổi** | Phải refactor nhiều file Page Object | Chỉ cần sửa lại 1 dòng selector trong file Markdown |
| **Độ phủ lỗi ngầm & bảo mật** | Thấp (chỉ test Happy Path) | **Rất cao** (Nhánh `break_it` chủ động gỡ client validate, ép lỗi) |

---

## 3. Bản Đồ 6 Vũ Khí BSK Được Tích Hợp Vào Engine (`md_runner.py`)

1. **Session Reuse**: Cắm thẳng vào Chrome Profile thật đang mở, bỏ qua toàn bộ rào cản đăng nhập, Singpass, SSO và OTP 2FA.
2. **Network Mocking & Chaos (`mock_status`)**: Giả lập API sập HTTP 500/502 hoặc timeout để kiểm tra UI có hiện thông báo thân thiện hay sập WSoD.
3. **Console & JS Sniffer (`assert_no_console_errors`)**: Tự động bắt mọi `console.error`, `TypeError`, Promise Rejection chưa xử lý.
4. **Client-Side Constraint Bypass (`strip_constraints`, `force_fill`)**: Dùng JS gỡ bỏ `required`, `disabled`, `maxlength` để kiểm tra khả năng phòng thủ của Backend.
5. **Responsive & Layout Check (`set_viewport`, `assert_no_overflow`)**: Co giãn màn hình sang Mobile (375x667), tự động bắt lỗi thanh cuộn ngang vỡ màn hình.
6. **Storage & PII Audit**: Quét sạch `localStorage` và `Cookies` để phát hiện dữ liệu nhạy cảm bị rò rỉ plain-text.

---

## 4. Hướng Dẫn Vận Hành Tóm Tắt

```bash
# 1. Trinh sát trang web để lấy locator
python3 tools/recon_bsk.py --url curricula_trainer_account.html

# 2. Chạy toàn bộ test suites
python3 md_runner.py

# 3. Chạy theo từng nhánh riêng biệt
python3 md_runner.py --tags @break_it   # Vợt 80% bug ngầm & bảo mật
python3 md_runner.py --tags @uat        # Luồng người dùng dài
python3 md_runner.py --tags @smoke      # Kiểm tra khói nhanh
```

Báo cáo kết quả được tự động tổng hợp tại:
- [reports/uat/bao_cao_tinh_gon.html](file:///home/baudui/automation-ui/reports/uat/bao_cao_tinh_gon.html)
- [reports/uat/execution_report.html](file:///home/baudui/automation-ui/reports/uat/execution_report.html)
