# Acceptance Criteria - US-04 Curricula Trainer Account (68 Test Cases)

This document serves as the authoritative Source of Truth for acceptance criteria and technical specifications for the **Create Trainer Account (Curricula)** feature.
Encompasses all 68 Test Cases across 7 Test Suites (TS-01 to TS-07), structured with the 4 mandatory technical subsections defined in `AGENTS.md`.

---

## TS-01 Personal Information

### TC_PI_001 — Preferred Name - Valid string entry
- **Original Business Requirement (FSD Standard)**: Value accepted without error.
- **Priority & Design Technique**: P1 | EP Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.PREFERRED_NAME` = `"#preferredName"`
  - Action method: `CurriculaTrainerPage.set_preferred_name(name)`
  - Error locator & key: `data-for="preferredName"`, CSS selector `.error[data-for='preferredName']`, helper `get_error_text("preferredName")`, `is_error_visible("preferredName")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Preferred Name = "Bob Wang"` | Value accepted without error. |

  **Expected Result:**
  - Error Field: `preferredName` (attribute `data-for="preferredName"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_002 — Preferred Name - Boundary Max 100 characters
- **Original Business Requirement (FSD Standard)**: All 100 characters accepted successfully.
- **Priority & Design Technique**: P2 | BVA Max

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.PREFERRED_NAME` = `"#preferredName"`
  - Action method: `CurriculaTrainerPage.set_preferred_name(name)`
  - Error locator & key: `data-for="preferredName"`, CSS selector `.error[data-for='preferredName']`, helper `get_error_text("preferredName")`, `is_error_visible("preferredName")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `String of 100 characters ("A"*100)` | All 100 characters accepted successfully. |

  **Expected Result:**
  - Error Field: `preferredName` (attribute `data-for="preferredName"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_003 — Preferred Name - Exceeds 100 chars (BVA Max+1)
- **Original Business Requirement (FSD Standard)**: System does not accept Preferred Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows 101 characters -> BUG-007.]
- **Priority & Design Technique**: P2 | BVA Max+1

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.PREFERRED_NAME` = `"#preferredName"`
  - Action method: `CurriculaTrainerPage.set_preferred_name(name)`
  - Error locator & key: `data-for="preferredName"`, CSS selector `.error[data-for='preferredName']`, helper `get_error_text("preferredName")`, `is_error_visible("preferredName")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `String of 101 characters ("A"*101)` | System does not accept Preferred Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows 101 characters -> BUG-007.] |
  | **[BUG-HUNTING CASE]** | `String of 101 characters ("A"*101)` | Standard discrepancy detected (BUG-007) |

  **Expected Result:**
  - Error Field: `preferredName` (attribute `data-for="preferredName"`)
  - Actual Error Text on UI: `"This field is required."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-007.

  **Exceptor Method:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-007")`

### TC_PI_004 — Preferred Name - Auto-trim whitespace
- **Original Business Requirement (FSD Standard)**: System trims whitespace and stores "Bob Wang".
- **Priority & Design Technique**: P3 | Error Guessing

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.PREFERRED_NAME` = `"#preferredName"`
  - Action method: `CurriculaTrainerPage.set_preferred_name(name)`
  - Error locator & key: `data-for="preferredName"`, CSS selector `.error[data-for='preferredName']`, helper `get_error_text("preferredName")`, `is_error_visible("preferredName")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `"  Bob Wang  "` | System trims whitespace and stores "Bob Wang". |

  **Expected Result:**
  - Error Field: `preferredName` (attribute `data-for="preferredName"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_005 — Gender - Select Male / Female
- **Original Business Requirement (FSD Standard)**: Radio button switches smoothly, single value selected.
- **Priority & Design Technique**: P1 | EP Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.GENDER_MALE / GENDER_FEMALE` = `"input[name='gender']"`
  - Action method: `CurriculaTrainerPage.select_gender(gender)`
  - Error locator & key: `data-for="gender"`, CSS selector `.error[data-for='gender']`, helper `get_error_text("gender")`, `is_error_visible("gender")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Click Radio Male, then Female` | Radio button switches smoothly, single value selected. |

  **Expected Result:**
  - Error Field: `gender` (attribute `data-for="gender"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_006 — ID Type - 4 Document types per FSD 4.1
- **Original Business Requirement (FSD Standard)**: Exactly 4 document types: NRIC, FIN, Employment Pass, Passport. [Mock App Deviation: shows extra "S-Pass" -> BUG-009 / FSD Table 4.1 vs narrative section mismatch; clarification required.]
- **Priority & Design Technique**: P1 | EP Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.ID_TYPE` = `"#idType"`
  - Action method: `CurriculaTrainerPage.select_id_type(id_type)`
  - Error locator & key: `data-for="idType"`, CSS selector `.error[data-for='idType']`, helper `get_error_text("idType")`, `is_error_visible("idType")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Open ID Type dropdown` | Exactly 4 document types: NRIC, FIN, Employment Pass, Passport. [Mock App Deviation: shows extra "S-Pass" -> BUG-009 / FSD Table 4.1 vs narrative section mismatch; clarification required.] |
  | **[BUG-HUNTING CASE]** | `Open ID Type dropdown` | Standard discrepancy detected (BUG-009 / CQ-08) |

  **Expected Result:**
  - Error Field: `idType` (attribute `data-for="idType"`)
  - Actual Error Text on UI: `"This field is required."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-009 / CQ-08.

  **Exceptor Method:**
  - `Exceptor.expect_bug_if_rejected(curricula.get_state_snapshot(), field="idType", context="BUG-009 / CQ-08")`

### TC_PI_007 — ID Number - Valid NRIC format
- **Original Business Requirement (FSD Standard)**: Value accepted and stored accurately.
- **Priority & Design Technique**: P1 | EP Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.ID_NUMBER` = `"#idNumber"`
  - Action method: `CurriculaTrainerPage.set_id_number(id_number)`
  - Error locator & key: `data-for="idNumber"`, CSS selector `.error[data-for='idNumber']`, helper `get_error_text("idNumber")`, `is_error_visible("idNumber")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `ID Type = "NRIC", ID Number = "G7666564N"` | Value accepted and stored accurately. |

  **Expected Result:**
  - Error Field: `idNumber` (attribute `data-for="idNumber"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_008 — ID Number - ID Checksum validation
- **Original Business Requirement (FSD Standard)**: System validates ID Checksum per FSD Section 5d and blocks save. (FSD checksum requirement; test data provisional pending BA/PO confirmation; Mock App does not implement any checksum logic -> BUG-010).
- **Priority & Design Technique**: P1 | EP Invalid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.ID_NUMBER` = `"#idNumber"`
  - Action method: `CurriculaTrainerPage.set_id_number(id_number)`
  - Error locator & key: `data-for="idNumber"`, CSS selector `.error[data-for='idNumber']`, helper `get_error_text("idNumber")`, `is_error_visible("idNumber")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `ID Type = "NRIC", ID Number = "S1234567A"` | System validates ID Checksum per FSD Section 5d and blocks save. (FSD checksum requirement; test data provisional pending BA/PO confirmation; Mock App does not implement any checksum logic -> BUG-010). |
  | **[BUG-HUNTING CASE]** | `ID Type = "NRIC", ID Number = "S1234567A"` | Standard discrepancy detected (BUG-010) |

  **Expected Result:**
  - Error Field: `idNumber` (attribute `data-for="idNumber"`)
  - Actual Error Text on UI: `"This field is required."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-010.

  **Exceptor Method:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-010")`

### TC_PI_009 — ID Number - Exceeds 20 chars (BVA Max+1)
- **Original Business Requirement (FSD Standard)**: System does not accept ID Number exceeding 20 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 20 characters -> BUG-007.]
- **Priority & Design Technique**: P2 | BVA Max+1

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.ID_NUMBER` = `"#idNumber"`
  - Action method: `CurriculaTrainerPage.set_id_number(id_number)`
  - Error locator & key: `data-for="idNumber"`, CSS selector `.error[data-for='idNumber']`, helper `get_error_text("idNumber")`, `is_error_visible("idNumber")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `String of 21 characters ("A"*21)` | System does not accept ID Number exceeding 20 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 20 characters -> BUG-007.] |
  | **[BUG-HUNTING CASE]** | `String of 21 characters ("A"*21)` | Standard discrepancy detected (BUG-007) |

  **Expected Result:**
  - Error Field: `idNumber` (attribute `data-for="idNumber"`)
  - Actual Error Text on UI: `"This field is required."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-007.

  **Exceptor Method:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-007")`

### TC_PI_010 — Date of Birth - Valid past date
- **Original Business Requirement (FSD Standard)**: System accepts date successfully.
- **Priority & Design Technique**: P1 | EP Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.DOB` = `"#dob"`
  - Action method: `CurriculaTrainerPage.set_dob(dob_str)`
  - Error locator & key: `data-for="dob"`, CSS selector `.error[data-for='dob']`, helper `get_error_text("dob")`, `is_error_visible("dob")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `DOB = "1990-05-15"` | System accepts date successfully. |

  **Expected Result:**
  - Error Field: `dob` (attribute `data-for="dob"`)
  - Actual Error Text on UI: `"Enter a valid date of birth."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_011 — Date of Birth - Future date rejection
- **Original Business Requirement (FSD Standard)**: System rejects future date of birth, displays inline validation at Date of Birth field, and does not create Trainer Account. Specific error message is TBD pending BA/PO confirmation.
- **Priority & Design Technique**: P1 | EP / BVA

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.DOB` = `"#dob"`
  - Action method: `CurriculaTrainerPage.set_dob(dob_str)`
  - Error locator & key: `data-for="dob"`, CSS selector `.error[data-for='dob']`, helper `get_error_text("dob")`, `is_error_visible("dob")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `DOB = "2030-01-01"` | System rejects future date of birth, displays inline validation at Date of Birth field, and does not create Trainer Account. Specific error message is TBD pending BA/PO confirmation. |

  **Expected Result:**
  - Error Field: `dob` (attribute `data-for="dob"`)
  - Actual Error Text on UI: `"Enter a valid date of birth."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="dob", message_contains="Enter a valid date of birth.")`

### TC_PI_012 — File Upload - PDF/PNG/JPG/JPEG <= 10MB
- **Original Business Requirement (FSD Standard)**: File uploaded successfully, file name displayed.
- **Priority & Design Technique**: P1 | EP / BVA

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.ID_DOCUMENT` = `"#idDocument"`
  - Action method: `CurriculaTrainerPage.upload_document(file_path)`
  - Error locator & key: `data-for="idDocument"`, CSS selector `.error[data-for='idDocument']`, helper `get_error_text("idDocument")`, `is_error_visible("idDocument")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `PDF file of 5MB` | File uploaded successfully, file name displayed. |

  **Expected Result:**
  - Error Field: `idDocument` (attribute `data-for="idDocument"`)
  - Actual Error Text on UI: `"Please upload a valid document."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_013 — File Upload - Exceeds 10MB limit
