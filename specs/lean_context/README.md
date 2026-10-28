# Lean context — dùng chung cho mọi UAT

Mục tiêu: đọc đúng phần nguồn một lần, tái sử dụng khi bàn giao và giảm nội dung lặp. Spec vẫn là nguồn chuẩn; chỉ mục/pack không tự chứng minh coverage hoặc phê duyệt. Không chạy automation test từ các công cụ này.

## Bốn cơ chế giảm token

1. **Indexing:** tạo danh mục ID, heading, đường dẫn, khoảng dòng và SHA-256 cho tài liệu Markdown. Agent tìm ID như `F01-AC01` bằng `query.py`, sau đó chỉ đọc section liên quan. Index là bản đồ tra cứu; nó không thay thế nội dung nguồn hoặc chứng minh coverage.
2. **RAG cục bộ:** `retrieve.py` truy xuất và xếp hạng các section cần thiết từ index hoặc source pack. Hệ thống dùng từ khóa, ID và metadata ngay trên máy, chưa dùng vector database hay embedding. Kết quả luôn giữ đường dẫn và dòng nguồn để agent mở đúng section, kiểm tra điều kiện, ngoại lệ và dependency trước khi dùng.
3. **JSON có cấu trúc:** lưu nguồn, ma trận testcase, coverage, locator, fixture và trạng thái thiết kế trong JSON. `render.py` dùng cùng dữ liệu để sinh Markdown và Excel, tránh bắt AI viết lại bảng dài. JSON không được chứa kết quả chạy giả; testcase mới luôn `Not Run`, Actual Result và evidence để trống.
4. **Caching phía project:** source pack lưu chính xác các đoạn nguồn đã chọn, khoảng dòng, vai trò và SHA-256. Chat thiết kế và chat coding tái sử dụng pack/testcase đã duyệt mà không rà lại toàn bộ spec. Khi nguồn thay đổi, checksum làm pack stale và buộc review lại phần liên quan. Prompt cache của model là cơ chế riêng do nền tảng quản lý, không phải source pack.

Luồng chuẩn:

```text
UAT ID
  → Indexing: scope/query xác định nguồn
  → Local RAG: retrieve chọn section liên quan
  → Project cache: manifest + source pack có checksum
  → Structured JSON: testcase + coverage + fixture + locator
  → Renderer: Markdown + Excel
  → Chat coding mới: testcase đã duyệt + fixture + BSK
```

Các cơ chế trên giảm lượng tài liệu lặp trong context. Chúng không cho phép bỏ qua 5 pillars, live DOM, coverage 12 lớp, traceability hoặc oracle.

## Bắt đầu bằng mã UAT

Từ root, dùng một lệnh để thấy testcase, module, component specs, FSD và pack ứng viên:

```bash
python3 2_Code_Automation/tools/lean_context/scope.py UAT-001
```

Đây là danh mục ứng viên. Cần tra tiếp quyết định dùng chung, backlog, UI và phụ thuộc xuyên module; danh mục không chứng minh coverage. UAT-001 đã có pack nguồn **draft**, chưa xác nhận đủ coverage hoặc testcase đã duyệt:

```bash
python3 2_Code_Automation/tools/lean_context/pack.py check 1_Nghiep_Vu_va_Specs/specs/lean_context/packs/uat-001/source.pack.json
python3 2_Code_Automation/tools/lean_context/pack.py list 1_Nghiep_Vu_va_Specs/specs/lean_context/packs/uat-001/source.pack.json
python3 2_Code_Automation/tools/lean_context/pack.py read 1_Nghiep_Vu_va_Specs/specs/lean_context/packs/uat-001/source.pack.json --entry 0 --max-chars 6000
```

`list` hiển thị số entry; `read --entry N` chỉ in entry cần đọc. Trang dài có `next offset`; đọc tiếp với `--offset N`. Nội dung chưa đọc không được coi là đã kiểm chứng. Mặc định giới hạn **6.000 ký tự nội dung mỗi lần**, không phải 6.000 token. Không `cat source.pack.json` hoặc `source_index.json`.

Với UAT mới, tạo danh sách ứng viên rồi chọn nguồn cần thiết:

```bash
python3 2_Code_Automation/tools/lean_context/discover.py UAT-002 --output 1_Nghiep_Vu_va_Specs/specs/lean_context/packs/uat-002/manifest.draft.json
```

Discovery chỉ dùng metadata, có thể bỏ sót nguồn chung không nhắc UAT. Tiếp tục tìm BR/AC, validation, flow, errors và UI tương ứng. Không đưa mọi ứng viên vào pack; chọn đoạn có điều kiện/ngoại lệ/phụ thuộc cần thiết. Không quét sản phẩm `copy/`.

