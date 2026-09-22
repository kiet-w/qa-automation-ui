# AGENTS.md - UI Automation Architecture & Agent Guidelines

## 1. Project Overview & Architecture
This project implements a Python UI Automation Framework using **Playwright** and **pytest**, structured according to the Page Object Model (POM) and modular UI component design.

```text
automation-ui/
├── AGENTS.md            # Guidelines, architectural roles, and conventions for AI agents
├── requirements.txt     # Python dependencies (pytest, pytest-playwright, pytest-html, pytest-xdist)
├── pytest.ini           # Pytest settings, browser modes, reporting configurations
├── conftest.py          # Shared fixtures, anti-bot stealth hooks, browser setup
├── data/                # Inputs and test data files
│   └── search_data.json # Parameterized test keywords and expected outputs
├── components/          # Reusable shared UI pieces across multiple pages
│   └── search_box.py    # Search bar component (shared between Bing home & results)
├── pages/               # Page Objects (encapsulates page locators & interactions)
│   ├── bing_home_page.py    # Bing landing page actions
│   ├── bing_results_page.py # Search results page & link navigation
│   └── youtube_page.py      # Target website page object (User Story Step 4 & 5)
├── tests/               # Test suites (verifications, assertions, and workflows only)
│   └── test_bing_search.py  # User Story 1 end-to-end test execution
└── reports/             # Execution reports, HTML reports, and evidence (screenshots, test-results/ videos)
```

---

## 2. Directory Responsibilities & Boundary Rules

### `pages/` (How to interact with a page)
- **Role:** Encapsulates web elements and page actions.
- **Rule:** DO NOT put test assertions (`assert`) inside page objects. Page objects return data, status, or self.
- **Rule:** Integrate reusable components from `components/` where appropriate.

### `components/` (Reusable shared UI pieces)
- **Role:** Independent UI widgets present on multiple pages or sections (e.g., search bars, navbars, modals).
- **Rule:** Decoupled from full page logic. Operates on a `page` or scoped locator.

### `data/` (Inputs and test files)
- **Role:** Stores test inputs, credentials, keywords in JSON format.
- **Rule:** Never hardcode test data inside test files or page objects.

### `conftest.py` (Shared fixtures and setup)
- **Role:** Centralized fixtures (`search_data`, `launch_options`, `browser_context_args`, hooks).
- **Rule:** Uses system Brave browser (`/usr/bin/brave`) with anti-detection flags, overlay dismissals, and screenshot attachments.

### `tests/` (What to verify)
- **Role:** Orchestrates Page Objects and Components to execute business flows and make assertions (`assert`).
- **Rule:** Keep test functions clean and readable: Arrange -> Act -> Assert.

### `reports/` (Run results and evidence)
- **Role:** Destination for all generated HTML reports, run logs, and execution evidence screenshots.

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
   - Verify page loaded, interact with a target element (e.g. search bar, play, or browse).
   - Save execution screenshot to `reports/execution_step5.png` as deliverable evidence.
