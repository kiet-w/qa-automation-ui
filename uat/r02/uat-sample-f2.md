# UAT-022 worked sample: individual top-up

Prepared 25 October 2026 for the QA team walkthrough.
Planning example only.
Status: Not Run.
The team still needs to confirm the proposed rules and test values.
EA means education account.

Open [the sample workbook](uat-sample-f2.xlsx) on **Case**, then **Steps**, then **Guide**.
The workbook follows that order.
Edit this Markdown file, then run `python3 -B build-uat-sample-f2.py` to rebuild the workbook.
Make a dated copy of the workbook before recording test results.

## Case summary

| Field | Value |
|---|---|
| Local scenario | UAT-022, Credit an individual account after review and confirmation |
| Sample route | One successful individual top-up, followed by HQ and parent history checks. Test cancellation and repeated requests separately. |
| Business purpose | An authorized HQ user adds money to the correct education account. The balance and transaction history show the same result. |
| Owner / reviewer | Josh / Gavin |
| Supporting owner | Howard checks the balance and history through the linked parent's account. Chan supplies the test user IDs and roles. |
| Coverage | US-028 Individual EA Top-Up; US-032 Individual & Bulk Top-Up History |
| Role and page | MOE HQ user on Top-Up / Individual Top-Up / Top-Up History. Linked parent for step 6. Confirm the actual screen names before testing. |
| Expected calculation | Opening SGD 10.00 + top-up SGD 20.00 = closing SGD 30.00. Add SGD 20.00 exactly once. These are proposed test values. |
| Decisions to confirm | UAT-D01: individual top-up rules. UAT-D03: account eligibility. UAT-D09: build, test data and access. |
| Scope limit | This covers the successful route within UAT-022. It does not replace the full scenario or prove that repeated requests are safe. The pack's scenario count stays the same. |

## Preconditions

| Check | What must be ready before testing |
|---|---|
| Environment | Record the approved QA build and URL. Use an isolated test environment. Identify which services are real and which use mock responses. Do not use production or shared financial records. |
| Test users | Set up an HQ user who can top up and a separate verified parent linked to the test child. Keep passwords and tokens out of this case. |
| Account | Use a test child record for a Singapore Citizen aged 10 on the recorded business date. Link the correct EA. It must be Active and pass the agreed eligibility check, with no pending transaction. |
| Eligibility service | The required government or eligibility check must return a known eligible result. Account closure, CPF transfers and service failures are separate cases. |
| Starting state | Set the balance to SGD 10.00 using the approved setup. Save the opening balance, history and ledger records. No other tester, payment or background job may change this account during the test. |
| Rules | BA confirms the search, amount, reason, review, confirmation and history rules. Check that SGD 20.00 is within the allowed limit for one top-up. Bulk-selection and scheduling questions do not block this route. |
| Evidence access | Complete the Evidence support table with approved screens, reports or read-only queries. Include the balance, top-up result, Function 1 ledger entry and audit record. A success message alone is not enough to pass. |
| Reset | Josh has an approved way to restore only this test's data. Restore balances, ledger entries, references and audit records together. Do not make another top-up, delete shared history or create an unapproved reversal to reset the test. |

## Test data

Enter the test user IDs and account number before running the case.
Do not enter a setup label such as DATA-TOPUP in the product.

| Field | Planned value | Test value / ID |
|---|---|---|
| HQ user ID | Test HQ user who can top up. Record the user ID only. | |
| EA account number | Test eligible EA reserved for this case, with opening SGD 10.00. Uses DATA-TOPUP setup. | |
| Child ID | Test child record: Singapore Citizen, age 10 on the recorded business date. | |
| Parent user ID | Test parent user linked to that child. Uses DATA-ROLES setup. | |
| Top-up amount | SGD 20.00 | |
| Reason | UAT individual top-up | |
| Expected closing balance | SGD 30.00 | |

## Script

Use the approved QA account number, not an invented NRIC.
Check each result against the expectation below.
Leave Actual result and Evidence reference blank until the test.

