# AGENTS.md - UI Automation Architecture & Agent Guidelines

## 1. Project Overview & Architecture
This project implements an Enterprise Python UI Automation Framework using **Playwright** and **pytest**, structured according to the Page Object Model (POM), modular UI component design, ticket-driven test isolation, decoupled business assertions (Exceptor & Interceptor), and a dedicated, self-contained HTML reporting engine.

```text
automation-ui/
├── README.md            # Central framework overview and quickstart
├── requirements.txt     # Python dependencies (pytest, pytest-playwright, pytest-html, pytest-xdist)
├── pytest.ini           # Pytest settings, browser modes, default reporting options, custom markers
├── conftest.py          # Shared fixtures, ticket detection, dynamic report isolation, stealth hooks
├── run_tests.py         # Two-phase test execution orchestrator (pytest -> reporting)
├── generate_report.py   # Slim CLI entrypoint for the HTML report engine (~40 lines)
│
├── docs/                # Comprehensive User Story & Architectural Documentation
│   ├── INSTRUCTIONS_FOR_EVALUATION.md # Evaluation checklist, grading roadmap & deliverable mappings
│   ├── AGENTS.md        # This architectural blueprint & developer invariant guide
│   ├── us01_bing_search/ # User Story 01: Bing Search -> YouTube Navigation
│   │   └── README.md    # US01 specs, step breakdown, and parallel execution guide
│   └── us04_curricula_trainer/ # User Story 04: Curricula Trainer Account Form
│       ├── README.md    # US04 overview, 7 test suites, execution commands
│       ├── test_cases/  # 68 Test Cases, AC-01 -> AC-68, Traceability Matrix
│       ├── defects_and_analysis/ # 10 Bugs Matrix, Severity Matrix, D4 Answer Key
│       └── ai_prompts/  # AI Generation Prompts (Deliverable 0)
│
├── core/                # Gatekeeper architecture: Business Exceptor & Infra Interceptor
│   ├── __init__.py
│   ├── exceptor.py      # Business Assertion Gate (expect_success, expect_rejection, bug hunters)
│   ├── interceptor.py   # Infrastructure Interceptor (wraps Playwright actions, categorizes infra errors)
│   ├── catalog.py       # Error Catalog (classifies timeouts, browser crashes, network failures)
│   └── exceptions.py    # BusinessAssertionError vs InfrastructureError
│
├── data/                # Inputs and test data files
│   ├── search_data.json # Parameterized test keywords and expected outputs
│   └── curricula_trainer_data.json # Trainer account profiles, boundaries & auto-populate fixtures
│
├── components/          # Reusable shared UI pieces across multiple pages
│   ├── __init__.py
│   └── search_box.py    # Search bar component (shared between Bing home & results, human typing)
│
├── pages/               # Page Objects (encapsulates page locators & interactions)
│   ├── __init__.py          # Exports BasePage, BingHomePage, BingResultsPage, CurriculaTrainerPage, YouTubePage
│   ├── base_page.py         # Base Page Object: common browser interactions (navigate, click, fill, screenshot)
│   ├── bing_home_page.py    # Bing landing page actions (inherits BasePage)
│   ├── bing_results_page.py # Search results page & link navigation (inherits BasePage)
│   ├── curricula_trainer_page.py # Curricula Trainer Account Page Object (inputs, toggles, snapshots)
│   └── youtube_page.py      # Target website page object (inherits BasePage, cookie consent, channel actions)
│
├── tests/               # Test suites (verifications, assertions, and business flows only)
│   ├── __init__.py          # Exports BaseTest
│   ├── base_test.py         # Base Test class: autouse setup, Page Object injection, report helpers
│   ├── us01_bing_search/    # User Story 1 test package (Bing search -> YouTube)
│   │   ├── __init__.py
│   │   ├── test_bing_search.py          # Single sequential test suite
│   │   └── test_bing_search_parallel.py # Parallel DDT test suite
│   └── us04_curricula_trainer/ # User Story 4 test package (Curricula Trainer Account - 7 Suites)
│       ├── __init__.py
│       ├── test_ts01_personal_info.py   # Personal Information test suite
│       ├── test_ts02_contact_info.py    # Contact Information test suite
│       ├── test_ts03_emergency_contact.py # Emergency Contact test suite
│       ├── test_ts04_singapore_address.py # Singapore Address test suite
│       ├── test_ts05_non_singapore_address.py # Non-Singapore Address test suite
│       ├── test_ts06_save_action.py     # Save Action test suite
│       └── test_ts07_cancel_action.py   # Cancel Action test suite
│
├── reporting/           # Modular HTML Report Engine (100% offline & self-contained)
│   ├── __init__.py      # Exports ReportGenerator and generate_report
│   │
│   ├── core/            # Core processing and HTML document assembly
│   │   ├── __init__.py
│   │   ├── parser.py            # Parses report.json, computes step timeline offsets, KPIs & stats
│   │   ├── media.py             # Locates videos/screenshots, encodes binary to Base64 Data URLs
│   │   ├── generator.py         # ReportGenerator: coordinates data loading, isolation & persistence
│   │   ├── document.py          # Assembles complete, self-contained HTML document
│   │   ├── views_dashboard.py   # Renders ExtentReports summary KPI dashboard cards
│   │   ├── views_tests.py       # Renders detailed test steps, timelines, and media views
│   │   └── builder.py           # Facade module re-exporting reporting components
│   │
│   ├── charts/          # Pure SVG mathematical chart renderers (Zero external JS/CDN)
│   │   ├── __init__.py
│   │   ├── donut.py     # Pure SVG Donut Chart (Pass Rate %)
│   │   ├── bar.py       # Pure SVG Duration Bar Chart for individual steps
│   │   ├── pipeline.py  # Pure SVG Interactive Step Pipeline (Step 1 -> 5 with click/pulse)
│   │   ├── diagram.py   # Pure SVG Architecture and execution flow diagram
│   │   └── trend.py     # Pure SVG Multi-Run Historical Trend Chart (Pass Rate & Duration)
│   │
│   └── assets/          # Presentation assets (syntax-highlightable, embedded at runtime)
│       ├── __init__.py  # Asset loader (inlines CSS/JS into final HTML)
│       ├── report.css   # Dark theme dashboard styles, 16:9 video, lightbox, pulse keyframes
│       └── report.js    # Client-side JS: scroll-to-video-then-play, 2-way sync, bilingual EN/VI
│
└── reports/             # Execution artifacts, reports, and evidence (ISOLATED PER TICKET)
    ├── .gitkeep         # Keeps directory tracked in Git
    └── us04_curricula_trainer/ # Isolated ticket artifacts folder (created automatically on execution)
        ├── execution_report.html # Final self-contained HTML report (latest run)
        ├── report.json           # Structured pytest execution log for this ticket
        ├── history/              # Timestamped historical run reports (RUN-*.html)
        ├── screenshots/          # ALL screenshots (deliverable evidence and failure captures)
        └── test-results/         # Playwright WebM video recordings organized by Run ID (<run_id>/)
```