- **Original Business Requirement (FSD Standard)**: System rejects file and displays: "File size must not exceed 10 MB."
- **Priority & Design Technique**: P1 | BVA Max+1

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.ID_DOCUMENT` = `"#idDocument"`
  - Action method: `CurriculaTrainerPage.upload_document(file_path)`
  - Error locator & key: `data-for="idDocument"`, CSS selector `.error[data-for='idDocument']`, helper `get_error_text("idDocument")`, `is_error_visible("idDocument")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `PDF file of 11MB` | System rejects file and displays: "File size must not exceed 10 MB." |

  **Expected Result:**
  - Error Field: `idDocument` (attribute `data-for="idDocument"`)
  - Actual Error Text on UI: `"Please upload a valid document."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="idDocument", message_contains="Please upload a valid document.")`

### TC_PI_014 — File Upload - Invalid file format (.docx)
- **Original Business Requirement (FSD Standard)**: System rejects file and displays: "Unsupported file format."
- **Priority & Design Technique**: P1 | EP Invalid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.ID_DOCUMENT` = `"#idDocument"`
  - Action method: `CurriculaTrainerPage.upload_document(file_path)`
  - Error locator & key: `data-for="idDocument"`, CSS selector `.error[data-for='idDocument']`, helper `get_error_text("idDocument")`, `is_error_visible("idDocument")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `File document.docx (500KB)` | System rejects file and displays: "Unsupported file format." |
  | **[BUG-HUNTING CASE]** | `File document.docx (500KB)` | Standard discrepancy detected (BUG-008) |

  **Expected Result:**
  - Error Field: `idDocument` (attribute `data-for="idDocument"`)
  - Actual Error Text on UI: `"Please upload a valid document."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-008.

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="idDocument", message_contains="Please upload a valid document.")`

### TC_PI_015 — Nationality - Select from Dropdown
- **Original Business Requirement (FSD Standard)**: Dropdown correctly registers selected value.
- **Priority & Design Technique**: P1 | EP Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.NATIONALITY` = `"#nationality"`
  - Action method: `CurriculaTrainerPage.select_nationality(nationality)`
  - Error locator & key: `data-for="nationality"`, CSS selector `.error[data-for='nationality']`, helper `get_error_text("nationality")`, `is_error_visible("nationality")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Select Singaporean` | Dropdown correctly registers selected value. |

  **Expected Result:**
  - Error Field: `nationality` (attribute `data-for="nationality"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_016 — Country of Birth - Select from Dropdown
- **Original Business Requirement (FSD Standard)**: Dropdown correctly registers selected value.
- **Priority & Design Technique**: P1 | EP Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.BIRTH_COUNTRY` = `"#birthCountry"`
  - Action method: `CurriculaTrainerPage.select_birth_country(country)`
  - Error locator & key: `data-for="birthCountry"`, CSS selector `.error[data-for='birthCountry']`, helper `get_error_text("birthCountry")`, `is_error_visible("birthCountry")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Select Singapore` | Dropdown correctly registers selected value. |

  **Expected Result:**
  - Error Field: `birthCountry` (attribute `data-for="birthCountry"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_017 — Preferred Name - Empty mandatory check
