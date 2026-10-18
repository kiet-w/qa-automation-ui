# Enterprise QA Automation UI Framework — Complete Codebase Context

> **Target Audience:** AI Coding Assistants (LLMs) & Automation Engineers  
> **Repository:** `kiet-w/qa-automation-ui`  
> **Language / Runtime:** Python 3.10+ (Sync Playwright)  
> **Core Frameworks:** `pytest`, `playwright`, `pytest-xdist`, `pytest-json-report`  
> **Reporting Engine:** 100% Offline Self-Contained ExtentReports Engine (Zero External CDN)  
> **Last Updated:** October 2026  

---

## 1. Executive Summary & Purpose

This repository is an enterprise-grade UI test automation framework written in Python using Playwright (synchronous API) and Pytest. It is specifically engineered around high reliability, zero flakiness, dual-gate error supervision, and complete offline auditability.

### Primary Missions & Scope
1. **User Story 1 (`tests/us01_bing_search`)**:
   - End-to-end multi-step navigation: Bing Search Engine -> Search Facebook -> Search YouTube -> Navigate to target website -> Search VTV channel -> Filter by earliest video -> Play video & capture screenshot evidence.
   - Features bot-evasion techniques, human-like typing cadence (`press_sequentially`), and URL redirect decoding.
2. **User Story 2 & 4 (`tests/us04_curricula_trainer`)**:
   - Comprehensive test automation for the **Curricula Create Trainer Account** web application (`curricula_trainer_account.html`).
   - 68 Test Cases mapped 1:1 against Acceptance Criteria (`AC.md`) across 7 test suites (Personal Info, Contact Info, Emergency Contact, Singapore Address, Non-Singapore Address, Save Action, Cancel Action).
   - Deep testing of 10 known application defects/bugs using intentional bug-hunting assertions.
3. **Dual-Gate Framework Verification (`tests/unit`)**:
   - 26 unit tests verifying the framework's internal error taxonomy (`catalog.py`), business gates (`exceptor.py`), and infrastructure supervisor (`interceptor.py`).

---

## 2. Architectural Pillars & Core Patterns

```text
       ┌────────────────────────────────────────────────────────┐
       │             User Story Requirements (AC.md)            │
       └───────────────────────────┬────────────────────────────┘
                                   │  1. Map Test Intent
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │       Traceability Matrix (traceability_matrix.md)     │
       │   [Assign: expect_success / expect_rejection / ...]    │
       └───────────────────────────┬────────────────────────────┘
                                   │  2. Direct Method Assignment
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           TEST CASE EXECUTION                           │
│                                                                         │
│   ┌───────────────────────────┐         ┌───────────────────────────┐   │
│   │    Playwright Actions     │         │     Page Object State     │   │
│   │  (click, fill, save, ...) │         │  (Snapshot: errors, box)  │   │
│   └─────────────┬─────────────┘         └─────────────┬─────────────┘   │
│                 │                                     │                 │
│                 ▼                                     ▼                 │
│   ┌───────────────────────────┐         ┌───────────────────────────┐   │
│   │        Interceptor        │         │         Exceptor          │   │
│   │ (Catches technical infra) │         │(Adjudicates business rule)│   │
│   └─────────────┬─────────────┘         └─────────────┬─────────────┘   │
└─────────────────┼─────────────────────────────────────┼─────────────────┘
                  │                                     │
                  ▼                                     ▼
     ┌────────────────────────┐            ┌────────────────────────┐
     │  InfrastructureError   │            │ BusinessAssertionError │
     │ [TIMEOUT, CRASH, NET]  │            │  [BUG / REJECTION OK]  │
     └────────────────────────┘            └────────────────────────┘
```

### Pillar 1: Dual-Gate Error Supervision (`core/`)
Traditional test frameworks lump all failures into a generic `FAILED` status, making it impossible to quickly differentiate between a real software bug and an infrastructure timeout/flakiness. This framework completely separates them:

1. **`Exceptor` (`core/exceptor.py`) — Business Assertion Gate**:
   - The **SOLE** authority deciding whether a test passes or fails from a business perspective.
   - Operates strictly on **static UI snapshots** (`dict` containing `{"success_visible": bool, "visible_errors": Dict[str, str]}`) provided by Page Objects.
   - It **never** invokes Playwright directly.
   - Raises `BusinessAssertionError` (subclasses standard Python `AssertionError`), which Pytest treats as a test failure.
   - **4 Intent-Driven Assertion Methods**:
     - `expect_success(snapshot, context)`: Asserts `success_visible is True` and `visible_errors` is empty (Happy Path).
     - `expect_rejection(snapshot, field, message_contains, context)`: Asserts `success_visible is False`, error exists on `field`, and message contains expected text (Unhappy Path).
     - `expect_bug_if_rejected(snapshot, field, context)`: When input is legally valid according to FSD, but the application incorrectly rejects it. If rejected, raises `[BUG DETECTED]`.
     - `expect_bug_if_accepted(snapshot, context)`: When input is invalid according to FSD, but the application incorrectly accepts it (Validation Bypass). If accepted, raises `[BUG DETECTED]`.

2. **`Interceptor` (`core/interceptor.py`) — Infrastructure Supervisor**:
   - Explicitly wraps Playwright interactions (`click`, `fill`, `navigate`, `save`) via `Interceptor.run(action_fn, action_name="...", context="...")`.
   - Catches technical exceptions (network cut, browser crash, element detach, timeout).
   - Passes the exception through the **Error Catalog** (`core/catalog.py`) for automated diagnosis.
   - Raises `InfrastructureError` (subclasses `Exception`, **NOT** `AssertionError`), preserving root-cause traceback via `raise ... from exc`.

3. **`Error Catalog` (`core/catalog.py`)**:
   - Pattern-matching engine classifying technical errors into 5 standard categories:
     - `TIMEOUT`: Playwright TimeoutError or `Timeout \d+ms exceeded`. Hint: Check selector or increase timeout.
     - `BROWSER_CRASH`: `Target closed`, `browser has been closed`. Hint: Browser process crashed unexpectedly.
     - `STALE_ELEMENT`: `Element is not attached to the DOM`, `stale element reference`. Hint: DOM re-rendered; refresh locator.
     - `NETWORK`: `net::ERR_`, `NS_ERROR_CONNECTION_REFUSED`. Hint: Network connectivity error.
     - `UNKNOWN`: Unclassified technical failure.

---

### Pillar 2: Pure Separation in Page Object Model (`pages/` & `components/`)
- **Strict Invariant**: **Page Objects NEVER contain assertions (`assert`)**.
- Page Objects are strictly element locators and interaction drivers. They return data, state, or snapshots:
  ```python
  # In CurriculaTrainerPage:
  def get_state_snapshot(self) -> Dict[str, Any]:
      return {
          "success_visible": self.is_success_visible(),
          "visible_errors": self.get_all_visible_errors(), # dict: {"fieldName": "Error text"}
      }
  ```
- All verifications belong exclusively in the test layer (`tests/`) using `Exceptor`.
- Reusable components (e.g. `components/search_box.py`) handle shared widgets and human typing cadence (`press_sequentially`).

---

### Pillar 3: Ticket-Driven Test Isolation (`reports/<ticket>/`)
- Tests are executed and organized per Ticket / User Story:
  - `tests/us01_bing_search/` -> Isolated reports under `reports/us01_bing_search/`
  - `tests/us04_curricula_trainer/` -> Isolated reports under `reports/us04_curricula_trainer/`
  - `tests/unit/` -> Isolated reports under `reports/unit/`
- Every test session generates a unique `run_id` (e.g. `RUN-20260923-61EC0C`).
- Videos and artifacts are stored in `reports/<ticket>/test-results/<run_id>/`.
- Running tests for one ticket **never** wipes or interferes with reports or history of other tickets.
- Permanent, immutable historical HTML snapshots are saved under `reports/<ticket>/history/<run_id>.html`.

---

