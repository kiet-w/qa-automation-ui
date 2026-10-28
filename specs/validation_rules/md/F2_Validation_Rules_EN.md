# F2_Validation_Rules_EN


Function 2. Top-Up Validation Rules

# 1. Document control


| Field | Value |
| :--- | :--- |
| Project | EAFAMS (MOE education account and financial assistance platform) |
| Theme | Function 2. Top-Up: individual credits, campaign bulk, history |
| Deliverable | Validation rules, EN edition |
| Version and date | Draft 0.2, 26/10/2026 |
| Author | QA (generated locally from captured sources) |
| Structure | Rules sit with the page that enforces them. Sections 5.1 to 5.10 each carry the page purpose, its fields, the rules that act on it, its messages, exceptions and open questions, with an explicit note where none is captured. Section 4 holds rules that apply on every page; section 6 holds run processing and state transitions. |
| Main sources | Captured narrow F2 draft tab, 22 October capture (Team sources/2026-10-22-f2/tab_t.7jlsws8ic0aa.txt), sections 3.1.1 to 4.2, 5.1, Appendices A to C; the QA test plan v1.2.1 (function-2-test-plan.md and its workbook) for the open-point register |
| Source standing | The narrow clean tab is the proposed QA baseline for Sprint 2 only, not a recorded team or client approval (open point D-16). Rules, field tables, screens, states and messages below quote or paraphrase exactly what that captured draft holds. |
| Figma note | The F2 draft has no Figma evidence, so unlike the R4 rules this document uses no figure-number field codes |
| Companion seed | F2_TopUp_Seed_Data_DB.xlsx and F2_TopUp_Seed_Data.sql stage the dataset these rules talk about |


# 2. Scope and sources


