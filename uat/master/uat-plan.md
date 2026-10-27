---
status: Local QA working draft
date: 25 October 2026
---

# User acceptance test plan

This is the working plan for a full-scope UAT rehearsal, not a claim that product testing or customer sign-off has happened.

## Scope and Wednesday completion

Scope is fixed: cover all Sprint 1 and Sprint 2 stories working properly, include Function 7 as View As, and provide a simple chatbot that answers system-use FAQs.
Read-only View As checks come from the captured F7 draft and require the behavior confirmation recorded in UAT-D07.
The Product Backlog V3 lists 53 stories, US-001 through US-053, with Sprint TBD; this plan conservatively covers all 53 and flags the current build-to-story mapping as an entry question.
It does not claim that V3 assigns those stories to Sprint 1 or Sprint 2 at story level.
The plan also covers R6 budget and statistics and the user-authorized FAS and extension assignments below.
No story is removed, deferred, or subject to a feature-selection meeting.

Wednesday means the reviewed execution-ready planning pack is complete: scope and traceability are present, named owners and independent rehearsal reviewers are assigned, scenarios and fixtures are defined, open behavior decisions remain visible, and the build/environment/readiness handoff is documented.
Wednesday does not mean the product has been tested, business rules have been approved, or customer acceptance has been obtained.

Pending business behavior is not excluded functionality.
Record it as a question or conditional oracle, and do not turn an implementation's observed behavior into an accepted rule.

## Ownership and review

The proposed FAS and extension work is an assignment authorized by the user's current Go, not evidence of a historical scope selection.
Source-reported story assignments are distinguished from this new QA split.

| QA owner | Work and concrete deliverables | Independent rehearsal reviewer |
|---|---|---|
| Josh, lead | Own R1 and R2; integrate the scope/story map, unresolved-rule log, readiness gates, and final pack consistency. Review the combined rehearsal report. | Gavin |
| Kent | R3 fees and school-side FAS scheme/manual review; prepare fee setup, publication/charge, school permissions, scheme configuration, manual review, and fee-to-assistance scenarios. | Chan |
| Chan | Environment, roles and shared-data controls; R3 school/enrolment; paper application/OCR; lead View As. Deliver environment/reset/fault instructions, role matrix, enrolment scenarios, paper/OCR checks, and View As checks. | Kent |
| Howard | Parent R8, online FAS submission/details and FAQ; common scenario format. Deliver parent identity/access/history and application journeys, FAQ question-and-answer coverage, and an independent rehearsal record using Gavin's scenarios. | Gavin |
| Gavin | R9 payments, FAS assessment/subsidy/reconciliation, R6 budget/statistics. Deliver payment lifecycle and reconciliation scenarios, MOEFAS assessment/subsidy cases, and budget/statistics coverage. | Howard |

The source captures and Padlet report Kent's F3 plan and Kent/Chan's fee module, Chan's environment/login automation, Howard's R8, and Gavin's R9 plus income synthetic task.
Treat those as reported prior work, not product acceptance evidence or proof that current builds contain the work.
The assignments above preserve those source-reported areas and add the explicit current split.

Each member records an independent rehearsal with a different member's scenario set, fixture, expected result, observed result, evidence reference, and any mismatch.
The reviewer must not simply endorse the author's expected result; unresolved rule conflicts stay unresolved.

## Common scenario record

Use one record per user-visible behavior or meaningful failure boundary, linked to the relevant source story or local scenario reference.
Do not create official US or BUG identifiers.

| Field | Record |
|---|---|
| Local scenario reference | Stable local reference; no invented official story or defect ID. |
| Story and source trace | V3 story or requirement, source document/version/section, and whether the source is draft, board-reported, or approved. |
| User and purpose | Role, task, and intended outcome in plain language. |
| Preconditions and fixture | Synthetic account/person, relationships, statuses, balances, dates, and required setup. |
| Steps | Numbered actions a tester can repeat. |
| Expected result | Rule-backed result, or a clearly marked conditional expectation linked to a pending decision. |
| Evidence | Build, environment, timestamp, screenshots/API or audit evidence, and data reconciliation where relevant. |
| Actual outcome | Blank until an authorized run; never fill from a source report or rehearsal assumption. |
| Result and follow-up | Not Run until execution; use Passed, Failed, Blocked or Not Run, preserve existing team IDs and link unresolved rules. No conditional pass. |
| Rehearsal | Author, independent reviewer, rehearsal date, and review notes. |

## Integrated journeys

### FAS application through payment

Rehearse the end-to-end business path with synthetic data and linked evidence.