---

## 2. Detailed Directory Responsibilities & Boundary Rules

### `docs/` (Specifications & User Story Documentation)
- **Role:** Centralized repository for all architectural standards, evaluation roadmaps, and User Story specifications.
- **`INSTRUCTIONS_FOR_EVALUATION.md`:** Deliverable checklist (0-3), grading guide, and rapid report evaluation without running code.
- **`AGENTS.md`:** This master architectural blueprint, Gatekeeper patterns, and developer invariants.
- **`docs/us01_bing_search/`:** User Story 1 specifications, step execution breakdown, and parallel DDT guide.
- **`docs/us04_curricula_trainer/`:** User Story 4 specifications organized into:
  - `test_cases/`: 68 Test Cases (`US04_68_TestCases.md`), Acceptance Criteria (`us04_curricula_trainer_AC.md`), and Traceability Matrix (`us04_curricula_trainer_traceability_matrix.md`).
  - `defects_and_analysis/`: Bug Traceability Matrix, Severity Matrix, and D4 Answer Key.
  - `ai_prompts/`: Prompts used for AI test generation (Deliverable 0).

### `core/` (Gatekeeper Architecture: Business Exceptor & Infra Interceptor)
- **Role:** Strictly decouples UI data harvesting (Page Object), technical error interception (Interceptor), and business correctness validation (Exceptor).
- **`Exceptor` (`core/exceptor.py`):**
  - The sole gatekeeper determining whether a test passes or fails from a business perspective.
  - Operates completely independently of Playwright, consuming and analyzing only UI state `snapshot` data provided by Page Objects: `{"success_visible": bool, "visible_errors": Dict[str, str]}`.
  - Strictly prevents test code from writing arbitrary assertions that deviate from business requirements.
