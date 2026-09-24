# Acceptance Criteria - US-04 Curricula Trainer Account (68 Test Cases)

Tài liệu này là nguồn tham chiếu cố định (Source of Truth) về các tiêu chí chấp nhận và yêu cầu kỹ thuật cho tính năng **Create Trainer Account (Curricula)**.
Bao gồm toàn bộ 68 Test Cases theo 7 Test Suites (TS-01 đến TS-07), được cấu trúc chuẩn hóa với 4 mục con kỹ thuật bắt buộc theo `AGENTS.md`.

---

## TS-01 Personal Information

### TC_PI_001 — Preferred Name - Valid string entry
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Value accepted without error.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.PREFERRED_NAME` = `"#preferredName"`
  - Action method: `CurriculaTrainerPage.set_preferred_name(name)`
  - Error locator & key: `data-for="preferredName"`, CSS selector `.error[data-for='preferredName']`, helper `get_error_text("preferredName")`, `is_error_visible("preferredName")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Preferred Name = "Bob Wang"` | Value accepted without error. |

  **Expected Result:**
  - Field lỗi: `preferredName` (thuộc tính `data-for="preferredName"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_002 — Preferred Name - Boundary Max 100 characters
- **Mô tả nghiệp vụ gốc (FSD Standard)**: All 100 characters accepted successfully.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | BVA Max

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.PREFERRED_NAME` = `"#preferredName"`
  - Action method: `CurriculaTrainerPage.set_preferred_name(name)`
  - Error locator & key: `data-for="preferredName"`, CSS selector `.error[data-for='preferredName']`, helper `get_error_text("preferredName")`, `is_error_visible("preferredName")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `String of 100 characters ("A"*100)` | All 100 characters accepted successfully. |

  **Expected Result:**
  - Field lỗi: `preferredName` (thuộc tính `data-for="preferredName"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_003 — Preferred Name - Exceeds 100 chars (BVA Max+1)
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System does not accept Preferred Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows 101 characters -> BUG-007.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | BVA Max+1

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.PREFERRED_NAME` = `"#preferredName"`
  - Action method: `CurriculaTrainerPage.set_preferred_name(name)`
  - Error locator & key: `data-for="preferredName"`, CSS selector `.error[data-for='preferredName']`, helper `get_error_text("preferredName")`, `is_error_visible("preferredName")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `String of 101 characters ("A"*101)` | System does not accept Preferred Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows 101 characters -> BUG-007.] |
  | **[BUG-HUNTING CASE]** | `String of 101 characters ("A"*101)` | Phát hiện lệch chuẩn (BUG-007) |

  **Expected Result:**
  - Field lỗi: `preferredName` (thuộc tính `data-for="preferredName"`)
  - Text lỗi thực tế trên UI: `"This field is required."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-007.

  **Nhãn Exceptor:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-007")`

### TC_PI_004 — Preferred Name - Auto-trim whitespace
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System trims whitespace and stores "Bob Wang".
- **Độ ưu tiên & Kỹ thuật thiết kế**: P3 | Error Guessing

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.PREFERRED_NAME` = `"#preferredName"`
  - Action method: `CurriculaTrainerPage.set_preferred_name(name)`
  - Error locator & key: `data-for="preferredName"`, CSS selector `.error[data-for='preferredName']`, helper `get_error_text("preferredName")`, `is_error_visible("preferredName")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `"  Bob Wang  "` | System trims whitespace and stores "Bob Wang". |

  **Expected Result:**
  - Field lỗi: `preferredName` (thuộc tính `data-for="preferredName"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_005 — Gender - Select Male / Female
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Radio button switches smoothly, single value selected.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.GENDER_MALE / GENDER_FEMALE` = `"input[name='gender']"`
  - Action method: `CurriculaTrainerPage.select_gender(gender)`
  - Error locator & key: `data-for="gender"`, CSS selector `.error[data-for='gender']`, helper `get_error_text("gender")`, `is_error_visible("gender")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Click Radio Male, then Female` | Radio button switches smoothly, single value selected. |

  **Expected Result:**
  - Field lỗi: `gender` (thuộc tính `data-for="gender"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_006 — ID Type - 4 Document types per FSD 4.1
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Exactly 4 document types: NRIC, FIN, Employment Pass, Passport. [Mock App Deviation: shows extra "S-Pass" -> BUG-009 / FSD Table 4.1 vs narrative section mismatch; clarification required.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.ID_TYPE` = `"#idType"`
  - Action method: `CurriculaTrainerPage.select_id_type(id_type)`
  - Error locator & key: `data-for="idType"`, CSS selector `.error[data-for='idType']`, helper `get_error_text("idType")`, `is_error_visible("idType")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Open ID Type dropdown` | Exactly 4 document types: NRIC, FIN, Employment Pass, Passport. [Mock App Deviation: shows extra "S-Pass" -> BUG-009 / FSD Table 4.1 vs narrative section mismatch; clarification required.] |
  | **[BUG-HUNTING CASE]** | `Open ID Type dropdown` | Phát hiện lệch chuẩn (BUG-009 / CQ-08) |

  **Expected Result:**
  - Field lỗi: `idType` (thuộc tính `data-for="idType"`)
  - Text lỗi thực tế trên UI: `"This field is required."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-009 / CQ-08.

  **Nhãn Exceptor:**
  - `Exceptor.expect_bug_if_rejected(curricula.get_state_snapshot(), field="idType", context="BUG-009 / CQ-08")`

### TC_PI_007 — ID Number - Valid NRIC format
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Value accepted and stored accurately.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.ID_NUMBER` = `"#idNumber"`
  - Action method: `CurriculaTrainerPage.set_id_number(id_number)`
  - Error locator & key: `data-for="idNumber"`, CSS selector `.error[data-for='idNumber']`, helper `get_error_text("idNumber")`, `is_error_visible("idNumber")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `ID Type = "NRIC", ID Number = "G7666564N"` | Value accepted and stored accurately. |

  **Expected Result:**
  - Field lỗi: `idNumber` (thuộc tính `data-for="idNumber"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_008 — ID Number - ID Checksum validation
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System validates ID Checksum per FSD Section 5d and blocks save. (FSD checksum requirement; test data provisional pending BA/PO confirmation; Mock App does not implement any checksum logic -> BUG-010).
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Invalid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.ID_NUMBER` = `"#idNumber"`
  - Action method: `CurriculaTrainerPage.set_id_number(id_number)`
  - Error locator & key: `data-for="idNumber"`, CSS selector `.error[data-for='idNumber']`, helper `get_error_text("idNumber")`, `is_error_visible("idNumber")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `ID Type = "NRIC", ID Number = "S1234567A"` | System validates ID Checksum per FSD Section 5d and blocks save. (FSD checksum requirement; test data provisional pending BA/PO confirmation; Mock App does not implement any checksum logic -> BUG-010). |
  | **[BUG-HUNTING CASE]** | `ID Type = "NRIC", ID Number = "S1234567A"` | Phát hiện lệch chuẩn (BUG-010) |

  **Expected Result:**
  - Field lỗi: `idNumber` (thuộc tính `data-for="idNumber"`)
  - Text lỗi thực tế trên UI: `"This field is required."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-010.

  **Nhãn Exceptor:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-010")`

### TC_PI_009 — ID Number - Exceeds 20 chars (BVA Max+1)
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System does not accept ID Number exceeding 20 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 20 characters -> BUG-007.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | BVA Max+1

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.ID_NUMBER` = `"#idNumber"`
  - Action method: `CurriculaTrainerPage.set_id_number(id_number)`
  - Error locator & key: `data-for="idNumber"`, CSS selector `.error[data-for='idNumber']`, helper `get_error_text("idNumber")`, `is_error_visible("idNumber")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `String of 21 characters ("A"*21)` | System does not accept ID Number exceeding 20 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 20 characters -> BUG-007.] |
  | **[BUG-HUNTING CASE]** | `String of 21 characters ("A"*21)` | Phát hiện lệch chuẩn (BUG-007) |

  **Expected Result:**
  - Field lỗi: `idNumber` (thuộc tính `data-for="idNumber"`)
  - Text lỗi thực tế trên UI: `"This field is required."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-007.

  **Nhãn Exceptor:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-007")`

### TC_PI_010 — Date of Birth - Valid past date
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System accepts date successfully.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.DOB` = `"#dob"`
  - Action method: `CurriculaTrainerPage.set_dob(dob_str)`
  - Error locator & key: `data-for="dob"`, CSS selector `.error[data-for='dob']`, helper `get_error_text("dob")`, `is_error_visible("dob")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `DOB = "1990-05-15"` | System accepts date successfully. |

  **Expected Result:**
  - Field lỗi: `dob` (thuộc tính `data-for="dob"`)
  - Text lỗi thực tế trên UI: `"Enter a valid date of birth."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_011 — Date of Birth - Future date rejection
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System rejects future date of birth, displays inline validation at Date of Birth field, and does not create Trainer Account. Specific error message is TBD pending BA/PO confirmation.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP / BVA

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.DOB` = `"#dob"`
  - Action method: `CurriculaTrainerPage.set_dob(dob_str)`
  - Error locator & key: `data-for="dob"`, CSS selector `.error[data-for='dob']`, helper `get_error_text("dob")`, `is_error_visible("dob")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `DOB = "2030-01-01"` | System rejects future date of birth, displays inline validation at Date of Birth field, and does not create Trainer Account. Specific error message is TBD pending BA/PO confirmation. |

  **Expected Result:**
  - Field lỗi: `dob` (thuộc tính `data-for="dob"`)
  - Text lỗi thực tế trên UI: `"Enter a valid date of birth."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="dob", message_contains="Enter a valid date of birth.")`

### TC_PI_012 — File Upload - PDF/PNG/JPG/JPEG <= 10MB
- **Mô tả nghiệp vụ gốc (FSD Standard)**: File uploaded successfully, file name displayed.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP / BVA

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.ID_DOCUMENT` = `"#idDocument"`
  - Action method: `CurriculaTrainerPage.upload_document(file_path)`
  - Error locator & key: `data-for="idDocument"`, CSS selector `.error[data-for='idDocument']`, helper `get_error_text("idDocument")`, `is_error_visible("idDocument")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `PDF file of 5MB` | File uploaded successfully, file name displayed. |

  **Expected Result:**
  - Field lỗi: `idDocument` (thuộc tính `data-for="idDocument"`)
  - Text lỗi thực tế trên UI: `"Please upload a valid document."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_013 — File Upload - Exceeds 10MB limit
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System rejects file and displays: "File size must not exceed 10 MB."
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | BVA Max+1

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.ID_DOCUMENT` = `"#idDocument"`
  - Action method: `CurriculaTrainerPage.upload_document(file_path)`
  - Error locator & key: `data-for="idDocument"`, CSS selector `.error[data-for='idDocument']`, helper `get_error_text("idDocument")`, `is_error_visible("idDocument")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `PDF file of 11MB` | System rejects file and displays: "File size must not exceed 10 MB." |

  **Expected Result:**
  - Field lỗi: `idDocument` (thuộc tính `data-for="idDocument"`)
  - Text lỗi thực tế trên UI: `"Please upload a valid document."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="idDocument", message_contains="Please upload a valid document.")`

### TC_PI_014 — File Upload - Invalid file format (.docx)
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System rejects file and displays: "Unsupported file format."
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Invalid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.ID_DOCUMENT` = `"#idDocument"`
  - Action method: `CurriculaTrainerPage.upload_document(file_path)`
  - Error locator & key: `data-for="idDocument"`, CSS selector `.error[data-for='idDocument']`, helper `get_error_text("idDocument")`, `is_error_visible("idDocument")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `File document.docx (500KB)` | System rejects file and displays: "Unsupported file format." |
  | **[BUG-HUNTING CASE]** | `File document.docx (500KB)` | Phát hiện lệch chuẩn (BUG-008) |

  **Expected Result:**
  - Field lỗi: `idDocument` (thuộc tính `data-for="idDocument"`)
  - Text lỗi thực tế trên UI: `"Please upload a valid document."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-008.

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="idDocument", message_contains="Please upload a valid document.")`

### TC_PI_015 — Nationality - Select from Dropdown
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Dropdown correctly registers selected value.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.NATIONALITY` = `"#nationality"`
  - Action method: `CurriculaTrainerPage.select_nationality(nationality)`
  - Error locator & key: `data-for="nationality"`, CSS selector `.error[data-for='nationality']`, helper `get_error_text("nationality")`, `is_error_visible("nationality")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Select Singaporean` | Dropdown correctly registers selected value. |

  **Expected Result:**
  - Field lỗi: `nationality` (thuộc tính `data-for="nationality"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_016 — Country of Birth - Select from Dropdown
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Dropdown correctly registers selected value.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.BIRTH_COUNTRY` = `"#birthCountry"`
  - Action method: `CurriculaTrainerPage.select_birth_country(country)`
  - Error locator & key: `data-for="birthCountry"`, CSS selector `.error[data-for='birthCountry']`, helper `get_error_text("birthCountry")`, `is_error_visible("birthCountry")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Select Singapore` | Dropdown correctly registers selected value. |

  **Expected Result:**
  - Field lỗi: `birthCountry` (thuộc tính `data-for="birthCountry"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_PI_017 — Preferred Name - Empty mandatory check
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays inline error: "This field is required."
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Negative

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.PREFERRED_NAME` = `"#preferredName"`
  - Action method: `CurriculaTrainerPage.set_preferred_name('')`
  - Error locator & key: `data-for="preferredName"`, CSS selector `.error[data-for='preferredName']`, helper `get_error_text("preferredName")`, `is_error_visible("preferredName")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Preferred Name = ""` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Field lỗi: `preferredName` (thuộc tính `data-for="preferredName"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="preferredName", message_contains="This field is required.")`

### TC_PI_018 — ID Number - Empty mandatory check
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays inline error: "This field is required."
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Negative

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.ID_NUMBER` = `"#idNumber"`
  - Action method: `CurriculaTrainerPage.set_id_number('')`
  - Error locator & key: `data-for="idNumber"`, CSS selector `.error[data-for='idNumber']`, helper `get_error_text("idNumber")`, `is_error_visible("idNumber")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `ID Number = ""` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Field lỗi: `idNumber` (thuộc tính `data-for="idNumber"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="idNumber", message_contains="This field is required.")`

### TC_PI_019 — Date of Birth - Empty mandatory check
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid date of birth." -> BUG-008.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Negative

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.DOB` = `"#dob"`
  - Action method: `CurriculaTrainerPage.set_dob('')`
  - Error locator & key: `data-for="dob"`, CSS selector `.error[data-for='dob']`, helper `get_error_text("dob")`, `is_error_visible("dob")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `DOB = ""` | Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid date of birth." -> BUG-008.] |
  | **[BUG-HUNTING CASE]** | `DOB = ""` | Phát hiện lệch chuẩn (BUG-008) |

  **Expected Result:**
  - Field lỗi: `dob` (thuộc tính `data-for="dob"`)
  - Text lỗi thực tế trên UI: `"Enter a valid date of birth."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-008.

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="dob", message_contains="Enter a valid date of birth.")`

### TC_PI_020 — Nationality - Unselected mandatory check
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays inline error: "This field is required."
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Negative

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.NATIONALITY` = `"#nationality"`
  - Action method: `CurriculaTrainerPage.select_nationality('')`
  - Error locator & key: `data-for="nationality"`, CSS selector `.error[data-for='nationality']`, helper `get_error_text("nationality")`, `is_error_visible("nationality")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `No selection made` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Field lỗi: `nationality` (thuộc tính `data-for="nationality"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="nationality", message_contains="This field is required.")`

### TC_PI_021 — Country of Birth - Unselected mandatory check
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays inline error: "This field is required."
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Negative

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.BIRTH_COUNTRY` = `"#birthCountry"`
  - Action method: `CurriculaTrainerPage.select_birth_country('')`
  - Error locator & key: `data-for="birthCountry"`, CSS selector `.error[data-for='birthCountry']`, helper `get_error_text("birthCountry")`, `is_error_visible("birthCountry")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `No selection made` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Field lỗi: `birthCountry` (thuộc tính `data-for="birthCountry"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="birthCountry", message_contains="This field is required.")`

### TC_PI_022 — Gender, Race & Tax Resident - Unselected check
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays "This field is required." error for all 3 fields.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Negative

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.GENDER / RACE / TAX_RESIDENT` = `"gender, #race, taxResident"`
  - Action method: `CurriculaTrainerPage.leave unselected`
  - Error locator & key: `data-for="gender / race / taxResident"`, CSS selector `.error[data-for='gender / race / taxResident']`, helper `get_error_text("gender / race / taxResident")`, `is_error_visible("gender / race / taxResident")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Leave all 3 unselected` | Displays "This field is required." error for all 3 fields. |

  **Expected Result:**
  - Field lỗi: `gender / race / taxResident` (thuộc tính `data-for="gender / race / taxResident"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="gender / race / taxResident", message_contains="This field is required.")`

### TC_PI_023 — Race Dropdown - Ethnic groups options (CQ-07)
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays 4 standard groups: Chinese, Malay, Indian, Others.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | EP Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.RACE` = `"#race"`
  - Action method: `CurriculaTrainerPage.select_race(race)`
  - Error locator & key: `data-for="race"`, CSS selector `.error[data-for='race']`, helper `get_error_text("race")`, `is_error_visible("race")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Open Race dropdown` | Displays 4 standard groups: Chinese, Malay, Indian, Others. |
  | **[BUG-HUNTING CASE]** | `Open Race dropdown` | Phát hiện lệch chuẩn (CQ-07) |

  **Expected Result:**
  - Field lỗi: `race` (thuộc tính `data-for="race"`)
  - Text lỗi thực tế trên UI: `"This field is required."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại CQ-07.

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`


## TS-02 Contact Information

### TC_CI_001 — Primary Email - Valid email format
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Email accepted without error.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_EMAIL` = `"#primaryEmail"`
  - Action method: `CurriculaTrainerPage.set_primary_email(email)`
  - Error locator & key: `data-for="primaryEmail"`, CSS selector `.error[data-for='primaryEmail']`, helper `get_error_text("primaryEmail")`, `is_error_visible("primaryEmail")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Primary Email = "trainer.bob@curricula.edu.sg"` | Email accepted without error. |

  **Expected Result:**
  - Field lỗi: `primaryEmail` (thuộc tính `data-for="primaryEmail"`)
  - Text lỗi thực tế trên UI: `"Enter a valid email address."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_CI_002 — Primary Email - Invalid format rejection
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays inline error: "Enter a valid email address."
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Invalid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_EMAIL` = `"#primaryEmail"`
  - Action method: `CurriculaTrainerPage.set_primary_email(email)`
  - Error locator & key: `data-for="primaryEmail"`, CSS selector `.error[data-for='primaryEmail']`, helper `get_error_text("primaryEmail")`, `is_error_visible("primaryEmail")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `"plainaddress", "@missinguser.com"` | Displays inline error: "Enter a valid email address." |

  **Expected Result:**
  - Field lỗi: `primaryEmail` (thuộc tính `data-for="primaryEmail"`)
  - Text lỗi thực tế trên UI: `"Enter a valid email address."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="primaryEmail", message_contains="Enter a valid email address.")`

### TC_CI_003 — Primary Email - Boundary Max 100 characters
- **Mô tả nghiệp vụ gốc (FSD Standard)**: 100-character email accepted successfully.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | BVA Max

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_EMAIL` = `"#primaryEmail"`
  - Action method: `CurriculaTrainerPage.set_primary_email(email)`
  - Error locator & key: `data-for="primaryEmail"`, CSS selector `.error[data-for='primaryEmail']`, helper `get_error_text("primaryEmail")`, `is_error_visible("primaryEmail")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Valid email of exactly 100 chars` | 100-character email accepted successfully. |

  **Expected Result:**
  - Field lỗi: `primaryEmail` (thuộc tính `data-for="primaryEmail"`)
  - Text lỗi thực tế trên UI: `"Enter a valid email address."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_CI_004 — Primary Phone - Valid Singapore 8 digits (+65)
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Phone number accepted without error.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | BVA Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_PHONE` = `"#primaryPhone"`
  - Action method: `CurriculaTrainerPage.set_primary_phone(code, phone)`
  - Error locator & key: `data-for="primaryPhone"`, CSS selector `.error[data-for='primaryPhone']`, helper `get_error_text("primaryPhone")`, `is_error_visible("primaryPhone")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Code = "+65", Number = "91234567"` | Phone number accepted without error. |

  **Expected Result:**
  - Field lỗi: `primaryPhone` (thuộc tính `data-for="primaryPhone"`)
  - Text lỗi thực tế trên UI: `"Enter a valid contact number."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_CI_005 — Primary Phone - 7 digits rejection (BVA Min-1)
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System rejects 7-digit phone number, displays inline validation, and does not create Trainer Account.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | BVA Min-1

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_PHONE` = `"#primaryPhone"`
  - Action method: `CurriculaTrainerPage.set_primary_phone(code, phone)`
  - Error locator & key: `data-for="primaryPhone"`, CSS selector `.error[data-for='primaryPhone']`, helper `get_error_text("primaryPhone")`, `is_error_visible("primaryPhone")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Code = "+65", Number = "9123456"` | System rejects 7-digit phone number, displays inline validation, and does not create Trainer Account. |

  **Expected Result:**
  - Field lỗi: `primaryPhone` (thuộc tính `data-for="primaryPhone"`)
  - Text lỗi thực tế trên UI: `"Enter a valid contact number."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="primaryPhone", message_contains="Enter a valid contact number.")`

