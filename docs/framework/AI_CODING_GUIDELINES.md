# AI Coding Guidelines: Enterprise UI Test Generation

> **Target Audience:** AI Coding Assistants (Claude, Cursor, Copilot, Antigravity, ChatGPT) & Automation Engineers.  
> **Framework:** Python 3.10+ | Sync Playwright | Pytest | ExtentReports Engine.  
> **Scope:** Generating automated test suites for user stories and acceptance criteria without hallucinations or architecture violations.

---

## 0. QUY TRÌNH BẮT BUỘC KHI NHẬN PROMPT TEST BẤT KỲ URL NÀO (E.G. http://localhost:5174/profile)

> [!CAUTION]
> **2 SAI LẦM PHỔ BIẾN AI CẦN TRÁNH TUYỆT ĐỐI**:
> 1. **KHÔNG ĐƯỢC PHÂN TÍCH SOURCE CODE**: Tuyệt đối không mở `copy/` hay code React/Vue/Node.js để tìm selector hay logic. QA là kiểm thử Black-box trên UI!
> 2. **BSK KHÔNG PHẢI TEST RUNNER**: BSK **CHỈ DÙNG ĐỂ SCAN LOCATOR** (`python3 tools/recon_bsk.py --url <URL>`). Tuyệt đối không dùng BSK để click hay assert chạy test!

### 4 Bước Chuẩn Hóa Bắt Buộc:

```text
[1. Nhận yêu cầu: Test URL / Màn hình]
                 │
                 ▼
[2. Dùng BSK Soi DOM] ──► Chạy: python3 tools/recon_bsk.py --url <URL>
                 │        (BSK mở web thật, quét cây DOM, trả về bảng Selector 100% chuẩn)
                 ▼
[3. Cấu Trúc File & Báo Cáo Cha/Con] ──► Tổ chức theo cây thư mục Cha / Con:
                 ├── THƯ MỤC PYTEST:
                 │   tests/<fs_module>/<fs_module>-<tên-component>/
                 │   ├── __init__.py
                 │   ├── conftest.py
                 │   ├── test_atomic_<feature>_components.py     # ĐƠN COMPONENT (Atomic UI Unit)
                 │   └── test_integration_<feature>.py          # GIỮA NHIỀU COMPONENT (Tương tác / Form)
                 │
                 ├── THƯ MỤC KỊCH BẢN MARKDOWN (test_specs/):
                 │   ├── Yêu cầu "Đơn Component"  ➔ test_specs/atomic/<fs_module>/<name>.md (@atomic @p0)
                 │   │   👉 Chỉ test riêng 1 component độc lập: ô input, button, dirty state, mask toggle.
                 │   ├── Yêu cầu "Nhiều Component" ➔ test_specs/integration/<fs_module>/<name>.md (@integration @api)
                 │   │   👉 Tương tác: 1 Comp ➔ 1 Comp khác, Master ➔ Detail, Form 🔁 API, Trigger ➔ Modal.
                 │   ├── Yêu cầu "UAT luồng dài"   ➔ test_specs/uat/<fs_module>/<name>.md (@uat @journey)
                 │   │   👉 Đi xuyên suốt nhiều màn hình, giữ session liên tục.
                 │   └── Yêu cầu "Break_It / Phá"  ➔ test_specs/break_it/<fs_module>/<name>.md (@break_it)
                 │       👉 Thử thách độ bền: Gỡ client validate, double-click, 10k ký tự, server 500 chaos.
                 │
                 └── THƯ MỤC BÁO CÁO CÔ LẬP CHA/CON (reports/):
                     reports/<fs_module>/<fs_module>-<tên-component>/
                     ├── execution_report.html  (Báo cáo ExtentReports Dashboard mới nhất)
                     ├── bao_cao_tinh_gon.html  (Báo cáo tinh gọn 1 trang)
                     ├── report.json            (Dữ liệu JSON chi tiết)
                     ├── history/<RUN_ID>.html  (Lịch sử từng phiên chạy)
                     └── test-results/<RUN_ID>/ (Video WebM 1080p và ảnh bằng chứng)
                 │
                 ▼
[4. Playwright Thực Thi] ──► Chạy từ thư mục gốc /home/baudui/automation-ui:
                             • Pytest: .venv/bin/python run_tests.py tests/<fs_module>/<fs_module>-<tên-component>/
                             • Markdown: .venv/bin/python md_runner.py test_specs/<tier>/<fs_module>/<name>.md
```