### Pillar 4: 100% Offline ExtentReports HTML Engine (`reporting/`)
- **Zero External Dependencies**: Does **NOT** load Chart.js, Tailwind, Google Fonts, or external CDNs.
- **Pure SVG Mathematical Renderers** (`reporting/charts/`):
  - `donut.py`: Circle math calculating stroke-dasharray & stroke-dashoffset for Pass/Fail rates.
  - `bar.py`: SVG timeline bar chart rendering execution durations for each step.
  - `pipeline.py`: Step-by-step interactive workflow pipeline (Step 1 -> N) with click listeners.
  - `diagram.py`: Architecture topology diagrams.
  - `trend.py`: Historical multi-run pass rate and duration trend lines.
- **Base64 Embedded Media** (`reporting/core/media.py`):
  - 1080p WebM videos and PNG screenshots are converted into Base64 Data URIs (`data:video/webm;base64,...`) and embedded directly into the standalone HTML file.
- **Two-Way Diagram-to-Video Synchronization** (`reporting/assets/report.js`):
  - Clicking any step in the SVG execution pipeline diagram automatically scrolls to the embedded video player, seeks to the exact step timestamp, and plays back the video.
- **Built-in Bilingual Toggle**: Real-time client-side switching between English (`EN`) and Vietnamese (`VI`).

---

## 3. Detailed Repository File Structure