### TC_CI_006 — Primary Phone - 9 digits with code +65
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Under general FSD rule of 8–15 digits, 9-digit number is accepted. (Mock App rejects when country code is +65 -> Fail / Requirement inconsistency tracked under CQ-09).
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | BVA / Observed

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_PHONE` = `"#primaryPhone"`
  - Action method: `CurriculaTrainerPage.set_primary_phone(code, phone)`
  - Error locator & key: `data-for="primaryPhone"`, CSS selector `.error[data-for='primaryPhone']`, helper `get_error_text("primaryPhone")`, `is_error_visible("primaryPhone")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Code = "+65", Number = "912345678"` | Under general FSD rule of 8–15 digits, 9-digit number is accepted. (Mock App rejects when country code is +65 -> Fail / Requirement inconsistency tracked under CQ-09). |
  | **[BUG-HUNTING CASE]** | `Code = "+65", Number = "912345678"` | Phát hiện lệch chuẩn (CQ-09) |

  **Expected Result:**
  - Field lỗi: `primaryPhone` (thuộc tính `data-for="primaryPhone"`)
  - Text lỗi thực tế trên UI: `"Enter a valid contact number."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại CQ-09.

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="primaryPhone", message_contains="Enter a valid contact number.")`

### TC_CI_007 — Phone Numbers - Reject alphabetic characters
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System prevents non-digit input or displays format error.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | EP Invalid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_PHONE` = `"#primaryPhone"`
  - Action method: `CurriculaTrainerPage.set_primary_phone(code, phone)`
  - Error locator & key: `data-for="primaryPhone"`, CSS selector `.error[data-for='primaryPhone']`, helper `get_error_text("primaryPhone")`, `is_error_visible("primaryPhone")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Number = "9123ABCD"` | System prevents non-digit input or displays format error. |

  **Expected Result:**
  - Field lỗi: `primaryPhone` (thuộc tính `data-for="primaryPhone"`)
  - Text lỗi thực tế trên UI: `"Enter a valid contact number."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="primaryPhone", message_contains="Enter a valid contact number.")`