1. Prepare school/student/enrolment data, fee catalogues and rates, then preview and publish charges once, independently of FAS.
2. Configure MOEFAS and school-owned SBFAS schemes, submission windows and effective periods.
3. Submit online parent applications and paper applications, including human review/correction of simulated OCR values.
   UAT-049 covers a two-child family submission through both channels, shared household data and family ID, separate child application IDs and independent decisions/subsidies.
   Its cross-school sibling variant follows UAT-D04; a paper submission with no child at the submitting school is a separate rejection control, not a blanket ban on other-school siblings.
4. Reopen the same application at the correct reviewer; follow the selected assessment timing, routing and permission rules under UAT-D04.
5. Apply the agreed subsidy to eligible unpaid charges, retaining the original amount and correct net payable.
6. Pay the net amount through the parent journey, including split payment, failure/recovery and matching invoice, receipt and EA history.
7. Reconcile the application decision, grant, charge, payment, budget statistics and role-scoped views using the same entity IDs throughout.

Top-up has separate configuration, preview, execution, history, scheduled-run, partial-failure recovery and correction scenarios.
Account lifecycle/CPF scenarios connect to parent access, top-up and payment checks.
Requested scheduling and failed-only retry behavior remain visible without assuming the team has already agreed their implementation contract.

FAS submission through review, subsidy, charge and payment is the main integrated demonstration journey.
Setup and master data remain full coverage: school and class structure, enrolment, fee types/components/rules, scheme setup, publication, rates, user/role setup, and relevant budgets are tested as their own scenarios even when they are not on the main demo path.

### View As and FAQ boundaries

Function 7 is tested as a proposed MOE HQ support view of a selected School Officer or specific Parent, matching the target user's visible screen in read-only mode, displaying a clear simulation banner, and recording session details for audit.
These are the captured doc1 requirements 7.1-7.3, not confirmation of unresolved target, authority, or session rules.
Verify that simulated actions cannot mutate target data, that the real operator remains identifiable, and that exit returns to the operator's own context; treat exact session and audit semantics as pending where not specified.

The chatbot is limited to simple answers about using the system, based on an approved FAQ set.
It does not submit applications, make decisions, execute payments, alter records, or auto-fill forms as an engine.
Test answer correctness, clear fallback for an unsupported question, and no claim that the bot performed a transaction.
FAQ answer list, location, languages, and fallback remain readiness questions.

## Fixtures, controls and safety

Use synthetic identities and records only.
No real NRIC, parent, student, payment credential, password, token, or production secret belongs in this plan or its evidence.
Chan owns the shared fixture and environment-control instructions; each scenario owner identifies required fixture rows and reset dependencies.
Before a run, record the named build/commit, environment, service dependencies, mocks, role mapping, date/time control, fault controls, and authorized reset method.
Reset must be isolated, reversible, and owned; reconcile balances, ledger, charges, applications, decisions, payments, and audit evidence before and after a journey.
Never change a shared record or stop an unowned process.
Use controlled business dates and per-case fault injection only where authorized; document unavailable controls as gates, not assumed behavior.

## Entry and exit gates

### Entry

- Named test build/commit and story-to-build mapping, including V3 US-001 through US-053 and the intended Sprint 1/Sprint 2 coverage.
- Isolated environment URL, service/component availability, mock boundaries, test roles, and synthetic identity mappings.
- Approved fixture/reset ownership, date control, fault/retry controls, and access to authoritative persisted evidence.
- Scenario owners and independent rehearsal reviewers named; resolve the relevant UAT-D01 through UAT-D10 questions before scoring an affected scenario.
- Named business acceptance representative and authority to accept or reject each business outcome.

### Preparation completion

- Every in-scope story and added area has a traceable scenario or a documented readiness blocker; no scope is silently dropped.
- All planned scenarios have evidence-backed outcomes or remain explicitly Blocked/Not Run with the unmet gate recorded.
- Financial and application state reconciles across submission, decision, subsidy, charge, payment, top-up, history, and audit where applicable.
- Independent rehearsal records are complete, mismatches are logged, and rule questions remain open until an authorized answer is recorded.
- Report ready and blocked journeys separately; a missing build, fixture or rule means the affected journey is not yet execution-ready.

### UAT acceptance exit

- Every included scenario and meaningful variant has a build-specific executed result and evidence; unresolved rules and Not Run outcomes are not accepted coverage.
- Blocking defects are fixed and retested, or acceptance is withheld for the affected journey.
- The authorized business representative records a dated acceptance decision with any exact residual limitations and linked failed tests.

An accepted defect is not a pass.
Record the defect, risk, owner, disposition, and retest need.
Even if the acceptance authority accepts a residual risk, the underlying failed test remains Failed.
QA/BA rehearsal is preparation, not business acceptance.
The representative is currently unknown and must be named before UAT entry.