```text
automation-ui/
├── CODEBASE_CONTEXT.md                      # [THIS FILE] Master context for AI agents & engineers
├── README.md                                # Central documentation, quickstart & usage guide
├── requirements.txt                         # Python dependencies
├── pytest.ini                               # Pytest configuration, markers, and default CLI flags
├── conftest.py                              # Master Pytest hooks, browser engines, isolation, video hooks
├── run_tests.py                             # 3-Phase orchestrator (Pytest -> HTML Report -> Terminal Summary)
├── generate_report.py                       # Standalone CLI entrypoint for HTML report generation
├── curricula_trainer_account.html           # Local web application under test (User Story 2/4)
│
├── core/                                    # 🛡️ Dual-Gate Error Supervision Layer
│   ├── __init__.py                          # Exports Exceptor, Interceptor, BusinessAssertionError, InfrastructureError
│   ├── exceptions.py                        # Custom Exception classes (BusinessAssertionError vs InfrastructureError)
│   ├── exceptor.py                          # Sole business assertion gate (expect_success, expect_rejection, bug hunters)
│   ├── interceptor.py                       # Playwright interaction supervisor & error classifier
│   └── catalog.py                           # Centralized Error Catalog (TIMEOUT, BROWSER_CRASH, STALE_ELEMENT, NETWORK)
│
├── pages/                                   # 📄 Page Object Model Layer (NO ASSERTIONS ALLOWED)
│   ├── __init__.py                          # Exports BasePage, BingHomePage, BingResultsPage, CurriculaTrainerPage, YouTubePage
│   ├── base_page.py                         # Common web actions: navigate, wait, click, fill, screenshot
│   ├── bing_home_page.py                    # Bing landing page locators & search flow
│   ├── bing_results_page.py                 # Bing search results page & redirect handling
│   ├── curricula_trainer_page.py            # Comprehensive Curricula form locators, toggles, fills, get_state_snapshot
│   └── youtube_page.py                      # Target website page object: cookie consent, search channel, filter earliest
│
├── components/                              # 🧩 Modular Reusable UI Components
│   ├── __init__.py                          # Exports SearchBoxComponent
│   └── search_box.py                        # Search bar component with human typing emulation (press_sequentially)
│
├── tests/                                   # 🧪 Test Suites & Verification Logic
│   ├── __init__.py                          # Exports BaseTest
│   ├── base_test.py                         # Base test class: autouse setup, Page Object injection, StepTracker, helpers
│   ├── unit/                                # Internal Framework Reliability Unit Tests (26 tests)
│   │   ├── __init__.py
│   │   ├── test_catalog.py                  # Validates error regex and exception matching
│   │   ├── test_exceptor.py                 # Validates Exceptor 4 gatekeeper methods
│   │   └── test_interceptor.py              # Validates Interceptor exception translation
│   ├── us01_bing_search/                    # User Story 1: Bing Search -> YouTube Navigation
│   │   ├── __init__.py
│   │   └── test_bing_search.py              # 5-step sequential E2E test with bot evasion
│   └── us04_curricula_trainer/              # User Story 4: Curricula Trainer Account (68 Tests, 7 Suites)
│       ├── __init__.py
│       ├── requirements/                    # Formal specifications & Source of Truth
│       │   ├── us04_curricula_trainer_AC.md # Verbatim Acceptance Criteria (AC-01 -> AC-68)
│       │   └── us04_curricula_trainer_traceability_matrix.md # 1:1 mapping from AC to Exceptor method
│       ├── test_ts01_personal_info.py       # Test Suite 1: Preferred Name, Gender, ID, Nationality, DOB, Tax
│       ├── test_ts02_contact_info.py        # Test Suite 2: Email, Primary/Secondary Country Code & Phone
│       ├── test_ts03_emergency_contact.py   # Test Suite 3: Contact Name, Relationship, Code & Phone
│       ├── test_ts04_singapore_address.py   # Test Suite 4: Postal code, Block, Building, Street, Floor, Unit
│       ├── test_ts05_non_singapore_address.py # Test Suite 5: Country, Address Lines 1-2, City, State/Province
│       ├── test_ts06_save_action.py         # Test Suite 6: Save triggers, mandatory checks, bug verification
│       └── test_ts07_cancel_action.py       # Test Suite 7: Cancel confirmation dialog & form reset
│
├── reporting/                               # 📊 100% Offline ExtentReports HTML Engine
│   ├── __init__.py                          # Exports ReportGenerator
│   ├── core/
│   │   ├── __init__.py
│   │   ├── parser.py                        # Parses report.json, computes timeline offsets & duration KPIs
│   │   ├── media.py                         # WebM / PNG Base64 Data URI encoder
│   │   ├── generator.py                     # Coordinates data loading, chart rendering & HTML compilation
│   │   ├── document.py                      # Assembles monolithic standalone HTML document
│   │   ├── views_dashboard.py               # ExtentReports summary KPI dashboard cards
│   │   ├── views_tests.py                   # Detailed test step cards, timelines, videos, screenshots
│   │   └── builder.py                       # Facade module re-exporting reporting sub-modules
│   ├── charts/                              # Pure mathematical SVG chart generators (Zero JS chart libs)
│   │   ├── __init__.py
│   │   ├── donut.py                         # Pure SVG Donut Chart (Pass/Fail %)
│   │   ├── bar.py                           # Pure SVG Step Duration Bar Chart
│   │   ├── pipeline.py                      # Pure SVG Interactive Step Pipeline (Step 1 -> 5)
│   │   ├── diagram.py                       # Pure SVG Architecture & test flow diagram
│   │   └── trend.py                         # Pure SVG Historical Trend Chart
│   └── assets/
│       ├── __init__.py                      # Inlines CSS and JS assets at build time
│       ├── report.css                       # Modern dark-theme UI, 16:9 responsive video, animations
│       └── report.js                        # Client-side 2-way sync, video seek, bilingual EN/VI toggle
│
├── data/                                    # 🗄️ Test Data Fixtures & Payloads (Zero Hardcoding)
│   ├── search_data.json                     # Search terms, keywords, target action configs
│   ├── curricula_trainer_data.json          # Pre-built trainer profiles (valid SG resident, edge cases)
│   └── fixtures/                            # Upload files for ID document testing
│       ├── valid_id.pdf                     # Valid 2MB PDF document
│       ├── valid_id.png                     # Valid PNG image
│       ├── oversized_11mb.pdf               # >10MB PDF testing boundary rejection
│       ├── invalid_document.txt             # Disallowed extension testing MIME filter
│       ├── malicious.exe                    # Dangerous executable testing security rejection
│       └── document.docx                    # Disallowed office format
│
├── docs/                                    # 📚 Documentation, Specs & Deliverables
│   ├── INSTRUCTIONS_FOR_EVALUATION.md       # Quickstart, Deliverables checklist & grading roadmap
│   ├── AGENTS.md                            # Technical guidelines & developer invariants
│   ├── us01_bing_search/README.md           # US01 specs & parallel execution guide
│   └── us04_curricula_trainer/              # US04 documentation
│       ├── README.md                        # US04 overview, 7 test suites, execution commands
│       ├── test_cases/                      # 68 Test Cases (US04_68_TestCases.md)
│       ├── defects_and_analysis/            # Bug Traceability Matrix, Severity Matrix, D4 Answer Key
│       └── ai_prompts/                      # Deliverable 0: AI Generation Prompt
│
├── examples/                                # Reference examples & parallel test showcases
│   ├── example_usage.py                     # Standalone demo of Exceptor & Interceptor
│   └── test_bing_search_parallel.py         # Parallel DDT Bing search example
│
└── reports/                                 # 📂 Generated Test Artifacts (ISOLATED PER TICKET)
    ├── us01_bing_search/                    # Artifacts for US01
    ├── us04_curricula_trainer/              # Artifacts for US04 (HTML report, history, screenshots, videos)
    └── unit/                                # Artifacts for Unit Tests
```