- **`Interceptor` (`core/interceptor.py`):**
  - Wraps every Playwright interaction (`click`, `fill`, `navigate`, `save`) via `Interceptor.run(lambda: ..., action_name="...")`.
  - Catches infrastructure failures (Timeout, Browser crash, Stale DOM, Network disconnect), classifies them via `core/catalog.py`, and raises `InfrastructureError` (inherits from `Exception`), ensuring they are never confused with business assertion failures (`BusinessAssertionError`).

### `tests/<ticket>/requirements/` (Source of Truth & Traceability)
- **Role:** Contains Acceptance Criteria specifications (`<ticket>_AC.md`) and test traceability matrices (`<ticket>_traceability_matrix.md`).
- **Core Invariant:** Strictly eliminates the need for AI coding assistants to guess selectors, test data, or Exceptor assertion gates during test implementation.

### `pages/` (How to interact with a page)
- **Role:** Encapsulates web elements, selectors, and browser interactions.
- **Base Class:** Every Page Object MUST inherit from `BasePage` (`pages/base_page.py`).
- **Common Methods in `BasePage`:**
  - `navigate(url)`: Navigates to target URL with `domcontentloaded`.
  - `click_element(selector_or_locator, timeout)`: Waits until visible and clicks.
  - `fill_text(selector_or_locator, text, timeout)`: Waits and fills text input.
  - `wait_for_visible(selector_or_locator, timeout)`: Ensures element presence.
  - `get_title()` & `get_current_url()`: Retrieves page metadata.
  - `take_screenshot(filepath, full_page)`: Saves page screenshot.
- **Rule:** DO NOT put test assertions (`assert`) inside page objects. Page objects return data, status, snapshot, or self.
- **Rule:** Integrate reusable components from `components/` where appropriate.
- **Rule:** Always use explicit locators and Playwright expect/waits; never rely on arbitrary `time.sleep()`.

### `components/` (Reusable shared UI pieces)
- **Role:** Independent UI widgets present on multiple pages or sections (e.g., search bars, navbars, modals).
- **Decoupled Design:** Operates on a `Page` or scoped `Locator`. Example: `SearchBoxComponent` handles human-like keystroke delays (`press_sequentially`).

### `data/` (Inputs and test files)
- **Role:** Stores test inputs, credentials, search terms in JSON format (`search_data.json`, `curricula_trainer_data.json`).
- **Rule:** Never hardcode test data inside test files or page objects. Always read from `data/`.

### `tests/` (What to verify - Ticket-Driven Structure)
- **Role:** Orchestrates Page Objects and Components to execute business flows and call `Exceptor` gates.
- **Base Class:** Every test class SHOULD inherit from `BaseTest` (`tests/base_test.py`).
- **`BaseTest` Capabilities:**
  - Automatically provides `self.page`, `self.step`, `self.search_data` via `autouse=True`.
  - Provides `self.reports_dir` and `self.get_report_path(filename)` to store deliverables directly into the active ticket's report folder.
  - Provides assertion helper `self.assert_contains(actual, expected_fragment)`.