- **Original Business Requirement (FSD Standard)**: Displays inline error: "This field is required."
- **Priority & Design Technique**: P1 | EP Negative

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.PREFERRED_NAME` = `"#preferredName"`
  - Action method: `CurriculaTrainerPage.set_preferred_name('')`
  - Error locator & key: `data-for="preferredName"`, CSS selector `.error[data-for='preferredName']`, helper `get_error_text("preferredName")`, `is_error_visible("preferredName")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Preferred Name = ""` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Error Field: `preferredName` (attribute `data-for="preferredName"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="preferredName", message_contains="This field is required.")`

### TC_PI_018 — ID Number - Empty mandatory check
- **Original Business Requirement (FSD Standard)**: Displays inline error: "This field is required."
- **Priority & Design Technique**: P1 | EP Negative

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.ID_NUMBER` = `"#idNumber"`
  - Action method: `CurriculaTrainerPage.set_id_number('')`
  - Error locator & key: `data-for="idNumber"`, CSS selector `.error[data-for='idNumber']`, helper `get_error_text("idNumber")`, `is_error_visible("idNumber")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `ID Number = ""` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Error Field: `idNumber` (attribute `data-for="idNumber"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="idNumber", message_contains="This field is required.")`

### TC_PI_019 — Date of Birth - Empty mandatory check
- **Original Business Requirement (FSD Standard)**: Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid date of birth." -> BUG-008.]
- **Priority & Design Technique**: P1 | EP Negative

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.DOB` = `"#dob"`
  - Action method: `CurriculaTrainerPage.set_dob('')`
  - Error locator & key: `data-for="dob"`, CSS selector `.error[data-for='dob']`, helper `get_error_text("dob")`, `is_error_visible("dob")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `DOB = ""` | Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid date of birth." -> BUG-008.] |
  | **[BUG-HUNTING CASE]** | `DOB = ""` | Standard discrepancy detected (BUG-008) |

  **Expected Result:**
  - Error Field: `dob` (attribute `data-for="dob"`)
  - Actual Error Text on UI: `"Enter a valid date of birth."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-008.

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="dob", message_contains="Enter a valid date of birth.")`

### TC_PI_020 — Nationality - Unselected mandatory check
- **Original Business Requirement (FSD Standard)**: Displays inline error: "This field is required."
- **Priority & Design Technique**: P1 | EP Negative

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.NATIONALITY` = `"#nationality"`
  - Action method: `CurriculaTrainerPage.select_nationality('')`
  - Error locator & key: `data-for="nationality"`, CSS selector `.error[data-for='nationality']`, helper `get_error_text("nationality")`, `is_error_visible("nationality")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `No selection made` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Error Field: `nationality` (attribute `data-for="nationality"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="nationality", message_contains="This field is required.")`

### TC_PI_021 — Country of Birth - Unselected mandatory check
- **Original Business Requirement (FSD Standard)**: Displays inline error: "This field is required."
- **Priority & Design Technique**: P1 | EP Negative

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.BIRTH_COUNTRY` = `"#birthCountry"`
  - Action method: `CurriculaTrainerPage.select_birth_country('')`
  - Error locator & key: `data-for="birthCountry"`, CSS selector `.error[data-for='birthCountry']`, helper `get_error_text("birthCountry")`, `is_error_visible("birthCountry")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `No selection made` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Error Field: `birthCountry` (attribute `data-for="birthCountry"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="birthCountry", message_contains="This field is required.")`

### TC_PI_022 — Gender, Race & Tax Resident - Unselected check
- **Original Business Requirement (FSD Standard)**: Displays "This field is required." error for all 3 fields.
- **Priority & Design Technique**: P1 | EP Negative

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.GENDER / RACE / TAX_RESIDENT` = `"gender, #race, taxResident"`
  - Action method: `CurriculaTrainerPage.leave unselected`
  - Error locator & key: `data-for="gender / race / taxResident"`, CSS selector `.error[data-for='gender / race / taxResident']`, helper `get_error_text("gender / race / taxResident")`, `is_error_visible("gender / race / taxResident")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Leave all 3 unselected` | Displays "This field is required." error for all 3 fields. |

  **Expected Result:**
  - Error Field: `gender / race / taxResident` (attribute `data-for="gender / race / taxResident"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="gender / race / taxResident", message_contains="This field is required.")`

### TC_PI_023 — Race Dropdown - Ethnic groups options (CQ-07)
- **Original Business Requirement (FSD Standard)**: Displays 4 standard groups: Chinese, Malay, Indian, Others.
- **Priority & Design Technique**: P2 | EP Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.RACE` = `"#race"`
  - Action method: `CurriculaTrainerPage.select_race(race)`
  - Error locator & key: `data-for="race"`, CSS selector `.error[data-for='race']`, helper `get_error_text("race")`, `is_error_visible("race")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Open Race dropdown` | Displays 4 standard groups: Chinese, Malay, Indian, Others. |
  | **[BUG-HUNTING CASE]** | `Open Race dropdown` | Standard discrepancy detected (CQ-07) |

  **Expected Result:**
  - Error Field: `race` (attribute `data-for="race"`)
  - Actual Error Text on UI: `"This field is required."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under CQ-07.

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`


## TS-02 Contact Information

### TC_CI_001 — Primary Email - Valid email format
- **Original Business Requirement (FSD Standard)**: Email accepted without error.
- **Priority & Design Technique**: P1 | EP Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_EMAIL` = `"#primaryEmail"`
  - Action method: `CurriculaTrainerPage.set_primary_email(email)`
  - Error locator & key: `data-for="primaryEmail"`, CSS selector `.error[data-for='primaryEmail']`, helper `get_error_text("primaryEmail")`, `is_error_visible("primaryEmail")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Primary Email = "trainer.bob@curricula.edu.sg"` | Email accepted without error. |

  **Expected Result:**
  - Error Field: `primaryEmail` (attribute `data-for="primaryEmail"`)
  - Actual Error Text on UI: `"Enter a valid email address."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_CI_002 — Primary Email - Invalid format rejection
- **Original Business Requirement (FSD Standard)**: Displays inline error: "Enter a valid email address."
- **Priority & Design Technique**: P1 | EP Invalid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_EMAIL` = `"#primaryEmail"`
  - Action method: `CurriculaTrainerPage.set_primary_email(email)`
  - Error locator & key: `data-for="primaryEmail"`, CSS selector `.error[data-for='primaryEmail']`, helper `get_error_text("primaryEmail")`, `is_error_visible("primaryEmail")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `"plainaddress", "@missinguser.com"` | Displays inline error: "Enter a valid email address." |

  **Expected Result:**
  - Error Field: `primaryEmail` (attribute `data-for="primaryEmail"`)
  - Actual Error Text on UI: `"Enter a valid email address."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="primaryEmail", message_contains="Enter a valid email address.")`

### TC_CI_003 — Primary Email - Boundary Max 100 characters
- **Original Business Requirement (FSD Standard)**: 100-character email accepted successfully.
- **Priority & Design Technique**: P2 | BVA Max

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_EMAIL` = `"#primaryEmail"`
  - Action method: `CurriculaTrainerPage.set_primary_email(email)`
  - Error locator & key: `data-for="primaryEmail"`, CSS selector `.error[data-for='primaryEmail']`, helper `get_error_text("primaryEmail")`, `is_error_visible("primaryEmail")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Valid email of exactly 100 chars` | 100-character email accepted successfully. |

  **Expected Result:**
  - Error Field: `primaryEmail` (attribute `data-for="primaryEmail"`)
  - Actual Error Text on UI: `"Enter a valid email address."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_CI_004 — Primary Phone - Valid Singapore 8 digits (+65)
- **Original Business Requirement (FSD Standard)**: Phone number accepted without error.
- **Priority & Design Technique**: P1 | BVA Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_PHONE` = `"#primaryPhone"`
  - Action method: `CurriculaTrainerPage.set_primary_phone(code, phone)`
  - Error locator & key: `data-for="primaryPhone"`, CSS selector `.error[data-for='primaryPhone']`, helper `get_error_text("primaryPhone")`, `is_error_visible("primaryPhone")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Code = "+65", Number = "91234567"` | Phone number accepted without error. |

  **Expected Result:**
  - Error Field: `primaryPhone` (attribute `data-for="primaryPhone"`)
  - Actual Error Text on UI: `"Enter a valid contact number."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_CI_005 — Primary Phone - 7 digits rejection (BVA Min-1)
- **Original Business Requirement (FSD Standard)**: System rejects 7-digit phone number, displays inline validation, and does not create Trainer Account.
- **Priority & Design Technique**: P2 | BVA Min-1

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_PHONE` = `"#primaryPhone"`
  - Action method: `CurriculaTrainerPage.set_primary_phone(code, phone)`
  - Error locator & key: `data-for="primaryPhone"`, CSS selector `.error[data-for='primaryPhone']`, helper `get_error_text("primaryPhone")`, `is_error_visible("primaryPhone")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Code = "+65", Number = "9123456"` | System rejects 7-digit phone number, displays inline validation, and does not create Trainer Account. |

  **Expected Result:**
  - Error Field: `primaryPhone` (attribute `data-for="primaryPhone"`)
  - Actual Error Text on UI: `"Enter a valid contact number."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="primaryPhone", message_contains="Enter a valid contact number.")`

