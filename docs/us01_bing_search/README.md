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
| `tests/us01_bing_search/test_bing_search_parallel.py` | Parallel Data-Driven Testing (DDT) running multiple parameterized scenarios concurrently. |
| `data/search_data.json` | Centralized test data containing search keywords, target channels, and filter modes. |
| `pages/bing_home_page.py` | Page Object for Bing landing search page. |
| `pages/bing_search_results_page.py` | Page Object for Bing organic results and result clicking. |
| `pages/youtube_page.py` | Page Object for YouTube channel search, tabs, and video playback. |

---

## ⚡ Execution Commands

### 1. Run Standard Sequential Test
```bash
python run_tests.py tests/us01_bing_search/test_bing_search.py
```

### 2. Run Parallel Data-Driven Test (xdist)
```bash
python run_tests.py tests/us01_bing_search/test_bing_search_parallel.py -n 2
```

### 3. Run with Visible Browser (Headed Mode)
```bash
python run_tests.py tests/us01_bing_search/test_bing_search.py --headed
```

---

## 📊 Reports & Evidence
- **HTML Report**: `reports/us01_bing_search/execution_report.html`
- **Screenshots**: `reports/us01_bing_search/screenshots/`
- **Video Recordings**: Embedded directly inside the offline HTML report as Base64 Data URIs.