- **Folder Convention:**
  - Tests are grouped by Ticket / User Story packages: `tests/us<NN>_<ticket_name>/`.
  - Each package must contain `__init__.py`, `requirements/` folder, and test module(s) (e.g. `test_curricula_trainer.py`).
- **Step Tracking & Dynamic Reporting Rule:**
  - Every functional test step MUST be wrapped in `with self.step("Step Title", expected="...", actual="..."):`.
  - The `expected` argument MUST be extracted directly from the **Expected Result** section in the corresponding `<ticket>_AC.md` and `<ticket>_traceability_matrix.md`.
  - The `actual` argument records the exact runtime execution state (or the error message caught via `Exceptor`).
  - **Reporting Engine Standards (`reporting/`):** NEVER hardcode any scenarios, test steps, or default text of any specific User Story (such as Bing Search). All User Story Titles, Jira IDs, Step Expected, and Step Actual values MUST be dynamically extracted 100% from test nodeids, docstrings, and `self.step()` parameters.

### `reports/` (Ticket-Isolated Reporting & Artifacts)
- **Role:** Isolated target folders for test outputs, logs, videos, and HTML deliverables.
- **Isolation Mechanism:**
  - All artifacts are automatically scoped to `reports/<ticket>/`.
  - Running a ticket test will **only** clean up artifacts for that ticket; other tickets' artifacts and historical run IDs are never touched or deleted.
- **Rule:** Gitignored (except `.gitkeep`). Never commit generated test runs or large `.webm` files.

---

## 3. Acceptance Criteria (AC.md) & Traceability Matrix Authoring Standards

### 3.1 Problem Statement & Core Invariants
Previously, when AI coding agents read AC documentation containing only business descriptions, they were forced to **speculate** on three critical elements:
1. **Specific selectors / Page Object methods** → Leading to hallucinated selectors that did not exist or incorrect method calls.
2. **Specific Test Data (concrete input values)** → Leading to missed boundary cases or format discrepancies.
3. **Direct mapping to Exceptor assertion methods and error messages** → Leading to assertions against wrong field IDs or error texts that did not match the real DOM.

To completely resolve this issue, every `<ticket>_AC.md` and `<ticket>_traceability_matrix.md` file in `tests/<ticket>/requirements/` MUST strictly adhere to the following rules:

1. **Preserve 100% of Original Business Requirements**: Never delete, alter, or rephrase any wording from existing business requirement descriptions.
2. **Zero Selector Hallucination**:
   - Cross-reference directly with the corresponding Page Object file in `pages/`.
   - Explicitly document locator constants, action methods, and code line references.
   - If the Page Object **does not yet have** an independent method for that field: Explicitly tag it with `[NEEDS ADDITION TO PAGE OBJECT]` alongside a concise description; never invent non-existent selectors in code.
3. **Verbatim Error Text Extraction from Real HTML/DOM**:
   - Directly inspect the feature's HTML/DOM source, quoting the exact error message character-for-character (including punctuation and trailing periods).
   - If there is a known discrepancy between the AC and the actual UI display (e.g., leaving a field blank causes the system to display a format validation error instead of a required message - BUG-008): **Both must be explicitly documented** (the text per AC and the actual text displayed on the UI) with an explanation.
4. **Standardized Exceptor Labels & Naming Conventions**:
   - The `field` parameter passed to Exceptor functions must use the **exact DOM error identifier attribute** (e.g., `data-for` in `camelCase` such as `field="primaryPhone"`, `field="floorUnit"`).
   - Clearly label Bug-hunting cases for confirmed system defects:
     - `expect_bug_if_rejected`: For cases where input is valid per AC/real-world standards, but the system incorrectly blocks it and raises an error (e.g., Singapore alphanumeric unit numbers blocked by a digits-only regex - BUG-006).
     - `expect_bug_if_accepted`: For cases where input is invalid per AC, but the system misses validation and permits successful submission (e.g., Singapore phone numbers with an invalid prefix accepted because only length is checked - BUG-009).
