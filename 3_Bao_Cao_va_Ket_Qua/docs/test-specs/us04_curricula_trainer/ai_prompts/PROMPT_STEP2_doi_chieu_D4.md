# Results Reconciliation Requirements (Run AFTER completing code generation from PROMPT_MAIN)

## Prerequisites to Start This Step
Execute this step ONLY AFTER all (or a batch of) Python test cases have been fully implemented
according to `PROMPT_MAIN_gen_test_from_deliverables.md`, and HAVE BEEN run with pytest
to obtain the actual Pass/Fail results.

## Reference Documents for This Step
- `D4_ExecutionResults_ANSWERKEY.md` — Manual execution results for the 68 test cases (Actual
  Result, Execution Status: PASSED/FAILED, associated Bug ID) previously conducted by a
  human QA engineer on the same Mock App.
- Pytest execution results obtained from the newly written Python code.

## Required Tasks

### 1. Reconcile Each Test Case (TC ID)
For each implemented test case, compare:
- **Execution Status according to Deliverable 4** (manual human execution) — PASSED or
  FAILED.
- **Pytest result** (automated code execution) — pass or fail.

### 2. Classify Reconciliation Results into 3 Groups

**Group A — Matching (Expected)**
Deliverable 4 and pytest yield the same conclusion (both Pass or both Fail, and if
Fail, both reference the correct Bug ID). No further action is required.

**Group B — Automated Code PASSES but Deliverable 4 Marks FAILED**
This is a CRITICAL warning sign — the Python code may be using the wrong Exceptor helper
(e.g., using `expect_success` for a test case that should be `expect_bug_if_accepted`),
causing actual bugs to be missed by automation. You must inspect the exact code lines for
that test case, cross-check against the `[Mock App Deviation...]` column in
`US03_68_TestCases.md`, and correct it to the appropriate Exceptor function.

**Group C — Automated Code FAILS but Deliverable 4 Marks PASSED**
There are two possibilities that must be clearly distinguished; do not assume one over the other by default:
  (a) Python code implementation error (incorrect selector, insufficient wait time, inverted
      assertion logic) — code fix required.
  (b) The actual behavior of the Mock App has changed compared to when manual QA testing was
      previously conducted, or the execution environment differs (e.g., Interceptor caught
      an InfrastructureError) — document this; do not arbitrarily alter code just to
      "force a match" without verifying the true root cause.

### 3. Report Reconciliation Results as a Table
```markdown
| TC ID | D4 Status (Manual) | Pytest Status (Automated) | Group | Notes / Actions |
|-------|--------------------|---------------------------|-------|-----------------|
| TC_PI_003 | FAILED (BUG-007) | FAILED (BUG-007, expect_bug_if_accepted) | A | Matched, no changes needed |
| TC_XX_0xx | FAILED (BUG-xxx) | PASSED | B | Incorrect Exceptor function — corrected to expect_bug_if_... |
```

## Mandatory Constraints
- DO NOT modify code solely to force pytest results to match Deliverable 4 without
  first clearly identifying whether the discrepancy belongs to Group B or Group C(a)/(b).
- For all cases falling into Group B, immediate correction is required because this introduces
  the risk of missing real bugs.
- For Group C, you must clearly state whether the root cause belongs to branch (a) or (b),
  supported by evidence (log excerpts, failure screenshots, or citations of flawed code lines)
  before deciding whether or not to modify the code.
- Upon completion, update `us03_curricula_trainer_traceability_matrix.md`
  if any test case was found to have an incorrect Exceptor label assigned from the previous step.