### ⚠️ BẢNG ĐỐI CHIẾU 2 SAI LẦM PHỔ BIẾN CẦN TRÁNH TUYỆT ĐỐI:
| Hành vi Sai Trái (BỊ CẤM) | Hành vi Đúng Chuẩn Của Dự Án |
| :--- | :--- |
| ❌ Mở mã nguồn trong `copy/` hoặc file `.tsx`, `.jsx` để đọc component và đoán tên selector / ID. | ✅ Chạy `python3 tools/recon_bsk.py --url <URL>` để BSK mở web thật và nhặt đúng selector từ DOM sống. |
| ❌ Dùng lệnh BSK (`bsk click`, `bsk type`, `bsk eval`) để chạy kịch bản kiểm thử. | ✅ BSK chỉ làm nhiệm vụ trinh sát (Reconnaissance) nhặt locator. Kịch bản test PHẢI viết ra file Markdown và thực thi bằng Playwright (`md_runner.py`). |

---

## 1. Core Invariants (Zero Exceptions)

When generating Python test code for this repository, you **MUST** follow these five core invariants:

1. **Zero Assertions in Page Objects**: All validations belong exclusively in `tests/`. Page Objects (`pages/`) only perform actions and query UI state.
2. **Zero Hardcoded Test Data**: Never hardcode test strings (`"Tan Wei Ling"`, `"123456"`) inside test methods. Always load from `data/` JSON fixtures and use `copy.deepcopy()`.
3. **Traceability**: Every test method must be named `test_tc_<scenario_id>_<brief_slug>` and include a docstring documenting: Scenario ID, Test Data, and Expected Behavior.
4. **Zero `time.sleep()`**: Never use `time.sleep()`. Rely on Playwright auto-waiting, `wait_for_visible()`, or `expect(locator)`.
5. **No Locator Invention**: Always use existing methods on Page Objects. If a selector is missing, mark with `# [TO BE ADDED TO PAGE OBJECT: selector_name]`. Never write `page.locator("...")` directly inside test suites.
6. **Zero Assumptions on Requirements (BẢN CHẤT UI AUTOMATION TESTING - ZERO ASSUMPTIONS)**: AI coding assistants must NEVER guess business rules, form validation error text, button disabled states, or calculation formulas. ONLY retrieve information from `specs/md/` (FS documents, `FS_SPECIFICATIONS_SUMMARY.md`, `EAFAMS_SPLIT_PAYMENT_AND_AI_FAS_TEST_CASES_AND_AC.md`, `MEETINGS_AND_DECISIONS_SUMMARY.md`). If details are missing or conflicting, consult `specs/md/FSD_ALIGNMENT_AND_GAP_AUDIT_REPORT.md` or STOP AND ASK THE USER.

---

## 2. Standard Test Class Structure

All test suites must inherit from `BaseTest` located in `tests.base_test`:

```python
import copy
import pytest
from core.exceptor import Exceptor
from tests.base_test import BaseTest


@pytest.fixture(scope="class")
def trainer_data(request):
    """Load test data for curricula trainer account."""
    from tests.base_test import BaseTest
    bt = BaseTest()
    return bt.load_json_data("data/curricula_trainer_data.json")


class TestSuiteName(BaseTest):
    """Docstring explaining the test suite and covered requirement scope."""
```

### Subclass Built-In Properties (Do Not Re-instantiate):
- `self.page`: Active Playwright `Page` instance.
- `self.step`: Isolated `StepTracker` context manager for timeline & video synchronization.
- `self.curricula`: Pre-initialized `CurriculaTrainerPage` instance (lazy loaded).
- `self.get_page(PageClass)`: Dynamically load any other Page Object.
- `self.get_fixture_file(rel_path)`: Resolves absolute path to files in `data/fixtures/`.

---

## 3. Canonical Code Templates (Few-Shot Examples)

### Template 1: Standard Happy Path (Form Submission Succeeded)
```python
def test_tc_save_001_valid_submission(self, trainer_data):
    """
    TC_SAVE_001 — Create Trainer Account - Valid Form Submission
    Test Data: trainer_data["valid_singapore_resident"]
    Expected (FSD): Trainer account created successfully with active status and Trainer ID.
    """
    data = copy.deepcopy(trainer_data["valid_singapore_resident"])

    with self.step("Step 1: Open registration form"):
        self.curricula.open()

    with self.step("Step 2: Fill mandatory fields with valid data"):
        self.curricula.fill_full_form(data)

    with self.step("Step 3: Click Save button"):
        self.curricula.save()

    with self.step("Step 4: Verify account created successfully"):
        snapshot = self.curricula.get_state_snapshot()
        Exceptor.expect_success(snapshot, context="TC_SAVE_001", step=self.step)
        self.step.set_actual(f"Account created: {self.curricula.get_success_text()}")
```