## Open behavior and readiness questions

These local references capture questions, not scope exclusions or official product IDs.

| Local ref | Question to resolve or carry as conditional |
|---|---|
| UAT-D01 | F2 criteria AND/OR, current authoritative criterion, budget, re-execution, and correction behavior conflict across drafts. Do not infer one contract from the board or implementation. |
| UAT-D02 | Customer feedback requests scheduled top-up and failed-only retry behavior; whether and how these work in the implementation is not agreed. |
| UAT-D03 | R1 closure and CPF: v1.2 includes mixed CR/TD/WA and CPF deferred language, while the sprint report says Done. Confirm the deployed lifecycle and settlement contract. |
| UAT-D04 | FAS timing and permissions: FS F4 1.3 says MOEFAS decisions occur after form closure and HQ is read-only for decisions; older backlog describes immediate auto-grant. Confirm applicable rule, cross-school family submission/visibility, and separate child-school routing and decisions. |
| UAT-D05 | R6 budget behavior: source conflict between warning-only and older budget-block grant behavior. Confirm whether a threshold warns or prevents a grant. |
| UAT-D06 | FAS additional-income inclusion, supporting-document limits, rounding, paid charges, and multiple grants need business rules before exact expected totals can be accepted. |
| UAT-D07 | View As target eligibility, authorities, server-enforced read-only behavior, audit fields, and exit/session semantics require confirmation. |
| UAT-D08 | FAQ approved answers, location, languages, and unsupported-question fallback need an owner and confirmation; the scope remains a simple system-use FAQ. |
| UAT-D09 | Named build, mocks, environment, operators, and business acceptance representative are missing; identify them before execution. |
| UAT-D10 | Choose the R3 effective-date, transfer, rate-period, publication/replay and CSV row-processing rules used by the school/fee scenarios. |

## Source standing and companion files

The Product Backlog V3, sprint board, requirements analysis, functional specifications, and meeting records have different authority.
The captured source register describes documents as drafts or reported status, not approvals; meeting minutes and transcript have conflicting date headers, so this plan does not choose a date or treat either as acceptance.
The 22 October F2 receipt likewise labels captures as private team documents, not approvals or execution evidence.
The R1 v1.2 source carries mixed CR/TD/WA status and CPF-related deferral; it does not settle the current contract.
Sources identify requested work and questions; only an authorized business decision can settle a business rule.

The sibling [uat-workbook.xlsx](uat-workbook.xlsx) is the readable execution companion, and [uat-register.json](uat-register.json) is its scenario dataset source.
The pack contains 49 scenarios, 151 action/expected-result steps and 66 coverage rows: 53 backlog stories, 11 R6 requirements and the two local addition labels.
Use Assignments for the work split, Coverage for the story map, Scenarios and Script steps for execution, and Data, Decisions, Readiness and Sources for preparation.
The full source locators and standing are in the workbook's Sources sheet and the JSON source register.
All execution statuses begin Not Run, with actual-result and build-evidence fields blank.
This planning task performs no product tests.

The [readiness audit](uat-readiness-audit.md) records the remaining execution gaps, per-owner tasks and earlier observations to retest.
It reads the definition pack and two local defect records; it adds no scenario and no result.

The companion [UI/BSK coverage matrix](ui-bsk-coverage.md) maps the captured 26 screen groups to UAT scenario families. Use it with this business plan when deriving screen and control-level testcases. It does not add execution results or replace BR/AC/validation/flow/error oracles; unresolved behavior remains `SPEC GAP` and blocks a full-coverage claim.
Keep a dated workbook copy for execution; do not edit the generated definition workbook by hand.
Use `python3 -B build-uat-workbook.py` to rebuild definitions and `python3 -B build-uat-workbook.py --check` to check that the blank planning workbook matches the source.
The checker intentionally does not accept a filled execution copy as the reusable definition workbook.
Run `python3 -B -m unittest -v test_uat_workbook.py` for artifact validation, not product testing.

### Worked example for the team

Use [Josh's individual top-up sample](uat-sample-f2.md) and its [presentation workbook](uat-sample-f2.xlsx) to demonstrate how an owner completes a case.
It expands the successful route within UAT-022, with proposed SGD 10.00 opening balance, SGD 20.00 top-up and SGD 30.00 closing balance, plus matching HQ/parent evidence.
The sample remains Not Run, with blank execution fields and explicit rule/data/readiness gates.
Cancellation and same-operation replay remain separate variants; the sample does not replace UAT-022 or change the pack's scenario counts.