### TC_CI_008 — Primary Email - Empty mandatory check
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays inline error: "This field is required."
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Negative

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_EMAIL` = `"#primaryEmail"`
  - Action method: `CurriculaTrainerPage.set_primary_email('')`
  - Error locator & key: `data-for="primaryEmail"`, CSS selector `.error[data-for='primaryEmail']`, helper `get_error_text("primaryEmail")`, `is_error_visible("primaryEmail")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Primary Email = ""` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Field lỗi: `primaryEmail` (thuộc tính `data-for="primaryEmail"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="primaryEmail", message_contains="This field is required.")`

### TC_CI_009 — Primary Phone - Empty mandatory check
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid contact number." -> BUG-008.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Negative

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.PRIMARY_PHONE` = `"#primaryPhone"`
  - Action method: `CurriculaTrainerPage.set_primary_phone('+65', '')`
  - Error locator & key: `data-for="primaryPhone"`, CSS selector `.error[data-for='primaryPhone']`, helper `get_error_text("primaryPhone")`, `is_error_visible("primaryPhone")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Primary Phone = ""` | Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid contact number." -> BUG-008.] |
  | **[BUG-HUNTING CASE]** | `Primary Phone = ""` | Phát hiện lệch chuẩn (BUG-008) |

  **Expected Result:**
  - Field lỗi: `primaryPhone` (thuộc tính `data-for="primaryPhone"`)
  - Text lỗi thực tế trên UI: `"Enter a valid contact number."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-008.

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="primaryPhone", message_contains="Enter a valid contact number.")`


