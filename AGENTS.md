# AGENTS.md - UI Automation Architecture & Agent Guidelines

## 1. Project Overview & Architecture
This project implements an Enterprise Python UI Automation Framework using **Playwright** and **pytest**, structured according to the Page Object Model (POM), modular UI component design, ticket-driven test isolation, and a dedicated, self-contained HTML reporting engine.

```text
automation-ui/
├── AGENTS.md            # Guidelines, architectural roles, conventions, and folder specifications
├── requirements.txt     # Python dependencies (pytest, pytest-playwright, pytest-html, pytest-xdist)
├── pytest.ini           # Pytest settings, browser modes, default reporting options, custom markers
├── conftest.py          # Shared fixtures, ticket detection, dynamic report isolation, stealth hooks
├── run_tests.py         # Two-phase test execution orchestrator (pytest -> reporting)
├── generate_report.py   # Slim CLI entrypoint for the HTML report engine (~40 lines)
│
├── data/                # Inputs and test data files
│   └── search_data.json # Parameterized test keywords and expected outputs
│
├── components/          # Reusable shared UI pieces across multiple pages
│   ├── __init__.py
│   └── search_box.py    # Search bar component (shared between Bing home & results, human typing)
│
├── pages/               # Page Objects (encapsulates page locators & interactions)
│   ├── __init__.py          # Exports BasePage, BingHomePage, BingResultsPage, YouTubePage
│   ├── base_page.py         # Base Page Object: common browser interactions (navigate, click, fill, screenshot)
│   ├── bing_home_page.py    # Bing landing page actions (inherits BasePage)
│   ├── bing_results_page.py # Search results page & link navigation (inherits BasePage)
│   └── youtube_page.py      # Target website page object (inherits BasePage, cookie consent, channel actions)
│
├── tests/               # Test suites (verifications, assertions, and business flows only)
│   ├── __init__.py          # Exports BaseTest
│   ├── base_test.py         # Base Test class: autouse setup, Page Object injection, report helpers
│   └── us01_bing_search/    # Isolated Ticket / User Story 1 test package
│       ├── __init__.py
│       └── test_bing_search.py  # User Story 1 end-to-end test suite (inherits BaseTest)
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
    └── us01_bing_search/ # Isolated ticket artifacts folder (created automatically on execution)
        ├── execution_report.html # Final self-contained HTML report (latest run)
        ├── report.json           # Structured pytest execution log for this ticket
        ├── history/              # Timestamped historical run reports (RUN-*.html)
        ├── screenshots/          # ALL screenshots (deliverable evidence and failure captures)
        └── test-results/         # Playwright WebM video recordings organized by Run ID (<run_id>/)
```

---

## 2. Detailed Directory Responsibilities & Boundary Rules

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
- **Rule:** DO NOT put test assertions (`assert`) inside page objects. Page objects return data, status, or self.
- **Rule:** Integrate reusable components from `components/` where appropriate.
- **Rule:** Always use explicit locators and Playwright expect/waits; never rely on arbitrary `time.sleep()`.

### `components/` (Reusable shared UI pieces)
- **Role:** Independent UI widgets present on multiple pages or sections (e.g., search bars, navbars, modals).
- **Decoupled Design:** Operates on a `Page` or scoped `Locator`. Example: `SearchBoxComponent` handles human-like keystroke delays (`press_sequentially`) across both Bing Home and Results pages.

### `data/` (Inputs and test files)
- **Role:** Stores test inputs, credentials, search terms in JSON format (`search_data.json`).
- **Rule:** Never hardcode test data inside test files or page objects. Always read from `data/`.

### `tests/` (What to verify - Ticket-Driven Structure)
- **Role:** Orchestrates Page Objects and Components to execute business flows and make assertions (`assert`).
- **Base Class:** Every test class SHOULD inherit from `BaseTest` (`tests/base_test.py`).
- **`BaseTest` Capabilities:**
  - Automatically provides `self.page`, `self.step`, `self.search_data` via `autouse=True`.
  - Automatically instantiates common pages: `self.bing_home`, `self.bing_results`, `self.youtube`.
  - Provides `self.reports_dir` and `self.get_report_path(filename)` to store deliverables directly into the active ticket's report folder.
  - Provides assertion helper `self.assert_contains(actual, expected_fragment)`.
- **Folder Convention:**
  - Tests are grouped by Ticket / User Story packages: `tests/us<NN>_<ticket_name>/`.
  - Each package must contain `__init__.py` and test module(s) (e.g. `test_bing_search.py`).
- **Step Tracking Rule:** Every functional step MUST be wrapped inside `with self.step("Step Name", expected=..., actual=...):` to record timing data for the interactive pipeline and video synchronization.

