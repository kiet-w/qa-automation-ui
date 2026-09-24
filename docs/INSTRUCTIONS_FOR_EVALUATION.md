# Course Assignment Evaluation & Execution Guide

This document outlines the deliverables, grading roadmap, and verification steps for evaluating this Enterprise UI Automation project.

> [!TIP]
> **Looking for Deep Architectural Specifications?**  
> For complete technical blueprints, design patterns, Page Object Model standards, the Dual-Gate (Exceptor & Interceptor) architecture, and error catalog taxonomy, please refer to **[`AGENTS.md`](./AGENTS.md)**.

---

## 🗺 Documentation Map: Where to Look

| Document | Purpose & Contents | Recommended Reader |
| :--- | :--- | :--- |
| **`INSTRUCTIONS_FOR_EVALUATION.md`** *(This file)* | **Evaluation Roadmap & Quickstart**: Deliverable mapping (0, 1, 2, 3), instant HTML report review, and 3-step test execution commands. | Course Evaluators & Graders |
| **[`AGENTS.md`](./AGENTS.md)** | **Deep Architectural Source of Truth**: Comprehensive technical guidelines, Gatekeeper architecture (Exceptor vs Interceptor), Page Object design, Acceptance Criteria mapping, and zero-hardcoding rules. | Technical Architects & Code Reviewers |
| **[`us01_bing_search/README.md`](./us01_bing_search/README.md)** | **User Story 01 Documentation**: Bing Search -> YouTube Navigation specifications, step breakdown, and parallel execution guide. | Evaluators & Testers |
| **[`us04_curricula_trainer/README.md`](./us04_curricula_trainer/README.md)** | **User Story 04 Documentation**: Trainer Account Form overview, 68 Test Cases, 10 Bugs Analysis, and AI Prompts. | Evaluators & Testers |
| **[`../README.md`](../README.md)** | **Framework Overview**: General open-source style overview, module architecture diagram, parallel worker configurations, and component descriptions. | Developers & Testers |
| **[`us04_curricula_trainer/ai_prompts/PROMPT_MAIN_ai_test_generation_en.md`](./us04_curricula_trainer/ai_prompts/PROMPT_MAIN_ai_test_generation_en.md)** | **Deliverable 0**: Complete English prompt used with the AI coding assistant to architect and generate the project. | Assignment Grading |

---

## 📋 Deliverables Summary

This submission satisfies all requirements of the course assignment for **User Story 2: Curricula Trainer Account Form** (`curricula_trainer_account.html`), alongside an implementation of **User Story 1: Bing Search -> YouTube Navigation** (`tests/us01_bing_search/`).

| Deliverable # | Required Item | Location in Project | Description |
| :---: | :--- | :--- | :--- |
| **0** | **AI Generation Prompt** | [`docs/us04_curricula_trainer/ai_prompts/PROMPT_MAIN_ai_test_generation_en.md`](./us04_curricula_trainer/ai_prompts/PROMPT_MAIN_ai_test_generation_en.md) | Complete prompt used with the AI coding assistant to generate the POM architecture and test suites. |
| **1** | **Completed Project Files** | Project Root (`automation-ui/`) | Full source code with Page Object Model, Exceptor/Interceptor architecture, and offline HTML reporting engine. |
| **2** | **Execution Screenshots** | [`reports/us04_curricula_trainer/screenshots/`](../reports/us04_curricula_trainer/screenshots/) | Evidence screenshots showing test execution, form population, and passed verification states. |
| **3** | **Generated Execution Report** | [`reports/us04_curricula_trainer/execution_report.html`](../reports/us04_curricula_trainer/execution_report.html) | 100% offline, self-contained HTML report with embedded HD videos, SVG charts, and step logs. |

---

## ⚡ Option A: Rapid Evaluation (Without Running Code)

If you prefer to inspect the deliverables directly without configuring Python or Playwright:

1. **View the Interactive HTML Execution Report**:
   - Double-click to open **[`reports/us04_curricula_trainer/execution_report.html`](../reports/us04_curricula_trainer/execution_report.html)** in any web browser (Google Chrome, Microsoft Edge, Mozilla Firefox, Safari).
   - **Key Highlights inside the Report**:
     - **Executive KPI Dashboard Cards**: Pass rate percentage, total tests, total steps, duration.
     - **Pure Mathematical SVG Charts**: Donut chart (Pass/Fail) and step duration timeline bar chart.
     - **Interactive Step Pipeline**: Click any step in the pipeline diagram to automatically scroll to the embedded video and jump to that exact timestamp.
     - **Zero External Dependencies**: WebM Full HD (1080p) video recordings and screenshot evidence are embedded as Base64 Data URIs directly in the single HTML file. No internet or web server is required.
     - **Instant Bilingual Switcher**: Click the language toggle button in the top navigation bar to switch between English and Vietnamese.

2. **Inspect Screenshot Evidence**:
   - Browse high-resolution screenshot evidence captured during test execution in **[`reports/us04_curricula_trainer/screenshots/`](../reports/us04_curricula_trainer/screenshots/)**.

3. **Inspect the AI Generation Prompt**:
   - Review **[`docs/us04_curricula_trainer/ai_prompts/PROMPT_MAIN_ai_test_generation_en.md`](./us04_curricula_trainer/ai_prompts/PROMPT_MAIN_ai_test_generation_en.md)**.

---

## 🔍 How to View HTML Reports & Verify Run IDs (CRITICAL FOR EVALUATION)

> [!CAUTION]
> **ESSENTIAL FOR COURSE EVALUATORS: AVOID ACCIDENTALLY VIEWING THE WRONG REPORT OR RUN ID!**  
> In automated UI test frameworks, executing an isolated single test (e.g., `test_tc_pi_001` for smoke testing) immediately updates the active report `reports/us04_curricula_trainer/execution_report.html` to display **only that 1 test**.  
> If an evaluator runs a quick single test and then opens `execution_report.html`, they might mistakenly conclude that the remaining 67 test cases were lost or unexecuted!  
> **To ensure accurate grading, always verify the Run ID and Total Tests KPI in the report header as outlined below.**

### 1. Report File Structure & Scope Partitioning

Test reports are strictly separated by Ticket / User Story to eliminate cross-suite interference:

| Deliverable Scope | Active Report (Latest Run) | Certified Baseline Snapshot | Expected Tests |
| :--- | :--- | :--- | :---: |
| **User Story 2: Curricula Trainer** *(Primary Assignment Deliverable)* | [`reports/us04_curricula_trainer/execution_report.html`](../reports/us04_curricula_trainer/execution_report.html) | [`reports/us04_curricula_trainer/history/RUN-20260923-61EC0C.html`](../reports/us04_curricula_trainer/history/RUN-20260923-61EC0C.html) | **68 Tests** |
| **User Story 1: Bing Search -> YouTube** | [`reports/us01_bing_search/execution_report.html`](../reports/us01_bing_search/execution_report.html) | [`reports/us01_bing_search/history/RUN-20260923-F8329E.html`](../reports/us01_bing_search/history/RUN-20260923-F8329E.html) | **2 Tests** |
| **Framework Unit Tests** *(Exceptor / Interceptor / Catalog)* | [`reports/unit/execution_report.html`](../reports/unit/execution_report.html) | [`reports/unit/history/RUN-20260923-6FE013.html`](../reports/unit/history/RUN-20260923-6FE013.html) | **26 Tests** |
| **Workspace Root Report** *(Convenience mirror of the most recent execution)* | [`reports/execution_report.html`](../reports/execution_report.html) | *(Preserved under individual ticket history directories)* | *Dynamic* |