5. **1:1 Strict Synchronization with Traceability Matrix**:
   - Every Test Data row defined in the tables of `AC.md` must have an exact 1:1 corresponding row in `traceability_matrix.md`, leaving zero discrepancy between the two documents.

---

### 3.2 Standard 4-Section Specification for Each AC in `<ticket>_AC.md`

Under each business requirement bullet for every AC identifier, you MUST append the following 4 standardized sub-sections:

```markdown
- **AC-XX (Standard Name)**: [Retain 100% of original business requirement text]

  **Reference Selectors:**
  - Locator element: `PageObject.<LOCATOR_CONST>` = `"<selector>"` (line ... in `pages/<page_name>.py`)
  - Action method: `PageObject.<method_name>(...)` (line ...)
  - Error locator & key: `data-for="<errorKey>"`, CSS selector `.error[data-for='<errorKey>']`, helper `get_error_text("<errorKey>")`, `is_error_visible("<errorKey>")`
  - Page Object Assessment: [Fully Available] or `[NEEDS ADDITION TO PAGE OBJECT] <Description of required method>`

  **Test Data:**
  | Case | Input Value | Expected |
  |---|---|---|
  | Valid - Standard | "Valid value" | Success |
  | Valid - Special / Unicode | "Accented characters / other languages" | Success |
  | Boundary - Upper / Lower Bound | "Boundary length string" | Success |
  | Invalid - Empty | "" | Rejected |
  | Invalid - Malformed Format | "Malformed string" | Rejected |
  | Boundary - Exceeded Limit | "String exceeding limit" | Truncated / Rejected |
  | **[BUG-HUNTING CASE]** (if any) | "Bug-triggering input value" | [Bug behavior description] |

  **Expected Result:**
  - Error Field: `<errorKey>` (exact `data-for` attribute from DOM)
  - Actual UI Error Text: `"<Verbatim error string extracted from DOM>"`
  - Known Discrepancy Notes (if any): Detail discrepancies between AC specification text and actual UI behavior.

  **Exceptor Label:**
  - Valid Case → `expect_success`
  - Invalid Case → `expect_rejection(field="<errorKey>", message_contains="<error_text>")`
  - Bug-hunting Case (Valid rejected) → `expect_bug_if_rejected(field="<errorKey>", context="...")`
  - Bug-hunting Case (Invalid accepted) → `expect_bug_if_accepted(context="...")`
```

---

### 3.3 Traceability Matrix Standards (`<ticket>_traceability_matrix.md`)

The Traceability Matrix serves as the quality control baseline, directly linking Acceptance Criteria, Test Case IDs, and Exceptor functions:

```markdown
# Traceability Matrix - <User Story Name>

1:1 cross-reference table between **Acceptance Criteria (AC.md)** and **Actual System Behavior**.
Serves as the sole authoritative reference for test suite implementation and Exceptor gate selection.

---

| AC ref | Test case ID | Input / Test Condition | Actual System Behavior | Matches AC? | Applied Exceptor Label |
|:---|:---|:---|:---|:---:|:---|
| **AC-01** | TC01 | Valid English Preferred Name ("Tan Wei Ling") | System accepts valid value and permits submission | ✅ Match | `expect_success` |
| **AC-01** | TC29 | Preferred Name containing accented Vietnamese Unicode characters | System preserves accented Vietnamese string intact | ✅ Match | `expect_success` |
| **AC-01** | TC08 | Leave Preferred Name blank and click Save | System displays error message "This field is required." at `preferredName` | ✅ Match | `expect_rejection` |
| **AC-12** | TC12_BUG | Enter 8-digit Singapore (+65) phone number starting with prefix 1 | System only validates 8-digit length and permits submission (BUG-009) | ❌ Mismatch | `expect_bug_if_accepted` |
| **AC-18** | TC17 | Enter Unit Number containing alphanumeric characters ("12A") | System blocks submission and raises error due to digits-only regex (BUG-006) | ❌ Mismatch | `expect_bug_if_rejected` |
```