## TS-03 Emergency Contact

### TC_EC_001 — Emergency Contact - Valid complete data
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Emergency contact information recorded successfully.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.EMERGENCY_NAME / EMERGENCY_PHONE` = `"#emergencyName, #emergencyPhone"`
  - Action method: `CurriculaTrainerPage.set_emergency_contact(...)`
  - Error locator & key: `data-for="emergencyName"`, CSS selector `.error[data-for='emergencyName']`, helper `get_error_text("emergencyName")`, `is_error_visible("emergencyName")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Name: "David Wang", Relationship: "Parent", Number: "98765432"` | Emergency contact information recorded successfully. |

  **Expected Result:**
  - Field lỗi: `emergencyName` (thuộc tính `data-for="emergencyName"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_EC_002 — Emergency Name - Exceeds 100 chars (BVA Max+1)
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System does not accept Emergency Contact Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 100 characters -> BUG-007.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | BVA Max+1

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.EMERGENCY_NAME` = `"#emergencyName"`
  - Action method: `CurriculaTrainerPage.set_emergency_contact(...)`
  - Error locator & key: `data-for="emergencyName"`, CSS selector `.error[data-for='emergencyName']`, helper `get_error_text("emergencyName")`, `is_error_visible("emergencyName")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `String of 101 characters ("A"*101)` | System does not accept Emergency Contact Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 100 characters -> BUG-007.] |
  | **[BUG-HUNTING CASE]** | `String of 101 characters ("A"*101)` | Phát hiện lệch chuẩn (BUG-007) |

  **Expected Result:**
  - Field lỗi: `emergencyName` (thuộc tính `data-for="emergencyName"`)
  - Text lỗi thực tế trên UI: `"This field is required."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-007.

  **Nhãn Exceptor:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-007")`

### TC_EC_003 — Emergency Relationship - Enum per FSD 4.3
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays exact FSD Table 4.3 enum: Parent, Spouse, Sibling, Relative, Friend, Others. [Mock App Deviation: shows Father, Mother -> BUG-005.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | EP Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.EMERGENCY_RELATIONSHIP` = `"#emergencyRelationship"`
  - Action method: `CurriculaTrainerPage.select relationship`
  - Error locator & key: `data-for="emergencyRelationship"`, CSS selector `.error[data-for='emergencyRelationship']`, helper `get_error_text("emergencyRelationship")`, `is_error_visible("emergencyRelationship")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Open Relationship dropdown` | Displays exact FSD Table 4.3 enum: Parent, Spouse, Sibling, Relative, Friend, Others. [Mock App Deviation: shows Father, Mother -> BUG-005.] |
  | **[BUG-HUNTING CASE]** | `Open Relationship dropdown` | Phát hiện lệch chuẩn (BUG-005) |

  **Expected Result:**
  - Field lỗi: `emergencyRelationship` (thuộc tính `data-for="emergencyRelationship"`)
  - Text lỗi thực tế trên UI: `"This field is required."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-005.

  **Nhãn Exceptor:**
  - `Exceptor.expect_bug_if_rejected(curricula.get_state_snapshot(), field="emergencyRelationship", context="BUG-005")`

### TC_EC_004 — Emergency Name - Empty mandatory check
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays inline error: "This field is required."
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Negative

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.EMERGENCY_NAME` = `"#emergencyName"`
  - Action method: `CurriculaTrainerPage.set_emergency_contact('', ...)`
  - Error locator & key: `data-for="emergencyName"`, CSS selector `.error[data-for='emergencyName']`, helper `get_error_text("emergencyName")`, `is_error_visible("emergencyName")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Emergency Name = ""` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Field lỗi: `emergencyName` (thuộc tính `data-for="emergencyName"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="emergencyName", message_contains="This field is required.")`

### TC_EC_005 — Emergency Number - Empty mandatory check
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid contact number." -> BUG-008.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Negative

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.EMERGENCY_PHONE` = `"#emergencyPhone"`
  - Action method: `CurriculaTrainerPage.set_emergency_contact(..., '')`
  - Error locator & key: `data-for="emergencyPhone"`, CSS selector `.error[data-for='emergencyPhone']`, helper `get_error_text("emergencyPhone")`, `is_error_visible("emergencyPhone")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Emergency Number = ""` | Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid contact number." -> BUG-008.] |
  | **[BUG-HUNTING CASE]** | `Emergency Number = ""` | Phát hiện lệch chuẩn (BUG-008) |

  **Expected Result:**
  - Field lỗi: `emergencyPhone` (thuộc tính `data-for="emergencyPhone"`)
  - Text lỗi thực tế trên UI: `"Enter a valid contact number."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-008.

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="emergencyPhone", message_contains="Enter a valid contact number.")`