> [!TIP]
> **Immutable Historical Snapshots**:  
> Every execution automatically saves a permanent, immutable copy at `reports/<ticket>/history/RUN-YYYYMMDD-XXXXXX.html`.  
> Even if you run a partial command that overwrites `execution_report.html`, the complete 68-test report remains preserved in **[`reports/us04_curricula_trainer/history/RUN-20260923-61EC0C.html`](../reports/us04_curricula_trainer/history/RUN-20260923-61EC0C.html)**.

---

### 2. 4-Point UI Verification Checklist (Ensure You Are Reviewing the Intended Run)

When you open any execution report in your browser, check these four visual indicators:

```
+---------------------------------------------------------------------------------------------------------------+
| ExtentReports UI Automation Test Report              [ID: RUN-20260923-61EC0C]     [2026-09-23 15:54] [PASSED]| <-- [1] Check RUN ID
+---------------------------------------------------------------------------------------------------------------+
| [ TESTS: 68 ]                 [ STEPS: 136 ]                 [ START TIME ]                 [ DURATION ]      | <-- [2] Check KPI TESTS = 68
| 60 passed, 8 skipped                                                                                          |
+---------------------------------------------------------------------------------------------------------------+
| Filter: [ Search by TC ID (e.g. TC_PI_001, TC_ACC_005) ]                                                     | <-- [3] Search by Test Case ID
+---------------------------------------------------------------------------------------------------------------+
| > [PASS] test_tc_pi_001_first_name_valid_alphabetic [TC_PI_001] [Personal Information]                       | <-- [4] Verify Ticket & Suite
+---------------------------------------------------------------------------------------------------------------+
```

1. **Verify the Run ID Pill in the Top Header (`pill-run-id`)**:
   - Located on the top-right of the navigation bar with a badge formatted as `ID: RUN-YYYYMMDD-XXXXXX`.
   - The certified complete baseline for User Story 2 is **`RUN-20260923-61EC0C`**.
   - If the ID does not match, you are inspecting a different test session.
2. **Verify Total Test Count in the KPI Dashboard (`kpi-card`)**:
   - The top-left KPI card displays **TESTS**.
   - For User Story 2, this card **MUST display 68**.
   - If it displays `1` or `12`, an isolated test was run. Open **[`reports/us04_curricula_trainer/history/RUN-20260923-61EC0C.html`](../reports/us04_curricula_trainer/history/RUN-20260923-61EC0C.html)** to inspect all 68 tests.
3. **Verify Ticket Subfolder in File Path**:
   - Ensure the browser address bar points to `/reports/us04_curricula_trainer/` for User Story 2.
   - Do not inspect `reports/us01_bing_search/` or `reports/unit/` when assessing the Curricula Trainer form.
4. **Locate & Filter Tests by Test Case ID (Traceability)**:
   - Every test card displays its official **Test Case ID** corresponding to the Traceability Matrix:
     - **`TC_PI_001` - `TC_PI_010`**: Personal Information (First Name, Last Name, Gender, DOB, Nationality)
     - **`TC_ACC_001` - `TC_ACC_012`**: Account Setup (Username, Email, Password strength, Confirm Password)
     - **`TC_ROL_001` - `TC_ROL_008`**: Trainer Role & Domains (Domain pill selection, Bio, LinkedIn, Website)
     - **`TC_SUB_001` - `TC_SUB_013`**: Form Submission & Gatekeeper (Mandatory field blocking, terms checkbox)
     - **`TC_SAV_001` - `TC_SAV_008`**: Draft Saving (Auto-save debounce, localStorage persistence, restore prompts)
     - **`TC_DEF_001` - `TC_DEF_007`**: Default State Validation (Initial field states, pristine radio buttons)
     - **`TC_E2E_001` - `TC_E2E_010`**: End-to-End Registration (Full valid flows, end-to-end edge cases)
   - Evaluators can type any ID into the report search bar or press `Ctrl+F` to instantly jump to that test's step-by-step logs, assertion results, and video recording.

---

## 🛠 Option B: Live Execution (Run Tests on Your Machine)

To execute the test suites locally on your own machine:

### Step 1: Initialize Virtual Environment
- **On Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
- **On Windows (cmd / PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\activate
  ```

### Step 2: Install Dependencies & Playwright Browser
```bash
pip install -r requirements.txt
playwright install chromium
```
*(On fresh Linux systems without graphical libraries, run: `playwright install-deps`)*

### Step 3: Execute the Test Suite

#### 1. User Story 2 (Curricula Trainer Account Form — `tests/us04_curricula_trainer/`)
- **Interactive Run with Visible Browser Window (Headed Mode):**
  ```bash
  python run_tests.py tests/us04_curricula_trainer/test_ts01_personal_info.py -k "test_tc_pi_001" --headed
  ```
- **Run a Specific Test Suite (e.g. Personal Information):**
  ```bash
  python run_tests.py tests/us04_curricula_trainer/test_ts01_personal_info.py
  ```
- **Full Test Suite Execution (All 7 Suites):**
  ```bash
  python run_tests.py tests/us04_curricula_trainer/
  ```
- **High-Speed Parallel Execution (4 Workers via pytest-xdist):**
  ```bash
  python run_tests.py tests/us04_curricula_trainer/ -n 4
  ```

#### 2. User Story 1 (Bing Search & Navigation — `tests/us01_bing_search/`)
- **Execute User Story 1 in Headed Mode:**
  ```bash
  python run_tests.py tests/us01_bing_search/test_bing_search.py --headed
  ```

#### 3. Run Internal Framework Architecture Unit Tests
Verifies the dual-gate error isolation mechanism (`Exceptor`, `Interceptor`, and `Catalog`):
```bash
python run_tests.py tests/unit/
```

> [!NOTE]
> **What Happens When You Run Live Tests?**  
> Every execution of `python run_tests.py` automatically generates a brand new session with a unique Run ID (e.g., `RUN-YYYYMMDD-XXXXXX`).  
> - The active report (`reports/<ticket>/execution_report.html`) is updated to reflect that specific execution.
> - An immutable historical copy is permanently stored in `reports/<ticket>/history/RUN-YYYYMMDD-XXXXXX.html`.
> - If you execute a single test (e.g., with `-k test_tc_pi_001`), the active report will display 1 test. To review the complete 68-test suite, re-run all suites (`python run_tests.py tests/us04_curricula_trainer/`) or directly open the baseline report **[`reports/us04_curricula_trainer/history/RUN-20260923-61EC0C.html`](../reports/us04_curricula_trainer/history/RUN-20260923-61EC0C.html)**.

---

## 📖 Deep Architectural Specifications (`AGENTS.md`)

For a comprehensive explanation of how this framework was engineered, consult **[`AGENTS.md`](./AGENTS.md)**. Key architectural sections include:

1. **Section 1 - Project Overview & Directory Responsibilities**:
   - Detailed rationale for the separation of concerns across `core/`, `pages/`, `components/`, `data/`, `reporting/`, and `tests/`.
2. **Section 2 - Gatekeeper Architecture (Exceptor & Interceptor)**:
   - **Exceptor (`core/exceptor.py`)**: The sole authority for business rules. Consumes static UI snapshots (`{"success_visible": bool, "visible_errors": Dict[str, str]}`) without touching Playwright.
   - **Interceptor (`core/interceptor.py`)**: Wraps Playwright interactions and categorizes technical failures (Timeouts, Browser crashes, Stale DOM, Network disconnects) via `core/catalog.py`.
3. **Section 3 - Acceptance Criteria & Traceability Matrix Standard**:
   - Explanation of the 1:1 mapped Traceability Matrix (`tests/us04_curricula_trainer/requirements/us04_curricula_trainer_traceability_matrix.md`) and how it eliminates guesswork when generating tests.
4. **Section 4 - Zero-Hardcoding Reporting Engine**:
   - How test names, Jira IDs, step expectations, and actual values are extracted dynamically from runtime metadata and `self.step()` blocks.