## Tìm section mà không đọc cả file

```bash
python3 2_Code_Automation/tools/lean_context/query.py F01-AC01 --limit 10
python3 2_Code_Automation/tools/lean_context/query.py F01-AC01 --read --offset 0 --text-offset 0 --max-chars 6000
```

- Hỗ trợ F01/FS08/R8 BR/AC, UAT001/UAT-001, TC/MSG/D/US. ID khớp đầy đủ; `AC01` không tự khớp `AC010`.
- Từ không phải ID tìm literal trong path/heading. `--path` chỉ là filter, không bảo đảm đủ scope. Nguồn chung có thể nằm ngoài folder module.
- Tìm full text bằng `rg` khi cần; đọc cả điều kiện, exception, heading cha/con liên quan. Không dùng grep để suy ra coverage.
- `--offset` là offset kết quả; `--text-offset` là offset ký tự trong section duy nhất ở chế độ read. Output cho biết tổng số và phần chưa in; tăng budget khi một dòng metadata vượt budget.
- SHA-256 phát hiện file khớp đã đổi/xóa. Tài liệu mới hoặc đổi ID khiến không còn khớp đòi rebuild thủ công. Index không theo dõi filesystem nền.

Khi câu hỏi nằm trong thân tài liệu hoặc không biết ID, dùng tìm kiếm nội dung cục bộ:

```bash
python3 2_Code_Automation/tools/lean_context/retrieve.py 'tuổi 7 đồng bộ lại' --module f01
python3 2_Code_Automation/tools/lean_context/retrieve.py 'F01-AC01 age eligibility' --pack 1_Nghiep_Vu_va_Specs/specs/lean_context/packs/uat-001/source.pack.json
```

`--module` chỉ tăng thứ tự ưu tiên; nguồn chung vẫn được tìm. `--pack` giới hạn trong các đoạn đã chọn, đồng thời kiểm tra checksum trước khi tìm. Công cụ dùng xếp hạng từ khóa trên máy, không gọi API, embedding hay vector database. Kết quả chỉ chứa dòng nguồn, trích đoạn ngắn và điểm xếp hạng, mặc định khoảng 4.000 ký tự mỗi trang; `--offset` đọc tiếp theo số ký tự được báo. Điểm cao không đồng nghĩa quy tắc áp dụng hay đã phủ đủ: mở toàn bộ section liên quan cùng điều kiện, ngoại lệ, heading cha/con và phụ thuộc trước khi thiết kế TC.

Index bao phủ Markdown ở specs/testcases/test_specs/uat thuộc nhóm 1; không quét copy hoặc file nhị phân. Build lại khi thêm/sửa/xóa nguồn (không cần lặp mỗi task):

```bash
python3 2_Code_Automation/tools/lean_context/index.py
```

## Manifest và pack tái sử dụng

Manifest có `scope`, `stage` (design/coding), `review` và `entries`. Mỗi entry có `path` từ root, `sha256` của file, `start/end` (dòng inclusive), `roles`, `reason`. Index cung cấp hash và bounds; không đoán range.

Roles design: BR, AC, Validation, Flow, Error, UI; coding: Testcase, Fixtures, UI. Có thể thêm Dependency. Ghi rõ nguồn chia sẻ/ngoại lệ. Pack hợp nhất range trùng để không lặp nội dung, giữ nguyên văn bản nguồn và provenance. File thay đổi khiến pack bị từ chối, phải xem lại lựa chọn trước khi cập nhật hash.

```bash
python3 2_Code_Automation/tools/lean_context/pack.py build PATH/manifest.json --output PATH/source.pack.json
```

`review.status`: draft/reviewed/approved; reviewed/approved cần `evidence` trỏ tới việc review thực tế. Công cụ không tự chuyển trạng thái hay chứng thực quyền phê duyệt. Hash chỉ chứng minh nội dung, không chứng minh dữ liệu UI còn đúng với build hiện tại. Coding chỉ dùng testcase được người dùng chấp thuận theo quy trình; draft không được quảng bá là đã duyệt.

## Sinh một lần từ dữ liệu dùng chung

Ma trận trong đúng `testcases/<module>/<ticket>/`, không để tại root. `matrix-template.json` là ví dụ cấu trúc, không phải testcase thật. Dùng `defaults` để chia sẻ các cột chung; dùng `step_sets` và `steps` để giảm lặp, ví dụ:

```json
{
  "defaults": {"Execution Status": "Not Run", "Environment": "môi trường của scope"},
  "step_sets": {"open": ["bước mở màn hình lấy từ testcase đã chốt"]},
  "cases": [{"ID": "TC-...", "steps": [{"ref": "open"}, "bước riêng"]}]
}
```

Đây chỉ là minh họa các trường bổ sung; vẫn phải có đủ trường trong template và 5 pillars, coverage, locators, fixtures, oracle. Renderer expand các bước, đánh số và điền số lượng; không dùng đồng thời `steps` và cột `Test Steps`/`Steps Test`. Mỗi case có thêm `Pillar`: BR, AC hoặc Tech/UI để renderer tự nhóm bảng; đây là metadata, không thêm cột Excel thứ 21. Các clause kỳ vọng không bị rút gọn bằng script.

```bash
python3 2_Code_Automation/tools/lean_context/render.py PATH/test_matrix.json --output PATH/TC_MODULE_FEATURE
```

Sinh MD 5 phần + XLSX 20 cột, 1 sheet, Not Run, actual trống. `--force` mới ghi đè. Đây là thiết kế, không phải execution evidence. Validator kiểm tra cấu trúc, ID, tham chiếu coverage; người thực hiện vẫn kiểm tra độ đầy đủ nguồn, 12 lớp, oracle và phân loại BR/AC/Tech theo rule 01/02. Legacy testcase không tự bị thay thế.

## Bàn giao sang chat coding

Lưu handoff ngắn với đường dẫn testcase đã duyệt, fixture, DOM evidence, quyết định và việc còn lại; chuẩn bị coding manifest có hash đúng. Chat coding đọc rule 04 và pack, chỉ quay về spec khi thiếu clause cụ thể. Không dán lại spec hoặc toàn lịch sử chat. `packs/uat-001/HANDOFF.md` ghi trạng thái thực tế của bộ nguồn hiện tại.

Prompt ngắn cho chat thiết kế: `Thiết kế testcase UAT-XXX theo AGENTS.md; dùng scope/query/retrieve và pack có sẵn, giữ đủ 5 pillars, DOM, coverage và oracle. Ghi JSON rồi render MD/XLSX. Trả đường dẫn và các điểm cần review.`

Sau khi duyệt, prompt cho chat coding mới: `Viết automation UAT-XXX từ testcase đã duyệt tại <đường dẫn>. Dùng fixture, BSK và rule 04; chỉ tra lại spec khi thiếu clause cụ thể. Bàn giao code và lệnh để tôi tự chạy.`

AGENTS/rule đã được rút gọn, bản trước giữ ở `.agent/reference/`. Không đọc cả thư mục reference mặc định. Theo [OpenAI Docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md), chuỗi chỉ dẫn được dựng khi bắt đầu run/session; nên bắt đầu chat mới để tránh mang lịch sử cũ. Sửa file không xóa lịch sử hiện tại; môi trường dùng agent khác cần kiểm tra cách nạp chỉ dẫn của agent đó.

## Đo token, tránh đếm trùng

Không tìm thấy transcript gốc trong workspace của lần thực hiện này. 880.831 vẫn là số người dùng cung cấp, chưa được xác minh từ log. Không suy ra giá/hạn mức từ byte hoặc token cache.

`usage.py` nhận JSONL đã chuẩn hóa (không tự đoán schema Gemini/Codex): mỗi record có string `session_id`, string `request_id` và integer `input_tokens`, `cached_input_tokens`, `output_tokens`. Output phải bao gồm reasoning theo định nghĩa provider; không cộng reasoning hai lần. Nếu provider thiếu số, không thay bằng 0. Khi log có streaming delta phải tổng hợp request trước.

```bash
python3 2_Code_Automation/tools/lean_context/usage.py PATH/usage.normalized.jsonl --mode per-request --input-kind total
python3 2_Code_Automation/tools/lean_context/usage.py PATH/usage.normalized.jsonl --mode cumulative --input-kind total
```

`total`: input đã bao gồm cache; `new`: input chưa bao gồm cache. Per-request: bỏ duplicate ID giống nhau, từ chối duplicate mâu thuẫn. Cumulative: lấy chênh lệch từng session, mặc định snapshot đầu là baseline và không tính phần trước baseline. Chỉ dùng `--from-zero` khi chắc log bắt đầu từ đầu session. Bộ đếm giảm bị từ chối; chia session khi có reset. Tool không xác nhận việc bạn map schema provider là đúng.

So sánh cùng UAT/scope/model, đủ mọi session/agent, token input/cache/output, thời gian và coverage/oracle; không cam kết 85% hoặc ≤300k khi chưa có run tương đương. Cắt output không được cắt yêu cầu.