---

## 4. Key Classes, Signatures & Code Examples

### 4.1 `core/exceptor.py`
```python
from core.exceptor import Exceptor

# 1. Happy Path: Expect action to succeed
Exceptor.expect_success(snapshot: dict, context: str = "")

# 2. Unhappy Path: Expect rejection at specific field with error message
Exceptor.expect_rejection(
    snapshot: dict,
    field: str,
    message_contains: str,
    context: str = ""
)

# 3. Bug Hunting: Valid business input was improperly rejected
Exceptor.expect_bug_if_rejected(snapshot: dict, field: str = "", context: str = "")

# 4. Bug Hunting: Invalid business input was improperly accepted (Validation Bypass)
Exceptor.expect_bug_if_accepted(snapshot: dict, context: str = "")
```

### 4.2 `core/interceptor.py`
```python
from core.interceptor import Interceptor

# Wrap Playwright execution
result = Interceptor.run(
    action_fn=lambda: page.click("#saveBtn"),
    action_name="click_save_button",
    context="Submitting Curricula Trainer creation form",
    retry=0  # Extensible for backoff
)
```

### 4.3 `pages/base_page.py`
```python
class BasePage:
    def __init__(self, page: Page): ...
    def navigate(self, url: str, wait_until: str = "domcontentloaded") -> "BasePage": ...
    def get_locator(self, selector_or_locator: Union[str, Locator]) -> Locator: ...
    def wait_for_visible(self, selector_or_locator: Union[str, Locator], timeout: int = 10000) -> Locator: ...
    def click_element(self, selector_or_locator: Union[str, Locator], timeout: int = 10000) -> None: ...
    def fill_text(self, selector_or_locator: Union[str, Locator], text: str, timeout: int = 10000) -> None: ...
    def take_screenshot(self, filepath: Union[str, Path], full_page: bool = False) -> str: ...
```

### 4.4 `pages/curricula_trainer_page.py`
Key Methods:
- `open()`: Navigates to `curricula_trainer_account.html`.
- `type_field(selector, text, delay=20)`: Real human typing cadence (`press_sequentially`).
- `fill_personal_info(data)` / `fill_contact_info(data)` / `fill_emergency_contact(data)` / `fill_singapore_address(data)` / `fill_non_singapore_address(data)`: Modular section fillers.
- `fill_full_form(data)`: End-to-end form completion.
- `save()` / `cancel()`: Form submission actions.
- `get_state_snapshot() -> Dict[str, Any]`:
  Returns:
  ```json
  {
    "success_visible": false,
    "visible_errors": {
      "primaryPhone": "Enter a valid contact number (8 digits starting with 8 or 9)",
      "postalCode": "Postal Code must be exactly 6 digits"
    }
  }
  ```

### 4.5 `tests/base_test.py` & `StepTracker`
```python
from tests.base_test import BaseTest

class TestMyFeature(BaseTest):
    def test_example_flow(self):
        # self.page, self.step, self.search_data are automatically injected
        with self.step(
            "Step 1: Open Application",
            expected="Application page loads successfully",
            actual="Application loaded with ready state"
        ):
            self.page.goto("http://localhost:8000")

        with self.step(
            "Step 2: Submit Valid Form",
            expected="Form submitted and success banner displayed",
            actual="Success banner visible"
        ):
            Interceptor.run(lambda: self.curricula.save(), action_name="save_form")
            Exceptor.expect_success(self.curricula.get_state_snapshot(), context="Verify Form")
```