---

### Template 2: Standard Unhappy Path (Validation Error Displayed)
```python
def test_tc_pi_002_preferred_name_empty(self, trainer_data):
    """
    TC_PI_002 — Preferred Name - Mandatory Field Blank
    Test Data: Preferred name left empty ("")
    Expected (FSD): Form displays validation error "This field is required." on preferredName.
    """
    data = copy.deepcopy(trainer_data["valid_singapore_resident"])
    data["preferred_name"] = ""

    with self.step("Step 1: Open registration form"):
        self.curricula.open()

    with self.step("Step 2: Fill form leaving Preferred Name empty"):
        self.curricula.fill_full_form(data)

    with self.step("Step 3: Attempt to Save form"):
        self.curricula.save()

    with self.step("Step 4: Verify validation error on Preferred Name"):
        snapshot = self.curricula.get_state_snapshot()
        Exceptor.expect_rejection(
            snapshot=snapshot,
            field="preferredName",
            message_contains="This field is required.",
            context="TC_PI_002",
            step=self.step,
        )
```

---

### Template 3: Known Bug Verification (Intentional Bug-Hunting)
When a specification defect exists in the application under test:

```python
# Mode A: Using Exceptor Bug Hunters
def test_tc_pi_003_preferred_name_exceeds_100_chars(self, trainer_data):
    """
    TC_PI_003 — Preferred Name - Exceeds 100 characters (Boundary Max+1)
    Test Data: 101 character string ("A"*101)
    Expected (FSD): System rejects input exceeding 100 characters.
    [Mock App Deviation: allows 101 characters -> BUG-007]
    """
    data = copy.deepcopy(trainer_data["valid_singapore_resident"])
    data["preferred_name"] = "A" * 101

    with self.step("Step 1: Open registration form and fill with 101 chars"):
        self.curricula.open()
        self.curricula.fill_full_form(data)
        self.curricula.save()

    with self.step("Step 2: Adjudicate known validation bypass bug"):
        snapshot = self.curricula.get_state_snapshot()
        # Input is INVALID per FSD. If app accepts it, raise BUG DETECTED!
        Exceptor.expect_bug_if_accepted(snapshot, context="BUG-007")

# Mode B: Using Strict Pytest XFAIL
@pytest.mark.xfail(strict=True, reason="BUG-007: Preferred Name allows > 100 characters")
def test_tc_pi_003_xfail_variant(self, trainer_data):
    data = copy.deepcopy(trainer_data["valid_singapore_resident"])
    data["preferred_name"] = "A" * 101
    self.curricula.open()
    self.curricula.fill_full_form(data)
    self.curricula.save()
    snapshot = self.curricula.get_state_snapshot()
    assert "preferredName" in snapshot["visible_errors"], "Form must reject > 100 characters"
```

---

### Template 4: Native Browser Dialog Handling (Cancel with Confirmation)
```python
def test_tc_cancel_001_confirm_dialog(self, trainer_data):
    """
    TC_CANCEL_001 — Cancel Button - Confirmation Dialog Accepted
    Expected: Browser triggers confirm dialog; upon accepting, form reloads.
    """
    with self.step("Step 1: Open form and input dirty data"):
        self.curricula.open()
        self.curricula.set_preferred_name("Draft Trainer")

    with self.step("Step 2: Pre-register dialog handler and click Cancel"):
        # CRITICAL: Always register dialog listener before triggering the action!
        self.curricula.handle_next_dialog(accept=True)
        self.curricula.cancel()

    with self.step("Step 3: Verify form has reset to blank state"):
        val = self.curricula.get_field_value(self.curricula.PREFERRED_NAME)
        assert val == "", f"Expected preferredName to be empty after cancel, got '{val}'"
```

---

### Template 5: File Upload with Dynamic Path Resolution
```python
def test_tc_upload_001_valid_document(self):
    """
    TC_UPLOAD_001 — ID Document - Valid PNG Upload
    """
    doc_path = self.get_fixture_file("data/fixtures/valid_id.png")

    with self.step("Step 1: Open form"):
        self.curricula.open()

    with self.step("Step 2: Upload valid PNG ID document"):
        self.curricula.upload_document(doc_path)

    with self.step("Step 3: Verify upload input has received file"):
        assert doc_path.exists()
```

---

