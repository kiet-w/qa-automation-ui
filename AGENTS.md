# AGENTS.md - UI Automation Architecture & Agent Guidelines

## 1. Architectural Philosophy
This repository implements an Enterprise UI Automation Framework using **Playwright** and **pytest**.
The architecture is designed for high reliability, minimal boilerplate, and strict verification gates.

```text
automation-ui/
├── core/                # Business exception types, error catalog & classification helpers
├── pages/               # Page Objects (encapsulate locators & user interactions)
├── components/          # Reusable UI widgets shared across pages
├── data/                # Parameterized test inputs & mock datasets (JSON)
├── tests/               # Test suites, assertions & functional verifications
├── conftest.py          # Central fixtures, video recordings & hook-based error classification
├── run_tests.py         # Test execution orchestrator
└── reporting/           # Offline, self-contained HTML report generator
```

---

## 2. Five Core Invariants for AI & Developers

### Invariant 1: Zero Assertions in Page Objects
- Page Objects (`pages/`) and Components (`components/`) must only perform actions and query UI state.
- **Never** place `assert` or validation logic inside Page Objects.
- All functional validations, assertions, and checks must live inside the `tests/` suites.

### Invariant 2: Zero Hardcoded Test Data
- All test parameters, form inputs, credentials, and expected boundary values must come from `data/` JSON fixtures or pytest fixtures.
- Test suites must deep-copy data templates before modification (`copy.deepcopy(DATA[...])`).

### Invariant 3: Test Case Identification & Traceability
- Every test function must start with `test_tc_<scenario_id>_...` and correspond to an explicit functional requirement or Acceptance Criterion.
- Maintain a structured docstring describing: Scenario, Test Data, and Expected Behavior.

### Invariant 4: Zero `time.sleep()`
- Never use `time.sleep()`.
- Rely entirely on Playwright's built-in auto-waiting, `wait_for_selector()`, `wait_for_load_state()`, or Playwright's `expect(locator)` assertions.

### Invariant 5: Verification-First Bug Handling & Hook-Based Classification
- **Business Assertion Options (Two Compatible Modes)**:
  1. **Snapshot Gatekeeper (`Exceptor`)**: For complex forms and UI snapshots, use `Exceptor.expect_success(snapshot)`, `Exceptor.expect_rejection(snapshot, field, message_contains)`, `Exceptor.expect_bug_if_accepted(snapshot)`, or `Exceptor.expect_bug_if_rejected(snapshot)`.
  2. **Pytest Strict XFAIL**: For known bugs tracked via Jira/ticket IDs, decorate with `@pytest.mark.xfail(strict=True, reason="BUG-xxx: <description>")` and assert genuine business specification.
- **Infrastructure vs Business Errors**: Technical errors (timeouts, browser crashes, network disconnects) are categorized automatically in the central pytest hook `pytest_runtest_makereport` in `conftest.py`. Do **not** wrap actions in manual interceptors.

---

## 3. Step Tracking & Evidence
Tests use the `self.step()` context manager to structure execution timelines:
```python
with self.step("Step 1: Open form and submit valid data"):
    self.curricula.open()
    self.curricula.fill_full_form(data)
    self.curricula.save()

with self.step("Step 2: Verify success confirmation"):
    snapshot = self.curricula.get_state_snapshot()
    Exceptor.expect_success(snapshot, step=self.step)
    # Or optionally attach dynamic runtime details:
    self.step.set_actual(f"Trainer ID created successfully.")
```
- `actual=` is recorded automatically at runtime: on pass it confirms success; on failure it records the exception stack trace.

---

## 4. Special Directives for AI Coding Assistants
When generating automated tests from Acceptance Criteria (AC), User Stories, or Test Case matrices:
1. **Never Invent Locators**: Always inspect and reuse methods in `pages/`. If a selector is missing, mark with `[TO BE ADDED TO PAGE OBJECT]` rather than writing raw `page.locator()` in the test file.
2. **Inherit from `BaseTest`**: Subclasses have immediate access to `self.page`, `self.step`, `self.curricula`, `self.get_page(PageClass)`, and `self.get_fixture_file(path)`.
3. **Handle Native Browser Dialogs**: If an action triggers `confirm()` or `alert()` (e.g. Cancel button), always call `self.curricula.handle_next_dialog(accept=True)` before clicking the trigger.
4. **Deep Copy Data Payloads**: Always use `copy.deepcopy(curricula_data["..."])` before modifying payload dictionaries to ensure test isolation during parallel execution.
5. **Never Swallow Exceptions**: Do not wrap test assertions in empty `try...except` blocks. If an error occurs, let it raise so `StepTracker` and `pytest_runtest_makereport` can record diagnostic evidence.

---

## 5. Execution Commands & Concurrency Control
```bash
# Run specific test suite
python3 run_tests.py tests/us04_curricula_trainer/test_ts06_save_action.py -v

# Run entire ticket suite and auto-generate HTML report
python3 run_tests.py tests/us04_curricula_trainer
```

### Execution Isolation & Artifact Retention:
1. **Concurrency Lock**: `run_tests.py` enforces a ticket-scoped file lock (`fcntl.flock`). Concurrent runs targeting the same ticket will be safely rejected with a `[LOCKED ERROR]` to prevent test data collision and report corruption.
2. **Permanent Run History**: Every execution permanently archives its standalone HTML report in `reports/<ticket>/history/<RUN_ID>.html` and raw video recordings in `reports/<ticket>/test-results/<RUN_ID>/`. The top-level `reports/<ticket>/execution_report.html` always points to the latest run.


