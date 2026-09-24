# Enterprise QA Automation UI Framework

Enterprise-grade UI Automation Framework built on **Python**, **Playwright**, and **Pytest**. Features the **Page Object Model (POM)** combined with **Component-based** reusable UI architecture, **Ticket-Isolated Test Execution**, **Requirements Traceability Matrix**, an independent dual-gate error supervisory ecosystem (**Exceptor & Interceptor**), and a **100% Offline Self-Contained ExtentReports HTML Engine**.

> 📌 **Course Evaluator / Grader?**  
> - For the complete grading roadmap, deliverable checklist, and rapid evaluation guide, start with **[`docs/INSTRUCTIONS_FOR_EVALUATION.md`](docs/INSTRUCTIONS_FOR_EVALUATION.md)**.
> - For deep architectural blueprints and technical specifications, refer to **[`docs/AGENTS.md`](docs/AGENTS.md)**.

---

## 📑 Table of Contents

1. [Key Framework Highlights](#-key-framework-highlights)
2. [Architecture & Core Modules](#-architecture--core-modules)
   - [Exceptor Module — Business Assertion Gate](#1-exceptor-module--business-assertion-gate)
   - [Interceptor Module — Infrastructure Supervisor](#2-interceptor-module--infrastructure-supervisor)
   - [Error Catalog — Classification & Diagnostics](#3-error-catalog--classification--diagnostics)
   - [Requirements-First & Traceability Matrix](#4-requirements-first--traceability-matrix)
   - [ExtentReports HTML Engine (100% Offline)](#5-extentreports-html-engine-100-offline)
3. [Project Directory Structure](#-project-directory-structure)
4. [Installation & Setup](#-installation--setup)
5. [Test Execution Guide](#-test-execution-guide)
   - [Run Specific User Story / Ticket](#1-run-specific-user-story--ticket)
   - [Run Parallel Tests (pytest-xdist)](#2-run-parallel-tests-pytest-xdist)
   - [Run Internal Framework Unit Tests](#3-run-internal-framework-unit-tests)
   - [Run with Visible Browser (Headed Mode)](#4-run-with-visible-browser-headed-mode)
   - [Regenerate HTML Report Without Re-running Tests](#5-regenerate-html-report-without-re-running-tests)
6. [Standards for Developing New Test Cases](#-standards-for-developing-new-test-cases)

---

## 🌟 Key Framework Highlights

- **Decoupled Business vs. Infrastructure Errors**: Eliminates generic "Failed" outcomes. Distinctly separates **True Application Defects (Bugs)** from **Environmental / Network / Timeout Failures (Infrastructure Errors)**.
- **Elimination of Reversed Assertions**: Replaces raw `assert x == True/False` assertions with 4 intent-driven assertion methods (`expect_success`, `expect_rejection`, `expect_bug_if_rejected`, `expect_bug_if_accepted`).
- **Single Source of Truth**: All test cases originate directly from formal specification documents (`AC.md`) and a 1:1 mapped `traceability_matrix.md` before implementation.
- **100% Self-Contained Offline HTML Report (Zero External CDN)**: Full HD (1080p) WebM videos, screenshot evidence, Pure mathematical SVG charts (Donut, Bar, Pipeline, Diagram, Trend), CSS, and JS are embedded directly as Base64 Data URIs into a single HTML file. No dependencies on internet access, Chart.js, Tailwind CDN, or Google Fonts.
- **Two-Way Interactive Diagram-to-Video Sync**: Clicking on any step in the interactive execution pipeline diagram automatically scrolls to the embedded video player, seeks to the exact step timestamp, and begins playback.
- **Built-in Bilingual Support (EN / VI)**: Instant on-the-fly language toggle between English and Vietnamese.
- **High-Performance Parallel Execution**: Fully optimized for `pytest-xdist` with independent 1:1 video mapping and automatic headless fallback during multi-worker runs (`-n > 1`).

---

## 🏗 Architecture & Core Modules

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

### 1. `Exceptor` Module — Business Assertion Gate
File: `core/exceptor.py`

The **sole authority** deciding pass/fail status for business behavior. The Exceptor operates strictly on static UI state `snapshots` collected by Page Objects, without invoking Playwright interactions directly.

```python
from core import Exceptor

# 1. Happy Path: Expect action to succeed
Exceptor.expect_success(snapshot, context="Valid form submission")

# 2. Unhappy Path: Expect rejection on specified field with specific error message
Exceptor.expect_rejection(
    snapshot,
    field="primaryPhone",
    message_contains="Enter a valid contact number",
    context="Invalid phone length validation",
)

# 3. Bug Hunting: Valid business input incorrectly rejected -> Raises [BUG DETECTED]
Exceptor.expect_bug_if_rejected(
    snapshot,
    field="unitNumber",
    context="Singapore alphanumeric unit number #04-12A",
)

# 4. Bug Hunting: Invalid business input improperly accepted -> Raises [BUG DETECTED]
Exceptor.expect_bug_if_accepted(
    snapshot,
    context="Singapore phone number starting with digit 1",
)
```

When conditions are violated, the Exceptor raises `BusinessAssertionError` (inherits from `AssertionError`), ensuring Pytest detects standard test failures distinct from internal execution crashes.

---

### 2. `Interceptor` Module — Infrastructure Supervisor
File: `core/interceptor.py`

Explicitly wraps Playwright interactions (`click`, `fill`, `save`, `navigate`...) to catch technical failures, classify them via the Error Catalog, and raise `InfrastructureError` (inherits from `Exception`, NOT `AssertionError`).

```python
from core import Interceptor

# Wrap Playwright action under supervisor
result = Interceptor.run(
    lambda: curricula_page.save(),
    action_name="save_curricula_form",
    context="Click Save button to finalize account creation",
)
```

**Features:**
- Preserves root-cause traceback via `original_exception` attribute and `raise ... from exc`.
- Standardized error logging format: `[INFRA ERROR:<CATEGORY>]`.

---

### 3. Error Catalog — Classification & Diagnostics
File: `core/catalog.py`

Centralized registry classifying Playwright/Python technical exceptions into standardized categories:

| Category | Detection Criteria (Pattern / Class) | Diagnostic Hint |
|---|---|---|
| `TIMEOUT` | Class `TimeoutError` or message matches `Timeout \d+ms exceeded` | Element did not appear/become ready in time; check selector or increase timeout. |
| `BROWSER_CRASH` | Message contains `Target closed`, `browser has been closed` | Browser or target page closed unexpectedly during execution. |
| `STALE_ELEMENT` | Message contains `Element is not attached to the DOM`, `stale element` | DOM changed (re-rendered); locator reference is detached from the DOM. |
| `NETWORK` | Message contains `net::ERR_`, `NS_ERROR_CONNECTION_REFUSED` | Network connection failure occurred while requesting resource. |
| `UNKNOWN` | Unmatched exceptions | Unclassified infrastructure error — add to catalog once root cause is diagnosed. |

> **Extensibility:** Add a new `ErrorRule(...)` to `ERROR_RULES` in `core/catalog.py` to register custom error classification rules.

---

### 4. Requirements-First & Traceability Matrix
Folder: `tests/<ticket_folder>/requirements/`

Prior to implementation, each ticket/User Story defines two formal artifacts as the **Source of Truth**:
1. `<ticket>_AC.md`: Complete verbatim listing of all Acceptance Criteria (**AC-01, AC-02, ...**).
2. `<ticket>_traceability_matrix.md`: 1:1 cross-reference table mapping each AC to actual form behavior, evaluation status (`✅ Match` or `❌ Mismatch`), and the **exact Exceptor method to invoke**.

---

### 5. ExtentReports HTML Engine (100% Offline)
Folder: `reporting/`

Self-contained HTML reporting engine:
- **Zero External Dependencies**: Full HD WebM videos and screenshots are embedded as Base64 Data URIs directly into the final HTML document.
- **Pure SVG Mathematical Renderers**: In-house SVG generation algorithms for Donut Chart (Pass rate), Bar Chart (Step duration), Pipeline (Step flow), Architecture Diagram, and Multi-Run Trend Chart.
- **Ticket Isolation**: Artifacts are automatically isolated under `reports/<ticket>/` without cross-ticket collisions.

---

## 📁 Project Directory Structure

```text
automation-ui/
├── README.md                                # Central framework documentation & entrypoint
├── requirements.txt                         # Python package dependencies
├── pytest.ini                               # Pytest configuration, browser modes, reporting flags
├── conftest.py                              # Shared fixtures, ticket detection, video/screenshot hooks
├── run_tests.py                             # Two-phase test execution orchestrator
├── generate_report.py                       # CLI entrypoint for HTML report generation
├── curricula_trainer_account.html           # Local web application for User Story 2 (Trainer Account)
│
├── docs/                                    # 📁 Complete Documentation & Specifications
│   ├── INSTRUCTIONS_FOR_EVALUATION.md       # Quickstart, Deliverables checklist & grading roadmap
│   ├── AGENTS.md                            # Deep architectural source of truth & agent guidelines
│   ├── us01_bing_search/                    # 📁 User Story 01: Bing Search -> YouTube Navigation
│   │   └── README.md                        # US01 specs, step breakdown, parallel DDT guide
│   └── us04_curricula_trainer/              # 📁 User Story 04: Curricula Trainer Account Form
│       ├── README.md                        # US04 overview, 7 test suites, execution commands
│       ├── test_cases/                      # 68 Test Cases, AC specifications, Traceability Matrix
│       ├── defects_and_analysis/            # Bug Matrix, Severity Matrix, D4 Answer Key
│       └── ai_prompts/                      # AI Generation Prompts (Deliverable 0)
│
├── examples/                                # 📁 Usage Demonstrations
│   └── example_usage.py                     # Demo script showing Exceptor & Interceptor usage
│
├── core/                                    # Gatekeeper architecture: Exceptor, Interceptor, Catalog
│   ├── __init__.py                          # Package exports
│   ├── exceptions.py                        # BusinessAssertionError vs InfrastructureError
│   ├── catalog.py                           # Infrastructure Error Catalog and classify()
│   ├── exceptor.py                          # Business Assertion Gate (expect_success, expect_rejection, etc.)
│   └── interceptor.py                       # Infrastructure supervisor (wraps Playwright calls)
│
├── components/                              # Reusable UI widgets across pages
│   ├── __init__.py
│   └── search_box.py                        # Search bar component with human typing cadence
│
├── pages/                                   # Page Objects (Locators and browser interactions)
│   ├── __init__.py
│   ├── base_page.py                         # BasePage: click, fill, wait, screenshot, highlight
│   ├── bing_home_page.py                    # Bing landing page actions
│   ├── bing_results_page.py                 # Bing search results page
│   ├── youtube_page.py                      # Target YouTube page and channel actions
│   └── curricula_trainer_page.py            # Curricula Trainer Account form Page Object
│
├── data/                                    # Input test fixtures (JSON)
│   ├── search_data.json                     # Search keywords for User Story 1
│   ├── curricula_trainer_data.json          # Profiles for User Story 2 (Singapore, Non-SG, Boundaries)
│   └── fixtures/                            # Upload test files (PDF, PNG, invalid files)
│
├── tests/                                   # Test suites organized by User Story / Ticket
│   ├── __init__.py
│   ├── base_test.py                         # BaseTest: setup autouse, report helpers, step tracking
│   ├── unit/                                # Internal framework unit tests (Exceptor, Interceptor, Catalog)
│   │   ├── test_exceptor.py
│   │   ├── test_interceptor.py
│   │   └── test_catalog.py
│   ├── us01_bing_search/                    # User Story 1: Bing Search -> YouTube channel actions
│   │   └── test_bing_search.py
│   └── us04_curricula_trainer/              # User Story 2: Curricula Trainer Account form (7 Suites)
│       ├── requirements/                    # Source of Truth specifications
│       │   ├── us04_curricula_trainer_AC.md
│       │   └── us04_curricula_trainer_traceability_matrix.md
│       ├── test_ts01_personal_info.py
│       ├── test_ts02_contact_info.py
│       ├── test_ts03_emergency_contact.py
│       ├── test_ts04_singapore_address.py
│       ├── test_ts05_non_singapore_address.py
│       ├── test_ts06_save_action.py
│       └── test_ts07_cancel_action.py
│
├── reporting/                               # Offline ExtentReports HTML Engine
│   ├── __init__.py
│   ├── core/                                # Data parsing, Base64 encoding, document assembly
│   ├── charts/                              # Pure SVG Renderers: donut, bar, pipeline, diagram, trend
│   └── assets/                              # Inlined CSS and JS (video sync, bilingual EN/VI)
│
└── reports/                                 # Generated test artifacts (Isolated per ticket)
    ├── .gitkeep
    ├── us01_bing_search/                    # US01 reports, videos, screenshots
    ├── us04_curricula_trainer/              # US04 reports, videos, screenshots
    └── unit/                                # Unit test execution artifacts
```

---

## 🚀 Installation & Setup

1. **Create and activate a Python virtual environment (Python 3.10+)**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate       # On Linux / macOS
   # or: .venv\Scripts\activate   # On Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright Browser Binaries**:
   ```bash
   playwright install chromium
   ```
   *(On clean Linux environments, run `playwright install-deps` if system graphics libraries are needed).*

---

## 🎯 Test Execution Guide

The `run_tests.py` orchestrator coordinates the complete two-phase lifecycle:
- **Phase 1**: Executes Pytest with live terminal streaming and generates ticket-isolated `report.json`.
- **Phase 2**: Automatically triggers `generate_report.py` to assemble the self-contained HTML report with Base64 embedded media.
- **Phase 3**: Renders an ANSI summary dashboard with test statistics and exit codes.

### 1. Run Specific User Story / Ticket
```bash
# Run User Story 2 (Curricula Trainer Account Form - All 7 Suites)
python run_tests.py tests/us04_curricula_trainer/

# Run specific suite (e.g. Personal Information)
python run_tests.py tests/us04_curricula_trainer/test_ts01_personal_info.py

# Run User Story 1 (Bing Search -> YouTube)
python run_tests.py tests/us01_bing_search/test_bing_search.py
```

### 2. Run Parallel Tests (pytest-xdist)
```bash
# Run tests with 4 parallel worker processes
python run_tests.py tests/us04_curricula_trainer/ -n 4

# Run with maximum available CPU cores
python run_tests.py -n auto
```

### 3. Run Internal Framework Unit Tests
Verify the integrity of `Exceptor`, `Interceptor`, and `Catalog`:
```bash
python run_tests.py tests/unit/
```

### 4. Run with Visible Browser (Headed Mode)
```bash
python run_tests.py tests/us04_curricula_trainer/test_ts01_personal_info.py -k "test_tc_pi_001" --headed
```

### 5. Regenerate HTML Report Without Re-running Tests
```bash
# Generate report from an existing JSON report file
python generate_report.py reports/us04_curricula_trainer/report.json
```

---

## 📊 Viewing HTML Reports & Verifying Run IDs

> [!IMPORTANT]
> **Avoid Viewing the Wrong Report or Run ID!**  
> Test executions generate unique session IDs (e.g., `RUN-YYYYMMDD-XXXXXX`). Running an isolated test case updates `reports/<ticket>/execution_report.html` to reflect only that single test.  
> - **User Story 2 Active Report**: [`reports/us04_curricula_trainer/execution_report.html`](./reports/us04_curricula_trainer/execution_report.html)
> - **User Story 2 Certified 68-Test Snapshot**: [`reports/us04_curricula_trainer/history/RUN-20260923-61EC0C.html`](./reports/us04_curricula_trainer/history/RUN-20260923-61EC0C.html)
> - **User Story 1 Active Report**: [`reports/us01_bing_search/execution_report.html`](./reports/us01_bing_search/execution_report.html)
> - **Framework Unit Tests Active Report**: [`reports/unit/execution_report.html`](./reports/unit/execution_report.html)
>
> When reviewing, verify the **Run ID badge** (`ID: RUN-20260923-61EC0C`) in the top navbar and ensure the **TESTS KPI card displays 68**. For the complete evaluation roadmap and ID verification checklist, see **[`docs/INSTRUCTIONS_FOR_EVALUATION.md`](./docs/INSTRUCTIONS_FOR_EVALUATION.md)**.

---

## 📝 Standards for Developing New Test Cases

When adding a new User Story (e.g. `us05_payment_gateway`), follow these 4 architectural steps:

### Step 1: Define Requirements Artifacts
Create `tests/us04_payment_gateway/requirements/`:
- `us04_payment_gateway_AC.md`: List verbatim Acceptance Criteria.
- `us04_payment_gateway_traceability_matrix.md`: Map each AC to expected DOM behavior and assign corresponding Exceptor method.

### Step 2: Implement Page Object (inherits `BasePage`)
Create `pages/payment_page.py`:
- Inherits from `BasePage`.
- Encapsulates locators and action methods (`open()`, `fill_payment()`, `submit()`).
- Exposes `get_state_snapshot()` returning:
  ```python
  {
      "success_visible": bool,
      "visible_errors": {"field_name": "error_message_text"}
  }
  ```
- **Never include raw test assertions (`assert`) inside Page Objects.**

### Step 3: Implement Test Suite (inherits `BaseTest`)
Create `tests/us04_payment_gateway/test_payment.py`:
- Wrap all Playwright interactions with `Interceptor.run()`:
  ```python
  Interceptor.run(
      lambda: self.payment_page.submit(),
      action_name="submit_payment",
      context="Submitting payment form",
  )
  ```
- Retrieve state: `snapshot = self.payment_page.get_state_snapshot()`.
- Evaluate condition via `Exceptor`:
  ```python
  # Happy Path:
  Exceptor.expect_success(snapshot, context="Valid credit card payment")

  # Unhappy Path:
  Exceptor.expect_rejection(snapshot, field="cardNumber", message_contains="Invalid card number")
  ```

### Step 4: Execute & Review Report
```bash
python run_tests.py tests/us04_payment_gateway/
```
The self-contained HTML report and WebM video recordings will be available at:
`reports/us04_payment_gateway/execution_report.html`.