### TC_EC_006 — Emergency Number - Độ dài 8-15 chữ số
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Validated and saved successfully.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | BVA Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.EMERGENCY_PHONE` = `"#emergencyPhone"`
  - Action method: `CurriculaTrainerPage.set_emergency_contact(...)`
  - Error locator & key: `data-for="emergencyPhone"`, CSS selector `.error[data-for='emergencyPhone']`, helper `get_error_text("emergencyPhone")`, `is_error_visible("emergencyPhone")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Code = "+65", Number = "98765432"` | Validated and saved successfully. |

  **Expected Result:**
  - Field lỗi: `emergencyPhone` (thuộc tính `data-for="emergencyPhone"`)
  - Text lỗi thực tế trên UI: `"Enter a valid contact number."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`


## TS-04 Singapore Residential Address

### TC_SG_001 — Singapore Address - Default selection
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Singapore radio selected by default; Country/Region automatically set to Singapore and disabled.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | Decision Table

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.RESIDENTIAL_TYPE_SG` = `"input[value='Singapore']"`
  - Action method: `CurriculaTrainerPage.set_residential_type('Singapore')`
  - Error locator & key: `data-for="residentialType"`, CSS selector `.error[data-for='residentialType']`, helper `get_error_text("residentialType")`, `is_error_visible("residentialType")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Open Create Trainer page` | Singapore radio selected by default; Country/Region automatically set to Singapore and disabled. |

  **Expected Result:**
  - Field lỗi: `residentialType` (thuộc tính `data-for="residentialType"`)
  - Text lỗi thực tế trên UI: `"N/A"`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_SG_002 — Postal Code 6 digits - Auto-fill (569933)
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Auto-populates Block: "10" and Street: "Ang Mo Kio Avenue 5".
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP / BVA

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.POSTAL_CODE / BLOCK_NUMBER / STREET_NAME` = `"#postalCode"`
  - Action method: `CurriculaTrainerPage.set_postal_code('569933')`
  - Error locator & key: `data-for="postalCode"`, CSS selector `.error[data-for='postalCode']`, helper `get_error_text("postalCode")`, `is_error_visible("postalCode")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Postal Code = "569933"` | Auto-populates Block: "10" and Street: "Ang Mo Kio Avenue 5". |

  **Expected Result:**
  - Field lỗi: `postalCode` (thuộc tính `data-for="postalCode"`)
  - Text lỗi thực tế trên UI: `"Enter a valid postal code."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_SG_003 — Postal Code - Malformed 5 digits rejection
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System rejects postal code without exactly 6 digits, displays inline validation, and does not create Trainer Account.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | BVA / EP

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.POSTAL_CODE` = `"#postalCode"`
  - Action method: `CurriculaTrainerPage.set_postal_code('12345')`
  - Error locator & key: `data-for="postalCode"`, CSS selector `.error[data-for='postalCode']`, helper `get_error_text("postalCode")`, `is_error_visible("postalCode")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Postal Code = "12345"` | System rejects postal code without exactly 6 digits, displays inline validation, and does not create Trainer Account. |

  **Expected Result:**
  - Field lỗi: `postalCode` (thuộc tính `data-for="postalCode"`)
  - Text lỗi thực tế trên UI: `"Enter a valid postal code."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="postalCode", message_contains="Enter a valid postal code.")`

### TC_SG_004 — Floor/Unit N/A - Checking disables inputs
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Floor and Unit disabled and no longer mandatory per FSD. Pre-existing values retained under Working Assumption CQ-04, pending BA/PO confirmation.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | Decision Table

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.FLOOR_NOT_APPLICABLE` = `"#floorNotApplicable"`
  - Action method: `CurriculaTrainerPage.set_floor_not_applicable(True)`
  - Error locator & key: `data-for="floorUnit"`, CSS selector `.error[data-for='floorUnit']`, helper `get_error_text("floorUnit")`, `is_error_visible("floorUnit")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Check Floor/Unit number is not applicable` | Floor and Unit disabled and no longer mandatory per FSD. Pre-existing values retained under Working Assumption CQ-04, pending BA/PO confirmation. |
  | **[BUG-HUNTING CASE]** | `Check Floor/Unit number is not applicable` | Phát hiện lệch chuẩn (CQ-04) |

  **Expected Result:**
  - Field lỗi: `floorUnit` (thuộc tính `data-for="floorUnit"`)
  - Text lỗi thực tế trên UI: `"Floor and unit number are required."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại CQ-04.

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_SG_005 — Floor/Unit N/A - Unchecking restores required
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Floor and Unit inputs enabled and marked mandatory.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | Decision Table

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.FLOOR_NOT_APPLICABLE` = `"#floorNotApplicable"`
  - Action method: `CurriculaTrainerPage.set_floor_not_applicable(False)`
  - Error locator & key: `data-for="floorUnit"`, CSS selector `.error[data-for='floorUnit']`, helper `get_error_text("floorUnit")`, `is_error_visible("floorUnit")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Uncheck N/A checkbox` | Floor and Unit inputs enabled and marked mandatory. |

  **Expected Result:**
  - Field lỗi: `floorUnit` (thuộc tính `data-for="floorUnit"`)
  - Text lỗi thực tế trên UI: `"Floor and unit number are required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_SG_006 — Postal Code Fallback - Manual Block & Street
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Block and Street remain editable under Working Assumption CQ-03. Expected behavior on lookup failure pending BA/PO confirmation.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | Error Guessing

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.POSTAL_CODE / BLOCK_NUMBER / STREET_NAME` = `"#postalCode"`
  - Action method: `CurriculaTrainerPage.set_postal_code('999999')`
  - Error locator & key: `data-for="postalCode"`, CSS selector `.error[data-for='postalCode']`, helper `get_error_text("postalCode")`, `is_error_visible("postalCode")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Postal = "999999", Block: "888", Street: "Custom St"` | Block and Street remain editable under Working Assumption CQ-03. Expected behavior on lookup failure pending BA/PO confirmation. |
  | **[BUG-HUNTING CASE]** | `Postal = "999999", Block: "888", Street: "Custom St"` | Phát hiện lệch chuẩn (CQ-03) |

  **Expected Result:**
  - Field lỗi: `postalCode` (thuộc tính `data-for="postalCode"`)
  - Text lỗi thực tế trên UI: `"Enter a valid postal code."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại CQ-03.

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_SG_007 — Block Number - Max 10 chars (FSD 4.4.1)
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System accepts Block Number up to 10 characters per FSD Section 4.4.1. [Mock App Deviation: only allows 9 characters -> BUG-007.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | BVA Max

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.BLOCK_NUMBER` = `"#blockNumber"`
  - Action method: `CurriculaTrainerPage.type_field(BLOCK_NUMBER, ...)`
  - Error locator & key: `data-for="blockNumber"`, CSS selector `.error[data-for='blockNumber']`, helper `get_error_text("blockNumber")`, `is_error_visible("blockNumber")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `String of 10 characters ("1234567890")` | System accepts Block Number up to 10 characters per FSD Section 4.4.1. [Mock App Deviation: only allows 9 characters -> BUG-007.] |
  | **[BUG-HUNTING CASE]** | `String of 10 characters ("1234567890")` | Phát hiện lệch chuẩn (BUG-007) |

  **Expected Result:**
  - Field lỗi: `blockNumber` (thuộc tính `data-for="blockNumber"`)
  - Text lỗi thực tế trên UI: `"N/A"`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-007.

  **Nhãn Exceptor:**
  - `Exceptor.expect_bug_if_rejected(curricula.get_state_snapshot(), field="blockNumber", context="BUG-007")`

### TC_SG_008 — Street Name - Exceeds 100 chars (BVA Max+1)
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System does not accept Street Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 100 characters -> BUG-007.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | BVA Max+1

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.STREET_NAME` = `"#streetName"`
  - Action method: `CurriculaTrainerPage.type_field(STREET_NAME, ...)`
  - Error locator & key: `data-for="streetName"`, CSS selector `.error[data-for='streetName']`, helper `get_error_text("streetName")`, `is_error_visible("streetName")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `String of 101 characters ("A"*101)` | System does not accept Street Name exceeding 100 characters. Trainer Account is not created until data complies with maximum limit. [Mock App Deviation: allows exceeding 100 characters -> BUG-007.] |
  | **[BUG-HUNTING CASE]** | `String of 101 characters ("A"*101)` | Phát hiện lệch chuẩn (BUG-007) |

  **Expected Result:**
  - Field lỗi: `streetName` (thuộc tính `data-for="streetName"`)
  - Text lỗi thực tế trên UI: `"N/A"`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-007.

  **Nhãn Exceptor:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-007")`