| Step | Action | Expected result | Evidence required |
|---|---|---|---|
| 1 | Sign in as the test HQ user. Open Individual Top-Up. Search using the exact test account number. | One account appears for the correct child. Its status is Active and its balance is SGD 10.00. Any displayed NRIC is partly hidden. | Test user role and account details. Opening balance and history. |
| 2 | Enter 20.00 and the reason "UAT individual top-up". Do not confirm yet. | The amount and reason match the test data. The balance stays SGD 10.00. No money has been added. | Input screen. Compare with the opening records to show no money was added, using Evidence support. |
| 3 | Continue to the review or confirmation screen. | Before confirmation, the screen shows the correct recipient, current SGD 10.00, top-up SGD 20.00, expected balance SGD 30.00 and reason. No money has been added. | Review screen showing the recipient, amounts and reason. A no-credit check using Evidence support. |
| 4 | Confirm the top-up once. Read the result and transaction reference. | The system confirms success and gives a reference for this top-up. If it times out or the result is unclear, stop. Check the saved result using the agreed method before any retry. Do not mark an unknown result as Passed. | Result and transaction reference. If unclear, save the result check described in Evidence support. |
| 5 | Open the account and HQ Top-Up History again. Match this top-up to the saved balance, Function 1 ledger entry and audit record. | The balance is SGD 30.00, an increase of SGD 20.00. This top-up added SGD 20.00 exactly once. The records match the account, transaction reference, HQ user and time. Earlier history is unchanged. | Opening and closing balances. Matching HQ history, ledger entry and audit record, using Evidence support. |
| 6 | With Howard, sign in separately as the linked parent. Open the same child's balance and transaction history. | The parent sees SGD 30.00 and the matching completed SGD 20.00 top-up entry. The internal HQ reason is hidden. If the agreed parent view shows a reference, check that it matches the HQ reference. Otherwise, use the matching method agreed before testing. | Parent balance and history. Match them to the HQ top-up using Evidence support. Hide private identifiers in saved evidence. |

## Execution record

Record results in the dated workbook copy.

| Field | Value |
|---|---|
| Execution status | Not Run |
| Test copy / run ID | |
| Build / commit | |
| QA URL / browser / real and mock service versions | |
| Business date / timezone | |
| Executed by / at | |
| Actual result | |
| Evidence references | |
| Transaction / ledger entry references | |
| Defect references | |
| What blocked the test / unknown result | |
| Reset check | |
| Reviewed by / at / notes | |

Mark Passed only when all six steps meet the confirmed expectations and have evidence.
If step 6 is not run, report the HQ checks separately, not as a pass for the whole sample.
Use Failed when evidence shows the product does not meet a confirmed expectation.
Use Blocked when a missing prerequisite prevents testing, and name what is missing.
An unconfirmed rule is a question for BA, not a confirmed product defect.

## Evidence support

Josh completes this table with Dev and Howard before the test.
The locations are blank because no screen, report or read-only query has been confirmed for this build.
Record the exact location, instructions and any matching fields in the dated workbook copy.
Do not change an expected result just to match what the build shows.

| Check | Who supplies it and what to use | Approved location / instructions |
|---|---|---|
| Opening state and no early credit, steps 1 to 3 | Josh with Dev: approved balance, history and read-only ledger checks. Save the opening records and compare them after data entry and review. | |
| Unclear top-up result, step 4 | Josh with Dev: an approved way to look up the original request's saved result. Record how to identify it if no transaction reference is returned. Do not submit a new request to find out. | |
| Final financial checks, step 5 | Josh with Dev: the official balance record, HQ history, linked Function 1 ledger entry and audit record. Record how to match the account, reference, HQ user and time. | |
| Parent history match, step 6 | Howard with Josh and BA: confirm the parent-history fields under UAT-D01. Match the reference if shown. If not, agree before testing how to use the child's account, amount, time and supporting transaction record to identify the same top-up. | |

Count actual money added, not the number of technical records.
Several linked records can describe one top-up without adding money twice.

## Readiness

The walkthrough can go ahead while these checks are open.
They must be complete before running the case.