### TC_CI_006 — Primary Phone - 9 digits with code +65
- **Original Business Requirement (FSD Standard)**: Under general FSD rule of 8–15 digits, 9-digit number is accepted. (Mock App rejects when country code is +65 -> Fail / Requirement inconsistency tracked under CQ-09).
- **Priority & Design Technique**: P2 | BVA / Observed

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_PHONE` = `"#primaryPhone"`
  - Action method: `CurriculaTrainerPage.set_primary_phone(code, phone)`
  - Error locator & key: `data-for="primaryPhone"`, CSS selector `.error[data-for='primaryPhone']`, helper `get_error_text("primaryPhone")`, `is_error_visible("primaryPhone")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Code = "+65", Number = "912345678"` | Under general FSD rule of 8–15 digits, 9-digit number is accepted. (Mock App rejects when country code is +65 -> Fail / Requirement inconsistency tracked under CQ-09). |
  | **[BUG-HUNTING CASE]** | `Code = "+65", Number = "912345678"` | Standard discrepancy detected (CQ-09) |

  **Expected Result:**
  - Error Field: `primaryPhone` (attribute `data-for="primaryPhone"`)
  - Actual Error Text on UI: `"Enter a valid contact number."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under CQ-09.

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="primaryPhone", message_contains="Enter a valid contact number.")`

### TC_CI_007 — Phone Numbers - Reject alphabetic characters
- **Original Business Requirement (FSD Standard)**: System prevents non-digit input or displays format error.
- **Priority & Design Technique**: P2 | EP Invalid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_PHONE` = `"#primaryPhone"`
  - Action method: `CurriculaTrainerPage.set_primary_phone(code, phone)`
  - Error locator & key: `data-for="primaryPhone"`, CSS selector `.error[data-for='primaryPhone']`, helper `get_error_text("primaryPhone")`, `is_error_visible("primaryPhone")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Number = "9123ABCD"` | System prevents non-digit input or displays format error. |

  **Expected Result:**
  - Error Field: `primaryPhone` (attribute `data-for="primaryPhone"`)
  - Actual Error Text on UI: `"Enter a valid contact number."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="primaryPhone", message_contains="Enter a valid contact number.")`

### TC_CI_008 — Primary Email - Empty mandatory check
- **Original Business Requirement (FSD Standard)**: Displays inline error: "This field is required."
- **Priority & Design Technique**: P1 | EP Negative

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_EMAIL` = `"#primaryEmail"`
  - Action method: `CurriculaTrainerPage.set_primary_email('')`
  - Error locator & key: `data-for="primaryEmail"`, CSS selector `.error[data-for='primaryEmail']`, helper `get_error_text("primaryEmail")`, `is_error_visible("primaryEmail")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Primary Email = ""` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Error Field: `primaryEmail` (attribute `data-for="primaryEmail"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="primaryEmail", message_contains="This field is required.")`

### TC_CI_009 — Primary Phone - Empty mandatory check
- **Original Business Requirement (FSD Standard)**: Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid contact number." -> BUG-008.]
- **Priority & Design Technique**: P1 | EP Negative

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_PHONE` = `"#primaryPhone"`
  - Action method: `CurriculaTrainerPage.set_primary_phone('+65', '')`
  - Error locator & key: `data-for="primaryPhone"`, CSS selector `.error[data-for='primaryPhone']`, helper `get_error_text("primaryPhone")`, `is_error_visible("primaryPhone")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Primary Phone = ""` | Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid contact number." -> BUG-008.] |
  | **[BUG-HUNTING CASE]** | `Primary Phone = ""` | Standard discrepancy detected (BUG-008) |

  **Expected Result:**
  - Error Field: `primaryPhone` (attribute `data-for="primaryPhone"`)
  - Actual Error Text on UI: `"Enter a valid contact number."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-008.

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="primaryPhone", message_contains="Enter a valid contact number.")`


## TS-03 Emergency Contact

### TC_EC_001 — Emergency Contact - Valid complete data
- **Original Business Requirement (FSD Standard)**: Emergency contact information recorded successfully.
- **Priority & Design Technique**: P1 | EP Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.EMERGENCY_NAME / EMERGENCY_PHONE` = `"#emergencyName, #emergencyPhone"`
  - Action method: `CurriculaTrainerPage.set_emergency_contact(...)`
  - Error locator & key: `data-for="emergencyName"`, CSS selector `.error[data-for='emergencyName']`, helper `get_error_text("emergencyName")`, `is_error_visible("emergencyName")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Name: "David Wang", Relationship: "Parent", Number: "98765432"` | Emergency contact information recorded successfully. |

  **Expected Result:**
  - Error Field: `emergencyName` (attribute `data-for="emergencyName"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_EC_002 — Emergency Name - Exceeds 100 chars (BVA Max+1)
- **Original Business Requirement (FSD Standard)**: System does not accept Emergency Contact Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 100 characters -> BUG-007.]
- **Priority & Design Technique**: P2 | BVA Max+1

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.EMERGENCY_NAME` = `"#emergencyName"`
  - Action method: `CurriculaTrainerPage.set_emergency_contact(...)`
  - Error locator & key: `data-for="emergencyName"`, CSS selector `.error[data-for='emergencyName']`, helper `get_error_text("emergencyName")`, `is_error_visible("emergencyName")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `String of 101 characters ("A"*101)` | System does not accept Emergency Contact Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 100 characters -> BUG-007.] |
  | **[BUG-HUNTING CASE]** | `String of 101 characters ("A"*101)` | Standard discrepancy detected (BUG-007) |

  **Expected Result:**
  - Error Field: `emergencyName` (attribute `data-for="emergencyName"`)
  - Actual Error Text on UI: `"This field is required."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-007.

  **Exceptor Method:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-007")`

### TC_EC_003 — Emergency Relationship - Enum per FSD 4.3
- **Original Business Requirement (FSD Standard)**: Displays exact FSD Table 4.3 enum: Parent, Spouse, Sibling, Relative, Friend, Others. [Mock App Deviation: shows Father, Mother -> BUG-005.]
- **Priority & Design Technique**: P2 | EP Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.EMERGENCY_RELATIONSHIP` = `"#emergencyRelationship"`
  - Action method: `CurriculaTrainerPage.select relationship`
  - Error locator & key: `data-for="emergencyRelationship"`, CSS selector `.error[data-for='emergencyRelationship']`, helper `get_error_text("emergencyRelationship")`, `is_error_visible("emergencyRelationship")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Open Relationship dropdown` | Displays exact FSD Table 4.3 enum: Parent, Spouse, Sibling, Relative, Friend, Others. [Mock App Deviation: shows Father, Mother -> BUG-005.] |
  | **[BUG-HUNTING CASE]** | `Open Relationship dropdown` | Standard discrepancy detected (BUG-005) |

  **Expected Result:**
  - Error Field: `emergencyRelationship` (attribute `data-for="emergencyRelationship"`)
  - Actual Error Text on UI: `"This field is required."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-005.

  **Exceptor Method:**
  - `Exceptor.expect_bug_if_rejected(curricula.get_state_snapshot(), field="emergencyRelationship", context="BUG-005")`

