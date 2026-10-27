# R3 Validation Rules

This document separates validation pages by signed-in role for development and automation test use.

## MOE Admin

### School Users

#### Page 1 — School User Management Validation

Page: `/school-users`

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| Search school users | No | No search validation is implemented. **(Assume...)** Search by Code, Username, Full name, or School. | None. |
| School assignment | Yes | School User must have an assignment to an Active School and can access only data for that School, as specified in R3 F02. | No page-level message is implemented; access must be enforced by authorization. |

##### List behavior

- Show Code, Username, Full name, School, and Actions.
- If no school is assigned, show `Unassigned in any school`.
- View opens the selected user’s details.
- Edit and Delete actions are shown. **(Assume...)** Edit opens the edit form; Delete asks for confirmation before deleting.
- Changing search or page size returns to page 1.
- Default page size is 10; options are 5, 10, and 25.

##### Messages

- Empty result: `No school users found`.
- Empty-result guidance: `Try changing the search.`
- Load error heading: `Unable to load school users`.
- Load error fallback: `Unable to load school users.` Show the API error message when available.
- Retry action: `Retry`.

##### Notes

- R3 F02 defines School User provisioning through CSV and Microsoft sign-in. It does not define list search fields or Edit/Delete behavior.
- Search fields and Edit/Delete behavior marked **(Assume...)** need confirmation.

---

#### Page 2 — Create School User (Single) Validation

Page: School Users → Create School User → Single tab

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| NRIC | Yes | Trim whitespace. Exactly 9 characters: 1 letter, 7 digits, 1 letter. | Blank: `NRIC is required.` Invalid format: `NRIC must be 1 letter, 7 digits and 1 letter (e.g. S1234567A).` |
| First name | Yes | Trim whitespace. Maximum 100 characters. | Blank: “Enter the user’s first name.” *(Assume message)* Over 100 characters: “First name cannot exceed 100 characters.” *(Assume message)* |
| Last name | Yes | Trim whitespace. Maximum 100 characters. | Blank: “Enter the user’s last name.” *(Assume message)* Over 100 characters: “Last name cannot exceed 100 characters.” *(Assume message)* |
| Email | Yes | Trim whitespace; validate email format in the browser. Maximum 100 characters. | Blank: “Enter the user’s email.” *(Assume message)* Invalid format: “Enter a valid email address.” *(Assume message)* Over 100 characters: “Email cannot exceed 100 characters.” *(Assume message)* |
| MOE school code | No | Optional in this form. If provided: 3–20 characters; letters, numbers, and hyphens only; must match an existing Active School. | Invalid format: `MOE school code must be between 3 and 20 characters.` / `MOE school code must contain only alphanumeric characters and hyphens.` Unknown school: `School code '{moeSchoolCode}' does not exist.` Inactive school: `School '{school.Code}' is inactive.` |

##### Create behavior

- Disable **Create** while a required field is blank or the create request is in progress.
- On API failure, show the API error when available; otherwise show: `The school user could not be created.`
- On success, show `School user created` and `The school user was created successfully.`
- **Reset** clears all fields and the created-user result.

##### Notes

- The screenshot and current form code mark MOE school code optional. R3 F02 requires a School ID for CSV import and says School Users need an Active School assignment for access. Confirm how the optional single-create field aligns with this assignment rule.
- R3 F02 specifies CSV provisioning with School User Email, Full Name, and School ID. This Single form uses NRIC, first name, last name, email, and optional MOE school code.
- NRIC format and school-code checks are implemented in backend validators/handler. The 100-character limits for first name, last name, and email come from database column limits; the create flow has no dedicated length-error message for them.

---

#### Page 3 — Bulk Create School Users Validation