| Prerequisite | Owner | What to confirm | Status |
|---|---|---|---|
| Agreed rules, UAT-D01 / UAT-D03 | Josh with BA | Confirm the rules listed in Preconditions and the parent matching method. Save the dated source or decision. Leave unrelated bulk questions open. | Not checked |
| Test build, UAT-D09 | Chan with Dev | Record the QA URL, build or commit, available screens and APIs, and real or mock services. Check access on this build. A task marked Done is not enough. | Not checked |
| Data and reset | Josh with Chan | Enter the test HQ, EA, child and parent IDs. Check the opening balance is SGD 10.00. Confirm that other tests cannot change this data, and record the approved reset instructions. | Not checked |
| Financial evidence | Josh with Dev | Fill the first three Evidence support rows with approved locations and read-only steps. Check access to the balance, saved result, ledger and audit records. | Not checked |
| Parent handoff | Howard | Confirm access as the linked parent and the same child's balance and history. Fill the last Evidence support row with the agreed matching method. | Not checked |
| Independent script review | Gavin | Check that another tester can follow the data, calculation, sources, steps and evidence instructions without Josh's help. Record the reviewer, date and issues. | Not checked |

## Walkthrough

| Point | What to demonstrate |
|---|---|
| Start with the purpose | Show that the correct account receives the correct amount. Check the balance and records, not only the success message. |
| Use the agreed test data | Show the test user IDs, account number and SGD 10.00 opening balance. If any are missing, stop and arrange setup. Do not pick another account. |
| Write the answer before running | Calculate 10.00 + 20.00 = 30.00 before opening the product. Expected results must not be copied from what the build happens to do. |
| Walk one step at a time | Show the action, expected result and evidence to save. During a walkthrough without the product, leave the result and evidence cells blank. |
| Show when money is added | Before confirmation, no money is added. After success, compare the balance, history and saved ledger entry. |
| Explain the handoff and review | Howard matches the parent history entry to the HQ top-up using the agreed method. Gavin checks whether another tester can follow the case. Reviewing the case does not mean the product has passed. |
| Give the team the same task | Ask each owner to complete the setup, test data, steps, expected results and evidence instructions. Link any rule questions and ask the assigned partner to review. |

## Separate variants

Keep these as separate cases in the full pack and functional tests.
The successful-route sample does not prove them.

| Variant | What the owner must specify |
|---|---|
| Cancel before confirmation | Use the agreed cancel control before confirming. The balance stays SGD 10.00 and no money is added. Use fresh or reset data before the success route. |
| Submit the same request again | Confirm the retry rules under UAT-D01. Use an approved method to send the original request again with the same request key. No second credit should occur. A new top-up is a different request and cannot prove this check. |
| Timeout or unknown result | Save the original request reference and look up its result. Do not submit again without checking, or assume no money moved. |
| Invalid amount, ineligible account or user without permission | Test amount rules, Closed accounts, age limits, eligibility-service failures and School/Parent permissions separately. One successful HQ top-up does not prove these controls. |

## Sources

| Reference | Where to find it | What it supports and does not prove |
|---|---|---|
| Existing UAT definition | uat-register.json, UAT-022; DATA-ROLES / DATA-TOPUP; US-028 / US-032 | Local draft with blank result fields. This sample expands its successful route without changing the original register or its counts. |
| Product Backlog V3, captured 22 October 2026 | ../Team sources/2026-10-22-f2/sheet1.xlsx, Product Backlog rows 33 and 37 | Story identities and intended outcomes. Sprint is TBD and the Acceptance Criteria sheet has no approved criteria. |
| Narrow F2 draft, captured 22 October 2026 | ../Team sources/2026-10-22-f2/tab_t.7jlsws8ic0aa.txt, Business Rules BR-F2-01 to 07; process steps 1 to 4; field definitions; section 5.2 AC-01 / AC-03 | Proposed rules, not approval. Supports HQ search, review, one credit only, history and hidden internal reason. The source uses 50.00; this sample uses the proposed 20.00. |
| Local F2 plan/spec v1.2.1 | function-2-test-plan.md, sections 3.1, 3.4 and 5.1 | Proposed rules, test data setup, parent history expectation and safe setup and reset. Older deferred labels do not narrow the current scope. |
| Source provenance and rule questions | ../Team sources/2026-10-22-f2/receipt.md; uat-plan.md, Open behavior and readiness questions | Competing F2 variants and current eligibility require confirmation. No source here proves the deployed UI, current build readiness or business approval. |