## 4. Top AI Anti-Patterns to Avoid

| # | Anti-Pattern | Why It Breaks | Correct Pattern |
|---|---|---|---|
| ❌ 1 | `time.sleep(3)` | Flaky, slow, violates Invariant 4 | Use Playwright auto-waiting or `page.wait_for_timeout()` |
| ❌ 2 | `page.locator("#saveBtn").click()` | Violates Invariant 1 (POM bypassing) | Use `self.curricula.save()` |
| ❌ 3 | `data = trainer_data["resident"]; data["name"] = "X"` | Mutates global fixture, breaks parallel xdist | Use `copy.deepcopy(trainer_data["..."])` |
| ❌ 4 | `try: self.curricula.save() except: pass` | Swallows errors, masks regressions, desyncs report | Allow exception to propagate so pytest captures evidence |
| ❌ 5 | `self.curricula.cancel()` without dialog handler | Native dialog blocks page, Playwright auto-dismisses | Call `self.curricula.handle_next_dialog(accept=True)` first |
| ❌ 6 | Hardcoding `"data/fixtures/valid_id.png"` | Fails when pytest runs from subdirectories | Use `self.get_fixture_file("data/fixtures/...")` |
| ❌ 7 | Missing `self.step()` context managers | HTML report timeline and video sync will be empty | Wrap each logical phase inside `with self.step("Step N: ..."):` |

---

## 5. Standard 19-Column Test Case Matrix Ingestion Standard

Whenever test cases are provided in the standard 19-column format, map every column strictly according to this table:

| # | Column Name | Code Mapping & Usage |
|---|---|---|
| 1 | **ID** (`TC-001`) | Prefix in test function: `def test_tc_001_<slug>(self):` & `json_metadata["tc_id"] = "TC-001"`. |
| 2 | **Scenario ID** (`TS-001`) | Test suite file name: `tests/<traceability>/test_ts01_<suite_slug>.py`. |
| 3 | **Title** | Suffix of test function and header in docstring. |
| 4 | **Test Suite** | Logical module/feature grouping. Each suite maps to 1 independent test file. |
| 5 | **Page** | Target Page Object in `pages/`. Create/update `pages/<page>.py` before writing test. |
| 6 | **Severity** (`P0`, `P1`, ...) | Pytest Marker: `@pytest.mark.p0`, `@pytest.mark.p1`. |
| 7 | **Priority** (`High`, `Medium`, `Low`) | Pytest Marker: `@pytest.mark.priority_high`, docstring & `json_metadata["priority"]`. |
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

## 6. SketchVLM Visual Overlays & Video Annotation Standards

The framework integrates a **Dual-Layer Visual Engine** inspired by SketchVLM (*arXiv:2604.22875*) to ensure all recorded Playwright WebM videos are self-explanatory and defect-evident:

```text
 ┌───────────────────────────┬───────────────────────────┐
 ▼                           ▼                           ▼
[1] LIVE STEP HUD           [2] ACTION SPOTLIGHT        [3] DEFECT SKETCH CALLOUT
- Injected on self.step()   - Pulse ring on click/fill  - Multi-stroke sketch ellipse
- Shows current step title  - Action pill: 👆 CLICK, ✏️  - Curved SVG pointer arrow
- Burned into 1080p video   - 500ms non-blocking fade   - Floating DEFECT EVIDENCE card
```

### Directives for AI Coding Assistants:
1. **Always Wrap Phases in `with self.step(...)`**:
   The Step HUD is triggered automatically by `StepTracker.__enter__`. Never write raw actions outside of a `with self.step("Step X: ..."):` block, or the video recording will lack the HUD indicator.
2. **Use Page Object Action Methods**:
   Always call methods like `click_element()`, `fill_text()`, `save()`, `cancel()` on Page Objects. These methods automatically trigger `SketchAnnotator.spotlight_action` to render action ripples in the video. Never bypass with raw `page.locator().click()`.
3. **Automatic Defect Highlighting on Assertion Failure**:
   When an assertion fails inside a step, `SketchAnnotator.highlight_defect()` automatically targets the defective element, scrolls it into center view, draws the organic sketch circle and SVG arrow, and pauses for 1.4s so the video camera captures the defect before browser shutdown.
4. **On-Demand AI Root Cause Triage**:
   For complex layout/visual defects (Tầng 3 Visual/Layout & Tầng 6 Accessibility in Invariant 7), use `tools/sketch_vlm_oracle.py` to analyze failure screenshots using Gemini VLM and generate `.sketch.svg` overlays.

