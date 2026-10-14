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
- **Known Application Bugs**: Must be asserted according to the genuine business specification and marked with `@pytest.mark.xfail(strict=True, reason="BUG-xxx: <description>")`.
  - When the bug exists, pytest records `XFAIL` without failing the pipeline.
  - When the developer fixes the bug, pytest flags `XPASS (strict failure)`, alerting the team to update the test.
- **Assertion Freedom**: Playwright's `expect()` and Python assertions are first-class citizens. `Exceptor` is a convenient helper for form snapshots, not a rigid gatekeeper.
- **Infrastructure vs Business Errors**: Technical errors (timeouts, browser crashes, network disconnects) are categorized automatically in the central pytest hook `pytest_runtest_makereport` in `conftest.py`. Do **not** wrap actions in manual interceptors.

---

## 3. Step Tracking & Evidence
Tests use the `self.step()` context manager to structure execution timelines:
```python
with self.step("Step 1: Open form and submit valid data"):
    curricula.open()
    curricula.fill_full_form(data)
    curricula.save()

with self.step("Step 2: Verify success confirmation"):
    assert "Status: Active" in curricula.get_success_text()
    # Or optionally attach dynamic runtime details:
    self.step.set_actual(f"Generated Trainer ID: {trainer_id}")
```
- `actual=` is recorded automatically at runtime: on pass it confirms success; on failure it records the exception stack trace.

---

## 4. Execution Commands
```bash
# Run specific test suite
pytest tests/us04_curricula_trainer/test_ts06_save_action.py -v

# Run entire ticket suite and auto-generate HTML report
python3 run_tests.py --ticket us04_curricula_trainer
```