Page: School Users → Create School User → Bulk CSV tab

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| CSV file | Yes | Select one `.csv` file. Import accepts up to 1,000 non-empty user rows. | No file selected: `Please choose a CSV file.` Empty file: `The CSV file is empty.` Over 1,000 rows: `The CSV file may contain at most 1000 rows.` |
| CSV headers | Yes | Include: `No`, `School User NRIC`, `School User Email`, `First Name`, `Last Name`, `School Code (optional)`. Header matching is case-insensitive. | Missing header: `Missing CSV column: {header}` |
| NRIC | Yes | Exactly 9 characters: 1 letter, 7 digits, 1 letter. Must be unique among existing users. | Blank: `NRIC is required.` Invalid: `NRIC must contain 1 letter, 7 digits, and 1 letter.` Duplicate: `User with NRIC '{username}' already exists.` |
| School User Email | Yes | Valid email; maximum 100 characters; must be unique among existing users. | Blank or invalid: `A valid Email is required.` Duplicate: `User with email '{email}' already exists.` |
| First Name | Yes | Maximum 100 characters. | Blank: `First Name is required.` Over 100 characters: “First Name cannot exceed 100 characters.” *(Assume message)* |
| Last Name | Yes | Maximum 100 characters. | Blank: `Last Name is required.` Over 100 characters: “Last Name cannot exceed 100 characters.” *(Assume message)* |
| School Code (optional) | No | If provided: 3–20 characters; letters, numbers, and hyphens only; must match an existing Active School. | Length: `MOE school code must be between 3 and 20 characters.` Invalid characters: `MOE school code must contain only alphanumeric characters and hyphens.` Unknown school: `School code '{code}' does not exist.` Inactive school: `School '{code}' is inactive.` |

##### Import behavior

- Ignore rows where all user-data fields are blank.
- Report each successful and failed row with its row number and reason. Continue processing other rows when a row fails.
- For malformed CSV, show: `Invalid CSV format near line {line}: {details}`.
- If a row contains too many columns, show: `CSV row {rowNumber} contains too many columns.`
- If the import request fails, show the API error when available; otherwise show: `The bulk import could not be completed.`
- **Reset** clears the selected file and import result.

##### Notes

- The template download is an `.xlsx` file, while the upload accepts `.csv`; save the completed template as CSV before importing.
- R3 F02 specifies School User Email, Full Name, and School ID as required CSV data. The current template instead has separate first/last names and an optional School Code. Confirm the template fields against F02.

---

### School Management

#### Page 1 — School Management List Validation

Page: `/school-management`

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| Search | No | Search by MOE school code or school name. Trim spaces before searching. No maximum length is defined. | None. |
| School type | No | Select `All school types` or one type: Government, Government aided, Autonomous, Independent, Specialised. | None. |
| MOE school code (inline edit) | Yes | 3–20 characters; letters, numbers, and hyphens only; unique across schools. | Required: `MOE school code is required.` Length: `MOE school code must be between 3 and 20 characters.` Invalid characters: `MOE school code must contain only alphanumeric characters and hyphens.` Duplicate: `A school with MOE code '{code}' already exists.` |
| School name (inline edit) | Yes | Maximum 150 characters. | Required: `School name is required.` Over 150 characters: `School name cannot exceed 150 characters.` |

##### List behavior

- Show MOE school code, School name, School type, Active classes, Active students, and Actions.
- **Search** applies the search text and selected school type. Changing school type applies the filter and resets to page 1.
- **Reset filters** clears the search and sets school type to All school types.
- View opens school details. Edit opens inline editing. Deactivate is shown; its current handler has no action.
- Page size defaults to 10; options are 5, 10, and 25. Changing page size resets to page 1.
- F01: School code must be unique. An Inactive School cannot be used for new School User assignments, academic configuration, or fee publications. Do not permanently delete a School that has assignments, enrolments, or Student Charges.

##### Messages

- Empty result: `No schools found`.
- Empty-result guidance: `Try changing your search or school type filter.`
- Load error heading: `Unable to load schools`.
- Load error fallback: `The school list could not be loaded. Please try again.` Show the API error when available.
- Retry action: `Try again`.
- Inline edit success: `School updated successfully.`
- Inline edit error heading: `Unable to update school`.
- Inline edit error fallback: `The school could not be updated. Please try again.` Show the API error when available.

##### Notes

- F01 requires School Code to be unique. The current inline edit flow does not perform a separate duplicate check; rely on the API response and show its message.
- Deactivate is visible in the screenshot, but its handler is not implemented in the current page code.

#### Page 2 — Create a School Validation