---

### 3.4 Exceptor Architecture & Intent-Driven Assertions (`core/exceptor.py`)

The framework strictly prohibits scattered, arbitrary `assert` statements across test files when verifying form submissions. All UI state evaluations must pass through the `Exceptor` class using four explicit methods:

1. **`Exceptor.expect_success(snapshot, context="")`**:
   - For Happy Path: Form submits successfully, success banner is visible (`success_visible=True`), and there are zero validation errors on the form (`visible_errors={}`).
2. **`Exceptor.expect_rejection(snapshot, field="...", message_contains="...", context="")`**:
   - For Unhappy Path: Submission must be blocked (`success_visible=False`), error displays at the correct `field` (matching the `data-for` key), and error text contains the `message_contains` string.
3. **`Exceptor.expect_bug_if_rejected(snapshot, field="", context="")`**:
   - For Bug-Hunting: Input data is **VALID** per business/real-world standards. If the system incorrectly blocks submission and displays an error, Exceptor immediately raises an error prefixed with `[BUG DETECTED]`.
4. **`Exceptor.expect_bug_if_accepted(snapshot, context="")`**:
   - For Bug-Hunting: Input data is **INVALID / VIOLATES** business rules. If the system incorrectly accepts submission (`success_visible=True`), Exceptor immediately raises an error prefixed with `[BUG DETECTED] Validation Bypass`.

Example invocation in a test method:
```python
# 1. Execute action wrapped by Interceptor
Interceptor.run(lambda: curricula.save(), action_name="submit_form")

# 2. Retrieve snapshot from Page Object
snapshot = curricula.get_state_snapshot()

# 3. Evaluate via the single Exceptor Gate
Exceptor.expect_rejection(
    snapshot,
    field="primaryPhone",
    message_contains="Enter a valid contact number.",
    context="TC12 Invalid SG Phone Length",
)
```

---

### 3.5 Python Test Implementation Directly from AC & Traceability Matrix (Zero Spec Deviation)

Every line of test code in `tests/<ticket>/` must be authored or generated following the principle of **100% fidelity to the Traceability Matrix and AC**:

1. **1:1 Mapping between Test Methods and Matrix/AC:**
   - Each test case is implemented as an independent test method following the naming convention: `def test_<tc_id_lowercase>_<short_desc>(self):` (e.g., `def test_tc_pi_001_preferred_name_valid_string_entry(self):`).
   - The test method docstring MUST contain the following identification fields:
     - `TC ID`: Test case identifier from the matrix (e.g., `TC_PI_001`).
     - `Test Case Name`: Test title/summary.
     - `Test Data`: Concrete input data values.
     - `Expected (AC/Matrix)`: Business expectation / system behavior specified in the matrix.
     - `Linked Defect / CQ` (if any): Defect ID (e.g., `BUG-010`, `BUG-007`) or business clarification question.

2. **Explicit Declaration of `expected` and `actual` in every `with self.step(...)` block:**
   - Never leave `expected` or `actual` parameters blank in `self.step()`.
   - `expected`: MUST contain the verbatim expectation string from the *Actual System Behavior* column of the Traceability Matrix and the *Expected Result* section in `<ticket>_AC.md`.
   - `actual`: Accurately describes the runtime UI verification state or business outcome returned by Page Object / Exceptor.
   - Standardized example:
     ```python
     with self.step(
         "Step 1: Open page and fill form with valid Preferred Name 'Bob Wang'",
         expected="Form inputs filled and ready for submission.",
         actual="Form loaded and fields populated successfully."
     ):
         curricula.open()
         curricula.fill_full_form(data)

     with self.step(
         "Step 2: Submit form and verify successful account creation",
         expected="Value accepted without error. Account created successfully.",
         actual="Form submitted, success banner visible, and zero validation errors."
     ):
         Interceptor.run(lambda: curricula.save(), action_name="submit_form")
         Exceptor.expect_success(curricula.get_state_snapshot(), context="TC_PI_001")
     ```