### TC_EC_004 — Emergency Name - Empty mandatory check
- **Original Business Requirement (FSD Standard)**: Displays inline error: "This field is required."
- **Priority & Design Technique**: P1 | EP Negative

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.EMERGENCY_NAME` = `"#emergencyName"`
  - Action method: `CurriculaTrainerPage.set_emergency_contact('', ...)`
  - Error locator & key: `data-for="emergencyName"`, CSS selector `.error[data-for='emergencyName']`, helper `get_error_text("emergencyName")`, `is_error_visible("emergencyName")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Emergency Name = ""` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Error Field: `emergencyName` (attribute `data-for="emergencyName"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="emergencyName", message_contains="This field is required.")`

### TC_EC_005 — Emergency Number - Empty mandatory check
- **Original Business Requirement (FSD Standard)**: Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid contact number." -> BUG-008.]
- **Priority & Design Technique**: P1 | EP Negative

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.EMERGENCY_PHONE` = `"#emergencyPhone"`
  - Action method: `CurriculaTrainerPage.set_emergency_contact(..., '')`
  - Error locator & key: `data-for="emergencyPhone"`, CSS selector `.error[data-for='emergencyPhone']`, helper `get_error_text("emergencyPhone")`, `is_error_visible("emergencyPhone")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Emergency Number = ""` | Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid contact number." -> BUG-008.] |
  | **[BUG-HUNTING CASE]** | `Emergency Number = ""` | Standard discrepancy detected (BUG-008) |

  **Expected Result:**
  - Error Field: `emergencyPhone` (attribute `data-for="emergencyPhone"`)
  - Actual Error Text on UI: `"Enter a valid contact number."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-008.

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="emergencyPhone", message_contains="Enter a valid contact number.")`

### TC_EC_006 — Emergency Number - Length 8-15 digits
- **Original Business Requirement (FSD Standard)**: Validated and saved successfully.
- **Priority & Design Technique**: P2 | BVA Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.EMERGENCY_PHONE` = `"#emergencyPhone"`
  - Action method: `CurriculaTrainerPage.set_emergency_contact(...)`
  - Error locator & key: `data-for="emergencyPhone"`, CSS selector `.error[data-for='emergencyPhone']`, helper `get_error_text("emergencyPhone")`, `is_error_visible("emergencyPhone")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Code = "+65", Number = "98765432"` | Validated and saved successfully. |

  **Expected Result:**
  - Error Field: `emergencyPhone` (attribute `data-for="emergencyPhone"`)
  - Actual Error Text on UI: `"Enter a valid contact number."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`


## TS-04 Singapore Residential Address

### TC_SG_001 — Singapore Address - Default selection
- **Original Business Requirement (FSD Standard)**: Singapore radio selected by default; Country/Region automatically set to Singapore and disabled.
- **Priority & Design Technique**: P1 | Decision Table

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.RESIDENTIAL_TYPE_SG` = `"input[value='Singapore']"`
  - Action method: `CurriculaTrainerPage.set_residential_type('Singapore')`
  - Error locator & key: `data-for="residentialType"`, CSS selector `.error[data-for='residentialType']`, helper `get_error_text("residentialType")`, `is_error_visible("residentialType")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Open Create Trainer page` | Singapore radio selected by default; Country/Region automatically set to Singapore and disabled. |

  **Expected Result:**
  - Error Field: `residentialType` (attribute `data-for="residentialType"`)
  - Actual Error Text on UI: `"N/A"`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_SG_002 — Postal Code 6 digits - Auto-fill (569933)
- **Original Business Requirement (FSD Standard)**: Auto-populates Block: "10" and Street: "Ang Mo Kio Avenue 5".
- **Priority & Design Technique**: P1 | EP / BVA

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.POSTAL_CODE / BLOCK_NUMBER / STREET_NAME` = `"#postalCode"`
  - Action method: `CurriculaTrainerPage.set_postal_code('569933')`
  - Error locator & key: `data-for="postalCode"`, CSS selector `.error[data-for='postalCode']`, helper `get_error_text("postalCode")`, `is_error_visible("postalCode")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Postal Code = "569933"` | Auto-populates Block: "10" and Street: "Ang Mo Kio Avenue 5". |

  **Expected Result:**
  - Error Field: `postalCode` (attribute `data-for="postalCode"`)
  - Actual Error Text on UI: `"Enter a valid postal code."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_SG_003 — Postal Code - Malformed 5 digits rejection
- **Original Business Requirement (FSD Standard)**: System rejects postal code without exactly 6 digits, displays inline validation, and does not create Trainer Account.
- **Priority & Design Technique**: P1 | BVA / EP

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.POSTAL_CODE` = `"#postalCode"`
  - Action method: `CurriculaTrainerPage.set_postal_code('12345')`
  - Error locator & key: `data-for="postalCode"`, CSS selector `.error[data-for='postalCode']`, helper `get_error_text("postalCode")`, `is_error_visible("postalCode")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Postal Code = "12345"` | System rejects postal code without exactly 6 digits, displays inline validation, and does not create Trainer Account. |

  **Expected Result:**
  - Error Field: `postalCode` (attribute `data-for="postalCode"`)
  - Actual Error Text on UI: `"Enter a valid postal code."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="postalCode", message_contains="Enter a valid postal code.")`

### TC_SG_004 — Floor/Unit N/A - Checking disables inputs
- **Original Business Requirement (FSD Standard)**: Floor and Unit disabled and no longer mandatory per FSD. Pre-existing values retained under Working Assumption CQ-04, pending BA/PO confirmation.
- **Priority & Design Technique**: P1 | Decision Table

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.FLOOR_NOT_APPLICABLE` = `"#floorNotApplicable"`
  - Action method: `CurriculaTrainerPage.set_floor_not_applicable(True)`
  - Error locator & key: `data-for="floorUnit"`, CSS selector `.error[data-for='floorUnit']`, helper `get_error_text("floorUnit")`, `is_error_visible("floorUnit")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Check Floor/Unit number is not applicable` | Floor and Unit disabled and no longer mandatory per FSD. Pre-existing values retained under Working Assumption CQ-04, pending BA/PO confirmation. |
  | **[BUG-HUNTING CASE]** | `Check Floor/Unit number is not applicable` | Standard discrepancy detected (CQ-04) |

  **Expected Result:**
  - Error Field: `floorUnit` (attribute `data-for="floorUnit"`)
  - Actual Error Text on UI: `"Floor and unit number are required."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under CQ-04.

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_SG_005 — Floor/Unit N/A - Unchecking restores required
- **Original Business Requirement (FSD Standard)**: Floor and Unit inputs enabled and marked mandatory.
- **Priority & Design Technique**: P1 | Decision Table

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.FLOOR_NOT_APPLICABLE` = `"#floorNotApplicable"`
  - Action method: `CurriculaTrainerPage.set_floor_not_applicable(False)`
  - Error locator & key: `data-for="floorUnit"`, CSS selector `.error[data-for='floorUnit']`, helper `get_error_text("floorUnit")`, `is_error_visible("floorUnit")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Uncheck N/A checkbox` | Floor and Unit inputs enabled and marked mandatory. |

  **Expected Result:**
  - Error Field: `floorUnit` (attribute `data-for="floorUnit"`)
  - Actual Error Text on UI: `"Floor and unit number are required."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_SG_006 — Postal Code Fallback - Manual Block & Street
- **Original Business Requirement (FSD Standard)**: Block and Street remain editable under Working Assumption CQ-03. Expected behavior on lookup failure pending BA/PO confirmation.
- **Priority & Design Technique**: P2 | Error Guessing

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.POSTAL_CODE / BLOCK_NUMBER / STREET_NAME` = `"#postalCode"`
  - Action method: `CurriculaTrainerPage.set_postal_code('999999')`
  - Error locator & key: `data-for="postalCode"`, CSS selector `.error[data-for='postalCode']`, helper `get_error_text("postalCode")`, `is_error_visible("postalCode")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Postal = "999999", Block: "888", Street: "Custom St"` | Block and Street remain editable under Working Assumption CQ-03. Expected behavior on lookup failure pending BA/PO confirmation. |
  | **[BUG-HUNTING CASE]** | `Postal = "999999", Block: "888", Street: "Custom St"` | Standard discrepancy detected (CQ-03) |

  **Expected Result:**
  - Error Field: `postalCode` (attribute `data-for="postalCode"`)
  - Actual Error Text on UI: `"Enter a valid postal code."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under CQ-03.

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_SG_007 — Block Number - Max 10 chars (FSD 4.4.1)
- **Original Business Requirement (FSD Standard)**: System accepts Block Number up to 10 characters per FSD Section 4.4.1. [Mock App Deviation: only allows 9 characters -> BUG-007.]
- **Priority & Design Technique**: P2 | BVA Max

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.BLOCK_NUMBER` = `"#blockNumber"`
  - Action method: `CurriculaTrainerPage.type_field(BLOCK_NUMBER, ...)`
  - Error locator & key: `data-for="blockNumber"`, CSS selector `.error[data-for='blockNumber']`, helper `get_error_text("blockNumber")`, `is_error_visible("blockNumber")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `String of 10 characters ("1234567890")` | System accepts Block Number up to 10 characters per FSD Section 4.4.1. [Mock App Deviation: only allows 9 characters -> BUG-007.] |
  | **[BUG-HUNTING CASE]** | `String of 10 characters ("1234567890")` | Standard discrepancy detected (BUG-007) |

  **Expected Result:**
  - Error Field: `blockNumber` (attribute `data-for="blockNumber"`)
  - Actual Error Text on UI: `"N/A"`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-007.

  **Exceptor Method:**
  - `Exceptor.expect_bug_if_rejected(curricula.get_state_snapshot(), field="blockNumber", context="BUG-007")`

### TC_SG_008 — Street Name - Exceeds 100 chars (BVA Max+1)
- **Original Business Requirement (FSD Standard)**: System does not accept Street Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 100 characters -> BUG-007.]
- **Priority & Design Technique**: P2 | BVA Max+1

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.STREET_NAME` = `"#streetName"`
  - Action method: `CurriculaTrainerPage.type_field(STREET_NAME, ...)`
  - Error locator & key: `data-for="streetName"`, CSS selector `.error[data-for='streetName']`, helper `get_error_text("streetName")`, `is_error_visible("streetName")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `String of 101 characters ("A"*101)` | System does not accept Street Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 100 characters -> BUG-007.] |
  | **[BUG-HUNTING CASE]** | `String of 101 characters ("A"*101)` | Standard discrepancy detected (BUG-007) |

  **Expected Result:**
  - Error Field: `streetName` (attribute `data-for="streetName"`)
  - Actual Error Text on UI: `"N/A"`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-007.

  **Exceptor Method:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-007")`

