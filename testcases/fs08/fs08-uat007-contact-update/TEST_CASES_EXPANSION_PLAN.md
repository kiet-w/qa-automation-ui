# FS08/UAT007 Contact Update - Comprehensive Test Cases Expansion Plan

## Current Status
- **Existing UAT acceptance cases**: 9
- **Automation implemented**: 83 test functions (9 baseline + 64 atomic + 4 resilience/request-contract + 6 UI-health)
- **Execution status**: Not Run (execution is reserved for the user; no Actual Result or evidence is claimed)
- **Required minimum**: 30-45 test cases (Invariant 7 for 7 editable fields)
- **Target comprehensive**: 100+ test cases

## Field Classification & 12-Layer Matrix Application

### 1. Mobile Number (Numeric Field - Group 1)
**12-layer matrix application:**
1. Empty required → MSG-0001
2. All whitespace → MSG-0001  
3. Leading/trailing spaces → Auto trim
4. BVA Min: 7 digits → MSG-0805
5. BVA Max: 9 digits → MSG-0805
6. Invalid prefix (1,2,3,4,5,7) → MSG-0805
7. Valid prefix (6,8,9) → Accept
8. Letters mixed → MSG-0805
9. Special characters → MSG-0805
10. XSS vectors → Safe encoding
11. 1000 chars paste → Maxlength/choke
12. Persistence after save → Verify

**Test cases needed**: 12+ (12-layer matrix)

### 2. Email (Email Format - Group 4)
**12-layer matrix application:**
1. Empty required → MSG-0001
2. All whitespace → MSG-0001
3. Leading/trailing spaces → Auto trim
4. No @ symbol → MSG-0806
5. No domain → MSG-0806
6. No TLD → MSG-0806
7. Double @ → MSG-0806
8. Spaces in email → MSG-0806
9. Valid RFC 5322 → Accept
10. XSS vectors → Safe encoding
11. 151 chars (>150 limit) → Maxlength/reject
12. Persistence after save → Verify

**Test cases needed**: 12+ (12-layer matrix)