Page: `/school-management/new`

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| MOE school code | Yes | Trim spaces. 3–20 characters; letters, numbers, and hyphens only; unique across schools. | Blank: `MOE school code is required.` Length: `MOE school code must be between 3 and 20 characters.` Invalid characters: `MOE school code must contain only alphanumeric characters and hyphens.` Duplicate: `School with MOE code '{code}' already exists.` |
| School name | Yes | Trim spaces. Maximum 150 characters. | Blank: `School name is required.` Over 150 characters: `School name cannot exceed 150 characters.` |
| School type | Yes | Select one: Government, Government aided, Autonomous, Independent, Specialised. | Blank: `Select a school type.` Invalid value: `School type must be one of GOVERNMENT, GOVERNMENT_AIDED, AUTONOMOUS, INDEPENDENT, SPECIALISED.` |
| School users | No | Select zero or more users. | None. |
| Academic levels | Yes | Select at least one active academic level. | None selected: `Select at least one academic level.` |

##### Create behavior

- Do not submit while a required field is invalid. Show the form summary: `Please correct the errors below.`
- On success, show `School created` and `School created successfully.`
- On API failure, show the API error when available; otherwise show `The school could not be created. Please try again.`
- Keep entered values when creation fails.

##### Notes

- Academic Levels are required by the current form code, but the screenshot does not show a required marker beside the label.
- School Users are optional in the current form code, although the hint says “Select one or more users to associate with this school.”
- The School Type options shown here come from the current frontend. Confirm the allowed values against R3 before changing the list.

#### Page 3 — School Details Validation

Page: `/school-management/:schoolId`

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| School name, code, ID, type, status | N/A | Read-only. Show the selected School's saved details. | None. |
| Level offerings and classes | N/A | Read-only. Show each offering's academic year, level, status, and classes. | No offerings: `No level offerings configured.` No classes in an offering: `No classes configured` / `No classes are assigned to this offering.` |
| Students | N/A | Read-only. Show student, date of birth, enrolment status, and active class. | No students: `No students found` / `This school has no students yet.` No active class: `Not assigned`. |

##### Display behavior

- Show Total students, Active students, Level offerings, and Classes counts.
- Show Active academic years, Active offerings, and Students with a class in Quick summary.
- **Back to schools** returns to the School Management list.
- F01: Inactive Schools remain viewable, but cannot be used for new School User assignments, academic configuration, or fee publications.

##### Messages

- Loading: `Loading school details…`
- Load error heading: `Unable to load school details`.
- Load error fallback: `The school details could not be loaded.` Show the API error when available.
- Retry action: `Retry`.

---

### Students

#### Page 1 — Students List Validation

Page: `/student-management`

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| Search students | No | Search by student name or code. Spaces are trimmed by the API. No maximum length is defined. Changing the search returns to page 1. | None. |
| Rows per page | No | Default 10; options are 5, 10, and 25. Changing the size returns to page 1. | None. |
| Student, date of birth, category, school, class | N/A | Read-only list data. Show the current enrolled school and active class, when present. | No current enrolment: `Not enrolled`. No active class: `Not assigned`. |

##### List behavior

- Show Student (name and ID), Date of birth, Category, School, Class, and the View action.
- **View** opens the selected student's details.
- Show the total student count and page navigation. A School user sees students enrolled in their school; the System Admin list in the screenshot shows all students.
- The code shows **Create student** only for users with the `SCHOOL` role.

##### Messages

- Empty result: `No students found`.
- Empty-result guidance: `Try changing your search.`
- Load error heading: `Unable to load students`.
- Load error fallback: `The students could not be loaded.` Show the API error when available.
- Retry action: `Retry`.

---

### Fee Batches

#### Page 1 — Fee Publication Batches List Validation

Page: `/fee-batches`

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| Search fee batches | No | Enter search text and select **Search** to apply. Trim spaces before searching. No maximum length is defined. | None. |
| Status | No | Default `All statuses`; filter by `DRAFT`, `PROCESSING`, `COMPLETED`, `PARTIALLY_FAILED`, `FAILED`, or `PUBLISHED`. Changing status returns to page 1. | None. |
| Rows per page | No | Default 10; options are 10, 25, and 50. Changing page size returns to page 1. | None. |

##### List behavior

- Show Title, Fee component, Period, School scope, Publications, Status, Created at, and Actions.
- **View details** opens the selected fee batch.
- **Reset filters** clears search and returns Status to All statuses; disabled when no filters are set.
- Show total count and page navigation.

##### Messages

- Empty result: `No fee publication batches found`.
- Empty-result guidance: `Try changing the filters or check back later.`
- Load error fallback: `Fee publication batches could not be loaded.` Show the API error when available.
- Retry action: `Try again`.

### Fees

#### Page 1 — Fee Management: Create Fee Type

