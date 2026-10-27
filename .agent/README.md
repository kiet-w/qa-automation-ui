# `.agent` — Intent Router and Rule Governance

Thư mục này chứa các chỉ dẫn chuyên sâu được nạp theo intent. [`AGENTS.md`](../AGENTS.md) là master constitution; rule module chỉ được mở rộng chi tiết, không được ghi đè hoặc mâu thuẫn với master.

## Rule router

| Intent | Rule phải đọc đầy đủ |
| :--- | :--- |
| Thiết kế test case, test màn hình mới, chuyển testcase sang code | [`rules/01-two-stage-workflow.md`](rules/01-two-stage-workflow.md) |
| Field validation, form lifecycle, UI health, PII | [`rules/02-field-test-matrix.md`](rules/02-field-test-matrix.md) |
| Failure triage, resilience, adversarial/break-it | [`rules/03-failure-triage-adversarial.md`](rules/03-failure-triage-adversarial.md) |
| Page Object, test code, evidence, spec lookup | [`rules/04-automation-coding-standards.md`](rules/04-automation-coding-standards.md) |

Nếu task chạm nhiều intent, đọc tất cả rule liên quan. Không đọc một phần rồi hành động.

## Instruction precedence

1. Yêu cầu trực tiếp và hợp lệ của user.
2. `AGENTS.md` — master constitution và 12 invariants.
3. Rule module được route theo intent.
4. README/ADR/tài liệu lịch sử.

Khi có mâu thuẫn, dừng việc mở rộng giả định, ghi rõ conflict hoặc `SPEC GAP`, rồi ưu tiên nguồn ở cấp cao hơn.

## Canonical path contract

Ba folder số ở root là navigation views bằng symlink:

- `1_Nghiep_Vu_va_Specs/`
- `2_Code_Automation/`
- `3_Bao_Cao_va_Ket_Qua/`

Rule, code và command luôn dùng canonical paths như `specs/`, `tests/`, `reports/`. Không dùng navigation paths làm Python imports, output path hoặc nguồn dữ liệu độc lập. Không xóa canonical root targets vì thấy shortcut cùng tên trong folder nhóm.

## Global constants shared by all rules

- Test-case schema: 20 cột, một tab, có `Steps Test`.
- New testcase status: `Not Run`; `Actual Result` và evidence để trống trước execution.
- Coverage: 5 pillars + live DOM + coverage matrix trước khi sinh case.
- UI/BSK inventory đã thu thập: `specs/ui_bsk/`; `tools/` chỉ chứa script recon. Alias `locator-bsk` chỉ dùng tương thích.
- Runtime: `-n 3`, `--video=off` mặc định.
- Deep visual debugging: user có thể bật `--video=retain-on-failure`.
- AI không tự chạy `pytest`, `run_tests.py` hoặc test scripts.
- `run_tests.py` hiện nhận test path/options trực tiếp; không dùng `--ticket` cho đến khi runner triển khai parser đó.
- Repository root chuẩn: `/home/baudui/Projects/automation-ui`.
- `copy/` và shortcut trỏ tới nó là read-only tuyệt đối.

## Rule maintenance checklist

Khi cập nhật rule:

- Không hạ chuẩn hoặc vô hiệu hóa invariant trong `AGENTS.md`.
- Không ghi absolute link tới checkout cũ khi relative link đủ dùng.
- Không mô tả tính năng chưa tồn tại trong code như một hành vi tự động.
- Phân biệt rõ default behavior và opt-in behavior.
- Lệnh test chỉ được ghi dưới nhãn “User tự chạy”.
- Sau cập nhật, rà các chuỗi stale: `19 cột`, `-n auto`, `--ticket`, auto video, auto deploy và đường dẫn checkout cũ.