3. **Zero Hardcoding Principle for Reporting Engine:**
   - The Reporting Engine (`reporting/`) and Fixtures (`conftest.py`) MUST NEVER contain hardcoded strings referencing any specific User Story (no hardcoded Bing, YouTube, Curricula, or PROJ-1042).
   - All User Story Names, Jira IDs, Test Steps, Step Expected, and Step Actual values must be 100% dynamically extracted from the package structure (`tests/us<NN>_<name>/`), test method names (`TC_...`), docstrings, and arguments passed to `self.step()`.

---

## 4. Creating New Tests via Inheritance (Quick Guide)

### Step 1: Create a new Page Object (if testing a new page)
In `pages/` (e.g. `pages/shopee_page.py`):
```python
from pages.base_page import BasePage

class ShopeePage(BasePage):
    URL = "https://shopee.vn"

    def open_home(self):
        return self.navigate(self.URL)

    def get_state_snapshot(self):
        # Return snapshot for Exceptor consumption
        return {
            "success_visible": self.page.locator("#success").is_visible(),
            "visible_errors": {
                el.get_attribute("data-for"): el.inner_text().strip()
                for el in self.page.locator(".error:visible").all()
            }
        }
```

### Step 2: Create Requirements & Test Specifications
In `tests/us<NN>_<ticket>/requirements/`:
1. Create `<ticket>_AC.md`: Write business requirement descriptions and append the full 4 technical sub-sections for each AC.
2. Create `<ticket>_traceability_matrix.md`: Construct a 1:1 cross-reference table corresponding to each Test Data row.

### Step 3: Create the Test Suite
In `tests/us<NN>_<ticket>/test_<ticket>.py`:
```python
import pytest
from tests.base_test import BaseTest
from core import Exceptor, Interceptor

@pytest.mark.curricula
class TestMyFeature(BaseTest):
    def test_tc01_valid_submission(self):
        with self.step("Step 1: Fill form and submit"):
            # Page interaction
            Interceptor.run(lambda: self.my_page.save(), action_name="save")
            Exceptor.expect_success(self.my_page.get_state_snapshot(), context="TC01")
```

### Step 4: Run the Ticket Test
```bash
python run_tests.py tests/us<NN>_<ticket>/
```

---

## 5. User Story 1 Implementation Guide

1. **Step 1:** Navigate to `bing.com` (using `self.bing_home.navigate()`).
2. **Step 2:** Search for `{Keyword1}` (Facebook) and verify first organic result title.
3. **Step 3:** Search for `{Keyword2}` (YouTube) using `self.bing_results.search_again()`.
4. **Step 4: Access target website:**
   - On `BingResultsPage`, click the first result link in the same tab (`access_first_result()`) to maintain a single continuous video.
   - Switch active context via `self.step.set_page(target_page)`.
5. **Step 5: Perform defined page actions on YouTube:**
   - Handled by `YouTubePage` (`self.youtube`).
   - Dismiss cookie consent, search channel ("VTV24"), open channel, go to Videos tab, sort oldest/latest, click to play target video.
   - Save execution screenshot evidence via `self.get_report_path("execution_step5.png")`.

---

## 6. Execution Commands Quick Reference

- **Run specific ticket test & generate isolated report:**
  ```bash
  python run_tests.py tests/us04_curricula_trainer/
  # or directly via pytest:
  pytest tests/us04_curricula_trainer/
  ```

- **Run all tests across all tickets:**
  ```bash
  python run_tests.py
  # or directly:
  pytest
  ```

- **Run parallel tests (4 workers with pytest-xdist):**
  ```bash
  python run_tests.py -n 4
  ```

- **Run with headed browser:**
  ```bash
  python run_tests.py tests/us04_curricula_trainer/ --headed
  ```

- **Regenerate HTML report without re-running tests:**
  ```bash
  python generate_report.py reports/us04_curricula_trainer/report.json
  ```
