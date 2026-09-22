# AGENTS.md - UI Automation Architecture & Agent Guidelines

## 1. Project Overview & Architecture
This project implements an Enterprise Python UI Automation Framework using **Playwright** and **pytest**, structured according to the Page Object Model (POM), modular UI component design, and a dedicated, self-contained HTML reporting engine.

```text
automation-ui/
├── AGENTS.md            # Guidelines, architectural roles, and conventions for AI agents
├── requirements.txt     # Python dependencies (pytest, pytest-playwright, pytest-html, pytest-xdist)
├── pytest.ini           # Pytest settings, browser modes, reporting configurations
├── conftest.py          # Shared fixtures, step tracking, anti-bot stealth hooks, browser setup
├── run_tests.py         # Two-phase test execution orchestrator (pytest -> reporting)
├── generate_report.py   # Slim CLI entrypoint for the HTML report engine (~40 lines)
│
├── data/                # Inputs and test data files
│   └── search_data.json # Parameterized test keywords and expected outputs
│
├── components/          # Reusable shared UI pieces across multiple pages
│   ├── __init__.py
│   └── search_box.py    # Search bar component (shared between Bing home & results)
│
├── pages/               # Page Objects (encapsulates page locators & interactions)
│   ├── __init__.py
│   ├── bing_home_page.py    # Bing landing page actions
│   ├── bing_results_page.py # Search results page & link navigation
│   └── youtube_page.py      # Target website page object (User Story Step 4 & 5)
│
├── tests/               # Test suites (verifications, assertions, and workflows only)
│   ├── __init__.py
│   └── test_bing_search.py  # User Story 1 end-to-end test execution
│
├── reporting/           # Modular HTML Report Engine (100% offline & self-contained)
│   ├── __init__.py      # Exports ReportGenerator and generate_report
│   ├── core/            # Core processing and HTML construction
│   │   ├── __init__.py
│   │   ├── parser.py    # Parses report.json, computes step timeline offsets & stats
│   │   ├── media.py     # Locates video/screenshots, encodes binary to Base64 Data URLs
│   │   └── builder.py   # HTML layout assembly & ReportGenerator class coordinator
│   ├── charts/          # Pure SVG mathematical chart renderers (Zero external JS/CDN)
│   │   ├── __init__.py
│   │   ├── donut.py     # Pure SVG Donut Chart (Pass Rate %)
│   │   ├── bar.py       # Pure SVG Duration Bar Chart for individual steps
│   │   └── pipeline.py  # Pure SVG Interactive Step Pipeline (Step 1 -> 5 with click/pulse)
│   └── assets/          # Isolated presentation assets (syntax-highlightable, embedded at runtime)
│       ├── __init__.py  # Asset loader (inlines CSS/JS into final HTML)
│       ├── report.css   # Dark theme dashboard styles, 16:9 video, lightbox, pulse keyframes
│       └── report.js    # Client-side JS: scroll-to-video-then-play, 2-way sync, bilingual EN/VI
│
└── reports/             # Execution artifacts, reports, and evidence
    ├── .gitkeep         # Keeps directory tracked in Git
    ├── report.json      # Structured pytest execution log (consumed by reporting/)
    ├── execution_report.html # Final self-contained HTML report
    ├── execution_step5.png   # Step 5 screenshot deliverable
    └── test-results/    # Playwright WebM video recordings (1920x1080 Full HD)
```

---

## 2. Directory Responsibilities & Boundary Rules

### `pages/` (How to interact with a page)
- **Role:** Encapsulates web elements and page actions.
- **Rule:** DO NOT put test assertions (`assert`) inside page objects. Page objects return data, status, or self.
- **Rule:** Integrate reusable components from `components/` where appropriate.
- **Rule:** Always use explicit locators and Playwright expect/waits; never rely on arbitrary `time.sleep()`.

### `components/` (Reusable shared UI pieces)
- **Role:** Independent UI widgets present on multiple pages or sections (e.g., search bars, navbars, modals).
- **Rule:** Decoupled from full page logic. Operates on a `page` or scoped locator.

### `data/` (Inputs and test files)
- **Role:** Stores test inputs, credentials, keywords in JSON format.
- **Rule:** Never hardcode test data inside test files or page objects. Always read from `data/`.