In scope: the six captured OR criteria, EA search, the individual credit flow, top-up history and its Top-Up Summary, the campaign state machine (Draft, Running, Completed, Cancelled), campaign criteria configuration, preview, confirm, the immediate run, stop, retry, run summary and audit. Excluded except as open points: campaign budget or cap, scheduling, correction of a credited top-up, parent notifications, two-step campaign approval (OOS #6), and the wider F2 variant's extra criteria models. The wider tab stays a recorded conflict; nothing here cancels client requirements.

The page set is the ten screens in Appendix C of the capture. SCR-06 and SCR-10 do not exist there, so their absence from this document is not a missing page. Run processing has no captured screen and sits in section 6.

The seed workbook stages the accounts, campaigns and history rows these rules refer to. The rules document does not depend on that seed being loaded, and the seed does not add a rule.

# 3. How this document is arranged

- Sections 5.1 to 5.10 follow the ten screens. Each section holds the page purpose, the fields the HQ user meets, the rules that act on that page, the messages it can show, the exceptions that change it, and the open questions that touch it.
- Section 4 holds rules that apply on every page. Section 6 holds run processing and state transitions, which no single screen owns.
- Rule IDs and the EN paraphrase are unchanged from Draft 0.1. Only their position changed. Section 9 indexes every rule and exception, including the unused and absent IDs.
- Field rows quote the captured 4.1 table. The wording stays Vietnamese for fidelity and the column headers are translated. A field appears under the screen where the HQ user meets it.
- Message text quotes the captured 5.1 table exactly. Section 7 maps each message to the section that shows it.
- Id prefixes follow the source. BR-F2-08 to BR-F2-12 are unused and EX-10 is absent; the gaps stay visible.
- Money is SGD with exactly two decimals. UI dates follow DD/MM/YYYY in SGT; the seed dataset stores times in UTC.
- Rules the QA plan left conditional stay conditional here; nothing is tightened or relaxed.
- Page purposes and the screen map are navigation aids written by QA. They add no rule and change no captured wording.

# 4. Rules that apply on every page


These rules are not tied to one screen. A page section relies on them without repeating the text.

## 4.1 Access and permission


| Rule | What this section requires |
| :--- | :--- |
| BR-F2-01 | Only MOE HQ users perform top-ups; every API checks permission server-side and school users and parents receive 403. |


| Code | Exact text | Behaviour in the capture |
| :--- | :--- | :--- |
| MSG-0003 | You do not have permission to perform this action. | Quay về màn hình chính |


| Ref | What happens |
| :--- | :--- |
| EX-01 | A school user, parent, or a tampered API identity touches a top-up or a campaign or transaction not owned: the server authorises every request, returns 403, leaks nothing and writes a security log (MSG-0003). |


## 4.2 Session and required fields


| Code | Exact text | Behaviour in the capture |
| :--- | :--- | :--- |
| MSG-0001 | Enter your <field> | Bỏ trống trường bắt buộc, báo theo từng trường |
| MSG-0002 | Your session has expired. Please log in again. | Chuyển đến đăng nhập Admin Portal |


| Ref | What happens |
| :--- | :--- |
| EX-06 | The admin session expires mid-flow: before confirm, re-login is required and no transaction exists; after confirm the transaction still completes and the HQ user sees the current state after re-login (MSG-0002). |


## 4.3 Audit and retention


| Rule | What this section requires |
| :--- | :--- |
| BR-F2-30 | Audit keeps the transaction reference, amount, time and actor (the HQ user, or "System" with the HQ user who triggered the campaign), campaign and run. Campaigns, runs, run items and transactions are never hard-deleted. |


# 5. Page sections


Each section reads the same way: what the page is for, the captured fields, the rules that act on it, the messages it can show, the exceptions that change it, and the questions still open. Field columns are field, data type, source, whether the HQ user enters it, whether it is required, and rules or notes.

| Code | Screen | Draft screen name | Actions (draft wording) | UI states (draft wording) |
| :--- | :--- | :--- | :--- | :--- |
| SCR-01 | Individual top-up: find EA | Individual Top-Up: Tìm EA | Search | Loading, Empty (không có kết quả), Error |
| SCR-02 | Verify owner and enter amount | Xác minh chủ tài khoản và nhập số tiền | Continue, quay lại | Ô nhập bị vô hiệu khi EA không Active |
| SCR-03 | Review and confirm | Xem lại và xác nhận | Xác nhận, hủy | Nút xác nhận bị vô hiệu sau khi bấm; Processing |
| SCR-04 | Top-up result | Kết quả top-up | Về SCR-01, xem Top-Up History | Success, Failed, Verifying |
| SCR-05 | Top-Up History | Top-Up History | Lọc, xem chi tiết | Loading, Empty, Error |
| SCR-07 | Campaign list | Danh sách Campaign | Create, mở, Cancel | Loading, Empty |
| SCR-08 | Campaign configuration | Cấu hình Campaign | Save, Preview | Draft; lỗi từng trường |
| SCR-09 | Preview | Preview | Confirm, quay lại sửa | Confirm bị vô hiệu khi không có tài khoản |
| SCR-11 | Runs list | Danh sách Run | Mở run, Stop | Pending, Running, Completed, CompletedWithErrors, Stopped |
| SCR-12 | Run summary and run item list | Run summary và Run Item | Export CSV, Retry failed | Loading, Empty, Error |


## 5.1 SCR-01 Individual top-up: find EA


Find one Education Account by an exact Account Number or a full NRIC.

Draft screen: Individual Top-Up: Tìm EA.

Actions: Search. UI states: Loading, Empty (không có kết quả), Error.

Fields

| Field | Data type | Source | Entered by user | Required | Rules / notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Search by | Enum ACCOUNT_NUMBER, NRIC | HQ User chọn | Có | Có | Khớp chính xác, không tìm gần đúng, không gợi ý khi nhập dở |
| Search value | Text | HQ User nhập | Có | Có | Account Number hoặc NRIC đầy đủ (9 ký tự) |


Page rules

| Rule | What this section requires |
| :--- | :--- |
| BR-F2-02 | Search matches an exact full Account Number or a full student NRIC only; partial, extra or wrong input returns nothing and shows only MSG-0201: no suggestions, no partial matches, at most one EA per search. The displayed NRIC is masked. |


Messages

| Code | Exact text | Behaviour in the capture |
| :--- | :--- | :--- |
| MSG-0201 | No Education Account found. Check the Account Number or NRIC and try again. | Giữ ở SCR-01 |


No page-specific exception is captured.

## 5.2 SCR-02 Verify owner and enter amount


Confirm the account owner, status and balance, then enter the amount and the reason.

Draft screen: Xác minh chủ tài khoản và nhập số tiền.

Actions: Continue, quay lại. UI states: Ô nhập bị vô hiệu khi EA không Active.

Fields

| Field | Data type | Source | Entered by user | Required | Rules / notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Student name | Text | Student Profile (R1) | Không | Có |  |
| NRIC | Text | Student Profile (R1) | Không | Có | Che một phần, không đưa NRIC đầy đủ vào URL |
| Age | Integer | Tính từ DOB | Không | Có | Số năm tròn tại ngày hiện tại |
| Account Number | Text | Function 1 | Không | Có |  |
| Account Status | Enum Active, Closed | Function 1 | Không | Có | Chỉ Active mới nhập được số tiền |
| Current Balance | Decimal(18,2), SGD | Function 1 | Không | Có |  |
| Top-Up Amount | Decimal(18,2), SGD | HQ User nhập | Có | Có | Lớn hơn 0; tối đa 2 chữ số thập phân; không vượt hạn mức mỗi lần (TBC) |
| Reason | Text, tối đa 200 ký tự | HQ User nhập | Có | Có | Chỉ dùng nội bộ, không hiển thị cho Parent |


Page rules

| Rule | What this section requires |
| :--- | :--- |
| BR-F2-03 | The top-up amount is greater than 0, at most two decimal places, and within the per-credit limit (TBC per OQ-03). The reason is required and at most 200 characters. |
| BR-F2-04 | Only Active EAs accept a top-up. Before crediting, the system runs the F02 Closure Eligibility Check; Closed, Closure Deferred, Eligibility Review Required, or a non-responsive Government API rejects with the balance unchanged. |


Messages

| Code | Exact text | Behaviour in the capture |
| :--- | :--- | :--- |
| MSG-0202 | Enter an amount greater than 0, with up to 2 decimal places. | Giữ ở SCR-02, đánh dấu ô nhập |
| MSG-0203 | The amount is more than the limit for one top-up. (TBC, OQ-03) | Giữ ở SCR-02 hoặc SCR-08 |
| MSG-0204 | This Education Account is not active. Top-up is not allowed. | Vô hiệu ô nhập số tiền |
| MSG-0206 | Enter a reason (up to 200 characters). | Giữ ở SCR-02 |


No page-specific exception is captured.

Open questions: OQ-01.

## 5.3 SCR-03 Review and confirm


Review the credit once more and confirm it.

Draft screen: Xem lại và xác nhận.

Actions: Xác nhận, hủy. UI states: Nút xác nhận bị vô hiệu sau khi bấm; Processing.

Fields

| Field | Data type | Source | Entered by user | Required | Rules / notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Balance after top-up | Decimal(18,2) | Tính | Không | Không | Chỉ để tham khảo |
| Idempotency key | Text, tối đa 100 ký tự | Client sinh | Không | Có | Duy nhất theo HQ User; bấm đúp giữ cùng key; thao tác mới dùng key mới |


Page rules

| Rule | What this section requires |
| :--- | :--- |
| BR-F2-05 | Each credit happens exactly once: an idempotency key unique per HQ user, a confirm button disabled after the first click, and a distinct FundingReference per credit. |


No page-specific message is captured. The shared messages in section 4 apply.

Exceptions

| Ref | What happens |
| :--- | :--- |
| EX-02 | The EA closes or the student turns 16 between viewing and confirming: the closure eligibility check runs at confirm and F02 closes the EA if needed; the top-up is rejected and the balance unchanged (MSG-0204). |
| EX-04 | A double confirm click or a resubmitted idempotency key produces exactly one transaction and one credit; the resend returns the first transaction's outcome. |


MSG-0204 is reused here if the account closes between viewing and confirming (EX-02).

## 5.4 SCR-04 Top-up result


Show the outcome, the transaction reference and the new balance.

Draft screen: Kết quả top-up.

Actions: Về SCR-01, xem Top-Up History. UI states: Success, Failed, Verifying.

Fields

| Field | Data type | Source | Entered by user | Required | Rules / notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Transaction Reference | Text, tối đa 50 ký tự | Hệ thống sinh | Không | Có | Duy nhất; định dạng đề xuất TUP-YYYYMMDD-XXXXXX (TBC) |
| Transaction Status | Enum Success, Failed, ReconciliationRequired | Transaction | Không | Có | ReconciliationRequired hiển thị là đang xác minh |
| New balance | Decimal(18,2) | Function 1 | Không | Không | Chỉ khi Success |


Page rules

| Rule | What this section requires |
| :--- | :--- |
| BR-F2-06 | Failed transactions change no balance but are logged with time, actor and reason. |


Messages

| Code | Exact text | Behaviour in the capture |
| :--- | :--- | :--- |
| MSG-0205 | We could not check the account status. No amount was credited. Please try again later. | SCR-04, cho thử lại; không đổi dữ liệu |
| MSG-0207 | Top-up completed. Reference: {Transaction Reference}. | SCR-04, hiện số dư mới |
| MSG-0208 | The top-up could not be completed. No amount was credited. | SCR-04, cho thử lại |
| MSG-0209 | We are verifying this top-up. Please check the history later. | SCR-04, trạng thái đang xác minh |


Exceptions

| Ref | What happens |
| :--- | :--- |
| EX-05 | Function 1 times out or the network fails after a credit request: the transaction stays Pending and re-asks Function 1 with the same FundingReference; Success if it was already credited, Failed if not, otherwise ReconciliationRequired with an operations alert. No unbounded retries. |


Open questions: OQ-11.

## 5.5 SCR-05 Top-Up History


List individual and bulk top-ups, with a summary of the filtered set.

Draft screen: Top-Up History.

Actions: Lọc, xem chi tiết. UI states: Loading, Empty, Error.

Fields

| Field | Data type | Source | Entered by user | Required | Rules / notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Filter: Account Number, NRIC | Text | HQ User nhập | Có | Không |  |
| Filter: From, To | Date | HQ User chọn | Có | Không | DD/MM/YYYY, SGT |
| Filter: Source | Enum All, Individual, Bulk | HQ User chọn | Có | Không |  |
| Filter: Status | Enum All, Success, Failed, ReconciliationRequired | HQ User chọn | Có | Không |  |
| Cột bảng | Date, Transaction Reference, Student, Account Number, Source, Campaign (nếu bulk), Amount, Status, Performed by | Transaction | Không | Có | Mới nhất trước, 20 dòng mỗi trang |
| Top-Up Summary: Total Spending | Decimal(18,2), SGD | Tính | Không | Có | Tổng Amount các giao dịch Success theo bộ lọc đang chọn |
| Top-Up Summary: Successful, Failed | Integer, Decimal(18,2) | Tính | Không | Có | Số lượng theo bộ lọc; Failed gồm cả ReconciliationRequired, hiển thị số riêng; số tiền Failed là số tiền dự kiến chưa ghi có |


Page rules

| Rule | What this section requires |
| :--- | :--- |
| BR-F2-07 | Top-Up History lists all individual and bulk top-ups; its filter-scoped Top-Up Summary shows Total Spending (sum of Success amounts), the Successful count, and the Failed count with the expected uncredited amount including the ReconciliationRequired count. Campaign, run and run-summary figures show the same three metrics read-only. |


No page-specific message is captured. The shared messages in section 4 apply.

No page-specific exception is captured.

## 5.6 SCR-07 Campaign list


List campaigns with their spending and status, and start a new one.

Draft screen: Danh sách Campaign.

Actions: Create, mở, Cancel. UI states: Loading, Empty.

Fields

| Field | Data type | Source | Entered by user | Required | Rules / notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Cột danh sách | Campaign Code, Name, Academic Year, Amount, Total Spending, Successful, Failed, Status | Campaign | Không | Có | Lọc theo Academic Year, Status; Total Spending, Successful, Failed của campaign |


Page rules

| Rule | What this section requires |
| :--- | :--- |
| BR-F2-13 | A campaign belongs to one Academic Year; its code is unique within the year; several campaigns may share a year with different criteria and amounts. |


No page-specific message is captured. The shared messages in section 4 apply.

No page-specific exception is captured.

Cancel is governed by BR-F2-23 in section 5.9 and shares the conflict rule EX-08 in section 5.7.

## 5.7 SCR-08 Campaign configuration


Set the campaign name, academic year, criteria, amount and eligibility date.

Draft screen: Cấu hình Campaign.

Actions: Save, Preview. UI states: Draft; lỗi từng trường.

Fields

| Field | Data type | Source | Entered by user | Required | Rules / notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Campaign Name | Text, tối đa 150 ký tự | HQ User nhập | Có | Có |  |
| Academic Year | Dropdown | academic_years (R3) | Có | Có | Chỉ DRAFT hoặc ACTIVE |
| Age Range: Minimum, Maximum Age | Integer | HQ User nhập | Có | Không | $7 \le \text{Min} \le \text{Max} \le 15$; nhập cả hai hoặc không nhập |
| Account Balance: operator, threshold | Enum, Decimal(18,2) | HQ User chọn, nhập | Có | Không | Toán tử <, <=, >, >=, =; ngưỡng không âm; nhập cả hai hoặc không |
| Schooling Status: Actively Enrolled | Checkbox | HQ User chọn | Có | Không | Bật thì criterion này thỏa với học sinh Actively Enrolled trong Academic Year |
| School | Multi-select | Master data trường (R3, TBC) | Có | Không | Chọn một hoặc nhiều trường; đã thêm criterion thì cần ít nhất một giá trị (MSG-0224) |
| Academic Level | Multi-select enum PRIMARY, SECONDARY | HQ User chọn | Có | Không | Chọn một hoặc cả hai; đã thêm criterion thì cần ít nhất một giá trị (MSG-0224) |
| Class | Multi-select | Master data lớp của Academic Year (R3, TBC) | Có | Không | Chỉ hiện lớp thuộc Academic Year đã chọn, kèm tên trường; đổi Academic Year thì bỏ các lớp không thuộc năm mới; cần ít nhất một giá trị (MSG-0224) |
| Top-Up Amount per account | Decimal(18,2), SGD | HQ User nhập | Có | Có | Lớn hơn 0; không vượt hạn mức mỗi lần (TBC) |
| Eligibility Date | Date | HQ User chọn | Có | Có | Mặc định ngày hiện tại; mốc tính tuổi, tình trạng đi học, trường, cấp học và lớp |


Page rules

| Rule | What this section requires |
| :--- | :--- |
| BR-F2-14 | Criteria combine by OR and at least one is required. Baseline conditions that are not criteria: the student is a Singapore Citizen (SC) and has a linked EA, the EA is Active, and it passes the Closure Eligibility Check. Six criterion types exist, each at most once per campaign: Age Range (inclusive ends measured at the Eligibility Date), Account Balance (operator against the SGD balance), Schooling Status (Actively Enrolled in the year), School, Academic Level and Class; the value lists of the last three also OR-combine and need at least one value each. An account matching several criteria appears once and receives one credit. |
| BR-F2-15 | Age Range ends are inclusive and age counts whole years at the Campaign Eligibility Date. EA existence bounds age between 7 and below 16. |
| BR-F2-16 | The HQ user picks the Campaign Eligibility Date at SCR-08 (default today); the run uses that exact date. |
| BR-F2-17 | Function 2 sets no campaign budget or cap; spending appears in Top-Up Summary figures only, with no budget gate or warning at preview, confirm or execution. |
| BR-F2-18 | A campaign is Draft, Running, Completed or Cancelled. Only Draft campaigns are editable. Confirm turns it Running and locks it; editing criteria, amount or the date after a preview invalidates that preview. |


Messages

| Code | Exact text | Behaviour in the capture |
| :--- | :--- | :--- |
| MSG-0215 | This campaign is running and cannot be changed. | Mọi nút sửa bị vô hiệu |
| MSG-0217 | Enter an age range from 7 to 15, with the minimum not more than the maximum. | SCR-08, đánh dấu ô nhập |
| MSG-0218 | Enter a balance operator and an amount of 0 or more. | SCR-08, đánh dấu ô nhập |
| MSG-0220 | This Academic Year is closed. Choose another Academic Year. | SCR-08 |
| MSG-0221 | Add at least one criterion. | SCR-08 |
| MSG-0224 | Select at least one value for {criterion}, or remove the criterion. | SCR-08, đánh dấu criterion |


Exceptions

| Ref | What happens |
| :--- | :--- |
| EX-07 | The HQ user edits criteria, amount or the date after previewing: the campaign stays Draft, the old preview is void, and a fresh preview is required before Confirm (BR-F2-20). After confirm the campaign is Running and cannot be edited (MSG-0215). |
| EX-08 | Two HQ users edit, cancel or confirm the same campaign simultaneously, or edit one while it is Running: the row version detects the conflict and the later user is asked to refresh. A Running campaign cannot be edited (MSG-0215). |


Open questions: OQ-01, OQ-06, OQ-07, OQ-12.

## 5.8 SCR-09 Preview


Preview the eligible accounts and the forecast amount before confirming.

Draft screen: Preview.

Actions: Confirm, quay lại sửa. UI states: Confirm bị vô hiệu khi không có tài khoản.

Fields

| Field | Data type | Source | Entered by user | Required | Rules / notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Cột preview | Student Name, Age, Balance, Schooling Status, School, Academic Level, Class, Matched Criteria, Top-Up Amount | Tính | Không | Có | 20 dòng mỗi trang |
| Total accounts, Total amount (forecast), Previewed at | Integer, Decimal, Datetime | Tính | Không | Có | Chỉ để xem; Confirm chỉ bị vô hiệu khi không có tài khoản eligible |


Page rules

| Rule | What this section requires |
| :--- | :--- |
| BR-F2-19 | Preview shows per account the student name, age, balance, schooling status, school, academic level, class, matched criteria and expected amount; plus the total number of accounts, the total expected amount and the computed-at time; read-only. |
| BR-F2-20 | Confirm is allowed only when the preview was computed on the current campaign version and at least one eligible account exists; editing criteria or amount invalidates the preview. |
| BR-F2-21 | Confirm turns the campaign Running and creates the run immediately; there is no execution-mode choice, schedule or recurrence. |
| BR-F2-22 | Each campaign has exactly one run. Only Draft campaigns confirm; a double click or two HQ users confirming at once still produce one run (row-version check). |


Messages

| Code | Exact text | Behaviour in the capture |
| :--- | :--- | :--- |
| MSG-0214 | No accounts match these criteria. | SCR-09, vô hiệu nút Confirm |
| MSG-0216 | The campaign has changed. Preview again before confirming. | Quay về SCR-09, bắt buộc preview lại |
| MSG-0222 | This campaign was changed by another user. Refresh and try again. | Làm mới dữ liệu |


No page-specific exception is captured.

Open questions: OQ-03, OQ-09.

BR-F2-25 in section 6.1 explains the duplicate-campaign warning, and EX-09 there explains what changes between this preview and the run.

## 5.9 SCR-11 Runs list


List campaign runs and open or stop one.

Draft screen: Danh sách Run.

Actions: Mở run, Stop. UI states: Pending, Running, Completed, CompletedWithErrors, Stopped.

Fields

| Field | Data type | Source | Entered by user | Required | Rules / notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Cột danh sách run | Campaign Code, Eligibility Date, Status, Total, Successful, Failed, Total credited, Started at, Completed at | Run | Không | Có |  |


Page rules

| Rule | What this section requires |
| :--- | :--- |
| BR-F2-23 | Draft campaigns can be Cancelled. A Running run can be Stopped: the in-flight slot finishes and the remaining items become Failed (RUN_STOPPED); already-credited items stay credited. |


No page-specific message is captured. The shared messages in section 4 apply.

No page-specific exception is captured.

Run states are listed in section 6.2.

## 5.10 SCR-12 Run summary and run item list


Show one run's totals and items, export them and retry failed items.

Draft screen: Run summary và Run Item.

Actions: Export CSV, Retry failed. UI states: Loading, Empty, Error.

Fields

| Field | Data type | Source | Entered by user | Required | Rules / notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Cột run item | Student, Account Number, Age, Balance, Schooling Status, Amount, Outcome, Failure Reason, Transaction Reference | Run item | Không | Có | Lọc theo Outcome; nút Export CSV, Retry failed |
| Run summary | Integer, Decimal(18,2) | Tính | Không | Có | Total Spending (Total credited), Successful, Failed (số lượng và số tiền), số ReconciliationRequired |


Page rules

| Rule | What this section requires |
| :--- | :--- |
| BR-F2-26 | Item results are only Successful or Failed. Failed items carry a failure code: no longer eligible at execution (EA_NOT_ACTIVE, ELIGIBILITY_REVIEW_REQUIRED, CRITERIA_NOT_MATCH when no criterion matches), run stopped (RUN_STOPPED), or a technical failure (for example ELIGIBILITY_CHECK_UNAVAILABLE, CREDIT_FAILED). ReconciliationRequired counts inside the Failed group with its own flag. |
| BR-F2-28 | Only Failed run items are retried (not ReconciliationRequired); retries pass every check again. |
| BR-F2-29 | Run summary shows the run's Total Spending (total credited), the Successful totals, the Failed count and amount, and the ReconciliationRequired count, filterable by outcome, with CSV export. Completed when no Failed items remain; CompletedWithErrors otherwise. |


No page-specific message is captured. The shared messages in section 4 apply.

No page-specific exception is captured.

Open questions: OQ-11.

EX-05 in section 5.4 and EX-11 in section 6.1 cover an uncertain credit and a resumed run.

# 6. Background processing and states


## 6.1 Run processing


No captured screen owns these rules. They decide what the run does between Confirm and the run summary.

| Rule | What this section requires |
| :--- | :--- |
| BR-F2-24 | Execution processes accounts in ascending Account Number order in small chunks: Closure Eligibility Check, EA still Active, criteria re-evaluated (at least one matches) with data current at that moment, then credit; the run's Successful, Failed and Total credited counters update after each chunk. |
| BR-F2-25 | Within a run each account is credited at most once (unique per run and EA); across different campaigns an account may receive several credits; preview warns when an account already received a top-up from another campaign in the same period. |
| BR-F2-27 | Each run item has one FundingReference created once; retries reuse it, so Function 1 cannot double-credit. |


| Ref | What happens |
| :--- | :--- |
| EX-03 | The Government API does not respond during the closure check: nothing is credited; individuals get an error and may retry; bulk items fail with ELIGIBILITY_CHECK_UNAVAILABLE and are retryable. The Account Status is never changed automatically. |
| EX-09 | Between preview and execution an account's balance changes, its EA closes, or the student stops being actively enrolled: the run re-evaluates; items no longer eligible fail with EA_NOT_ACTIVE or CRITERIA_NOT_MATCH; the actual list can differ from the preview. |
| EX-11 | A job halts abruptly or the server restarts mid-run: processing resumes from unprocessed items; an item already sent to Function 1 without a recorded result is re-asked by FundingReference, so nothing is credited twice. |


## 6.2 State transitions


From Appendix A of the capture. Page sections show the states the HQ user can see; this table covers the objects behind them.

| Object | From | To | Condition | Note |
| :--- | :--- | :--- | :--- | :--- |
| Campaign | (mới) | Draft | HQ User Save | Sửa được |
| Campaign | Draft | Running | Preview đạt, HQ User Confirm | Run bắt đầu ngay; không sửa được nữa |
| Campaign | Running | Completed | Run kết thúc (Completed, CompletedWithErrors hoặc Stopped) | Không sửa được nữa |
| Campaign | Draft | Cancelled | HQ User Cancel | Không tạo run |
| Run | (mới) | Pending | HQ User Confirm campaign | Khóa campaign |
| Run | Pending | Running | Bắt đầu lập danh sách và xử lý |  |
| Run | Running | Completed | Hết danh sách, không còn run item Failed hoặc ReconciliationRequired |  |
| Run | Running | CompletedWithErrors | Hết danh sách, còn run item Failed hoặc ReconciliationRequired |  |
| Run | Running | Stopped | HQ User Stop | Item còn lại Failed (RUN_STOPPED) |
| Run | CompletedWithErrors | Completed | Thử lại hoặc vận hành xử lý hết Failed và ReconciliationRequired |  |
| Run Item | (mới) | Pending | Lập danh sách khi run bắt đầu |  |
| Run Item | Pending | Successful | Function 1 ghi có thành công | Số dư tăng một lần |
| Run Item | Pending | Failed | Lỗi xử lý hoặc kiểm tra; không còn đủ điều kiện khi chạy; run bị Stop | Số dư không đổi; có Failure Code |
| Run Item | Pending | ReconciliationRequired | Không xác định được kết quả ghi có | Tính trong nhóm Failed |
| Run Item | Failed | Successful hoặc Failed | HQ User Retry failed | Dùng lại FundingReference |
| Run Item | ReconciliationRequired | Successful hoặc Failed | Bộ phận vận hành xử lý |  |
| Transaction | (mới) | Pending | HQ User xác nhận, hoặc run item bắt đầu ghi có | Có FundingReference |
| Transaction | Pending | Success | Function 1 ghi sổ cái thành công | Có mã bút toán của Function 1 |
| Transaction | Pending | Failed | Không đủ điều kiện, hoặc Function 1 báo lỗi | Số dư không đổi |
| Transaction | Pending | ReconciliationRequired | Không xác định được kết quả sau khi hỏi lại Function 1 | Cảnh báo vận hành |
| Transaction | ReconciliationRequired | Success hoặc Failed | Bộ phận vận hành xử lý |  |


# 7. Message index


Every captured message, with the section that shows it. MSG-0219 and MSG-0223 are absent from the capture; the gaps are kept.

| Code | Where it appears |
| :--- | :--- |
| MSG-0001 | 4.2 Session and required fields |
| MSG-0002 | 4.2 Session and required fields |
| MSG-0003 | 4.1 Access and permission |
| MSG-0201 | 5.1 SCR-01 Individual top-up: find EA |
| MSG-0202 | 5.2 SCR-02 Verify owner and enter amount |
| MSG-0203 | 5.2 SCR-02 Verify owner and enter amount |
| MSG-0204 | 5.2 SCR-02 Verify owner and enter amount |
| MSG-0205 | 5.4 SCR-04 Top-up result |
| MSG-0206 | 5.2 SCR-02 Verify owner and enter amount |
| MSG-0207 | 5.4 SCR-04 Top-up result |
| MSG-0208 | 5.4 SCR-04 Top-up result |
| MSG-0209 | 5.4 SCR-04 Top-up result |
| MSG-0214 | 5.8 SCR-09 Preview |
| MSG-0215 | 5.7 SCR-08 Campaign configuration |
| MSG-0216 | 5.8 SCR-09 Preview |
| MSG-0217 | 5.7 SCR-08 Campaign configuration |
| MSG-0218 | 5.7 SCR-08 Campaign configuration |
| MSG-0220 | 5.7 SCR-08 Campaign configuration |
| MSG-0221 | 5.7 SCR-08 Campaign configuration |
| MSG-0222 | 5.8 SCR-09 Preview |
| MSG-0224 | 5.7 SCR-08 Campaign configuration |


# 8. Open questions


## 8.1 Draft open questions (Appendix B)


OQ-08 concerns the parent-facing top-up description and sits outside the screens in this document. Page sections name the other questions that touch them.

| ID | Question (draft) | Affects | Interim approach in the FS |
| :--- | :--- | :--- | :--- |
| OQ-01 | Hạn mức tối đa mỗi lần top-up lẻ và mỗi tài khoản trong bulk | BR-F2-03, BR-F2-19, MSG-0203 | Chưa đặt hạn mức; cấu hình được |
| OQ-03 | Có cần phê duyệt hai bước (maker-checker) cho campaign | OOS #6 | Không; HQ User xác nhận một bước, có audit |
| OQ-06 | Actively Enrolled chỉ dựa trên enrollment hay cần cả class assignment | BR-F2-17 | Actively Enrolled chỉ dựa trên enrollment; riêng criterion Class dùng phân lớp của R3 |
| OQ-07 | Campaign Eligibility Date dùng ngày xác nhận hay một ngày cố định (ví dụ đầu năm học) | BR-F2-16 | HQ User chọn ở SCR-08, mặc định ngày hiện tại |
| OQ-08 | Description của top-up hiển thị cho Parent: tên campaign hay "MOE Top-up" chung | Mục 2.2 (R8) | "MOE Top-up" chung |
| OQ-09 | Tài khoản thỏa nhiều campaign cùng kỳ: cho nhận nhiều khoản hay chặn | BR-F2-28 | Cho phép, preview cảnh báo |
| OQ-11 | Ngưỡng thời gian Pending trước khi chuyển ReconciliationRequired; chu kỳ hỏi lại Function 1 | EX-05 | Do Dev cấu hình; không tự Failed |
| OQ-12 | Nguồn dữ liệu School, Academic Level, Class ở R3 (bảng, trường dữ liệu, cách xác định cấp học) | BR-F2-14, SCR-08 | Tạm dùng master data trường, cấp học, lớp và phân lớp của R3; tên bảng TBC |


## 8.2 QA open points carried into the test plan


From QA plan v1.2.1: the open-point register D-01 to D-16.

| ID | Question | Status |
| :--- | :--- | :--- |
| D-01 | Delivered operation-key and changed-payload contract? | Draft answer; interface pending |
| D-02 | Which R1 closure and CPF contract is deployed? | Conflict |
| D-03 | Deployed role and read-access mapping? | Draft answer; mapping pending |
| D-04 | Handling stale Active, PR-with-EA and Closed-positive records? | Partly specified |
| D-05 | Is campaign budget returning to Sprint 2? | Deferred scope conflict |
| D-06 | What is re-evaluated between preview and execution? | Draft answer |
| D-07 | Which exact identifiers and search parameters are deployed? | Draft answer; identity mapping pending |
| D-08 | Criterion data and date-boundary mappings? | Draft answer; boundary/outage mapping pending |
| D-09 | Does Sprint 2 send top-up email? | Cross-document conflict |
| D-10 | Entitlement across operations and campaigns? | Draft answer; recurrence deferred |
| D-11 | Maximum top-up and whitespace reason rules? | Partly specified |
| D-12 | Correction returning to scope? | Deferred |
| D-13 | Scheduling returning to scope? | Deferred |
| D-14 | Manual selection, campaign code and unresolved validation? | Partly specified |
| D-15 | Funding source/accounting contract? | Open; outside narrow scope |
| D-16 | Which F2 tab controls Sprint 2? | Confirmation required |


# 9. Rule and exception index


Every ID from the capture, with the section where it now sits. Unused and absent IDs are kept so the source numbering stays visible.

| ID | Type | Where it sits | Status |
| :--- | :--- | :--- | :--- |
| BR-F2-01 | Business rule | 4.1 Access and permission | Used |
| BR-F2-02 | Business rule | 5.1 SCR-01 Individual top-up: find EA | Used |
| BR-F2-03 | Business rule | 5.2 SCR-02 Verify owner and enter amount | Used |
| BR-F2-04 | Business rule | 5.2 SCR-02 Verify owner and enter amount | Used |
| BR-F2-05 | Business rule | 5.3 SCR-03 Review and confirm | Used |
| BR-F2-06 | Business rule | 5.4 SCR-04 Top-up result | Used |
| BR-F2-07 | Business rule | 5.5 SCR-05 Top-Up History | Used |
| BR-F2-08 | Business rule | Not used | Unused in the captured draft |
| BR-F2-09 | Business rule | Not used | Unused in the captured draft |
| BR-F2-10 | Business rule | Not used | Unused in the captured draft |
| BR-F2-11 | Business rule | Not used | Unused in the captured draft |
| BR-F2-12 | Business rule | Not used | Unused in the captured draft |
| BR-F2-13 | Business rule | 5.6 SCR-07 Campaign list | Used |
| BR-F2-14 | Business rule | 5.7 SCR-08 Campaign configuration | Used |
| BR-F2-15 | Business rule | 5.7 SCR-08 Campaign configuration | Used |
| BR-F2-16 | Business rule | 5.7 SCR-08 Campaign configuration | Used |
| BR-F2-17 | Business rule | 5.7 SCR-08 Campaign configuration | Used |
| BR-F2-18 | Business rule | 5.7 SCR-08 Campaign configuration | Used |
| BR-F2-19 | Business rule | 5.8 SCR-09 Preview | Used |
| BR-F2-20 | Business rule | 5.8 SCR-09 Preview | Used |
| BR-F2-21 | Business rule | 5.8 SCR-09 Preview | Used |
| BR-F2-22 | Business rule | 5.8 SCR-09 Preview | Used |
| BR-F2-23 | Business rule | 5.9 SCR-11 Runs list | Used |
| BR-F2-24 | Business rule | 6.1 Run processing | Used |
| BR-F2-25 | Business rule | 6.1 Run processing | Used |
| BR-F2-26 | Business rule | 5.10 SCR-12 Run summary and run item list | Used |
| BR-F2-27 | Business rule | 6.1 Run processing | Used |
| BR-F2-28 | Business rule | 5.10 SCR-12 Run summary and run item list | Used |
| BR-F2-29 | Business rule | 5.10 SCR-12 Run summary and run item list | Used |
| BR-F2-30 | Business rule | 4.3 Audit and retention | Used |
| EX-01 | Exception | 4.1 Access and permission | Used |
| EX-02 | Exception | 5.3 SCR-03 Review and confirm | Used |
| EX-03 | Exception | 6.1 Run processing | Used |
| EX-04 | Exception | 5.3 SCR-03 Review and confirm | Used |
| EX-05 | Exception | 5.4 SCR-04 Top-up result | Used |
| EX-06 | Exception | 4.2 Session and required fields | Used |
| EX-07 | Exception | 5.7 SCR-08 Campaign configuration | Used |
| EX-08 | Exception | 5.7 SCR-08 Campaign configuration | Used |
| EX-09 | Exception | 6.1 Run processing | Used |
| EX-10 | Exception | Not used | Absent from the capture |
| EX-11 | Exception | 6.1 Run processing | Used |


# 10. Limits and standing

- The narrow clean tab is the proposed QA baseline for Sprint 2 only. Team and client confirmation stays open under D-16.
- The page grouping is QA's arrangement of the capture. It does not create, remove or reword a rule.
- Field rows keep the captured Vietnamese wording. The English glosses around them explain where the field sits; they do not replace the source.
- No product, build or environment test ran for this document, and no Figma evidence exists for F2.
- The seed workbook stages the data these rules refer to. It is not an execution result and does not prove a rule.
- This document grants no approvals: a rule becomes agreed only after the team and the client accept the draft baseline. Profiles, scopes and numbers stay valid as captured; QA plan v1.2.1 keeps the corresponding case mapping.