### TC_SG_009 — Building Name - Optional field check
- **Original Business Requirement (FSD Standard)**: Address saved successfully without error.
- **Priority & Design Technique**: P3 | EP Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.BUILDING_NAME` = `"#buildingName"`
  - Action method: `CurriculaTrainerPage.type_field(BUILDING_NAME, '')`
  - Error locator & key: `data-for="buildingName"`, CSS selector `.error[data-for='buildingName']`, helper `get_error_text("buildingName")`, `is_error_visible("buildingName")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Building Name = ""` | Address saved successfully without error. |

  **Expected Result:**
  - Error Field: `buildingName` (attribute `data-for="buildingName"`)
  - Actual Error Text on UI: `"N/A"`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_SG_010 — Singapore Address - Empty Postal Code
- **Original Business Requirement (FSD Standard)**: Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid postal code." -> BUG-008.]
- **Priority & Design Technique**: P1 | EP Negative

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.POSTAL_CODE` = `"#postalCode"`
  - Action method: `CurriculaTrainerPage.set_postal_code('')`
  - Error locator & key: `data-for="postalCode"`, CSS selector `.error[data-for='postalCode']`, helper `get_error_text("postalCode")`, `is_error_visible("postalCode")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Postal Code = ""` | Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid postal code." -> BUG-008.] |
  | **[BUG-HUNTING CASE]** | `Postal Code = ""` | Standard discrepancy detected (BUG-008) |

  **Expected Result:**
  - Error Field: `postalCode` (attribute `data-for="postalCode"`)
  - Actual Error Text on UI: `"Enter a valid postal code."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-008.

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="postalCode", message_contains="Enter a valid postal code.")`

### TC_SG_011 — Floor/Unit - Empty when N/A is unchecked
- **Original Business Requirement (FSD Standard)**: Displays "This field is required." beneath Floor Number and Unit Number; Trainer Account is not created.
- **Priority & Design Technique**: P1 | EP Negative

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.FLOOR_NUMBER / UNIT_NUMBER` = `"#floorNumber, #unitNumber"`
  - Action method: `CurriculaTrainerPage.leave empty`
  - Error locator & key: `data-for="floorUnit"`, CSS selector `.error[data-for='floorUnit']`, helper `get_error_text("floorUnit")`, `is_error_visible("floorUnit")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Floor = "", Unit = "", N/A = Unchecked` | Displays "This field is required." beneath Floor Number and Unit Number; Trainer Account is not created. |
  | **[BUG-HUNTING CASE]** | `Floor = "", Unit = "", N/A = Unchecked` | Standard discrepancy detected (BUG-008) |

  **Expected Result:**
  - Error Field: `floorUnit` (attribute `data-for="floorUnit"`)
  - Actual Error Text on UI: `"Floor and unit number are required."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-008.

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="floorUnit", message_contains="Floor and unit number are required.")`


## TS-05 Non-Singapore Residential Address

### TC_NSG_001 — Non-SG Address - Switch to international form
- **Original Business Requirement (FSD Standard)**: Country dropdown enabled, international address inputs displayed.
- **Priority & Design Technique**: P1 | Decision Table

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.RESIDENTIAL_TYPE_NON_SG` = `"input[value='Non-Singapore']"`
  - Action method: `CurriculaTrainerPage.set_residential_type('Non-Singapore')`
  - Error locator & key: `data-for="residentialType"`, CSS selector `.error[data-for='residentialType']`, helper `get_error_text("residentialType")`, `is_error_visible("residentialType")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Click Radio Non-Singapore` | Country dropdown enabled, international address inputs displayed. |

  **Expected Result:**
  - Error Field: `residentialType` (attribute `data-for="residentialType"`)
  - Actual Error Text on UI: `"N/A"`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_NSG_002 — Non-SG Address - Country dropdown excludes SG