### `conftest.py` (Shared fixtures, hooks, and recording setup)
- **Role:** Centralized fixtures (`search_data`, `launch_options`, `browser_context_args`, `step` tracker, hooks).
- **Rule:** Maintain Full HD 1080p recording settings:
  ```python
  "record_video_size": {"width": 1920, "height": 1080},
  "viewport": {"width": 1920, "height": 1080}
  ```
- **Rule:** Maintain `StepTracker` and `step` context manager fixture to track individual step durations, statuses, and timestamps.
- **Rule:** Pytest session finish hook (`pytest_sessionfinish`) must be guarded with `if not hasattr(session.config, "workerinput"):` to guarantee safety with `pytest-xdist`.

### `tests/` (What to verify)
- **Role:** Orchestrates Page Objects and Components to execute business flows and make assertions (`assert`).
- **Rule:** Keep test functions clean and readable: Arrange -> Act -> Assert.
- **Rule: Step Tracking:** Every functional step MUST be wrapped inside `with step("Step Name"):` to record timing data for the interactive pipeline and video synchronization:
  ```python
  with step("Step 1: Navigate to Bing homepage"):
      home_page.navigate()
  ```

### `reporting/` (Modular HTML Report Engine)
- **Role:** Transforms `reports/report.json` and recorded media into a standalone, offline `execution_report.html`.
- **Subpackage Responsibilities:**
  - `reporting/core/`: Parser (`parser.py`), media locator/encoder (`media.py`), HTML assembly (`builder.py`).
  - `reporting/charts/`: Pure SVG math generators (`donut.py`, `bar.py`, `pipeline.py`). **NEVER** use external charting CDNs.
  - `reporting/assets/`: Keep CSS in `report.css` and JS in `report.js`. Loaded and inlined into the HTML by `assets/__init__.py`.
- **Boundary Rules:**
  - 100% self-contained: Videos and images must be Base64-encoded Data URLs.
  - Zero external CDN dependencies: No Chart.js, Tailwind CDN, or Google Fonts.
  - Interactive Diagram to Video Sync: Clicking diagram nodes must trigger `seekVideoAndScroll()` (scroll to video, wait until scroll finishes, then play).

### `generate_report.py` (Report Entrypoint)
- **Role:** Lightweight CLI wrapper around `reporting.ReportGenerator`.
- **Rule:** Keep this file minimal (~40 lines). Do not add business or rendering logic here; delegate to `reporting/`.

### `run_tests.py` (Test Execution Orchestrator)
- **Role:** Coordinates Phase 1 (`pytest`) and Phase 2 (`generate_report.py`), streaming live logs and displaying ANSI summaries.
- **Rule:** Must support passthrough flags (e.g., `-n 4`, `-m marker`, `-k filter`, `--headed`).

### `reports/` (Run outputs & deliverables)
- **Role:** Target folder for `report.json`, `execution_report.html`, screenshots, and video recordings.
- **Rule:** Gitignored (except `.gitkeep`). Never commit generated test runs or large `.webm` files.

---

## 3. User Story 1 Implementation Guide

1. **Step 1:** Navigate to `bing.com` (using `BingHomePage.navigate()`).
2. **Step 2:** Search for `{Keyword1}` (e.g., `facebook`).
3. **Step 3:** Search for `{Keyword2}` (e.g., `youtube`).
4. **Step 4: Access the target website:**
   - On `BingResultsPage`, click on the target link (handling whether it opens in a new tab or the same tab).
   - Switch context / wait for target page to reach ready state.
5. **Step 5: Perform defined page actions:**
   - Encapsulated in `YouTubePage` (or target page object).
   - Verify page loaded, interact with a target element (e.g. search channel, navigate to Videos tab, sort oldest, play video).
   - Save execution screenshot to `reports/execution_step5.png` as deliverable evidence.

---

## 4. Execution Commands Quick Reference

- Run all tests and auto-generate report:
  ```bash
  python run_tests.py
  # or directly:
  pytest
  ```
- Run parallel tests (4 workers):
  ```bash
  python run_tests.py -n 4
  ```
- Regenerate report without re-running tests:
  ```bash
  python generate_report.py reports/report.json
  ```