Page: `/fee-management` → **Create fee type** dialog

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| Name | Yes | Trim spaces. Maximum 150 characters. | Blank: `Name is required.` Backend over 150: `Fee type name cannot exceed 150 characters.` (Form shows generic failure below.) |
| Description | Yes in the form | Trim spaces. Maximum 500 characters when provided. | Blank: `Description is required.` Backend over 500: `Description cannot exceed 500 characters.` (Form shows generic failure below.) |

##### Create behavior

- **Create** submits the fee type. **Cancel** or the close icon closes the dialog.
- On success, show `Fee record created` and close the dialog.
- On failure, show `Action failed` and `The fee record could not be created. Try again.` Keep entered values so the user can retry.

##### Notes

- R3 F09 requires saving Fee Type Name, Description, Ownership Scope, and Status. This dialog only collects Name and Description; ownership is taken from the signed-in user and no Status field is shown.
- The form requires Description, but the backend allows it to be blank. The form has no input length limits; the backend enforces Name ≤150 and Description ≤500 characters.

#### Page 2 — Fee Types List Validation

Page: `/fee-management`

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| Search fee types | No | Search by fee type code or name. Trim spaces and select **Search** to apply. No maximum length is defined. | None. |
| Rows per page | No | Default 10; options are 10, 25, and 50. Changing page size returns to page 1. | None. |

##### List behavior

- Show Code, Name, Description, Component count, Status, Belongs to, and Actions.
- Sort by Component count, ascending by default. Selecting the column header toggles sort direction.
- **View** or selecting the fee type name opens its details.
- **Reset filters** clears the search and is disabled when search is empty.
- Show total count and page navigation. School users see shared fee types and fee types belonging to their school.

##### Messages

- Empty result: `No fee types found`.
- Empty-result guidance: `Try changing the filters or check back later.`
- Load error: `Fee types could not be loaded. Try again.`
- Retry action: `Try again`.

---

## School User Admin

### School Configuration

#### Page 1 — School Configuration Validation

Page: `/school-config` (School User)

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| Academic year | No | Defaults to the active year; if none is active, defaults to the latest year. The screenshot shows no required marker. | None. |
| Education stages | Yes when adding levels | Select one or more available stages: Primary, Secondary, or Pre-University. Adding a stage adds all active levels in that stage; levels already configured are excluded. | None selected: `Select at least one education stage.` |
| Search academic levels | No | Filter by academic level code or name. No maximum length is defined. | No matches: `No academic levels found` / `Try changing the search or stage filter.` |
| Stage filter | No | Select All, Primary, Secondary, or Pre-University. | None. |
| Class code | Yes when adding a class | Trim spaces. 2–50 characters. Must be unique within the School, Academic Year, and Academic Level. | Blank: `Class code is required.` Length: `Class code must be between 2 and 50 characters.` Duplicate: `Class code '{classCode}' already exists for this offering.` |
| Class name | Yes when adding a class | Trim spaces. Maximum 100 characters. | Blank: `Class name is required.` Over 100 characters: `Class name cannot exceed 100 characters.` |

##### Page behavior

- Show the School, selected Academic Year, last updated details, total Academic Levels, and total Classes.
- Show configured levels grouped by stage. Selecting a level shows its classes, active student count, and status.
- **Add Academic Levels** adds all active levels for the selected stage(s). **Add Class** creates a class under the selected level.
- R3 F03: configure education stages separately for each Academic Year and do not create duplicate levels. R3 F04: Class Code is unique within the School, Academic Year, and Academic Level; retain classes from previous years.
- **Copy Previous Year** currently returns `School configuration mutation API is not available yet.`

##### Messages

- No School assigned: `School context is required` / `This page is only available to a school user assigned to a school.`
- No academic years: `No academic years found` / `Create an academic year before configuring this school.`
- No levels configured: `No academic levels are configured for this academic year.`
- No levels available to add: `All active academic levels are already configured.`
- No classes: `No classes configured` / `Add a class to start managing students for this level.`
- Add levels success: `Academic levels added` / `The selected academic levels have been added to this school.`
- Add levels failure: `Could not add academic levels` / `The selected academic levels could not be added.` Show the API error when available.
- Add class success: `Class added` / `The class has been added to this academic level.`
- Add class failure: `Could not add class` / `The class could not be added.` Show the API error when available.
- Load error heading: `Unable to load school configuration`.
- Load error fallback: `The school configuration could not be loaded. Please try again.` Show the API error when available.
- Retry action: `Try again`.