- **Original Business Requirement (FSD Standard)**: Country list must NOT include "Singapore" (FSD 4.4.2). [Mock App Deviation: HTML line 382 includes Singapore -> BUG-003.]
- **Priority & Design Technique**: P1 | Decision Table

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.COUNTRY_REGION` = `"#countryRegion"`
  - Action method: `CurriculaTrainerPage.select_country_region(...)`
  - Error locator & key: `data-for="countryRegion"`, CSS selector `.error[data-for='countryRegion']`, helper `get_error_text("countryRegion")`, `is_error_visible("countryRegion")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Open Country/region dropdown` | Country list must NOT include "Singapore" (FSD 4.4.2). [Mock App Deviation: HTML line 382 includes Singapore -> BUG-003.] |
  | **[BUG-HUNTING CASE]** | `Open Country/region dropdown` | Standard discrepancy detected (BUG-003) |

  **Expected Result:**
  - Error Field: `countryRegion` (attribute `data-for="countryRegion"`)
  - Actual Error Text on UI: `"N/A"`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-003.

  **Exceptor Method:**
  - `Exceptor.expect_bug_if_rejected(curricula.get_state_snapshot(), field="countryRegion", context="BUG-003")`

### TC_NSG_003 — Non-SG Address - Complete valid address
- **Original Business Requirement (FSD Standard)**: International address saved successfully.
- **Priority & Design Technique**: P1 | EP Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.NON_SG_ADDRESS` = `"#address1, #city"`
  - Action method: `CurriculaTrainerPage.set_non_singapore_address(...)`
  - Error locator & key: `data-for="address1"`, CSS selector `.error[data-for='address1']`, helper `get_error_text("address1")`, `is_error_visible("address1")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Country: "Malaysia", Addr1: "123 Jalan Ampang", City: "KL"` | International address saved successfully. |

  **Expected Result:**
  - Error Field: `address1` (attribute `data-for="address1"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_NSG_004 — Address Line 1 - Empty mandatory check
- **Original Business Requirement (FSD Standard)**: Displays inline error: "This field is required."
- **Priority & Design Technique**: P1 | EP Negative

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.ADDRESS_1` = `"#address1"`
  - Action method: `CurriculaTrainerPage.type_field(ADDRESS_1, '')`
  - Error locator & key: `data-for="address1"`, CSS selector `.error[data-for='address1']`, helper `get_error_text("address1")`, `is_error_visible("address1")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Address Line 1 = ""` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Error Field: `address1` (attribute `data-for="address1"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="address1", message_contains="This field is required.")`

### TC_NSG_005 — City - Empty mandatory check
- **Original Business Requirement (FSD Standard)**: Displays inline error: "This field is required."
- **Priority & Design Technique**: P1 | EP Negative

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.CITY` = `"#city"`
  - Action method: `CurriculaTrainerPage.type_field(CITY, '')`
  - Error locator & key: `data-for="city"`, CSS selector `.error[data-for='city']`, helper `get_error_text("city")`, `is_error_visible("city")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `City = ""` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Error Field: `city` (attribute `data-for="city"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="city", message_contains="This field is required.")`

### TC_NSG_006 — Address Line 1 - Boundary Max 255 chars
- **Original Business Requirement (FSD Standard)**: System accepts all 255 valid characters on Address Line 1.
- **Priority & Design Technique**: P2 | BVA Max

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.ADDRESS_1` = `"#address1"`
  - Action method: `CurriculaTrainerPage.type_field(ADDRESS_1, 'A'*255)`
  - Error locator & key: `data-for="address1"`, CSS selector `.error[data-for='address1']`, helper `get_error_text("address1")`, `is_error_visible("address1")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `String of 255 characters ("A"*255)` | System accepts all 255 valid characters on Address Line 1. |

  **Expected Result:**
  - Error Field: `address1` (attribute `data-for="address1"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_NSG_007 — Non-Singapore Postal Code - Optional field
- **Original Business Requirement (FSD Standard)**: Saved successfully without error.
- **Priority & Design Technique**: P2 | EP Valid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.POSTAL_CODE` = `"#postalCode"`
  - Action method: `CurriculaTrainerPage.type_field(POSTAL_CODE, '')`
  - Error locator & key: `data-for="postalCode"`, CSS selector `.error[data-for='postalCode']`, helper `get_error_text("postalCode")`, `is_error_visible("postalCode")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Postal Code = ""` | Saved successfully without error. |

  **Expected Result:**
  - Error Field: `postalCode` (attribute `data-for="postalCode"`)
  - Actual Error Text on UI: `"Enter a valid postal code."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`


## TS-06 Save Action & System Logic

### TC_SAV_001 — Save - Success & Auto Trainer ID Generation
- **Original Business Requirement (FSD Standard)**: Trainer Account is created; unique Trainer ID formatted as TRN + 6 sequential digits; Status is Active; system displays "Trainer account has been created successfully." and navigates to Trainer Details page.
- **Priority & Design Technique**: P1 | State Transition

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.SAVE_BTN` = `"#saveBtn"`
  - Action method: `CurriculaTrainerPage.save()`
  - Error locator & key: `data-for="successBox"`, CSS selector `.error[data-for='successBox']`, helper `get_error_text("successBox")`, `is_error_visible("successBox")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Complete valid form data` | Trainer Account is created; unique Trainer ID formatted as TRN + 6 sequential digits; Status is Active; system displays "Trainer account has been created successfully." and navigates to Trainer Details page. |

  **Expected Result:**
  - Error Field: `successBox` (attribute `data-for="successBox"`)
  - Actual Error Text on UI: `"Trainer account has been created successfully."`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_SAV_002 — Save - Empty mandatory fields submit
- **Original Business Requirement (FSD Standard)**: Inline error messages displayed across all mandatory fields.
- **Priority & Design Technique**: P1 | EP Negative

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.SAVE_BTN` = `"#saveBtn"`
  - Action method: `CurriculaTrainerPage.save()`
  - Error locator & key: `data-for="multiple fields"`, CSS selector `.error[data-for='multiple fields']`, helper `get_error_text("multiple fields")`, `is_error_visible("multiple fields")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Empty form` | Inline error messages displayed across all mandatory fields. |

  **Expected Result:**
  - Error Field: `multiple fields` (attribute `data-for="multiple fields"`)
  - Actual Error Text on UI: `"This field is required."`

  **Exceptor Method:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="multiple fields", message_contains="This field is required.")`

### TC_SAV_003 — Duplicate Email - Exact match prevention
- **Original Business Requirement (FSD Standard)**: Creation blocked with error: "An account with this email address already exists." [Mock App Deviation: missing duplicate check -> BUG-001.]
- **Priority & Design Technique**: P1 | EP Invalid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.SAVE_BTN` = `"#saveBtn"`
  - Action method: `CurriculaTrainerPage.save()`
  - Error locator & key: `data-for="primaryEmail"`, CSS selector `.error[data-for='primaryEmail']`, helper `get_error_text("primaryEmail")`, `is_error_visible("primaryEmail")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Existing email: bob.wang@curricula.edu.sg` | Creation blocked with error: "An account with this email address already exists." [Mock App Deviation: missing duplicate check -> BUG-001.] |
  | **[BUG-HUNTING CASE]** | `Existing email: bob.wang@curricula.edu.sg` | Standard discrepancy detected (BUG-001) |

  **Expected Result:**
  - Error Field: `primaryEmail` (attribute `data-for="primaryEmail"`)
  - Actual Error Text on UI: `"An account with this email address already exists."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-001.

  **Exceptor Method:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-001")`

### TC_SAV_004 — Duplicate Email - Case-insensitive match
- **Original Business Requirement (FSD Standard)**: Case-insensitive check blocks creation and displays duplicate error. [Mock App Deviation: missing duplicate check -> BUG-001.]
- **Priority & Design Technique**: P1 | EP Invalid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.SAVE_BTN` = `"#saveBtn"`
  - Action method: `CurriculaTrainerPage.save()`
  - Error locator & key: `data-for="primaryEmail"`, CSS selector `.error[data-for='primaryEmail']`, helper `get_error_text("primaryEmail")`, `is_error_visible("primaryEmail")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `BOB.WANG@CURRICULA.EDU.SG` | Case-insensitive check blocks creation and displays duplicate error. [Mock App Deviation: missing duplicate check -> BUG-001.] |
  | **[BUG-HUNTING CASE]** | `BOB.WANG@CURRICULA.EDU.SG` | Standard discrepancy detected (BUG-001) |

  **Expected Result:**
  - Error Field: `primaryEmail` (attribute `data-for="primaryEmail"`)
  - Actual Error Text on UI: `"An account with this email address already exists."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-001.

  **Exceptor Method:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-001")`

### TC_SAV_005 — Duplicate ID Number - Exact match check
- **Original Business Requirement (FSD Standard)**: Creation blocked with error: "An account with this ID number already exists." [Mock App Deviation: missing duplicate check -> BUG-002.]
- **Priority & Design Technique**: P1 | EP Invalid

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.SAVE_BTN` = `"#saveBtn"`
  - Action method: `CurriculaTrainerPage.save()`
  - Error locator & key: `data-for="idNumber"`, CSS selector `.error[data-for='idNumber']`, helper `get_error_text("idNumber")`, `is_error_visible("idNumber")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Existing ID: G7666564N` | Creation blocked with error: "An account with this ID number already exists." [Mock App Deviation: missing duplicate check -> BUG-002.] |
  | **[BUG-HUNTING CASE]** | `Existing ID: G7666564N` | Standard discrepancy detected (BUG-002) |

  **Expected Result:**
  - Error Field: `idNumber` (attribute `data-for="idNumber"`)
  - Actual Error Text on UI: `"An account with this ID number already exists."`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-002.

  **Exceptor Method:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-002")`

### TC_SAV_006 — Concurrency - Multiple Save clicks handling
- **Original Business Requirement (FSD Standard)**: Only one account creation request is processed and exactly one Trainer Account/Trainer ID is generated. The system must not create duplicate records when the user clicks Save multiple times (Error Guessing -> BUG-004).
- **Priority & Design Technique**: P1 | Error Guessing

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.SAVE_BTN` = `"#saveBtn"`
  - Action method: `CurriculaTrainerPage.double click save`
  - Error locator & key: `data-for="concurrency"`, CSS selector `.error[data-for='concurrency']`, helper `get_error_text("concurrency")`, `is_error_visible("concurrency")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Complete valid form` | Only one account creation request is processed and exactly one Trainer Account/Trainer ID is generated. The system must not create duplicate records when the user clicks Save multiple times (Error Guessing -> BUG-004). |
  | **[BUG-HUNTING CASE]** | `Complete valid form` | Standard discrepancy detected (BUG-004) |

  **Expected Result:**
  - Error Field: `concurrency` (attribute `data-for="concurrency"`)
  - Actual Error Text on UI: `"Single account processed"`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-004.

  **Exceptor Method:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-004")`

### TC_SAV_007 — Trainer ID - Sequential increment rule
- **Original Business Requirement (FSD Standard)**: Trainer ID follows sequential increment TRN + 6 digits.
- **Priority & Design Technique**: P2 | State Transition

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.SUCCESS_BOX` = `"#successBox"`
  - Action method: `CurriculaTrainerPage.get_success_text()`
  - Error locator & key: `data-for="trainerId"`, CSS selector `.error[data-for='trainerId']`, helper `get_error_text("trainerId")`, `is_error_visible("trainerId")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Valid form` | Trainer ID follows sequential increment TRN + 6 digits. |
  | **[BUG-HUNTING CASE]** | `Valid form` | Standard discrepancy detected (CQ-06) |

  **Expected Result:**
  - Error Field: `trainerId` (attribute `data-for="trainerId"`)
  - Actual Error Text on UI: `"Sequential TRN+6 digits"`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under CQ-06.

  **Exceptor Method:**
  - `Exceptor.expect_bug_if_rejected(curricula.get_state_snapshot(), field="trainerId", context="CQ-06")`

### TC_SAV_008 — Data Hygiene - Automatic whitespace trim
- **Original Business Requirement (FSD Standard)**: System automatically trims whitespace before database persistence.
- **Priority & Design Technique**: P2 | Error Guessing

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.SAVE_BTN` = `"#saveBtn"`
  - Action method: `CurriculaTrainerPage.save()`
  - Error locator & key: `data-for="successBox"`, CSS selector `.error[data-for='successBox']`, helper `get_error_text("successBox")`, `is_error_visible("successBox")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Name & Email with surrounding spaces` | System automatically trims whitespace before database persistence. |

  **Expected Result:**
  - Error Field: `successBox` (attribute `data-for="successBox"`)
  - Actual Error Text on UI: `"Whitespace auto-trimmed"`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`


## TS-07 Cancel Action & Form State

### TC_CAN_001 — Cancel - Clean form discard without prompt
- **Original Business Requirement (FSD Standard)**: User is navigated back to Trainer Listing page without a confirmation popup.
- **Priority & Design Technique**: P2 | State Transition

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.CANCEL_BTN` = `"#cancelBtn"`
  - Action method: `CurriculaTrainerPage.cancel()`
  - Error locator & key: `data-for="dialog"`, CSS selector `.error[data-for='dialog']`, helper `get_error_text("dialog")`, `is_error_visible("dialog")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Form with zero user inputs` | User is navigated back to Trainer Listing page without a confirmation popup. |

  **Expected Result:**
  - Error Field: `dialog` (attribute `data-for="dialog"`)
  - Actual Error Text on UI: `"No confirmation dialog"`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_CAN_002 — Cancel - Unsaved changes -> Select "Stay"
- **Original Business Requirement (FSD Standard)**: Dialog closes, all entered form data retained.
- **Priority & Design Technique**: P1 | Decision Table

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.CANCEL_BTN` = `"#cancelBtn"`
  - Action method: `CurriculaTrainerPage.cancel() -> dismiss dialog`
  - Error locator & key: `data-for="dialog"`, CSS selector `.error[data-for='dialog']`, helper `get_error_text("dialog")`, `is_error_visible("dialog")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Partially populated form` | Dialog closes, all entered form data retained. |

  **Expected Result:**
  - Error Field: `dialog` (attribute `data-for="dialog"`)
  - Actual Error Text on UI: `"Data retained"`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_CAN_003 — Cancel - Unsaved changes -> Select "Leave"
- **Original Business Requirement (FSD Standard)**: Form changes discarded and user navigated back to Trainer Listing page.
- **Priority & Design Technique**: P1 | Decision Table

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.CANCEL_BTN` = `"#cancelBtn"`
  - Action method: `CurriculaTrainerPage.cancel() -> accept dialog`
  - Error locator & key: `data-for="dialog"`, CSS selector `.error[data-for='dialog']`, helper `get_error_text("dialog")`, `is_error_visible("dialog")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Partially populated form` | Form changes discarded and user navigated back to Trainer Listing page. |

  **Expected Result:**
  - Error Field: `dialog` (attribute `data-for="dialog"`)
  - Actual Error Text on UI: `"Form reset"`

  **Exceptor Method:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_CAN_004 — Cancel - Detect Dirty State on Radio/Select
- **Original Business Requirement (FSD Standard)**: System recognizes Dirty State and displays Unsaved Changes prompt. [Mock App Deviation: misses radio/select elements -> BUG-006.]
- **Priority & Design Technique**: P2 | Error Guessing

  **Reference Selectors:**
  - Locator element: `CurriculaTrainerPage.CANCEL_BTN` = `"#cancelBtn"`
  - Action method: `CurriculaTrainerPage.cancel()`
  - Error locator & key: `data-for="dialog"`, CSS selector `.error[data-for='dialog']`, helper `get_error_text("dialog")`, `is_error_visible("dialog")`
  - Page Object Assessment: Complete locator, action method, and error inspection already implemented.

  **Test Data:**
  | Case | Input Value | Expected Result |
  |---|---|---|
  | Primary Test Input | `Modified Gender = Female or Nationality` | System recognizes Dirty State and displays Unsaved Changes prompt. [Mock App Deviation: misses radio/select elements -> BUG-006.] |
  | **[BUG-HUNTING CASE]** | `Modified Gender = Female or Nationality` | Standard discrepancy detected (BUG-006) |

  **Expected Result:**
  - Error Field: `dialog` (attribute `data-for="dialog"`)
  - Actual Error Text on UI: `"Dirty state on radio/dropdown triggers dialog"`
  - Known Discrepancy Note: Actual behavior discrepancy tracked under BUG-006.

  **Exceptor Method:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-006")`