### 3. Block (Alphanumeric - Group 3)
**12-layer matrix application:**
1. Empty optional → Accept
2. All whitespace → Auto trim/empty
3. Leading/trailing spaces → Auto trim
4. Numbers only → Accept
5. Letters only → Accept
6. Mixed alphanumeric → Accept
7. Special chars (/, -, #) → Accept
8. Forbidden chars (<, >, ;) → Reject/clean
9. 21 chars (>20 limit) → Maxlength/choke
10. XSS vectors → Safe encoding
11. 1000 chars paste → Maxlength/choke
12. Persistence after save → Verify

**Test cases needed**: 12+ (12-layer matrix)

### 4. Street (Alphanumeric - Group 3)
**12-layer matrix application:**
1. Empty required → MSG-0001
2. All whitespace → MSG-0001
3. Leading/trailing spaces → Auto trim
4. Numbers only → Accept
5. Letters only → Accept
6. Mixed alphanumeric → Accept
7. Special chars (/, -, #, ,, .) → Accept
8. Forbidden chars (<, >, ;) → Reject/clean
9. 101 chars (>100 limit) → Maxlength/choke
10. XSS vectors → Safe encoding
11. 1000 chars paste → Maxlength/choke
12. Persistence after save → Verify

**Test cases needed**: 12+ (12-layer matrix)

### 5. Unit (Alphanumeric - Group 3)
**12-layer matrix application:**
1. Empty optional → Accept
2. All whitespace → Auto trim/empty
3. Leading/trailing spaces → Auto trim
4. Singapore format (#12-34) → Accept
5. Numbers only → Accept
6. Letters only → Accept
7. Mixed alphanumeric → Accept
8. Special chars (/, -, #) → Accept
9. 21 chars (>20 limit) → Maxlength/choke
10. XSS vectors → Safe encoding
11. 1000 chars paste → Maxlength/choke
12. Persistence after save → Verify

**Test cases needed**: 12+ (12-layer matrix)

### 6. Postal Code (Numeric - Group 1)
**12-layer matrix application:**
1. Empty required → MSG-0001
2. All whitespace → MSG-0001
3. Leading/trailing spaces → Auto trim
4. 5 digits → MSG-0001/validation error
5. 6 digits → Accept
6. 7 digits → MSG-0001/validation error
7. Letters mixed → Reject
8. Leading zeros → Preserve
9. Special characters → Reject
10. XSS vectors → Safe encoding
11. 1000 chars paste → Maxlength/choke
12. Persistence after save → Verify

**Test cases needed**: 12+ (12-layer matrix)

### 7. Country (Alpha - Group 2)
**12-layer matrix application:**
1. Empty required → MSG-0001
2. All whitespace → MSG-0001
3. Leading/trailing spaces → Auto trim
4. Letters only → Accept
5. Numbers mixed → Reject
6. Special characters → Reject
7. Accented characters → Accept
8. 101 chars (>100 limit) → Maxlength/choke
9. XSS vectors → Safe encoding
10. 1000 chars paste → Maxlength/choke
11. Dropdown selection (if applicable) → Verify
12. Persistence after save → Verify

**Test cases needed**: 12+ (12-layer matrix)

## Test Suite Organization

### A. Atomic Test Suites (Field-Level)
1. **TS-ATOMIC-001**: Mobile Number Validation (12+ test cases)
2. **TS-ATOMIC-002**: Email Validation (12+ test cases)  
3. **TS-ATOMIC-003**: Block Validation (12+ test cases)
4. **TS-ATOMIC-004**: Street Validation (12+ test cases)
5. **TS-ATOMIC-005**: Unit Validation (12+ test cases)
6. **TS-ATOMIC-006**: Postal Code Validation (12+ test cases)
7. **TS-ATOMIC-007**: Country Validation (12+ test cases)

**Total Atomic**: 84+ test cases

### B. Integration Test Suites (Form-Level)
8. **TS-INTEGRATION-001**: Form State Management
   - Pristine/Dirty transitions
   - Cancel functionality
   - Save enable/disable logic
   
9. **TS-INTEGRATION-002**: Modal Dialog Flow
   - Confirm dialog opening
   - Keep editing vs Save
   - Focus trap in modal
   
10. **TS-INTEGRATION-003**: Error Handling & Resilience
    - Multiple field errors
    - API 500 error handling
    - Network failure scenarios

**Total Integration**: 15+ test cases

### C. Business Rule Test Suites
11. **TS-BUSINESS-001**: SingPass Identity Immutability
    - Full Name read-only
    - NRIC read-only & masking
    - Residential Address read-only
    - Mass assignment protection

12. **TS-BUSINESS-002**: Access Control & Permissions
    - Child age access control (BR-08-01)
    - Independent parent editing (BR-08-02)
    - Zero notification spam (BR-08-04)

**Total Business Rules**: 8+ test cases

### D. UI Health & Accessibility
13. **TS-UIHEALTH-001**: Visual Integrity
    - Zero console errors
    - Zero horizontal scroll
    - CLS = 0 (no layout shift)
    - WCAG 2.1 AA compliance
    
14. **TS-UIHEALTH-002**: Keyboard Navigation
    - Tab navigation
    - Enter/Space key support
    - Skip link functionality

**Total UI Health**: 10+ test cases

### E. UAT Acceptance (Existing)
15. **TS-UAT007-E2E**: Full End-to-End Workflow (9 test cases)

## Total Test Cases Summary
- **Atomic Field Tests**: 84
- **Integration Tests**: 15
- **Business Rules**: 8
- **UI Health**: 10
- **UAT E2E**: 9

**GRAND TOTAL**: 126+ test cases

## Test Data Requirements
Need JSON parameterization for:
1. Valid test data vectors
2. Invalid test data vectors (per field type)
3. Edge cases (BVA, special chars, XSS)
4. Mock API responses (success/error)
5. Persona data (Howard/TAN WEI MING)

## Next Steps
1. Resolve the listed `SPEC GAP` items with named personas, backend contracts and observable notification/DB probes.
2. Synchronize the Markdown and Excel testcase matrices using the repository's 20-column format, including `Steps Test`.
3. Let the user execute the suite with three workers and video disabled.
4. Populate Actual Result, run ID, build/environment and evidence links only from that concrete run.

## Automation Delivery Mapping

| Coverage | TC IDs | Automation source | Status |
| :--- | :--- | :--- | :--- |
| Baseline BR/AC/UAT flow | `TC-UAT007-01`–`09` | `tests/fs08/fs08-uat007-contact-update/test_atomic_contact_fields.py`, `test_integration_contact_update.py` | Implemented / Not Run |
| Mobile 12-layer matrix | `TC-UAT007-10`–`29` | `test_atomic_mobile.py` | Implemented / Not Run |
| Email 12-layer matrix | `TC-UAT007-30`–`46` | `test_atomic_email.py` | Implemented / Not Run |
| Mailing address matrix | `TC-UAT007-47`–`73` | `test_atomic_mailing.py` | Implemented / Not Run |
| Network, double-submit, partial payload, focus trap | `TC-UAT007-74`–`77` | `test_integration_resilience.py` | Implemented / Not Run |
| DOM inventory, console health, responsive overflow, keyboard, i18n, labels | `TC-UAT007-78`–`83` | `test_ui_health.py` | Implemented / Not Run |

Atomic inputs and expected messages are centralized in `data/fs08/uat007_coverage_cases.json`; persona, restore data and UI-health configuration remain in `data/fs08/fs08_data.json`. Each atomic data row maps to one test function and one unique TC ID.

## Explicit SPEC GAP / Partial Coverage

The following expansion-plan items are not counted as automated coverage because the available UAT-007 sources do not provide a complete, independently verifiable oracle or fixture:

- `BR-08-01` child-age access control: requires named personas for all-children-16-or-over and at-least-one-under-16 states.
- `BR-08-02` independent parent editing: requires two linked parent sessions and authoritative backend verification.
- `BR-08-04` zero notification spam: requires an email/event-queue observation point.
- BOLA/IDOR backend rejection: requires an authorized request contract and safe second-parent target identity.
- Full WCAG 2.1 AA and CLS certification: smoke checks are implemented, but certification needs a defined audit tool, thresholds and supported viewport matrix.
- Backend/DB persistence: the E2E case checks reload-visible state; authoritative storage claims need API/DB read-back evidence.

These gaps remain `Blocked/Partial`; they must not be reported as Passed or fully covered until the missing specification and test fixtures are supplied.