### `reports/` (Ticket-Isolated Reporting & Artifacts)
- **Role:** Isolated target folders for test outputs, logs, videos, and HTML deliverables.
- **Isolation Mechanism:**
  - When running tests for `tests/us01_bing_search/`, all artifacts are automatically scoped to `reports/us01_bing_search/`.
  - Artifacts include `report.json`, `execution_report.html`, `history/` (RUN-*.html), `test-results/<run_id>/` (videos), and `screenshots/` (all PNG images).
  - Running a ticket test will **only** clean up artifacts for that ticket; other tickets' artifacts and historical run IDs are never touched or deleted.
- **Rule:** Gitignored (except `.gitkeep`). Never commit generated test runs or large `.webm` files.

### `conftest.py` (Dynamic Configuration & Stealth Setup)
- **Role:** Centralized fixtures, dynamic ticket path routing, anti-bot stealth hooks, and browser setup.
- **Dynamic Ticket Detection:**
  - Automatically inspects CLI arguments or collected tests to detect the active ticket folder.
  - Automatically configures Playwright `--output` to `reports/<ticket>/test-results/<run_id>/`.
  - Automatically configures `--json-report-file` to `reports/<ticket>/report.json`.
- **Display & Recording Standards:**
  - Viewport: 1920x1080 (Full HD).
  - Video Recording: 1920x1080 Full HD WebM.
  - Stealth: `playwright-stealth` evasions applied with automated cookie consent bypass.

### `reporting/` (Modular HTML Report Engine)
- **Role:** Transforms JSON execution logs and media into a standalone, 100% offline `execution_report.html`.
- **Subpackage Responsibilities:**
  - `reporting/core/`: Parser (`parser.py`), media locator/encoder (`media.py`), HTML assembly (`document.py`, `builder.py`), and report coordinator (`generator.py`).
  - `reporting/charts/`: Pure SVG mathematical chart renderers (`donut.py`, `bar.py`, `pipeline.py`, `diagram.py`, `trend.py`).
  - `reporting/assets/`: Presentation styles (`report.css`) and client-side scripts (`report.js`).
- **Boundary Rules:**
  - **100% self-contained:** Videos and images must be Base64-encoded Data URLs.
  - **Zero external CDN dependencies:** No Chart.js, Tailwind CDN, or Google Fonts.
  - **Interactive Diagram to Video Sync:** Clicking diagram nodes triggers `seekVideoAndScroll()` (scroll to video, wait until scroll finishes, then play).

### `run_tests.py` (Test Execution Orchestrator)
- **Role:** Coordinates Phase 1 (`pytest`), Phase 2 (`generate_report.py`), and Phase 3 (ANSI terminal summary).
- **Ticket Awareness:** Automatically detects ticket arguments (e.g. `python run_tests.py tests/us01_bing_search/`) and routes JSON and HTML outputs to the matching `reports/<ticket>/` folder.

### `generate_report.py` (Report Entrypoint)
- **Role:** Lightweight CLI wrapper around `reporting.ReportGenerator`.
- **Usage:** `python generate_report.py [path_to_report_json] [output_html_path]`.
- **Folder Scoping:** Automatically scopes reports and video discovery to `json_path.parent`.

---

## 3. Creating New Tests via Inheritance (Quick Guide)

### Step 1: Create a new Page Object (if testing a new page)
In `pages/` (e.g. `pages/shopee_page.py`):
```python
from pages.base_page import BasePage

class ShopeePage(BasePage):
    URL = "https://shopee.vn"

    def open_home(self):
        return self.navigate(self.URL)
```

### Step 2: Create a new Ticket Folder & Test Suite
In `tests/us02_shopee_cart/` (e.g. `test_cart.py`):
```python
import pytest
from tests.base_test import BaseTest

@pytest.mark.search
class TestShopeeCart(BaseTest):
    def test_add_to_cart(self):
        with self.step("Step 1: Open homepage"):
            self.page.goto("https://shopee.vn")

        with self.step("Step 2: Take deliverable evidence"):
            evidence_path = self.get_report_path("cart_evidence.png")
            self.page.screenshot(path=evidence_path)
            self.step.attach_screenshot(evidence_path)
```

### Step 3: Run the Ticket Test
```bash
python run_tests.py tests/us02_shopee_cart/
```
All outputs will automatically appear in `reports/us02_shopee_cart/` without affecting `us01_bing_search/`.

---

## 4. User Story 1 Implementation Guide

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

## 5. Execution Commands Quick Reference

- **Run specific ticket test & generate isolated report:**
  ```bash
  python run_tests.py tests/us01_bing_search/
  # or directly via pytest:
  pytest tests/us01_bing_search/
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
  python run_tests.py tests/us01_bing_search/ --headed
  ```

- **Regenerate HTML report without re-running tests:**
  ```bash
  python generate_report.py reports/us01_bing_search/report.json
  ```
