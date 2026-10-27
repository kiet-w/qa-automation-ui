# Repository Structure and Placement Rules

Tài liệu này là bản đồ chính thức để đặt file trong repository. `AGENTS.md` vẫn là nguồn quy tắc cao nhất; tài liệu này chỉ diễn giải cấu trúc thư mục và đường dẫn đích.

## 1. Cây thư mục chuẩn

```text
automation-ui/
├── .agent/rules/                     # Quy tắc tác nghiệp theo intent
├── copy/                             # READ-ONLY: mã nguồn sản phẩm công ty
├── specs/                            # BR, AC, FSD và component specifications
│   ├── raw/                          # Tài liệu nguồn chưa chuyển đổi
│   ├── md/                           # Tài liệu Markdown dùng để tra cứu
│   ├── component_specs/              # Atomic validation, integration flow, error catalog
│   └── validation_rules/             # Validation rules theo phân hệ
├── testcases/                        # Test-case source of truth theo module/ticket
├── test_specs/                       # Lean Markdown specs: atomic/integration/uat/break_it
├── uat/                              # Kịch bản UAT phân tách theo phân hệ
│   ├── master/                       # Master plan và master workbook
│   └── r<xx>/                        # Tài sản riêng của từng phân hệ
├── pages/                            # Page Objects và page-level components
├── components/                       # UI widgets dùng chung giữa nhiều page
├── core/                             # Pytest plugins và framework runtime
├── data/                             # Fixtures, JSON test data và mock assets
├── tests/                            # Automation suites theo module/component
├── reporting/                        # Mã nguồn engine sinh báo cáo
├── reports/                          # Kết quả chạy và evidence, không phải source code
│   ├── defects/evidence/             # Ảnh bằng chứng lỗi và bản tối ưu
│   ├── test-results/                 # Raw artifacts theo RUN_ID
│   │   └── legacy-root/              # Artifacts cũ từng nằm ở root/test-results
│   └── uat/r<xx>/                    # Báo cáo UAT theo phân hệ
├── tools/                            # Công cụ hỗ trợ, không chứa test suite
│   ├── env/                          # Quản lý môi trường
│   ├── examples/                     # Ví dụ sử dụng framework
│   ├── recon_and_resilience/         # Recon, locator inventory và break-it tools
│   │   ├── locators/                 # Kết quả BSK live-DOM theo portal/module
│   │   ├── break_it/
│   │   └── templates/
│   └── specs_sync/                   # Đồng bộ và chuyển đổi specifications
├── docs/                             # Tài liệu dành cho người đọc
│   ├── framework/                    # Handbook, ADR và coding guidelines
│   ├── test-specs/                   # Tài liệu test theo module/user story
│   ├── defects/                      # Defect log và tài liệu bàn giao lỗi
│   ├── manual/                       # Hướng dẫn chạy thủ công và assets
│   └── diagrams/                     # Sơ đồ kiến trúc và workflow
├── archive/                          # Snapshot/deliverable lịch sử, không dùng lúc runtime
├── AGENTS.md                         # Master constitution
├── conftest.py                       # Pytest entrypoint
├── pytest.ini                        # Cấu hình chạy test
├── run_tests.py                      # Test orchestration CLI
├── generate_report.py                # Report-generation CLI tương thích
├── generate_enterprise_report.py     # Enterprise report CLI tương thích
└── md_runner.py                      # Markdown runner CLI tương thích
```

## 2. Quy tắc quyết định nơi lưu file

| Loại tài sản | Đường dẫn bắt buộc | Không được đặt tại |
| :--- | :--- | :--- |
| FSD, BR, AC, quyết định nghiệp vụ | `specs/md/` | `docs/`, `tests/` |
| Validation/flow/error catalog | `specs/component_specs/<module>/` | `pages/`, `testcases/` |
| Test-case thiết kế | `testcases/<module>/<ticket>/` | root, `tests/` |
| Markdown executable spec | `test_specs/<tier>/<module>/` | root |
| Python test | `tests/<module>/<component>/` | root `tests/` |
| Page Object | `pages/<module>/` | `tests/`, `components/` |
| Shared widget | `components/` | page orchestrator |
| JSON/fixture/mock input | `data/<module>/` hoặc `data/fixtures/` | hardcode trong test |
| BSK locator inventory | `specs/ui_bsk/` | `tools/`, root |
| Defect document | `docs/defects/` | root `docs/` |
| Defect screenshot/evidence | `reports/defects/evidence/` | root |
| UAT plan chung | `uat/master/` | root `uat/` |
| UAT theo phân hệ | `uat/r<xx>/` | root `uat/` |
| UAT execution report | `reports/uat/r<xx>/` | root `reports/` |
| Runtime artifacts | `reports/test-results/` | root `test-results/` |
| Tài liệu lịch sử | `archive/` | thư mục runtime |

## 3. Alias tương thích ở root

Các alias dưới đây được giữ có chủ đích vì code hoặc tài liệu cũ vẫn tham chiếu tới chúng:

| Alias | Đích chuẩn | Lý do |
| :--- | :--- | :--- |
| `[agile] fs` | `specs/` | Tương thích với đường dẫn FSD/AC cũ |
| `validation_rules` | `specs/validation_rules/` | Tương thích tài liệu validation cũ |
| `locator-bsk` | `specs/ui_bsk/` | Tương thích link BSK hiện có |
| `evidence` | `reports/defects/evidence/` | Tương thích hyperlink defect workbook |
| `curricula_trainer_account.html` | `data/fixtures/mock_pages/curricula_trainer_account.html` | Mock application cũ |

Không tạo thêm thư mục nhóm chỉ chứa symlink. Cây thư mục thật phải thể hiện đúng ownership; alias chỉ được giữ khi có tham chiếu tương thích đã biết.

## 4. Quy tắc UAT và evidence

- Root `uat/` chỉ chứa `README.md` và các folder `master/`, `r<xx>/`.
- Mỗi phân hệ hoàn tất phải có một workbook master duy nhất, một tab, chuẩn 20 cột bao gồm `Steps Test`.
- `Actual Result`, trạng thái, timestamp và evidence chỉ được ghi sau một lần chạy xác định.
- Raw Playwright artifacts nằm tại `reports/test-results/<RUN_ID>/`; dữ liệu cũ đã gom tại `reports/test-results/legacy-root/`.
- `reports/` là output runtime và được `.gitignore` bỏ qua; tài liệu cần version control phải đặt dưới `docs/` hoặc `testcases/`.

## 5. Ranh giới không được vi phạm

- Không chỉnh sửa, format, thêm hoặc xóa bất kỳ nội dung nào trong `copy/`.
- Không đặt test Python trực tiếp tại root `tests/`.
- Không đặt file UAT trực tiếp tại root `uat/`.
- Không đặt screenshot, video hoặc raw run artifacts ở repository root.
- Không dùng thư mục chứa khoảng trắng cho module/ticket mới.
- Không chuyển CLI root nếu chưa cập nhật toàn bộ consumer; các CLI hiện tại được giữ để bảo toàn tương thích.