##### Notes

- R3 F03 says stages generate the corresponding levels. Current UI selects stages and adds all available active levels in those stages.
- The screenshot shows the main configuration page; the Add Academic Levels and Add Class field rules above come from the form code.

#### Page 2 — Class Management List Validation

Page: `/class-management` (School User)

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| Search by class code or name | No | Search by class code or class name. Trim spaces and select **Search** to apply. No maximum length is defined. | None. |
| Academic level filter | No | Filter by academic level name. Trim spaces and select **Search** to apply. No maximum length is defined. | None. |
| Academic year filter | No | Enter a numeric academic year, such as `2026`. Non-numeric input is ignored when applying the filter. | None. |
| Rows per page | No | Default 10; options are 5, 10, 25, and 50. Changing page size returns to page 1. | None. |

##### List behavior

- Show Class code, Class name, Academic level, Academic year, Enrolled students, Active students, and Actions.
- **Search** applies all filters and returns to page 1. **Reset filters** clears the filters and returns to page 1.
- **Create class** opens the create class page. **Detail** opens the selected class details.
- Show total count and page navigation. Classes are limited to the signed-in School.

##### Messages

- No School selected: `School context is required` / `A school must be selected before classes can be loaded or created.`
- Empty result: `No classes found`.
- Empty-result guidance: `Try changing the search or filters.`
- Load error heading: `Unable to load classes`.
- Load error fallback: `The class list could not be loaded. Please try again.` Show the API error when available.
- Retry action: `Try again`.

#### Page 3 — Create Class (Single) Validation

Page: `/class-management/new` → **Single** tab (School User)

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| Class code | Yes | Trim spaces. 2–50 characters. Must be unique within the selected school level offering. | Blank: `Class code is required.` Length: `Class code must be between 2 and 50 characters.` Duplicate: `Class code '{classCode}' already exists for this offering.` |
| Class name | Yes | Trim spaces. Maximum 100 characters. | Blank: `Class name is required.` Over 100 characters: `Class name cannot exceed 100 characters.` |
| School level offering | Yes on submit (no `*` shown) | Select one offering for this school; the choice sets the Academic Level and Academic Year for the class. | Missing: `Select a school level offering.` No matches: `No school level offerings found`. |

##### Create behavior

- **Create class** submits the class. Disable while submitting or when no School is selected.
- On success, show `Class created` / `Class created successfully.` and return to Class Management.
- On failure, show `Unable to create class` and the API error when available; otherwise show `The class could not be created. Please try again.`
- **Cancel** returns to Class Management.

##### Messages

- No School selected: `School context is required` / `A school must be selected before classes can be loaded or created.`
- Offering load error fallback: `The class list could not be loaded. Please try again.` Show **Try again** to retry.
- While loading offerings: `Loading offerings`.
- No School level offerings: `No school level offerings found`.

##### Notes

- The screenshot shows the **Single** tab. The page also has a **Bulk** tab; document its validation rules with its screenshot.
- The form has no client-side length limits. The backend enforces the 2–50 character Class Code and 100 character Class Name limits.

#### Page 4 — Create Classes (Bulk) Validation

Page: `/class-management/new` → **Bulk** tab (School User)

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| Class template | Yes | Upload one `.xlsx` template or CSV with Class Name, Class Code, and Academic Level columns. The template has a maximum of 1,000 class rows. | Empty: `The CSV file is empty.` Invalid columns: `Invalid class import template. Expected Class Name, Class Code, and Academic Level columns.` Empty file: `The selected file does not contain any class rows.` Over 1,000 rows: `The CSV file may contain at most 1000 rows.` |
| Class name (each row) | Yes | Trim spaces. Maximum 50 characters. | Blank: `Class name is required.` Over 50 characters: `Class name cannot exceed 50 characters.` |
| Class code (each row) | Yes | Trim spaces. 2–20 characters. Must be unique within the School Level Offering, including other rows in the same upload. | Blank: `Class code is required.` Length: `Class code must be between 2 and 20 characters.` Duplicate: `Class code '{classCode}' already exists for offering '{offeringId}'.` |
| Academic level (each row) | Yes | Must match a School Level Offering for this school. The selected offering supplies the Academic Year and Academic Level. | Missing offering: `No school level offering was found for row[s] {rows}. Update the Academic Level value in the preview.` Invalid offering: `School level offering '{offeringId}' does not exist.` |

