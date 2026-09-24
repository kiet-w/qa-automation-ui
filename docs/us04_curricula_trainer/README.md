# User Story 04: Curricula Trainer Account Form

## 📌 Overview
This User Story covers the comprehensive UI test automation suite for the **Trainer Account Creation Form** (`curricula_trainer_account.html`). It verifies complex business logic, strict validation boundaries, dynamic address toggling, file upload size limits, and save/cancel lifecycle workflows across **68 test cases** and identifies **10 distinct application defects**.

---

## 🗂 Documentation Index

All documentation for this User Story has been organized into dedicated subdirectories:

### 1. 📋 Test Cases & Requirements (`test_cases/`)
* **[`test_cases/US04_68_TestCases.md`](test_cases/US04_68_TestCases.md)**: Full catalog of all 68 test cases with IDs, descriptions, inputs, and expected outcomes.
* **[`test_cases/us04_curricula_trainer_AC.md`](test_cases/us04_curricula_trainer_AC.md)**: Formal Acceptance Criteria specifications (**AC-01** to **AC-68**).
* **[`test_cases/us04_curricula_trainer_traceability_matrix.md`](test_cases/us04_curricula_trainer_traceability_matrix.md)**: 1:1 Traceability Matrix linking ACs to UI behaviors and exact `Exceptor` assertions.

### 2. 🐛 Defect Reports & Analysis (`defects_and_analysis/`)
* **[`defects_and_analysis/Bug_Traceability_Matrix.md`](defects_and_analysis/Bug_Traceability_Matrix.md)**: Detailed mapping of the 10 detected application bugs, root causes, and affected fields.
* **[`defects_and_analysis/Severity_Matrix_10Bugs.md`](defects_and_analysis/Severity_Matrix_10Bugs.md)**: Severity classification matrix (Critical, High, Medium, Low) for all bugs.
* **[`defects_and_analysis/D4_ExecutionResults_ANSWERKEY.md`](defects_and_analysis/D4_ExecutionResults_ANSWERKEY.md)**: Comprehensive execution results baseline and answer key for grading evaluation.

### 3. 🤖 AI Generation Prompts (`ai_prompts/`)
* **[`ai_prompts/PROMPT_MAIN_ai_test_generation_en.md`](ai_prompts/PROMPT_MAIN_ai_test_generation_en.md)**: **Deliverable 0** - Full English system prompt used to architect the framework and generate test suites.
* **[`ai_prompts/PROMPT_MAIN_gen_test_from_deliverables.md`](ai_prompts/PROMPT_MAIN_gen_test_from_deliverables.md)**: Prompt for generating automated test suites directly from course deliverables.
* **[`ai_prompts/PROMPT_STEP2_doi_chieu_D4.md`](ai_prompts/PROMPT_STEP2_doi_chieu_D4.md)**: Prompt for cross-verifying execution results against Deliverable 4.

---

## 🧪 7 Modular Test Suites

The test implementation is divided into 7 distinct suites matching the functional sections of the form:

| Suite File | Scope & Field Validations |
|---|---|
| `test_ts01_personal_info.py` | Salutation, Name, NRIC/FIN ID validation, ID photo upload (10MB limit) |
| `test_ts02_contact_info.py` | Primary/Secondary emails, Country code, Phone formats |
| `test_ts03_emergency_contact.py` | Contact name, Relationship, Phone number validations |
| `test_ts04_singapore_address.py` | 6-digit postal code, Block/Street/Floor/Unit mandatory rules |
| `test_ts05_non_singapore_address.py` | Address Line 1-3, City, State/Province, Country selector |
| `test_ts06_save_action.py` | Form submission, duplicate email detection, mandatory field checks |
| `test_ts07_cancel_action.py` | Cancel confirmation modal, discard changes, redirect behavior |

---

## ⚡ Execution Commands

### 1. Run All 7 Suites (68 Tests)
```bash
python run_tests.py tests/us04_curricula_trainer/
```

### 2. Run Parallel Multi-Worker Execution (Recommended for Speed)
```bash
python run_tests.py tests/us04_curricula_trainer/ -n 4
```

### 3. Run a Specific Test Suite
```bash
# E.g. Personal Information suite
python run_tests.py tests/us04_curricula_trainer/test_ts01_personal_info.py
```

### 4. Run Single Test Case (Smoke Test)
```bash
python run_tests.py tests/us04_curricula_trainer/test_ts01_personal_info.py -k "test_tc_pi_001"
```

---

## 📊 Reports & Evidence
- **HTML Report**: `reports/us04_curricula_trainer/execution_report.html`
- **Screenshots**: `reports/us04_curricula_trainer/screenshots/`
- **Video Recordings**: 100% self-contained embedded Base64 WebM videos inside the HTML report.
