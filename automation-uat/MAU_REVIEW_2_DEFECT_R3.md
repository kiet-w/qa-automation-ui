# Dự thảo 2 defect theo mẫu R3

**Trạng thái tài liệu:** Dự thảo chờ review. Chưa thêm vào Google Sheet và chưa cấp Defect ID chính thức.

Nguồn: `BAO_CAO_2_BUG_EDUFAMS_UAT.xlsx`, `destructive_testing/DESTRUCTIVE_EXECUTION_REPORT.md`, `date_testing/DATE_TESTING_EXECUTION_REPORT.md` và các ảnh trong `evidence_bugs/`. Nội dung bên dưới dùng các cột của tab `R3_Defect_v4`. Giá trị chưa đủ bằng chứng được đánh dấu cần xác nhận.

## Draft 1 — SBFAS budget

| R3 field | Draft value |
|---|---|
| Defect ID | `TBD` — chỉ cấp sau khi kiểm tra ID còn trống trên sheet tại thời điểm thêm. |
| Defect Summary | SBFAS creation form accepts a negative total budget before moving to the next step |
| Severity | `TBD` — đề xuất **S3 - Moderate**, chờ xác nhận tác động và quy tắc phân loại. |
| Priority | `TBD` — đề xuất **Medium**, chờ triage. |
| Status | `Open` — đề xuất khi đưa vào sheet, sau khi xác nhận vẫn tái hiện. |
| Defect Type | Validation / financial data |
| Environment | EduFAMS School Portal; Create SBFAS scheme; URL, browser/version, build và ngày chạy: **cần xác nhận từ lần test gốc**. |
| Preconditions | Sign in with a school account authorized to create an SBFAS scheme. Open the Create SBFAS scheme form. |
| Steps to Reproduce | 1. Complete the required fields in the General step using valid test data. 2. Enter `-50000` in Total budget. 3. Select **Next**. 4. Observe the validation message and current step. |
| Expected Result | The application should validate Total budget against the approved business rules and show an actionable message when the value is invalid. Confirm with the approved requirement whether a negative value must be blocked at General/Next or at final submission. |
| Actual Result | The source execution report states that the form allowed progression to the next step with a negative or large budget. The input screenshot shows `-50000`; the next-step screenshot shows the Eligibility step but does not independently establish which budget value led to that step. |
| Linked Test Case(s) | `DEST-08` — local execution ID; map to an approved R3/UAT test case if one exists. |
| Evidence | `evidence_bugs/bug01_input_negative_budget.png`; `evidence_bugs/dest08_budget_cap_exceeded.png` — local paths only, not Google Sheet-accessible links. |
| Notes | Confirm the allowed minimum and maximum against the final spec. The source proposes `0.01–50,000 SGD`, but the evidence reviewed does not establish those limits. Reproduce with a continuous recording or before/after screenshots showing the **same** value. Final submission, persistence and API behavior have not been verified by these screenshots. The input screenshot contains an added red outline and annotation; those markings are not evidence of native UI validation. |
| Dev Notes | `TBD` |

## Draft 2 — Fee rate effective date

| R3 field | Draft value |
|---|---|
| Defect ID | `TBD` — chỉ cấp sau khi kiểm tra ID còn trống trên sheet tại thời điểm thêm. |
| Defect Summary | Fee rate Effective from field accepts a five-digit year during entry |
| Severity | `TBD` — đề xuất **S3 - Moderate** nếu xác nhận dữ liệu không hợp lệ có thể được lưu; nếu chỉ nhập được trên form, đánh giá theo tác động thực tế. |
| Priority | `TBD` — chờ triage sau khi xác nhận yêu cầu và hành vi submit. |
| Status | `Open` — đề xuất khi đưa vào sheet, sau khi xác nhận vẫn tái hiện. |
| Defect Type | Date validation |
| Environment | EduFAMS Admin Portal; Fees > Components > Rate Rules > Create; URL, browser/version, build và ngày chạy: **cần xác nhận từ lần test gốc**. |
| Preconditions | Sign in with an admin account authorized to configure fee rates. Open the Configure fee rates form for an eligible fee component. |
| Steps to Reproduce | 1. Open Configure fee rates and select Fixed Amount. 2. Enter `05/15/20266` in **Effective from** using the date field. 3. Observe the field value and any validation message. 4. If permitted by the test environment, complete the remaining fields with valid values and submit; record the actual response. |
| Expected Result | The date field and submission should enforce the valid date/year range defined in the approved specification and display an actionable validation message for an invalid value. Confirm the supported range and the point at which validation must occur. |
| Actual Result | The available screenshot shows **Effective from** displaying `05/15/20266` with no visible validation message at that moment. The available evidence does not show whether submission succeeds or the date is persisted. |
| Linked Test Case(s) | `TC-DATE-019` — local execution ID; map to an approved R3/UAT test case if one exists. |
| Evidence | `evidence_bugs/bug03_input_year_20266.png`; `evidence_bugs/tc_date_019_year_5digits_overflow.png` — local paths only, not Google Sheet-accessible links. |
| Notes | Confirm the valid year range from the final spec before asserting `1900–2099`; the source report suggests this range but the reviewed screenshots do not establish it. Do not claim the value was saved until submit and persistence are verified. The first image includes an added red outline and annotation. |
| Dev Notes | `TBD` |

## Cần chốt trước khi đăng lên sheet chung

1. Xác nhận hai mục trên đúng là hai bug bạn muốn đưa vào R3; kiểm tra trùng với các defect hiện có và cấp ID mới tại thời điểm đăng.
2. Điền môi trường, thời gian/build thật; đối chiếu AC/BR và xác nhận giới hạn ngân sách/ngày. Không mặc định các giới hạn đề xuất là yêu cầu đã được duyệt.
3. Tái hiện theo từng bước và bổ sung evidence trước/sau cùng dữ liệu, đặc biệt kết quả submit/persistence nếu muốn báo cáo phần đó. Ưu tiên ảnh UI gốc không overlay gây hiểu nhầm.
4. Chốt Severity, Priority, Status và liên kết testcase. Đưa evidence lên nơi người xem sheet có quyền truy cập rồi thay đường dẫn local bằng link phù hợp.
