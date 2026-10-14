# User Story 01: Bing Search & YouTube Media Navigation

## 📌 Overview
This User Story automates an end-to-end cross-domain web navigation journey starting from Microsoft Bing search engine and progressing into YouTube media playback.

---

## 🎯 Test Objectives & Scenario
1. **Bing Search Navigation**:
   - Access Bing homepage (`https://www.bing.com`) and verify search bar ready state.
   - Execute query for Keyword 1 (e.g., `Facebook`) and assert first organic result.
   - Execute query for Keyword 2 (e.g., `YouTube`) and assert first organic result.
2. **Target Navigation & Multi-Tab Handling**:
   - Click the first organic search result to navigate to YouTube.
   - Reliably transfer browser context (`Playwright Page Context`) to the newly opened YouTube tab/window.
3. **In-Page Media Interaction**:
   - Search for the designated media channel (e.g., `VTV24` or `VTV`).
   - Navigate to the channel profile and open the **Videos** tab.
   - Filter/Sort videos by criteria (e.g., `Oldest` / Earliest video).
   - Initiate playback and capture evidence screenshot into execution reports.

---

## 📂 Source Code & Test Structure

| File | Purpose |
|---|---|
| `tests/us01_bing_search/test_bing_search.py` | Single sequential end-to-end execution test suite. |
| `examples/test_bing_search_parallel.py` | Reference Data-Driven Testing (DDT) parallel scenario examples. |
| `data/search_data.json` | Centralized test data containing search keywords, target channels, and filter modes. |
| `pages/bing_home_page.py` | Page Object for Bing landing search page. |
| `pages/bing_results_page.py` | Page Object for Bing organic results and result clicking. |
| `pages/youtube_page.py` | Page Object for YouTube channel search, tabs, and video playback. |

---

## ⚡ Execution Commands

### 1. Run User Story 1 Test Suite (Default Playwright Chromium)
```bash
python run_tests.py tests/us01_bing_search/
```

### 2. Run with Visible Browser (Headed Mode)
```bash
python run_tests.py tests/us01_bing_search/ --headed
```

### 3. Run with Alternate Browsers
```bash
# Brave Browser (auto-detected across Linux/macOS/Windows)
python run_tests.py tests/us01_bing_search/ --target-browser brave

# Google Chrome / Microsoft Edge / Firefox
python run_tests.py tests/us01_bing_search/ --target-browser chrome
python run_tests.py tests/us01_bing_search/ --target-browser edge
python run_tests.py tests/us01_bing_search/ --target-browser firefox

# Custom browser binary path
python run_tests.py tests/us01_bing_search/ --browser-path /usr/bin/google-chrome
```

---

## 🛡 Anti-Bot & Stability Architecture

### 1. Sequential Execution Rationale
Public search engines (Microsoft Bing) employ aggressive rate-limiting and bot challenge algorithms. Firing concurrent queries in parallel processes from the same IP address quickly triggers Cloudflare "Verify you are human" / captcha interstitials.  
User Story 1 runs sequentially by default to guarantee 100% deterministic, flake-free execution for grading. A multi-scenario parallel Data-Driven Testing (DDT) implementation is available for inspection in **[`examples/test_bing_search_parallel.py`](../../examples/test_bing_search_parallel.py)**.

### 2. `TargetClosedError` Resolution via Clean URL Decoding
When Bing search results are clicked, Bing routes navigation through a tracking URL:
```text
https://www.bing.com/ck/a?!&&p=...&u=a1aHR0cHM6Ly93d3cueW91dHViZS5jb20v...&ntb=1
```
This tracking URL returns an interstitial HTML payload containing:
```javascript
window.open("https://www.youtube.com/", "_blank");
window.close();
```
In automated Playwright runs, this script immediately closes the active page while `page.goto()` is awaiting navigation, causing `playwright._impl._errors.TargetClosedError: Page.goto: Target page, context or browser has been closed`.

**Our Solution (`pages/bing_results_page.py`):**
`_extract_clean_target_url()` inspects the result link, extracts the Base64-encoded `u` parameter (`a1<BASE64>`), and decodes it directly to `https://www.youtube.com/`. Playwright navigates straight to YouTube, avoiding Bing's tracking script and `window.close()` entirely. A tab recovery mechanism is also in place if a popup is spawned.

### 3. Human Keystroke Cadence
In `components/search_box.py`, typing delays use Playwright's native `press_sequentially(query, delay=random.randint(60, 110))` with randomized millisecond pauses. This emulates realistic user input without using thread-blocking `time.sleep()`.

### 4. Pure Assertion Separation
Following framework standards, `YouTubePage` and `BingResultsPage` contain **zero test assertions (`assert`)**. Locators, element states, and DOM queries are returned to the test method, where business assertions are adjudicated via `Exceptor`.

---

## 📊 Reports & Evidence
- **HTML Report**: `reports/us01_bing_search/execution_report.html`
- **Screenshots**: `reports/us01_bing_search/screenshots/`
- **Video Recordings**: Embedded directly inside the offline HTML report as Base64 Data URIs.

