# Enterprise QA Automation UI Framework

Enterprise-grade UI Test Automation Framework engineered on **Python 3.10+**, **Playwright (Sync API)**, and **Pytest**. Designed around the **Page Object Model (POM)** with **Component Composition**, **Multi-Project Isolation**, an automated **Dual-Gate Error Supervision Engine**, an **AST Architectural Invariant Guard**, and a **100% Offline Standalone ExtentReports HTML Engine**.

> 📌 **Key Architectural References:**
> - **AI Test Generation Guidelines:** [`docs/AI_CODING_GUIDELINES.md`](docs/AI_CODING_GUIDELINES.md)
> - **19-Column QA Test Case Ingestion Standard:** [`docs/adr/0005-testcase-matrix-ingestion-and-ai-generation-spec.md`](docs/adr/0005-testcase-matrix-ingestion-and-ai-generation-spec.md)
> - **Multi-Project & Multi-Website Architecture:** [`docs/adr/0006-multi-website-project-automation-architecture.md`](docs/adr/0006-multi-website-project-automation-architecture.md)
> - **Core Developer Invariants & Directives:** [`AGENTS.md`](AGENTS.md)

---

## 📑 Table of Contents

1. [Key Framework Capabilities](#-key-framework-capabilities)
2. [Architectural Overview & Core Seams](#-architectural-overview--core-seams)
   - [Dual-Gate Error Supervision Engine](#1-dual-gate-error-supervision-engine)
   - [100% Offline ExtentReports HTML Engine](#2-100-offline-extentreports-html-engine)
   - [Multi-Browser & Anti-Bot Stealth Engine](#3-multi-browser--anti-bot-stealth-engine)
   - [Multi-Project & Multi-Website Isolation](#4-multi-project--multi-website-isolation)
   - [AST Architecture Invariant Guard](#5-ast-architecture-invariant-guard)
3. [Standard 19-Column QA Matrix to Pytest Mapping](#-standard-19-column-qa-matrix-to-pytest-mapping)
4. [Project Directory Structure](#-project-directory-structure)
5. [Installation & Setup](#-installation--setup)
6. [Test Execution Guide](#-test-execution-guide)
   - [Run Specific Ticket / User Story](#1-run-specific-ticket--user-story)
   - [Run Parallel Tests (pytest-xdist)](#2-run-parallel-tests-pytest-xdist)
   - [Cross-Browser Selection & Custom Executables](#3-cross-browser-selection--custom-executables)
   - [Run Internal Framework Unit Tests](#4-run-internal-framework-unit-tests)
   - [Regenerate HTML Report Without Rerunning Tests](#5-regenerate-html-report-without-rerunning-tests)
7. [AI Coding Assistants Quickstart](#-ai-coding-assistants-quickstart)

---

## 🌟 Key Framework Capabilities

- **Decoupled Business vs. Infrastructure Errors (Dual-Gate)**: Centrally classifies technical exceptions (Timeout, Browser crash, Stale DOM, Network drop, Unhandled dialog, Missing file) in `core/catalog.py` vs genuine business assertion failures (`core/exceptor.py`).
- **100% Offline Standalone HTML Report (Zero External CDN)**: Full HD (1080p) WebM videos, screenshot evidence, Pure SVG charts (Donut, Bar Timeline, Pipeline, Diagram, Trend), CSS, and JS are embedded directly as Base64 Data URIs into a single self-contained HTML file. No dependencies on Chart.js, Tailwind CDN, or Google Fonts.
- **Two-Way Diagram-to-Video Synchronization**: Clicking any step in the interactive SVG execution pipeline diagram automatically scrolls to the embedded video player, seeks to the exact step timestamp, and begins playback.
- **Native Browser Dialog Protection**: Automatic one-time listener (`handle_next_dialog()`) handles `alert()`, `confirm()`, and `prompt()` without locking the browser or triggering accidental dismissals.
- **Multi-Browser & Anti-Bot Stealth**: Zero hardcoded browser binaries. Supports Chromium, Google Chrome, Microsoft Edge, Brave Browser, Firefox, and WebKit via `--target-browser` with automatic Brave auto-detection and Playwright Stealth integration.
- **AST Architecture Invariant Guard**: Automated AST static analysis tests (`tests/unit/test_architecture_invariants.py`) strictly enforce zero `assert` in Page Objects, zero `time.sleep()`, zero external CDN in reports, and zero leftover debug prints.
- **Multi-Project / Multi-Website Reusability**: Easily scale to automate multiple websites simultaneously by compartmentalizing suites into `tests/<project>/`, `pages/<project>/`, `data/<project>/`, and `reports/<project>/`.

---

## 🏗 Architectural Overview & Core Seams

```text
       ┌────────────────────────────────────────────────────────┐
       │             User Story Requirements / FSD              │
       └───────────────────────────┬────────────────────────────┘
                                   │  1. Map Test Intent (19-Column Matrix)
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │          Traceability & AI Coding Guidelines           │
       │     [Exceptor / Pytest Strict XFAIL / Data Fixture]    │
       └───────────────────────────┬────────────────────────────┘
                                   │  2. Direct Method Execution
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           TEST CASE EXECUTION                           │
│                                                                         │
│   ┌───────────────────────────┐         ┌───────────────────────────┐   │
│   │    Playwright Actions     │         │     Page Object State     │   │
│   │ (click, fill, dialog, ...)│         │ (Snapshot: errors, success│   │
│   └─────────────┬─────────────┘         └─────────────┬─────────────┘   │
│                 │                                     │                 │
│                 ▼                                     ▼                 │
│   ┌───────────────────────────┐         ┌───────────────────────────┐   │
│   │   Hook Error Classifier   │         │         Exceptor          │   │
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

### 1. Dual-Gate Error Supervision Engine
- **`Exceptor` ([`core/exceptor.py`](core/exceptor.py))**: Sole business assertion authority. Operates on static UI snapshots (`{"success_visible": bool, "visible_errors": Dict[str, str]}`). Never calls Playwright directly.
  - `expect_success(snapshot, context, step)`
  - `expect_rejection(snapshot, field, message_contains, context, step)`
  - `expect_bug_if_accepted(snapshot, context)` (Validation bypass defect)
  - `expect_bug_if_rejected(snapshot, field, context)` (Valid input rejected defect)
- **`Catalog` ([`core/catalog.py`](core/catalog.py))**: Classifies runtime exceptions into 8 standardized technical categories:
  - `TIMEOUT`: Selector timeout or element not ready.
  - `BROWSER_CRASH`: Target closed or process terminated.
  - `STALE_ELEMENT`: DOM re-rendered; reference detached.
  - `NETWORK`: Connection refused or DNS lookup failure.
  - `JS_RUNTIME_ERROR`: Uncaught JavaScript exception or console error.
  - `DIALOG_UNHANDLED`: Unhandled native alert/confirm dialog.
  - `FILE_NOT_FOUND`: Fixture file or upload path missing.
  - `NAVIGATION_ERROR`: Navigation rejected or URL unreachable.

### 2. 100% Offline ExtentReports HTML Engine
- **Pure SVG Math Charts ([`reporting/charts/`](reporting/charts/))**:
  - `donut.py`: SVG Donut chart displaying Pass/Fail/Skipped rates.
  - `bar.py`: SVG Step Duration Timeline bar chart.
  - `pipeline.py`: Interactive Step Pipeline with 2-way video seek sync.
  - `diagram.py`: Architecture topology diagrams.
  - `trend.py`: Historical multi-run pass rate and duration trend lines.
- **Base64 Media Embedding**: Embedded Full HD (1080p) WebM videos and PNG screenshot evidence.
- **Bilingual Interface**: Client-side instant toggle between English (`EN`) and Vietnamese (`VI`).

### 3. Multi-Browser & Anti-Bot Stealth Engine
Configured via `core/pytest_plugins/browser_engine.py`:
- Supported engines: `chromium`, `chrome`, `edge`, `brave`, `firefox`, `webkit`.
- Linux, macOS, and Windows Brave binary auto-detection.
- Playwright Stealth evasion patches for Chromium-family browsers.
- Automatically enforces `headless=True` during parallel multi-worker execution unless `--headed` is explicitly requested.

### 4. Multi-Project & Multi-Website Isolation
- Each website or user story has an isolated directory structure:
  - Tests: `tests/<project>/`
  - Page Objects: `pages/<project>/`
  - Test Data: `data/<project>/`
  - Reports: `reports/<project>/`
- Generates a unique session `run_id` (e.g. `RUN-20261014-DBAB91`).
- Preserves historical runs in `reports/<project>/history/<run_id>.html` without wiping previous artifacts.

### 5. AST Architecture Invariant Guard
File: [`tests/unit/test_architecture_invariants.py`](tests/unit/test_architecture_invariants.py)
- **Invariant 1**: Zero assertions in Page Objects and Components.
- **Invariant 2**: Zero raw `time.sleep()` in all execution paths.
- **Invariant 7**: Zero external CDN URLs in offline reporting assets.
- **Hygiene**: Zero leftover debug `print()` statements in page objects & components.

---

## 📊 Standard 19-Column QA Matrix to Pytest Mapping

Based on **[ADR-0005](docs/adr/0005-testcase-matrix-ingestion-and-ai-generation-spec.md)**, any test case from Google Sheets or Excel maps 1:1 into Python code:

| # | Column Name | Code Mapping & Usage |
|---|---|---|
| 1 | **ID** (`TC-001`) | Prefix in test function: `def test_tc_001_<slug>(self):` & `json_metadata["tc_id"] = "TC-001"`. |
| 2 | **Scenario ID** (`TS-001`) | Test suite file name: `tests/<traceability>/test_ts01_<suite_slug>.py`. |
| 3 | **Title** | Suffix of test function and header in docstring. |
| 4 | **Test Suite** | Logical module/feature grouping. Each suite maps to 1 independent test file. |
| 5 | **Page** | Target Page Object in `pages/`. Create/update `pages/<page>.py` before writing test. |
| 6 | **Severity** (`P0`, `P1`, ...) | Pytest Marker: `@pytest.mark.p0`, `@pytest.mark.p1`. |
| 7 | **Priority** (`High`, `Medium`) | Pytest Marker: `@pytest.mark.priority_high`, docstring & `json_metadata["priority"]`. |
| 8 | **Execution Status** (`Passed`, `Failed`) | Determines if `@pytest.mark.xfail` is required. |
| 9 | **Test Type** (`Functional`, `UI`, `Regression`) | Pytest Marker: `@pytest.mark.functional`, `@pytest.mark.regression`, `@pytest.mark.ui`. |
| 10 | **Environment** | Documented in docstring & `json_metadata["target_env"]`. |
| 11 | **Preconditions** | Executed in initial step `with self.step("Step 0: Setup"):` or docstring. |
| 12 | **Test Data** | Extracted into `data/<traceability>_data.json`; load via fixture with `copy.deepcopy()`. |
| 13 | **Test Steps** | 1:1 mapped to `with self.step("Step X: <action>"):` with `self.step.set_actual(...)`. |
| 14 | **Expected Result** | Final verification logic using `Exceptor` or standard assertions. |
| 15 | **Actual Result** | Stored in reason string of `@pytest.mark.xfail` when Defect ID is present. |
| 16 | **Assumption Ref** | Documented in docstring and `json_metadata["assumptions"]`. |
| 17 | **Defect ID** (`BUG-012`) | Decorator `@pytest.mark.xfail(strict=True, reason="<Defect_ID>: <Actual_Result>")`. |
| 18 | **Traceability** (`US-05`, `BR-03`) | Subdirectory path `tests/<traceability>/` and `json_metadata["story"]`. |
| 19 | **Note** | Documented in docstring comments. |

---

## 📂 Project Directory Structure

```text
automation-ui/
├── core/                                    # 🛡️ Dual-Gate Error Supervision Layer
│   ├── catalog.py                           # Error Catalog (8 technical classification rules)
│   ├── exceptions.py                        # BusinessAssertionError vs InfrastructureError
│   ├── exceptor.py                          # Sole business assertion gate
│   ├── interceptor.py                       # Playwright interaction supervisor
│   └── pytest_plugins/                      # Modular Pytest Plugin Subsystem
│       ├── browser_engine.py                # Multi-browser & stealth setup
│       ├── ticket_isolation.py              # Run ID & artifact isolation
│       └── step_and_video_hook.py           # StepTracker & error classification hook
│
├── pages/                                   # 📄 Page Object Model Layer (NO ASSERTIONS)
│   ├── base_page.py                         # Shared web actions: navigate, dialog, download, fixture path
│   ├── curricula_trainer_page.py            # Curricula form locators & get_state_snapshot
│   ├── bing_home_page.py                    # Bing search landing page
│   ├── bing_results_page.py                 # Bing search results page
│   └── youtube_page.py                      # Target website interaction object
│
├── components/                              # 🧩 Modular Reusable UI Components
│   └── search_box.py                        # Search bar with human typing cadence emulation
│
├── data/                                    # 🗄️ Test Data Fixtures (Zero Hardcoding)
│   ├── search_data.json                     # Search keywords and parallel scenarios
│   ├── curricula_trainer_data.json          # Pre-built trainer profiles (valid SG resident, edge cases)
│   └── fixtures/                            # Upload files for document testing (valid, oversized, invalid)
│
├── tests/                                   # 🧪 Test Suites & Verification Logic
│   ├── base_test.py                         # Base test class: lazy page getters, json loaders, fixture files
│   ├── unit/                                # Internal Framework Unit Tests (36 tests)
│   │   ├── test_architecture_invariants.py  # AST verification of Invariants 1, 2, 7 & code hygiene
│   │   ├── test_catalog.py                  # Validates error regex and exception matching
│   │   ├── test_exceptor.py                 # Validates Exceptor 4 gatekeeper methods
│   │   └── test_interceptor.py              # Validates Interceptor exception translation
│   ├── us01_bing_search/                    # User Story 1: E2E Bing to YouTube Navigation
│   └── us04_curricula_trainer/              # User Story 4: Curricula Trainer Account (68 Tests, 7 Suites)
│
├── reporting/                               # 📊 100% Offline ExtentReports HTML Engine
│   ├── core/                                # Generator, parser, document assembler, dashboard & test views
│   ├── charts/                              # Pure mathematical SVG charts (donut, bar, pipeline, diagram, trend)
│   └── assets/                              # Inlined report.css and report.js (video sync, bilingual toggle)
│
├── docs/                                    # 📚 Technical Documentation & Specs
│   ├── AI_CODING_GUIDELINES.md              # Canonical templates & anti-patterns for AI assistants
│   ├── adr/                                 # Architecture Decision Records (ADR-0004 to ADR-0006)
│   └── INSTRUCTIONS_FOR_EVALUATION.md       # Evaluation guide & grading roadmap
│
├── curricula_trainer_account.html           # Local web application under test (US04)
├── conftest.py                              # Master Pytest entrypoint (delegates to core plugins)
├── pytest.ini                               # Pytest configuration, markers, and default CLI flags
├── requirements.txt                         # Python dependencies
└── run_tests.py                             # 3-Phase orchestrator (Pytest -> HTML Report -> Terminal Summary)
```

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Virtual Environment & Dependencies
```bash
# Clone the repository
git clone https://github.com/kiet-w/qa-automation-ui.git
cd qa-automation-ui

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install chromium firefox webkit
```

---

## 🏃 Test Execution Guide

### 1. Run Specific Ticket / User Story
The orchestrator automatically runs Pytest, extracts the JSON report, generates the offline ExtentReports HTML file, and prints an ANSI terminal summary:

```bash
# Run Curricula Trainer Account test suite
python3 run_tests.py --ticket us04_curricula_trainer

# Run Bing Search E2E test suite
python3 run_tests.py --ticket us01_bing_search

# Run directly via Pytest
pytest tests/us04_curricula_trainer/test_ts06_save_action.py -v
```

### 2. Run Parallel Tests (`pytest-xdist`)
Parallel multi-core execution automatically switches to headless mode and isolates artifacts:

```bash
# Run with 4 parallel worker processes
python3 run_tests.py --ticket us04_curricula_trainer -n 4

# Run with auto CPU detection
pytest tests/us04_curricula_trainer/ -n auto
```

### 3. Cross-Browser Selection & Custom Executables
```bash
# Run on Chromium (default)
python3 run_tests.py --ticket us04_curricula_trainer --target-browser=chromium

# Run on Microsoft Edge / Google Chrome
python3 run_tests.py --ticket us04_curricula_trainer --target-browser=edge
python3 run_tests.py --ticket us04_curricula_trainer --target-browser=chrome

# Run on Brave Browser (auto-detected across Linux/macOS/Windows)
python3 run_tests.py --ticket us04_curricula_trainer --target-browser=brave

# Run with a custom binary path
python3 run_tests.py --target-browser=brave --browser-path=/usr/bin/brave-browser
```

### 4. Run Internal Framework Unit Tests
Verify framework reliability, AST invariant guards, and dual-gate error classification:

```bash
python3 run_tests.py --ticket unit
# or directly:
pytest tests/unit/ -v
```

### 5. Regenerate HTML Report Without Rerunning Tests
```bash
# Regenerate latest report from existing JSON
python3 generate_report.py --json reports/us04_curricula_trainer/report.json

# Regenerate with Base64 embedded media
python3 generate_report.py --json reports/us04_curricula_trainer/report.json --embed-media
```

---

## 🤖 AI Coding Assistants Quickstart

When tasking an AI coding assistant (Cursor, Claude, Copilot, Antigravity) to generate automated tests for new user stories:

1. **Provide Reference Files:** Attach [`docs/AI_CODING_GUIDELINES.md`](docs/AI_CODING_GUIDELINES.md) and [`AGENTS.md`](AGENTS.md) in the prompt context.
2. **Input Test Cases:** Paste rows from the standard 19-column QA matrix.
3. **Inherit from `BaseTest`:** Subclasses automatically gain access to `self.page`, `self.step`, `self.curricula`, `self.get_page(PageCls)`, `self.get_fixture_file()`, and `self.load_json_data()`.
4. **Zero Violations:** AI is strictly forbidden from writing `time.sleep()`, adding assertions inside Page Objects, inventing locators outside `pages/`, or hardcoding test data.