---

## 5. Test Suites & Business Coverage

### 5.1 User Story 1: Bing Search -> YouTube Navigation (`tests/us01_bing_search`)
- **Step 1**: Navigate to `bing.com` (handles anti-bot headers, stealth flags).
- **Step 2**: Search for Facebook (`search_data.json`) and verify first organic result title.
- **Step 3**: Search for YouTube and verify results.
- **Step 4**: Click organic YouTube search link (intercepts Bing redirect tracking URLs to avoid `TargetClosedError`).
- **Step 5**: On YouTube, search for channel (default: `VTV24`), open Videos tab, sort by **Oldest/Earliest**, click to play earliest video, and capture high-resolution screenshot evidence.

### 5.2 User Story 2 & 4: Curricula Trainer Account Form (`tests/us04_curricula_trainer`)
68 automated test cases divided into 7 suites:
1. **`test_ts01_personal_info.py` (TC_PI_001 to 019)**:
   - Preferred name (valid string, 100-char boundary, >100 char rejection).
   - Gender radio selection (Male/Female).
   - ID Type (NRIC, FIN, Passport) and ID Number validation.
   - ID Document upload (PDF, PNG, >10MB rejection, malicious .exe rejection, MIME verification).
   - Nationality, Date of Birth (minimum 18 years old validation, future date rejection), Race, Country of Birth, Tax Resident status.
2. **`test_ts02_contact_info.py` (TC_CI_001 to 009)**:
   - Primary Email (standard format, boundary length 255, missing @, invalid domain, duplicate check).
   - Primary Country Code (+65, +1, +84...) & Phone Number (Singapore 8-digit starting with 8/9, non-SG variations).
   - Secondary Country Code & Phone Number.
3. **`test_ts03_emergency_contact.py` (TC_EC_001 to 006)**:
   - Emergency Contact Name (boundary 100 chars).
   - Relationship selection (Parent, Spouse, Sibling, Child, Friend, Other).
   - Country Code & Emergency Phone Number.
4. **`test_ts04_singapore_address.py` (TC_SG_001 to 010)**:
   - Postal Code (exactly 6 digits, auto-lookup simulation).
   - Block Number, Building Name, Street Name.
   - Floor & Unit Number (`#04-12A`), "Floor Not Applicable" checkbox toggle.
5. **`test_ts05_non_singapore_address.py` (TC_NSG_001 to 007)**:
   - Dynamic visibility toggle when selecting "Non-Singapore".
   - Country/Region dropdown (ensuring "Singapore" is excluded from non-SG dropdown).
   - Address Line 1 & Line 2, City, State/Province, International Postal Code.
6. **`test_ts06_save_action.py` (TC_SAV_001 to 007)**:
   - Full valid submission (Happy Path -> Success banner shown).
   - Mandatory field rejection across all sections.
   - Duplicate email & ID number checks.
   - Rapid double-click concurrency protection on Save button.
7. **`test_ts07_cancel_action.py` (TC_CAN_001 to 005)**:
   - Clean state cancel (navigates without prompt).
   - Dirty state cancel (prompts browser confirm dialog; cancel stays, OK discards).
   - Radio and dropdown dirty state change detection.

---

## 6. The 10 Known System Defects (Bug Matrix)

The application under test (`curricula_trainer_account.html`) contains 10 known bugs intentionally cataloged and asserted in the test suites:

| Bug ID | Module | Defect Description | Asserted in Test | Exceptor Gate Used |
|---|---|---|---|---|
| **BUG-001** | Save Action | Missing duplicate Email check; system accepts duplicate emails | `TC_SAV_003`, `TC_SAV_004` | `expect_bug_if_accepted` |
| **BUG-002** | Save Action | Missing duplicate ID Number check | `TC_SAV_005` | `expect_bug_if_accepted` |
| **BUG-003** | Non-SG Address | Non-Singapore Country dropdown incorrectly includes "Singapore" | `TC_NSG_002` | `expect_bug_if_rejected` |
| **BUG-004** | Save Action | Rapid double-clicking Save triggers duplicate account processing | `TC_SAV_006` | `expect_bug_if_accepted` |
| **BUG-005** | Emergency Contact | Relationship enum displays Father/Mother instead of standard FSD list | `TC_EC_003` | `expect_bug_if_rejected` |
| **BUG-006** | Cancel Action | Cancel button ignores dirty state on radio buttons and dropdowns | `TC_CAN_004` | `expect_bug_if_accepted` |
| **BUG-007** | Form Inputs | Maximum length validation does not enforce limits on 5 text fields | `TC_PI_003`, `TC_SG_007` | `expect_bug_if_accepted` |
| **BUG-008** | Validation | Mandatory validation messages do not match FSD standard wording | `TC_PI_019`, `TC_CI_009` | `expect_rejection` |
| **BUG-009** | Personal Info | ID Type dropdown contains undocumented option "S-Pass" | `TC_PI_006` | `expect_bug_if_rejected` |
| **BUG-010** | Personal Info | Missing NRIC/FIN Checksum validation (accepts invalid letter checksums) | `TC_PI_008` | `expect_bug_if_accepted` |

---

## 7. Execution CLI Commands

### 1. Run Complete Test Suite
```bash
# Run User Story 4 (all 68 tests) with visible browser
python run_tests.py tests/us04_curricula_trainer/

# Run User Story 1 (Bing Search -> YouTube)
python run_tests.py tests/us01_bing_search/test_bing_search.py

# Run Framework Unit Tests
python run_tests.py tests/unit/
```

### 2. High-Performance Parallel Execution (`pytest-xdist`)
```bash
# Run with 4 parallel workers (automatically falls back to headless mode for stability)
python run_tests.py tests/us04_curricula_trainer/ -n 4
```

### 3. Cross-Browser Selection
```bash
# Supported: chromium, chrome, edge, brave, firefox, webkit
python run_tests.py tests/us04_curricula_trainer/ --target-browser brave

# Explicit custom browser binary path
python run_tests.py tests/us04_curricula_trainer/ --browser-path /usr/bin/google-chrome-stable
```

### 4. Regenerate HTML Report Without Re-running Tests
```bash
python generate_report.py reports/us04_curricula_trainer/report.json reports/us04_curricula_trainer/execution_report.html
```

---

## 8. Invariants & Rules for AI Agents (The Developer Contract)

When modifying or extending this codebase, any AI agent **MUST STRICTLY ADHERE** to these fundamental invariants:

1. **Never Put `assert` in Page Objects**:
   - Page objects (`pages/*.py`) must only navigate, click, fill, query DOM elements, and return data or `get_state_snapshot()`.
   - All assertions belong in `tests/` using `Exceptor`.
2. **Never Use Raw `time.sleep()`**:
   - Use Playwright locators with built-in auto-waiting, `wait_for(state="visible")`, or `page.wait_for_timeout()` when simulating human settling pauses.
3. **Always Supervise Interactions with `Interceptor`**:
   - Any external interaction that might fail due to network/browser timeout must be wrapped with `Interceptor.run(lambda: ..., action_name="...")`.
4. **Always Wrap Functional Steps with `self.step`**:
   - Inside test methods inheriting `BaseTest`, wrap each phase in `with self.step("Step Description", expected="...", actual="..."):`.
   - The `expected` string must match the Acceptance Criteria verbatim.
5. **Never Hardcode Test Data in Test Files**:
   - Always load test profiles, search terms, and boundaries from `data/*.json`.
6. **Maintain Ticket Isolation**:
   - New User Stories must be placed in `tests/us<NN>_<name>/` with their own `requirements/` subfolder.
   - Reports must automatically isolate under `reports/us<NN>_<name>/`.
7. **Zero CDN Dependencies in Reporting**:
   - The reporting module (`reporting/`) must remain 100% self-contained. Never add `<script src="https://...">` or external stylesheets. All charts must be generated via pure Python SVG math, and all media must be Base64 embedded.
