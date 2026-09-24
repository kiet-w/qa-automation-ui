# Python Test Code Generation Requirements for US-03 Curricula Trainer Account
# (Based on the 68 Baselined Test Cases from Deliverable 3)

## Mandatory Reference Documents to Read Before Coding (in strict order)
1. `US03_68_TestCases.md` — All 68 original test cases (TC ID, Test Data, Execution
   Steps, Expected Result per FSD Standard, Priority, Technique), divided across
   7 test suites (TS-01 to TS-07).
2. `Bug_Traceability_Matrix.md` — List of 10 known bugs (BUG-001 → BUG-010),
   mapped to modules and related test cases.
3. `Severity_Matrix_10Bugs.md` — Severity level of each bug, used to identify
   release-blocking defects.
4. `core/exceptor.py`, `core/interceptor.py`, `core/exceptions.py`,
   `core/catalog.py` — Pre-existing error handling and assertion modules in the
   repository; MUST be reused, do not create new ones.
5. `pages/curricula_trainer_page.py` — Existing Page Object; MUST reuse existing
   methods/selectors; if a selector is missing for any field, explicitly mark it
   as `[TO BE ADDED TO PAGE OBJECT]`, do not invent selectors.

DO NOT read or reference the manual execution results file (Deliverable 4) at
this stage — that file is kept separate for INDEPENDENT verification after
coding is completed, ensuring test code validates genuine DOM/UI logic rather
than being tailored to match predetermined answers.

## Mandatory Principles for Converting a Test Case Row into a Python Test Function

### Step 1: Read the "Expected Result (FSD Standard)" column of each TC and categorize it into exactly 1 of 4 groups

| Identification Criteria in Expected Result Column | Group | Mandatory Exceptor Function |
|---|---|---|
| No `[Mock App Deviation...]` note, and description expects SUCCESSFUL action (e.g., "Value accepted", "accepted successfully", "Radio button switches smoothly") | Standard Happy Path | `expect_success(...)` |
| No `[Mock App Deviation...]` note, and description expects REJECTED action (e.g., "System does not accept...", "must display error...") | Standard Unhappy Path (valid validation) | `expect_rejection(snapshot, field=..., message_contains=...)` |
| CONTAINS note `[Mock App Deviation: allows ... -> BUG-XXX]`, meaning: per FSD this input must be rejected, but Mock App actually accepts it | Known Bug — INVALID input accepted by system | `expect_bug_if_accepted(snapshot, context="BUG-XXX")` |
| CONTAINS note `[Mock App Deviation: shows "..." -> BUG-XXX]` or similar, meaning: per FSD this input must be accepted/report standard error, but Mock App incorrectly rejects or shows wrong message | Known Bug — VALID input incorrectly rejected/misreported | `expect_bug_if_rejected(snapshot, field=..., context="BUG-XXX")` |

**Absolute Constraint**: DO NOT use raw `assert` statements in any test
function. All pass/fail evaluations must go through exactly 1 of the 4 Exceptor
functions above. If uncertain about which group a TC belongs to, DO NOT guess —
list that TC under the "Needs Clarification" section at the end of the report
instead of writing incorrect code.

### Step 2: Wrap all Playwright actions (click, fill, upload, save...) with Interceptor
```python
interceptor.run(lambda: curricula.save(), action_name="save_form")
```
Do not call Playwright methods directly outside of `Interceptor.run()` if that
action is susceptible to infrastructure errors (submit, navigate, upload file,
wait for element). Simple operations with no timeout risk (e.g., reading the
current value of a field to build a snapshot) may be called directly.

### Step 3: Name test functions strictly according to the original TC ID
For example, TC ID `TC_PI_003` → function name `test_tc_pi_003_preferred_name_exceeds_100_chars`
(keep the exact TC ID in the function name for easy reverse traceability to
Deliverable 3).

### Step 4: Each test must include a docstring citing the exact 3 original fields
```python
def test_tc_pi_003_preferred_name_exceeds_100_chars(self):
    """
    TC_PI_003 — Preferred Name - Exceeds 100 chars (BVA Max+1)
    Test Data: String of 101 characters ("A"*101)
    Expected (FSD): System does not accept Preferred Name exceeding 100 characters.
    [Mock App Deviation: allows 101 characters -> BUG-007]
    """
```

## Implementation Order (Do not code all 68 TCs simultaneously)
1. Implement all Priority = P1 test cases in TS-01 (Personal Information) first.
2. After completion and verifying basic execution passes (100% accuracy is not
   required immediately; code only needs to run without crashing), report back
   for review before proceeding with P1 for remaining suites.
3. Then proceed to P2 and P3 suite by suite, in strict sequence TS-01 → TS-07.
Do not write all 68 TCs at once before reporting — deliver in small batches to
detect defects early.

## Mandatory Reporting Items After Each Batch Completion
- List of implemented TCs, along with the Exceptor group applied to each TC
  (summary table).
- List of TCs with uncertain group classifications (under "Needs Clarification").
- List of missing fields/selectors in the Page Object, marked as
  `[TO BE ADDED TO PAGE OBJECT]`.
- DO NOT claim "100% completed" if any unresolved items from the above list
  remain.

## Prohibited Actions
- Do not read or use `D4_ExecutionResults_ANSWERKEY.md` at this stage.
- Do not write raw `assert` statements outside the 4 Exceptor functions.
- Do not fabricate Test Data that deviates from the "Test Data" column in
  `US03_68_TestCases.md` — if auxiliary data is needed (e.g., valid values to
  fill non-target fields), reuse standard data defined in
  `data/curricula_trainer_data.json` if available.
- Do not modify `core/exceptor.py` or `core/interceptor.py` simply "to make
  coding easier" — if an existing function is insufficient for a specific TC,
  halt and report rather than modifying core modules arbitrarily.