### TC_SG_009 — Building Name - Optional field check
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Address saved successfully without error.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P3 | EP Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.BUILDING_NAME` = `"#buildingName"`
  - Action method: `CurriculaTrainerPage.type_field(BUILDING_NAME, '')`
  - Error locator & key: `data-for="buildingName"`, CSS selector `.error[data-for='buildingName']`, helper `get_error_text("buildingName")`, `is_error_visible("buildingName")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Building Name = ""` | Address saved successfully without error. |

  **Expected Result:**
  - Field lỗi: `buildingName` (thuộc tính `data-for="buildingName"`)
  - Text lỗi thực tế trên UI: `"N/A"`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_SG_010 — Singapore Address - Empty Postal Code
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid postal code." -> BUG-008.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Negative

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.POSTAL_CODE` = `"#postalCode"`
  - Action method: `CurriculaTrainerPage.set_postal_code('')`
  - Error locator & key: `data-for="postalCode"`, CSS selector `.error[data-for='postalCode']`, helper `get_error_text("postalCode")`, `is_error_visible("postalCode")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Postal Code = ""` | Displays standard mandatory error: "This field is required." [Mock App Deviation: shows "Enter a valid postal code." -> BUG-008.] |
  | **[BUG-HUNTING CASE]** | `Postal Code = ""` | Phát hiện lệch chuẩn (BUG-008) |

  **Expected Result:**
  - Field lỗi: `postalCode` (thuộc tính `data-for="postalCode"`)
  - Text lỗi thực tế trên UI: `"Enter a valid postal code."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-008.

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="postalCode", message_contains="Enter a valid postal code.")`

