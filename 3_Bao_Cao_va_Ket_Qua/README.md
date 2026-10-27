# Nhóm 3 — Báo cáo và Kết quả

Thư mục điều hướng cho report engine, runtime output, tài liệu bàn giao và tài sản lịch sử.

| Shortcut | Nội dung | Quy tắc |
| :--- | :--- | :--- |
| `reporting/` | Source code của offline report engine | Không trộn với output thực thi. |
| `reports/` | Runtime reports, screenshots, evidence và test-results | Được `.gitignore` loại trừ. |
| `docs/` | Framework docs, defect docs, manuals và diagrams | Tài liệu cần version control. |
| `archive/` | Snapshot và deliverable lịch sử | Không dùng làm runtime input. |
| `generate_report.py` | CLI sinh report từ JSON | Không chạy lại test. |
| `generate_enterprise_report.py` | Enterprise report CLI | Giữ tương thích với workflow cũ. |

Các mục trong thư mục này là shortcut tới vị trí chuẩn ở repository root. Evidence thật nằm dưới `reports/`, còn tài liệu cần commit nằm dưới `docs/`.