##### Bulk create behavior

- **Get template** downloads an Excel template with Class Name, Class Code, and Academic Level columns. The Academic Level column provides a dropdown of this school's offerings.
- After upload, show an editable preview of the parsed rows. Resolve each Academic Level to a School Level Offering before submitting.
- Submit valid rows and report row-level failures. Show `Bulk class import completed` with successful and failed row counts.
- **Reset** clears the selected file, preview, and results. **Cancel** returns to Class Management.
- Disable **Submit classes** while parsing/submitting, when there are no rows, or when no school is selected.

##### Messages

- No School selected: heading `School context is required`; body `A school must be selected before classes can be created.`
- No school-level offerings for template: `Academic Levels cannot be empty.`
- Missing CSV column: `Missing CSV column: {column}`.
- Invalid CSV row: `CSV row {rowNumber} contains too many columns.`
- Malformed CSV: `Invalid CSV format near line {lineNumber}: {details}`.
- Offering lookup failure: `The school level offerings could not be loaded.`
- File read fallback: `The selected file could not be read.`
- Import failure fallback: `The bulk class import could not be completed.`

##### Notes

- Bulk import limits differ from Single: Class Name is at most 50 characters and Class Code is 2–20 characters.
- The upload hint says to upload the downloaded `.xlsx` or a CSV with the three displayed columns; the API request uses the resolved School Level Offering ID.

### Fee Batches

#### Page 5 — Fee Publication Batches List Validation

Page: `/fee-batches` (School User)

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| Search fee batches | No | Enter search text and select **Search** to apply. Trim spaces before searching. No maximum length is defined. | None. |
| Status | No | Default `All statuses`; filter by `DRAFT`, `PROCESSING`, `COMPLETED`, `PARTIALLY_FAILED`, `FAILED`, or `PUBLISHED`. Changing status returns to page 1. | None. |
| Rows per page | No | Default 10; options are 10, 25, and 50. Changing page size returns to page 1. | None. |

##### List behavior

- Show Title, Fee component, Period, School scope, Publications, Status, Created at, and Actions.
- **View details** opens the selected fee batch. Show total count and page navigation.
- **Reset filters** clears search and returns Status to All statuses; disabled when no filters are set.

##### Messages

- Empty result: `No fee publication batches found`.
- Empty-result guidance: `Try changing the filters or check back later.`
- Load error fallback: `Fee publication batches could not be loaded.` Show the API error when available.
- Retry action: `Try again`.

### Fee Management

#### Page 6 — Fee Management List Validation

Page: `/fee-management` (School User)

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| Search fee types | No | Search by fee type code or name. Trim spaces and select **Search** to apply. No maximum length is defined. | None. |
| Rows per page | No | Default 10; options are 10, 25, and 50. Changing page size returns to page 1. | None. |

##### List behavior

- Show Code, Name, Description, Component count, Status, Belongs to, and Actions.
- Sort by Component count, ascending by default. Selecting the column header toggles sort direction.
- **View** or selecting the fee type name opens its details. **Create fee type** opens the create dialog.
- **Reset filters** clears the search and is disabled when search is empty.
- Show total count and page navigation. School users see shared fee types and fee types belonging to their school.

##### Messages

- Empty result: `No fee types found`.
- Load error: `Fee information could not be loaded. Try again.`
- Retry action: `Try again`.

#### Page 7 — Create Fee Type Validation

Page: `/fee-management` → **Create fee type** dialog (School User)

##### Field rules

| Field | Required | Rule | Message |
|---|---|---|---|
| Name | Yes | Trim spaces. Maximum 150 characters. | Blank: `Name is required.` Over 150 characters: backend returns `Fee type name cannot exceed 150 characters.` |
| Description | Yes in the form | Trim spaces. Maximum 500 characters when provided. | Blank: `Description is required.` Over 500 characters: backend returns `Description cannot exceed 500 characters.` |

##### Create behavior

- **Create** submits the fee type with the School User's school assignment. **Cancel** or the close icon closes the dialog.
- On success, show `Fee record created` and close the dialog.
- On failure, show `Action failed` / `The fee record could not be created. Try again.` Keep entered values so the user can retry.

##### Notes

- The form has no input length limits. The backend allows a blank Description, but the form requires it.

---