### TC_SG_011 — Floor/Unit - Empty when N/A is unchecked
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays "This field is required." beneath Floor Number and Unit Number; Trainer Account is not created.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Negative

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.FLOOR_NUMBER / UNIT_NUMBER` = `"#floorNumber, #unitNumber"`
  - Action method: `CurriculaTrainerPage.leave empty`
  - Error locator & key: `data-for="floorUnit"`, CSS selector `.error[data-for='floorUnit']`, helper `get_error_text("floorUnit")`, `is_error_visible("floorUnit")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Floor = "", Unit = "", N/A = Unchecked` | Displays "This field is required." beneath Floor Number and Unit Number; Trainer Account is not created. |
  | **[BUG-HUNTING CASE]** | `Floor = "", Unit = "", N/A = Unchecked` | Phát hiện lệch chuẩn (BUG-008) |

  **Expected Result:**
  - Field lỗi: `floorUnit` (thuộc tính `data-for="floorUnit"`)
  - Text lỗi thực tế trên UI: `"Floor and unit number are required."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-008.

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="floorUnit", message_contains="Floor and unit number are required.")`


## TS-05 Non-Singapore Residential Address

### TC_NSG_001 — Non-SG Address - Switch to international form
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Country dropdown enabled, international address inputs displayed.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | Decision Table

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.RESIDENTIAL_TYPE_NON_SG` = `"input[value='Non-Singapore']"`
  - Action method: `CurriculaTrainerPage.set_residential_type('Non-Singapore')`
  - Error locator & key: `data-for="residentialType"`, CSS selector `.error[data-for='residentialType']`, helper `get_error_text("residentialType")`, `is_error_visible("residentialType")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Click Radio Non-Singapore` | Country dropdown enabled, international address inputs displayed. |

  **Expected Result:**
  - Field lỗi: `residentialType` (thuộc tính `data-for="residentialType"`)
  - Text lỗi thực tế trên UI: `"N/A"`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_NSG_002 — Non-SG Address - Country dropdown excludes SG
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Country list must NOT include "Singapore" (FSD 4.4.2). [Mock App Deviation: HTML line 382 includes Singapore -> BUG-003.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | Decision Table

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.COUNTRY_REGION` = `"#countryRegion"`
  - Action method: `CurriculaTrainerPage.select_country_region(...)`
  - Error locator & key: `data-for="countryRegion"`, CSS selector `.error[data-for='countryRegion']`, helper `get_error_text("countryRegion")`, `is_error_visible("countryRegion")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Open Country/region dropdown` | Country list must NOT include "Singapore" (FSD 4.4.2). [Mock App Deviation: HTML line 382 includes Singapore -> BUG-003.] |
  | **[BUG-HUNTING CASE]** | `Open Country/region dropdown` | Phát hiện lệch chuẩn (BUG-003) |

  **Expected Result:**
  - Field lỗi: `countryRegion` (thuộc tính `data-for="countryRegion"`)
  - Text lỗi thực tế trên UI: `"N/A"`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-003.

  **Nhãn Exceptor:**
  - `Exceptor.expect_bug_if_rejected(curricula.get_state_snapshot(), field="countryRegion", context="BUG-003")`

### TC_NSG_003 — Non-SG Address - Complete valid address
- **Mô tả nghiệp vụ gốc (FSD Standard)**: International address saved successfully.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.NON_SG_ADDRESS` = `"#address1, #city"`
  - Action method: `CurriculaTrainerPage.set_non_singapore_address(...)`
  - Error locator & key: `data-for="address1"`, CSS selector `.error[data-for='address1']`, helper `get_error_text("address1")`, `is_error_visible("address1")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Country: "Malaysia", Addr1: "123 Jalan Ampang", City: "KL"` | International address saved successfully. |

  **Expected Result:**
  - Field lỗi: `address1` (thuộc tính `data-for="address1"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_NSG_004 — Address Line 1 - Empty mandatory check
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays inline error: "This field is required."
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Negative

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.ADDRESS_1` = `"#address1"`
  - Action method: `CurriculaTrainerPage.type_field(ADDRESS_1, '')`
  - Error locator & key: `data-for="address1"`, CSS selector `.error[data-for='address1']`, helper `get_error_text("address1")`, `is_error_visible("address1")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Address Line 1 = ""` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Field lỗi: `address1` (thuộc tính `data-for="address1"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="address1", message_contains="This field is required.")`

### TC_NSG_005 — City - Empty mandatory check
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Displays inline error: "This field is required."
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Negative

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.CITY` = `"#city"`
  - Action method: `CurriculaTrainerPage.type_field(CITY, '')`
  - Error locator & key: `data-for="city"`, CSS selector `.error[data-for='city']`, helper `get_error_text("city")`, `is_error_visible("city")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `City = ""` | Displays inline error: "This field is required." |

  **Expected Result:**
  - Field lỗi: `city` (thuộc tính `data-for="city"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="city", message_contains="This field is required.")`

### TC_NSG_006 — Address Line 1 - Boundary Max 255 chars
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System accepts all 255 valid characters on Address Line 1.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | BVA Max

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.ADDRESS_1` = `"#address1"`
  - Action method: `CurriculaTrainerPage.type_field(ADDRESS_1, 'A'*255)`
  - Error locator & key: `data-for="address1"`, CSS selector `.error[data-for='address1']`, helper `get_error_text("address1")`, `is_error_visible("address1")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `String of 255 characters ("A"*255)` | System accepts all 255 valid characters on Address Line 1. |

  **Expected Result:**
  - Field lỗi: `address1` (thuộc tính `data-for="address1"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_NSG_007 — Non-Singapore Postal Code - Optional field
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Saved successfully without error.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | EP Valid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.POSTAL_CODE` = `"#postalCode"`
  - Action method: `CurriculaTrainerPage.type_field(POSTAL_CODE, '')`
  - Error locator & key: `data-for="postalCode"`, CSS selector `.error[data-for='postalCode']`, helper `get_error_text("postalCode")`, `is_error_visible("postalCode")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Postal Code = ""` | Saved successfully without error. |

  **Expected Result:**
  - Field lỗi: `postalCode` (thuộc tính `data-for="postalCode"`)
  - Text lỗi thực tế trên UI: `"Enter a valid postal code."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`


## TS-06 Save Action & System Logic

### TC_SAV_001 — Save - Success & Auto Trainer ID Generation
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Trainer Account is created; unique Trainer ID formatted as TRN + 6 sequential digits; Status is Active; hệ thống hiển thị "Trainer account has been created successfully." và điều hướng đến Trainer Details page.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | State Transition

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.SAVE_BTN` = `"#saveBtn"`
  - Action method: `CurriculaTrainerPage.save()`
  - Error locator & key: `data-for="successBox"`, CSS selector `.error[data-for='successBox']`, helper `get_error_text("successBox")`, `is_error_visible("successBox")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Complete valid form data` | Trainer Account is created; unique Trainer ID formatted as TRN + 6 sequential digits; Status is Active; hệ thống hiển thị "Trainer account has been created successfully." và điều hướng đến Trainer Details page. |

  **Expected Result:**
  - Field lỗi: `successBox` (thuộc tính `data-for="successBox"`)
  - Text lỗi thực tế trên UI: `"Trainer account has been created successfully."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_SAV_002 — Save - Empty mandatory fields submit
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Inline error messages displayed across all mandatory fields.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Negative

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.SAVE_BTN` = `"#saveBtn"`
  - Action method: `CurriculaTrainerPage.save()`
  - Error locator & key: `data-for="multiple fields"`, CSS selector `.error[data-for='multiple fields']`, helper `get_error_text("multiple fields")`, `is_error_visible("multiple fields")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Empty form` | Inline error messages displayed across all mandatory fields. |

  **Expected Result:**
  - Field lỗi: `multiple fields` (thuộc tính `data-for="multiple fields"`)
  - Text lỗi thực tế trên UI: `"This field is required."`

  **Nhãn Exceptor:**
  - `Exceptor.expect_rejection(curricula.get_state_snapshot(), field="multiple fields", message_contains="This field is required.")`

### TC_SAV_003 — Duplicate Email - Exact match prevention
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Creation blocked with error: "An account with this email address already exists." [Mock App Deviation: missing duplicate check -> BUG-001.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Invalid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.SAVE_BTN` = `"#saveBtn"`
  - Action method: `CurriculaTrainerPage.save()`
  - Error locator & key: `data-for="primaryEmail"`, CSS selector `.error[data-for='primaryEmail']`, helper `get_error_text("primaryEmail")`, `is_error_visible("primaryEmail")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Existing email: bob.wang@curricula.edu.sg` | Creation blocked with error: "An account with this email address already exists." [Mock App Deviation: missing duplicate check -> BUG-001.] |
  | **[BUG-HUNTING CASE]** | `Existing email: bob.wang@curricula.edu.sg` | Phát hiện lệch chuẩn (BUG-001) |

  **Expected Result:**
  - Field lỗi: `primaryEmail` (thuộc tính `data-for="primaryEmail"`)
  - Text lỗi thực tế trên UI: `"An account with this email address already exists."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-001.

  **Nhãn Exceptor:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-001")`

### TC_SAV_004 — Duplicate Email - Case-insensitive match
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Case-insensitive check blocks creation and displays duplicate error. [Mock App Deviation: missing duplicate check -> BUG-001.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Invalid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.SAVE_BTN` = `"#saveBtn"`
  - Action method: `CurriculaTrainerPage.save()`
  - Error locator & key: `data-for="primaryEmail"`, CSS selector `.error[data-for='primaryEmail']`, helper `get_error_text("primaryEmail")`, `is_error_visible("primaryEmail")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `BOB.WANG@CURRICULA.EDU.SG` | Case-insensitive check blocks creation and displays duplicate error. [Mock App Deviation: missing duplicate check -> BUG-001.] |
  | **[BUG-HUNTING CASE]** | `BOB.WANG@CURRICULA.EDU.SG` | Phát hiện lệch chuẩn (BUG-001) |

  **Expected Result:**
  - Field lỗi: `primaryEmail` (thuộc tính `data-for="primaryEmail"`)
  - Text lỗi thực tế trên UI: `"An account with this email address already exists."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-001.

  **Nhãn Exceptor:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-001")`

### TC_SAV_005 — Duplicate ID Number - Exact match check
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Creation blocked with error: "An account with this ID number already exists." [Mock App Deviation: missing duplicate check -> BUG-002.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | EP Invalid

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.SAVE_BTN` = `"#saveBtn"`
  - Action method: `CurriculaTrainerPage.save()`
  - Error locator & key: `data-for="idNumber"`, CSS selector `.error[data-for='idNumber']`, helper `get_error_text("idNumber")`, `is_error_visible("idNumber")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Existing ID: G7666564N` | Creation blocked with error: "An account with this ID number already exists." [Mock App Deviation: missing duplicate check -> BUG-002.] |
  | **[BUG-HUNTING CASE]** | `Existing ID: G7666564N` | Phát hiện lệch chuẩn (BUG-002) |

  **Expected Result:**
  - Field lỗi: `idNumber` (thuộc tính `data-for="idNumber"`)
  - Text lỗi thực tế trên UI: `"An account with this ID number already exists."`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-002.

  **Nhãn Exceptor:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-002")`

### TC_SAV_006 — Concurrency - Multiple Save clicks handling
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Only one account creation request is processed and exactly one Trainer Account/Trainer ID is generated. The system must not create duplicate records when the user clicks Save multiple times (Error Guessing -> BUG-004).
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | Error Guessing

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.SAVE_BTN` = `"#saveBtn"`
  - Action method: `CurriculaTrainerPage.double click save`
  - Error locator & key: `data-for="concurrency"`, CSS selector `.error[data-for='concurrency']`, helper `get_error_text("concurrency")`, `is_error_visible("concurrency")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Complete valid form` | Only one account creation request is processed and exactly one Trainer Account/Trainer ID is generated. The system must not create duplicate records when the user clicks Save multiple times (Error Guessing -> BUG-004). |
  | **[BUG-HUNTING CASE]** | `Complete valid form` | Phát hiện lệch chuẩn (BUG-004) |

  **Expected Result:**
  - Field lỗi: `concurrency` (thuộc tính `data-for="concurrency"`)
  - Text lỗi thực tế trên UI: `"Single account processed"`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-004.

  **Nhãn Exceptor:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-004")`

### TC_SAV_007 — Trainer ID - Sequential increment rule
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Trainer ID follows sequential increment TRN + 6 digits.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | State Transition

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.SUCCESS_BOX` = `"#successBox"`
  - Action method: `CurriculaTrainerPage.get_success_text()`
  - Error locator & key: `data-for="trainerId"`, CSS selector `.error[data-for='trainerId']`, helper `get_error_text("trainerId")`, `is_error_visible("trainerId")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Valid form` | Trainer ID follows sequential increment TRN + 6 digits. |
  | **[BUG-HUNTING CASE]** | `Valid form` | Phát hiện lệch chuẩn (CQ-06) |

  **Expected Result:**
  - Field lỗi: `trainerId` (thuộc tính `data-for="trainerId"`)
  - Text lỗi thực tế trên UI: `"Sequential TRN+6 digits"`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại CQ-06.

  **Nhãn Exceptor:**
  - `Exceptor.expect_bug_if_rejected(curricula.get_state_snapshot(), field="trainerId", context="CQ-06")`

### TC_SAV_008 — Data Hygiene - Automatic whitespace trim
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System automatically trims whitespace before database persistence.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | Error Guessing

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.SAVE_BTN` = `"#saveBtn"`
  - Action method: `CurriculaTrainerPage.save()`
  - Error locator & key: `data-for="successBox"`, CSS selector `.error[data-for='successBox']`, helper `get_error_text("successBox")`, `is_error_visible("successBox")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Name & Email with surrounding spaces` | System automatically trims whitespace before database persistence. |

  **Expected Result:**
  - Field lỗi: `successBox` (thuộc tính `data-for="successBox"`)
  - Text lỗi thực tế trên UI: `"Whitespace auto-trimmed"`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`


## TS-07 Cancel Action & Form State

### TC_CAN_001 — Cancel - Clean form discard without prompt
- **Mô tả nghiệp vụ gốc (FSD Standard)**: User is navigated back to Trainer Listing page without a confirmation popup.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | State Transition

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.CANCEL_BTN` = `"#cancelBtn"`
  - Action method: `CurriculaTrainerPage.cancel()`
  - Error locator & key: `data-for="dialog"`, CSS selector `.error[data-for='dialog']`, helper `get_error_text("dialog")`, `is_error_visible("dialog")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Form with zero user inputs` | User is navigated back to Trainer Listing page without a confirmation popup. |

  **Expected Result:**
  - Field lỗi: `dialog` (thuộc tính `data-for="dialog"`)
  - Text lỗi thực tế trên UI: `"No confirmation dialog"`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_CAN_002 — Cancel - Unsaved changes -> Select "Stay"
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Dialog closes, all entered form data retained.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | Decision Table

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.CANCEL_BTN` = `"#cancelBtn"`
  - Action method: `CurriculaTrainerPage.cancel() -> dismiss dialog`
  - Error locator & key: `data-for="dialog"`, CSS selector `.error[data-for='dialog']`, helper `get_error_text("dialog")`, `is_error_visible("dialog")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Partially populated form` | Dialog closes, all entered form data retained. |

  **Expected Result:**
  - Field lỗi: `dialog` (thuộc tính `data-for="dialog"`)
  - Text lỗi thực tế trên UI: `"Data retained"`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_CAN_003 — Cancel - Unsaved changes -> Select "Leave"
- **Mô tả nghiệp vụ gốc (FSD Standard)**: Form changes discarded and user navigated back to Trainer Listing page.
- **Độ ưu tiên & Kỹ thuật thiết kế**: P1 | Decision Table

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.CANCEL_BTN` = `"#cancelBtn"`
  - Action method: `CurriculaTrainerPage.cancel() -> accept dialog`
  - Error locator & key: `data-for="dialog"`, CSS selector `.error[data-for='dialog']`, helper `get_error_text("dialog")`, `is_error_visible("dialog")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Partially populated form` | Form changes discarded and user navigated back to Trainer Listing page. |

  **Expected Result:**
  - Field lỗi: `dialog` (thuộc tính `data-for="dialog"`)
  - Text lỗi thực tế trên UI: `"Form reset"`

  **Nhãn Exceptor:**
  - `Exceptor.expect_success(curricula.get_state_snapshot())`

### TC_CAN_004 — Cancel - Detect Dirty State on Radio/Select
- **Mô tả nghiệp vụ gốc (FSD Standard)**: System recognizes Dirty State and displays Unsaved Changes prompt. [Mock App Deviation: misses radio/select elements -> BUG-006.]
- **Độ ưu tiên & Kỹ thuật thiết kế**: P2 | Error Guessing

  **Selector tham chiếu:**
  - Locator element: `CurriculaTrainerPage.CANCEL_BTN` = `"#cancelBtn"`
  - Action method: `CurriculaTrainerPage.cancel()`
  - Error locator & key: `data-for="dialog"`, CSS selector `.error[data-for='dialog']`, helper `get_error_text("dialog")`, `is_error_visible("dialog")`
  - Đánh giá Page Object: Đã có sẵn đầy đủ locator, action method và error inspection.

  **Test Data:**
  | Case | Giá trị input | Kỳ vọng |
  |---|---|---|
  | Test Input chính | `Modified Gender = Female or Nationality` | System recognizes Dirty State and displays Unsaved Changes prompt. [Mock App Deviation: misses radio/select elements -> BUG-006.] |
  | **[BUG-HUNTING CASE]** | `Modified Gender = Female or Nationality` | Phát hiện lệch chuẩn (BUG-006) |

  **Expected Result:**
  - Field lỗi: `dialog` (thuộc tính `data-for="dialog"`)
  - Text lỗi thực tế trên UI: `"Dirty state on radio/dropdown triggers dialog"`
  - Ghi chú sai lệch đã biết: Có sai lệch thực tế được ghi nhận tại BUG-006.

  **Nhãn Exceptor:**
  - `Exceptor.expect_bug_if_accepted(curricula.get_state_snapshot(), context="BUG-006")`

