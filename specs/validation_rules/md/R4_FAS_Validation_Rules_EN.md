# R4_FAS_Validation_Rules_EN


VALIDATION RULES DOCUMENT

Requirement R4, Function 4: Assess FAS and apply subsidies (FAS Applications)

For Dev. Based on FS F4 FAS Applications v1.1 dated 18/10/2026 and compared with the Figma prototype.

| Item | Content |
| :--- | :--- |
| Project | Agileproject, MOE finance system, EAFAMS |
| Document version | Draft 0.5 (Comprehensive Coverage - FAS Applications & Schemes), 25/10/2026 |
| Author | QA |
| Main source | [Agile] FS.docx of requirement R4 (FS F4 FAS Applications v1.1)<br>Figma prototype Edusave, canvas F4 FAS applications, 12 screens (A1 to A4, B1, B2, C1 to C4, D1, D2) |
| Other sources | Database Design Function Specification, Func4 v0.3<br>Product Backlog PB-17 to PB-21<br>Function tree |
| Companion files | R4_FAS_Seed_Data.sql<br>R4_FAS_Seed_Data_DB.xlsx<br>R4_FAS_Seed_Data_QA_Read.xlsx |
| Status | Updated with complete Scheme Management (F4.13-F4.16) and AI/ML Deny Rules (F4.19) |


# 1. Scope


| Screen | Content | Figma screen |
| :--- | :--- | :--- |
| A | FAS applications list, School Admin view | C1 and C4 |
| B | FAS applications list, MOE HQ view | A1 and A4 |
| C | SBFAS review drawer | C2 and D1 |
| D | MOEFAS review drawer | A2 and B1 |
| E | Approve SBFAS dialog | C3 |
| F | Approve MOEFAS dialog | A3 |
| G | Reject application dialog | B2 and D2 |
| H | FAS schemes list, MOE HQ and School Admin view | F4 Schemes (Canvas F4) |
| I | New scheme wizard (General, Eligibility, Subsidy, Review) | F4 New Scheme (Canvas F4) |
| J | Review and publish scheme (Overlap Prevention rules) | F4 Publish dialog |
| K | Add fee to a published scheme dialog | F4 Add fee dialog |
| L | AI/ML Need Score calculation and Deny Rules engine | FS F4 section 7.2 |


# 2. Conventions


| Item | Rule |
| :--- | :--- |
| Red number in a figure | Same as the field code in the heading below it, for example box A4 is section A4 |
| Source in FS | Section, business rule (BR) or scenario (T) behind the rule |
| Messages | Exact wording of FS section 8 and 9 |
| QA proposal | Not in the FS. BA must confirm before Dev builds it |
| Figure | Value read from a figure of the FS or from the Figma prototype |
| Figma state | A Figma screen that shows a case the FS has no figure for. Rules of the state are listed under the figure |
| Figma screen id | Letter and number of the Figma frame (A1 to D2), listed in Appendix C |
| All text input | Treated as data, never as code<br>Queries are parameterized<br>Output is encoded for HTML<br>Never parsed as JSON, XML, template or command<br>Control characters removed<br>Stored as Unicode |
| Language | English only |
| Role School Admin | Sees and decides SBFAS of the own school |
| Role MOE HQ | Sees all applications<br>Decides MOEFAS<br>Views SBFAS only |
| Statuses | Pending, Approved, Rejected |


# 3. Screen A. FAS applications list, School Admin view


Menu Financial assistance, FAS applications. Opens on the Pending tab. A School Admin sees SBFAS applications of the own school only. Source: FS 3.1, 3.3 to 3.5.

Figure A, Figma screen C1

## 3.1. Field summary


| Code | Field | Type |
| :--- | :--- | :--- |
| A1 | Export button | Button |
| A2 | Summary cards | Display only |
| A3 | Status tabs | Selection |
| A4 | Search box | Text input |
| A5 | Level filter | Selection |
| A6 | Class filter | Selection |
| A7 | Source filter | Selection |
| A8 | Tier filter | Selection |
| A9 | Status filter | Selection |
| A10 | ML risk filter | Selection |
| A11 | Submitted filter | Selection |
| A12 | Applications table | Display only |
| A13 | Review or View button | Button |
| A14 | Footer and paging | Display only |


## 3.2. Field rules


### A1. Export button


| Item | Rule |
| :--- | :--- |
| Function | Download the current list as CSV |
| Shown when | Always |
| Disabled when | File is being prepared |
| On click | Export all rows matching tab, filters and search (all pages, QA proposal)<br>Columns: Application, Student, NRIC/FIN, School/Class, Scheme, Source, Submitted, System check, ML, ML risk, Tier, Status<br>Dates as DD/MM/YYYY<br>School Admin file: own school SBFAS only<br>No matching row: header row only<br>File name: fas-applications_YYYYMMDD.csv (QA proposal) |
| On double click | One file |
| On error | Something went wrong. Please try again. |
| Source in FS | FS 3.1 item 1, 3.4, T29, BR13 |


| Code | Field | Shows | Rule | Source in FS |
| :--- | :--- | :--- | :--- | :--- |
| A2 | Summary cards | Pending (SBFAS waiting for the school)<br>SBFAS approved (this year)<br>SBFAS rejected (this year) | Own school only<br>Not affected by filters or search<br>Refresh after every decision | FS 3.1 item 2, section 9 |


### A3. Status tabs


| Item | Rule |
| :--- | :--- |
| Options | Pending<br>All<br>Approved<br>Rejected<br>Each tab shows its count in brackets when above 0, for example Pending (3) |
| Default | Pending |
| Required | One tab is always active |
| Depends on | None |
| On change | Show rows with that status<br>Back to page 1<br>Filters and search stay (QA proposal)<br>After a decision the row leaves Pending and counts refresh |
| Message | No applications found. when the tab is empty |
| Source in FS | FS 3.1 item 3, section 9, T24, T27 |


### A4. Search box


| Rule | Valid | Invalid | Message |
| :--- | :--- | :--- | :--- |
| Required | Empty or filled | None | None |
| Length | 0 to 100 characters | 101 or more characters | Text cut to 100.<br>Helper text: Search is limited to 100 characters. |
| Leading and trailing spaces | Removed before search | None | None |
| Spaces only | Treated as empty, no filter | None | None |
| Tab or line break | Replaced by one space | None | None |
| Control characters (U+0000 to U+001F, U+007F) | Removed | None | None |
| Null byte | Removed, never reaches the database | None | None |
| Allowed characters | Any printable character<br>Letters, digits, space, apostrophe, hyphen, slash, period | None | None |
| Special characters ' " % _ \ ; -- * ? ( ) [ ] | Plain text | None | % and _ are not wildcards<br>No regular expression |
| SQL string, for example ' OR 1=1 -- | Plain text, parameterized query | None | No result<br>No applications found. |
| Script, for example <script>alert(1)</script>, <img onerror>, javascript: | Plain text, never executed or rendered | None | No result<br>No applications found. |
| JSON, XML, template, for example {"a":1}, ${jndi:ldap://x}, $(whoami), ../../etc/passwd | Plain text, never parsed or evaluated | None | No result<br>No applications found. |
| Percent code, for example %27 | Plain text, not decoded | None | None |
| Emoji, letters of any script | Accepted as text | None | No applications found. when nothing matches |
| Matching | Contains<br>Ignore case<br>Student name, NRIC/FIN or Application ID | None | No applications found. when nothing matches |
| Trigger | Enter key<br>Or 300 ms after the last key (QA proposal) | None | None |
| Combined with | Tab and filters by AND, back to page 1 | None | None |
| Scope | School Admin searches own school SBFAS applications only | None | None |
| Valid examples | aisha<br>AISHA<br>t1801177h<br>1801177<br>APP-2026-00412<br>00412<br>Lee Zhi<br>d'souza<br>zzzz (no match) | None | None |
| Source in FS | FS 3.1 item 4, FS 3.3, FS 3.5, T26, T27 | FS 3.1 item 4, FS 3.3, FS 3.5, T26, T27 | FS 3.1 item 4, FS 3.3, FS 3.5, T26, T27 |


### A5. Level filter


| Item | Rule |
| :--- | :--- |
| Options | All<br>Levels of the own school, ascending |
| Default | All |
| Required | No |
| Depends on | None |
| On change | Table reloads on page 1<br>Class options limited to the level |
| Message | No applications found. when empty |
| Source in FS | FS 3.3 row Level |


### A6. Class filter


| Item | Rule |
| :--- | :--- |
| Options | All<br>Classes of the chosen level<br>All classes of the school when Level is All |
| Default | All |
| Required | No |
| Depends on | Level |
| On change | Table reloads on page 1<br>When Level changes and the class is not in the new level, Class returns to All (QA proposal) |
| Message | No applications found. when empty |
| Source in FS | FS 3.3 row Class |


### A7. Source filter


| Item | Rule |
| :--- | :--- |
| Options | All<br>Online<br>Paper |
| Default | All |
| Required | No |
| Depends on | None |
| On change | Table reloads on page 1 |
| Message | No applications found. when empty |
| Source in FS | FS 3.3 row Source |


### A8. Tier filter


| Item | Rule |
| :--- | :--- |
| Options | All<br>Tier 1<br>Tier 2<br>Tier 3 |
| Default | All |
| Required | No |
| Depends on | Tiers of the Active SBFAS scheme |
| On change | Table reloads on page 1<br>Decided application matches the tier granted<br>Pending application matches the tier ML suggests<br>ML Reject has no tier and shows only under All |
| Message | No applications found. when empty |
| Source in FS | FS 3.3 row Tier |


### A9. Status filter


| Item | Rule |
| :--- | :--- |
| Options | All<br>Pending<br>Approved<br>Rejected |
| Default | All |
| Required | No |
| Depends on | Status tab |
| On change | Table reloads on page 1 |
| Message | No applications found. when empty |
| Source in FS | FS 3.3 row Status, section 2.2 |


### A10. ML risk filter


| Item | Rule |
| :--- | :--- |
| Options | All<br>Low<br>Medium<br>High |
| Default | All |
| Required | No |
| Depends on | None |
| On change | Table reloads on page 1 |
| Message | No applications found. when empty |
| Source in FS | FS 3.3 row ML risk |


### A11. Submitted filter


| Item | Rule |
| :--- | :--- |
| Options | Last 7 days<br>Last 30 days<br>Any time |
| Default | Last 30 days |
| Required | One value is always selected |
| Depends on | None |
| On change | Table reloads on page 1<br>Days counted in Singapore time (UTC+8), today included (QA proposal) |
| Message | No applications found. when empty |
| Source in FS | FS 3.3 row Submitted |


| Code | Field | Shows | Rule | Source in FS |
| :--- | :--- | :--- | :--- | :--- |
| A12 | Applications table | Columns: Application, Student (name and NRIC/FIN), Class, Source, Submitted, ML suggestion, ML risk, Tier, Status | Sort: Submitted, newest first<br>10 rows per page<br>Application ID: APP-YYYY-NNNNN, unique, one line<br>Date: DD/MM/YYYY<br>Tier: filled only when Approved<br>ML suggestion: Tier X · High, Medium or Low need, or Reject<br>Another school's link: You do not have access to this application. | FS 3.4, 3.5, BR13, BR14, BR16, T2, T3, T4, T28, T31 |


### A13. Review or View button


| Item | Rule |
| :--- | :--- |
| Function | Open the review drawer of the row |
| Shown when | Review: Pending SBFAS application of the own school<br>View: every other row |
| On click | Drawer opens on the right over the list<br>Review: drawer has Reject and Approve<br>View: drawer is read only |
| On error | Decided by someone else after the list loaded: drawer opens read only<br>This application was already decided by {user} on {DD/MM/YYYY}.<br>Another school's application: You do not have access to this application. |
| Source in FS | FS 3.1 item 7, 3.5, section 4, section 8 |


| Code | Field | Shows | Rule | Source in FS |
| :--- | :--- | :--- | :--- | :--- |
| A14 | Footer and paging | Showing X to Y of Z and page controls | 10 rows per page<br>Page controls only when more than 10 results<br>New tab, filter or search goes to page 1<br>No result: footer hidden, No applications found. | FS 3.1 item 8, 3.5, T27, T28 |


## 3.3. Figma state C4: list after the School Admin approves application 00412


Figure A, Figma screen C4

| Item | Rule |
| :--- | :--- |
| Pending card | Goes from 3 to 2 after the decision<br>Figma C4 still shows 3 (conflict, see open point O22) |
| SBFAS approved card | Goes from 34 to 35 after the decision<br>Figma C4 still shows 34 (conflict, see open point O22) |
| SBFAS rejected card | Stays 9 |
| Tab counts | Pending (2)<br>All (46), unchanged<br>Approved (35)<br>Rejected (9) |
| Row of application 00412 | Leaves the Pending tab<br>Shows in the Approved tab<br>Tier shows Tier 3<br>Status shows Approved<br>Button shows View |
| Rows shown in the Approved tab | Figma shows 2 rows and the footer Showing 1–2 of 2 while the tab says Approved (35)<br>The Submitted filter is Last 30 days<br>Tab counts therefore do not follow the filters (open point O1 and O23) |
| Class column | Shows the class name, for example P3 Respect, P4 Diligence |
| Source in Figma | Screen C4, sticky note of screen C1 |


## 3.4. Open points of screen A


| Field | Open point |
| :--- | :--- |
| A1 Export button | FS does not give the export scope or file name. All pages and the file name are QA proposals. |
| A2 Summary cards | FS does not define this year (calendar or school year). |
| A3 Status tabs<br>A9 Status filter | FS does not say if tab counts follow filters and search, or what Pending tab plus Status Approved shows. Figure: All (46) with the 30 day filter. |
| A4 Search box | FS gives no maximum length, whitespace rule, trigger or special character rule. All are QA proposals. |
| A6 Class filter | Class reset on Level change is a QA proposal. |
| A8 Tier filter | Tier 4 and Ineligible exist in the engine (FS 5.3) but not in the Tier filter or the Tier dropdown (FS 1.3, 6.1). |
| A11 Submitted filter | Today included and Singapore time are QA proposals. |
| A12 Applications table | Figure: Application ID wraps into two lines (APP-2026-00 and 412). Show on one line. |
| A2 Summary cards<br>A3 Status tabs | Figma C4 does not update the cards after a decision (Pending 3 and SBFAS approved 34) but updates the tab counts (Pending 2, Approved 35). FS 9 says cards and tab counts update. |
| A4 Search box | Figma shows the placeholder cut off: Search student, NRIC/FIN or Application I. Show the full text or shorten it. |


# 4. Screen B. FAS applications list, MOE HQ view


Same page as the School Admin list. MOE HQ sees all schools, MOEFAS and SBFAS. Source: FS 3.2 to 3.5.

Figure B, Figma screen A1

## 4.1. Field summary


| Code | Field | Type |
| :--- | :--- | :--- |
| B1 | Export button | Button |
| B2 | Summary cards | Display only |
| B3 | Status tabs | Selection |
| B4 | Search box | Text input |
| B5 | School filter | Selection |
| B6 | Scheme filter | Selection |
| B7 | Level filter | Selection |
| B8 | Source filter | Selection |
| B9 | Tier filter | Selection |
| B10 | Status filter | Selection |
| B11 | ML risk filter | Selection |
| B12 | Submitted filter | Selection |
| B13 | Applications table | Display only |
| B14 | System check column | Display only |
| B15 | ML recommendation column | Display only |
| B16 | Review or View button | Button |
| B17 | Footer and paging | Display only |


## 4.2. Field rules


### B1. Export button


| Item | Rule |
| :--- | :--- |
| Function | Download the current list as CSV |
| Shown when | Always |
| Disabled when | File is being prepared |
| On click | Export all rows matching tab, filters and search (all pages, QA proposal)<br>Columns: Application, Student, NRIC/FIN, School/Class, Scheme, Source, Submitted, System check, ML, ML risk, Tier, Status<br>Dates as DD/MM/YYYY<br>MOE HQ file: all schools, MOEFAS and SBFAS, System check empty for SBFAS<br>No matching row: header row only<br>File name: fas-applications_YYYYMMDD.csv (QA proposal) |
| On double click | One file |
| On error | Something went wrong. Please try again. |
| Source in FS | FS 3.2 item 1, 3.4, T29 |


| Code | Field | Shows | Rule | Source in FS |
| :--- | :--- | :--- | :--- | :--- |
| B2 | Summary cards | Total applications<br>Pending MOEFAS (waiting for MOE HQ)<br>Pending SBFAS (waiting for schools)<br>Approved<br>Rejected | All schools<br>Not affected by filters or search<br>Refresh after every decision | FS 3.2 item 2, section 9 |


### B3. Status tabs


| Item | Rule |
| :--- | :--- |
| Options | Pending<br>All<br>Approved<br>Rejected<br>Count in brackets when above 0 |
| Default | Pending |
| Required | One tab is always active |
| Depends on | None |
| On change | Show rows with that status<br>Back to page 1<br>Pending contains MOEFAS and SBFAS waiting for a decision |
| Message | No applications found. when the tab is empty |
| Source in FS | FS 3.2 item 3 |


### B4. Search box


| Rule | Valid | Invalid | Message |
| :--- | :--- | :--- | :--- |
| Required | Empty or filled | None | None |
| Length | 0 to 100 characters | 101 or more characters | Text cut to 100.<br>Helper text: Search is limited to 100 characters. |
| Leading and trailing spaces | Removed before search | None | None |
| Spaces only | Treated as empty, no filter | None | None |
| Tab or line break | Replaced by one space | None | None |
| Control characters (U+0000 to U+001F, U+007F) | Removed | None | None |
| Null byte | Removed, never reaches the database | None | None |
| Allowed characters | Any printable character<br>Letters, digits, space, apostrophe, hyphen, slash, period | None | None |
| Special characters ' " % _ \ ; -- * ? ( ) [ ] | Plain text | None | % and _ are not wildcards<br>No regular expression |
| SQL string, for example ' OR 1=1 -- | Plain text, parameterized query | None | No result<br>No applications found. |
| Script, for example <script>alert(1)</script>, <img onerror>, javascript: | Plain text, never executed or rendered | None | No result<br>No applications found. |
| JSON, XML, template, for example {"a":1}, ${jndi:ldap://x}, $(whoami), ../../etc/passwd | Plain text, never parsed or evaluated | None | No result<br>No applications found. |
| Percent code, for example %27 | Plain text, not decoded | None | None |
| Emoji, letters of any script | Accepted as text | None | No applications found. when nothing matches |
| Matching | Contains<br>Ignore case<br>Student name, NRIC/FIN or Application ID | None | No applications found. when nothing matches |
| Trigger | Enter key<br>Or 300 ms after the last key (QA proposal) | None | None |
| Combined with | Tab and filters by AND, back to page 1 | None | None |
| Scope | MOE HQ searches all schools. School name is not searched | None | None |
| Valid examples | aisha<br>AISHA<br>t1801177h<br>1801177<br>APP-2026-00412<br>00412<br>Lee Zhi<br>d'souza<br>zzzz (no match) | None | None |
| Source in FS | FS 3.1 item 4, FS 3.3, FS 3.5, T26, T27 | FS 3.1 item 4, FS 3.3, FS 3.5, T26, T27 | FS 3.1 item 4, FS 3.3, FS 3.5, T26, T27 |


### B5. School filter


| Item | Rule |
| :--- | :--- |
| Options | All<br>All schools, alphabetical (QA proposal) |
| Default | All |
| Required | No |
| Depends on | None |
| On change | Table reloads on page 1 |
| Message | No applications found. when empty |
| Source in FS | FS 3.3 row School |


### B6. Scheme filter


| Item | Rule |
| :--- | :--- |
| Options | All<br>MOEFAS<br>SBFAS |
| Default | All |
| Required | No |
| Depends on | None |
| On change | Table reloads on page 1 |
| Message | No applications found. when empty |
| Source in FS | FS 3.3 row Scheme |


### B7. Level filter


| Item | Rule |
| :--- | :--- |
| Options | All<br>Levels of all schools |
| Default | All |
| Required | No |
| Depends on | None |
| On change | Table reloads on page 1 |
| Message | No applications found. when empty |
| Source in FS | FS 3.3 row Level |


### B8. Source filter


| Item | Rule |
| :--- | :--- |
| Options | All<br>Online<br>Paper |
| Default | All |
| Required | No |
| Depends on | None |
| On change | Table reloads on page 1 |
| Message | No applications found. when empty |
| Source in FS | FS 3.3 row Source |


### B9. Tier filter


| Item | Rule |
| :--- | :--- |
| Options | All<br>Tier 1<br>Tier 2<br>Tier 3 |
| Default | All |
| Required | No |
| Depends on | Tiers of MOEFAS and SBFAS |
| On change | Table reloads on page 1<br>Decided application matches the tier granted<br>Pending application matches the tier ML suggests |
| Message | No applications found. when empty |
| Source in FS | FS 3.3 row Tier |


### B10. Status filter


| Item | Rule |
| :--- | :--- |
| Options | All<br>Pending<br>Approved<br>Rejected |
| Default | All |
| Required | No |
| Depends on | Status tab |
| On change | Table reloads on page 1 |
| Message | No applications found. when empty |
| Source in FS | FS 3.3 row Status |


### B11. ML risk filter


| Item | Rule |
| :--- | :--- |
| Options | All<br>Low<br>Medium<br>High |
| Default | All |
| Required | No |
| Depends on | None |
| On change | Table reloads on page 1 |
| Message | No applications found. when empty |
| Source in FS | FS 3.3 row ML risk |


### B12. Submitted filter


| Item | Rule |
| :--- | :--- |
| Options | Last 7 days<br>Last 30 days<br>Any time |
| Default | Last 30 days |
| Required | One value is always selected |
| Depends on | None |
| On change | Table reloads on page 1<br>Singapore time, today included (QA proposal) |
| Message | No applications found. when empty |
| Source in FS | FS 3.3 row Submitted |


| Code | Field | Shows | Rule | Source in FS |
| :--- | :--- | :--- | :--- | :--- |
| B13 | Applications table | Columns: Application, Student, School, Scheme, Source, Submitted, System check, ML recommendation, ML risk, Tier, Status | No Class column<br>Sort: Submitted, newest first<br>10 rows per page<br>Application ID: APP-YYYY-NNNNN, unique, one line<br>Date: DD/MM/YYYY<br>Tier: filled only when Approved | FS 3.4, 3.5, BR13, BR14, BR16 |
| B14 | System check column | Pass or Fail for MOEFAS, a dash for SBFAS | Information only, never approves or rejects<br>Pass and Fail applications both stay Pending for MOE HQ | FS 3.4, BR1, BR6, T7 |
| B15 | ML recommendation column | MOEFAS: Grant · Tier X, Borderline, Do not grant<br>SBFAS: Tier X · High, Medium or Low need, or Reject | Rule: engine calculation, see Appendix A<br>Reference only | FS 3.4, 5.4, BR19 |


### B16. Review or View button


| Item | Rule |
| :--- | :--- |
| Function | Open the review drawer of the row |
| Shown when | Review: Pending MOEFAS application<br>View: all SBFAS rows and decided MOEFAS rows |
| On click | MOEFAS: opens the MOEFAS review drawer<br>SBFAS: opens the SBFAS review drawer read only<br>MOE HQ never decides SBFAS |
| On error | Decided by someone else after the list loaded: drawer opens read only<br>This application was already decided by {user} on {DD/MM/YYYY}. |
| Source in FS | FS 3.2 item 7, BR2, T1, T19 |


| Code | Field | Shows | Rule | Source in FS |
| :--- | :--- | :--- | :--- | :--- |
| B17 | Footer and paging | Showing X to Y of Z and page controls | 10 rows per page<br>Page controls only when more than 10 results<br>New tab, filter or search goes to page 1<br>No result: footer hidden, No applications found. | FS 3.2 item 8 |


## 4.3. Figma state A4: list after MOE HQ approves application 00377


Figure B, Figma screen A4

| Item | Rule |
| :--- | :--- |
| Total applications card | Stays 9 |
| Pending MOEFAS card | Goes from 3 to 2 |
| Pending SBFAS card | Stays 3 |
| Approved card | Goes from 2 to 3 |
| Rejected card | Stays 1 |
| Tab counts | Pending (5)<br>All (9)<br>Approved (3)<br>Rejected (1) |
| Row of application 00377 | Leaves the Pending tab<br>Shows in the Approved tab<br>System check keeps Fail<br>ML recommendation keeps Grant · Tier 3 and ML risk keeps Medium<br>Tier shows Tier 3<br>Status shows Approved<br>Button shows View |
| Rows shown in the Approved tab | Figma shows 2 rows (00377 and 00386) and the footer Showing 1–2 of 2 while the tab says Approved (3)<br>Tab counts do not follow the filters (open point O1 and O23) |
| Source in Figma | Screen A4 |


## 4.4. Open points of screen B


| Field | Open point |
| :--- | :--- |
| B2 Summary cards | Figure data conflicts with the School Admin figure (Approved 2 for all schools against 34 for one school). |
| B4 Search box | FS gives no maximum length, whitespace rule, trigger or special character rule. All are QA proposals. |
| B13 Applications table | Figure: Application ID wraps (APP-2026-0 and 0377). |
| B14 System check column | FS 3.4: Pass when all criteria pass. FS 4.2: Pass when nationality passes and at least one of GHI or PCI passes. The two differ when only one of GHI or PCI passes. |
| B15 ML recommendation column | Borderline never occurs with the current formula: within 5 percent over the limit the Need Score is at least 50.50, so the result is always Grant. Figure: header wraps into RECOMMENDA and TION. |
| B3 Status tabs<br>B17 Footer and paging | Figma A4 shows Approved (3) with 2 rows and Showing 1–2 of 2 under the 30 day filter. Tab counts and the footer do not use the same scope (open point O1). |
| B4 Search box | Figma shows the placeholder cut off: Search student, NRIC. Show the full text or shorten it. |


# 5. Screen C. SBFAS review drawer


Opens from Review or View of an SBFAS application. Slides in from the right. Closes with X or a click outside. All fields read only. Source: FS section 4.

Figure C, Figma screen C2

## 5.1. Field summary


| Code | Field | Type |
| :--- | :--- | :--- |
| C1 | Header | Display only |
| C2 | Student | Display only |
| C3 | Parent | Display only |
| C4 | Household and income | Display only |
| C5 | ML suggestion | Display only |
| C6 | Documents | Display only |


## 5.2. Field rules


| Code | Field | Shows | Rule | Source in FS |
| :--- | :--- | :--- | :--- | :--- |
| C1 | Header | SBFAS REVIEW, Application ID, student name, class, source | School Admin sees class, MOE HQ sees school<br>X closes the drawer<br>Another school: You do not have access to this application. | FS 4.1 item 1, T3 |
| C2 | Student | Full name, NRIC/FIN, Class, Citizenship (MOE HQ also sees School) | Citizenship: Singapore Citizen or PR<br>Non citizen student is always SBFAS<br>NRIC/FIN: letter, 7 digits, letter (QA proposal) | FS 4.1 item 4, BR18, T32 |
| C3 | Parent | Name and relationship, NRIC/FIN, Mobile, Email | Not editable<br>Phone and email format: FS 08 | FS 4.1 item 5 |
| C4 | Household and income | Gross household income (S$ per month), Household size, Per capita income (S$), Income source (API or Paper) | Not editable<br>Per capita income = gross household income / household size<br>Household size above 0<br>Amounts in S$ with thousands separators | FS 1.3, 4.1 item 6, BR11, BR16, 5.1 |
| C5 | ML suggestion | Suggestion only, Confidence, Risk, Need Score, Base Tier, Adjusted Tier, Fast-track, deny rule, Factors, Score breakdown | Rule: engine calculation, see Appendix A<br>Never approves<br>Warning when the school has no Active SBFAS scheme | FS 4.1 item 7, section 5, BR19, T33 to T35 |
| C6 | Documents | File name and View link | View opens the file<br>Only users with access to the application can open it | FS 4.1 item 8 |


## 5.3. Items in the FS that are not in the cropped figure


| Item | Source | Content in the FS |
| :--- | :--- | :--- |
| History | FS 4.1 item 9, 4.4 | Date and time, action, oldest first<br>Actions: Uploaded, Submitted, SBFAS application (not a Singapore Citizen), Eligibility check, Approved, Rejected, Email sent to parent, Moved to SBFAS, Paper application edited |
| Decision section | FS 4.3 | Shown when Approved or Rejected<br>Reject and Approve hidden<br>Shows Result, Tier, Effective from or Reason, Comment, decider, date and time |
| Reject and Approve buttons | FS 4.1 item 10 | School Admin of the school, Pending only<br>Reject opens the Reject dialog<br>Approve opens the Approve SBFAS dialog |


## 5.4. Figma state D1: drawer of a student who is not a Singapore Citizen or PR (application 00398)


Figure C, Figma screen D1

| Item | Rule |
| :--- | :--- |
| Header | SBFAS REVIEW, APP-2026-00398, Daniel Ong · P2 Care · Online |
| Student section | Figma shows two rows: Full name, Citizenship<br>FS 4.1 item 4 lists four rows: Full name, NRIC/FIN, Class, Citizenship<br>Open point O24 |
| Citizenship value | Figma shows International Student<br>The FS does not list the Citizenship values (open point O24) |
| Parent section | Not shown in Figma<br>FS 4.1 item 5 shows it for SBFAS (open point O24) |
| Household and income | Gross household income S$ 2,600 / month<br>Household size 3<br>Per capita income S$ 867<br>Income source API |
| ML suggestion | Reject, red box, tag Suggestion only<br>Confidence 88%<br>Factors: nationality not covered by the school's SBFAS · single parent<br>No Risk, Need score, Base Tier or Adjusted Tier line, although the list shows ML risk Medium (open point O24) |
| Documents section | Not shown in Figma<br>Online application, so no scanned file<br>FS 4.1 item 8 does not say what shows when there is no file (open point O24) |
| Buttons | Reject and Approve, both enabled<br>The reviewer may approve although the suggestion is Reject (BR19) |
| Source in Figma | Screen D1, sticky note of screen C1 |


## 5.5. Open points of screen C


| Field | Open point |
| :--- | :--- |
| C4 Household and income | Figure shows PCI S$ 1,088, stored value is 1,087.50. Dev data design rounds to two decimals, the display rule is not stated. |
| C5 ML suggestion | Figure has no Score breakdown and no warning. Confidence starts at 92 and only subtracts, so the maximum is 92, and subtracting everything gives 46, below the stated minimum 55. |
| C6 Documents | Dev data design lists PDF, JPG, PNG, 10 MB, 5 files. Not in FS F4. |
| C2 Student<br>C3 Parent<br>C5 ML suggestion<br>C6 Documents | Figma D1 (student who is not a Citizen or PR) shows fewer rows and sections than the FS and Figma C2, see the Figma state in section 5.3. Open point O24. |


# 6. Screen D. MOEFAS review drawer


Opens from Review of a Pending MOEFAS application. MOE HQ only. All fields read only. Source: FS section 4.

Figure D, Figma screen A2

## 6.1. Field summary


| Code | Field | Type |
| :--- | :--- | :--- |
| D1 | Header | Display only |
| D2 | Eligibility check | Display only |
| D3 | Household and income | Display only |
| D4 | ML recommendation | Display only |
| D5 | Reject button | Button |
| D6 | Approve MOEFAS button | Button |


## 6.2. Field rules


| Code | Field | Shows | Rule | Source in FS |
| :--- | :--- | :--- | :--- | :--- |
| D1 | Header | MOEFAS REVIEW, Application ID, student name, school, source | X closes the drawer | FS 4.1 item 1 |
| D2 | Eligibility check | Each criterion: value, limit, percent above limit, Pass or Fail | Only for MOEFAS<br>Limits from the Active scheme: Singapore Citizen, GHI up to S$ 4,000, PCI up to S$ 1,000<br>GHI and PCI are separate rows<br>Pass: nationality passes and GHI or PCI passes<br>Value equal to the limit passes (QA proposal)<br>Information only: MOE HQ can approve a Fail and reject a Pass | FS 4.1 item 3, 4.2, BR5, BR6, T6 |
| D3 | Household and income | Gross household income (S$ per month), Household size, Per capita income (S$), Income source (API or Paper) | Not editable<br>Per capita income = gross household income / household size<br>Household size above 0<br>Amounts in S$ with thousands separators<br>Visible to MOE HQ only | FS 4.1 item 6, BR11, BR13 |
| D4 | ML recommendation | Recommendation only, Confidence, Risk, Need Score, Base Tier, Adjusted Tier, Factors | Result: Grant · Tier X, Borderline or Do not grant<br>Rule: engine calculation, see Appendix A<br>Never approves | FS 4.1 item 7, 5.4, BR19, T5, T33 |


### D5. Reject button


| Item | Rule |
| :--- | :--- |
| Function | Open the Reject dialog |
| Shown when | MOE HQ, Pending MOEFAS |
| Hidden when | Application decided<br>SBFAS application |
| On click | Dialog opens<br>Drawer stays open behind it |
| Source in FS | FS 4.1 item 10, 4.3, T5, T22 |


### D6. Approve MOEFAS button


| Item | Rule |
| :--- | :--- |
| Function | Open the Approve MOEFAS dialog |
| Shown when | MOE HQ, Pending MOEFAS |
| Hidden when | Application decided |
| Disabled when | Never disabled, also enabled when System check is Fail |
| On click | Dialog opens<br>Drawer stays open behind it |
| Source in FS | FS 4.1 item 10, BR6, T5, T6 |


## 6.3. Figma state B1: drawer of a MOEFAS application that passes the system check (application 00390)


Figure D, Figma screen B1

| Item | Rule |
| :--- | :--- |
| Header | MOEFAS REVIEW, APP-2026-00390, Chen Xin Yi · Bukit View Primary · Online |
| Eligibility check rows | Nationality: Pass<br>Gross household income: S$ 2,900 (limit ≤ S$ 4,000)<br>Per capita income: S$ 580 (limit ≤ S$ 1,000)<br>Figma B1 shows value and limit and no badge on the income rows<br>Figma A2 (Fail case) shows the badge and no value or limit<br>FS 4.1 item 3: value, limit, percent above when above, and Pass or Fail<br>Open point O25 |
| Information note | Information only. MOE HQ can approve a Fail or reject a Pass. Shown in both Figma states |
| ML recommendation | Grant · Tier 2, tag Recommendation only<br>Confidence 66% · Risk High<br>Need score 77.97 / 100 · Base Tier 1 · Adjusted Tier 1<br>Factors: per capita income within the Tier 2 band · single income earner · 4 dependants<br>The recommended tier (Tier 2, scheme band match, FS 5.4) differs from the Adjusted Tier (Tier 1, Need Score) |
| Buttons | Reject and Approve MOEFAS<br>Reject opens the Reject dialog of Figma screen B2 (Figure G) |
| Source in Figma | Screen B1 |


## 6.4. Open points of screen D


| Field | Open point |
| :--- | :--- |
| D2 Eligibility check | Figure shows only Pass or Fail, not value, limit or percent above. FS 3.4: Pass when all criteria pass. FS 4.2: Pass when nationality passes and at least one of GHI or PCI passes. The two differ when only one of GHI or PCI passes. |
| D4 ML recommendation | Borderline never occurs with the current formula: within 5 percent over the limit the Need Score is at least 50.50, so the result is always Grant. |
| D2 Eligibility check | Figma B1 shows value and limit and no Pass or Fail badge on the income rows. Figma A2 shows only the badge. Open point O25. |
| D4 ML recommendation | Figma B1 shows Grant · Tier 2 with Adjusted Tier 1. Recommended tier and Adjusted Tier are two different values, both are shown. |


# 7. Screen E. Approve SBFAS dialog


Opens from Approve in the SBFAS drawer. School Admin of the school. Title carries the scheme name. Source: FS 6.1, sections 8 and 9.

Figure E, Figma screen C3

## 7.1. Field summary


| Code | Field | Type |
| :--- | :--- | :--- |
| E1 | Tier | Selection |
| E2 | Comment (optional) | Text input |
| E3 | Fees that will be subsidised | Display only |
| E4 | Cancel button | Button |
| E5 | Confirm approval button | Button |


## 7.2. Field rules


### E1. Tier


| Item | Rule |
| :--- | :--- |
| Options | Tier 1 · High need<br>Tier 2 · Medium need<br>Tier 3 · Low need |
| Default | Tier ML suggests, with hint ML suggests Tier X<br>No selection when ML gives Reject, no tier or Tier 4 (QA proposal) |
| Required | Yes |
| Depends on | Active scheme |
| On change | Fee list recalculates<br>Total subsidy recalculates |
| Message | Not chosen: Select a tier to approve. (QA proposal)<br>Confirm approval disabled<br>Scheme not Active: No active SBFAS scheme. |
| Source in FS | FS 6.1 item 1, BR8, section 8 |


### E2. Comment (optional)


| Rule | Valid | Invalid | Message |
| :--- | :--- | :--- | :--- |
| Required | Empty or filled | None | None |
| Length | 0 to 500 characters | 501 or more characters | Counter turns red, for example 501/500<br>Error: Comment must be 500 characters or fewer.<br>Confirm approval disabled |
| Counter | Shows n/500<br>Line break counts 1<br>Emoji counts 1 | None | None |
| Paste over 500 | Text is kept, not cut | None | Counter shows for example 600/500 in red |
| Leading and trailing spaces and blank lines | Removed on save | None | None |
| Spaces only | Saved as empty | None | None |
| Allowed characters | Any printable Unicode character<br>Line break and tab | None | None |
| Control characters other than line break and tab | Removed | None | None |
| Null byte | Removed before save | None | None |
| Special characters ' " % \ ; | Saved exactly as typed | None | None |
| SQL string, for example ' OR 1=1 -- | Saved as text, parameterized query | None | No data changed |
| Script and HTML, for example <script>, <img onerror>, <b>text</b> | Saved as typed | None | Shown as plain text<br>Encoded in drawer, History, CSV and parent email |
| JSON, XML, template, for example {{7*7}}, ${7*7} | Saved as plain text, never parsed | None | API payload escapes quotes and backslash |
| CSV export | Value starting with =, +, - or @ gets an apostrophe prefix | None | None |
| Save fails | None | None | Something went wrong. Please try again.<br>Dialog stays open, text kept |
| Valid examples | A comment of exactly 500 characters<br>Two lines separated by a line break<br><b>ok</b><br>Approved after review | None | None |
| Invalid examples | 501 or more characters | None | None |
| Placeholder | Add a note for the record | Add a note for the record | Add a note for the record |
| Source in FS | FS 6.1 item 3, BR15, section 8, T14 | FS 6.1 item 3, BR15, section 8, T14 | FS 6.1 item 3, BR15, section 8, T14 |


| Code | Field | Shows | Rule | Source in FS |
| :--- | :--- | :--- | :--- | :--- |
| E3 | Fees that will be subsidised | Open fee name and amount, subsidy in S$ and percent, Total subsidy | Updates when Tier changes<br>Subsidy = amount x tier percent / 100, rounded half up to the cent<br>No open fee: No open fees right now. Fees issued later are subsidised automatically.<br>Paid fees unchanged, not refunded | FS 6.1 item 4, BR7, BR10, T9, T10 |


### E4. Cancel button


| Item | Rule |
| :--- | :--- |
| Function | Close the dialog without saving |
| Shown when | Dialog open |
| On click | Dialog closes<br>Tier and Comment discarded<br>Application stays Pending<br>Drawer stays open |
| Source in FS | FS 6.1 item 6 |


### E5. Confirm approval button


| Item | Rule |
| :--- | :--- |
| Function | Approve the application and apply the subsidy |
| Disabled when | No Tier chosen<br>Comment over 500 characters<br>Scheme has no Active version |
| On click | Status becomes Approved<br>Save tier, effective date (today), comment, decider, date and time<br>Apply subsidy to open and future EA fees<br>Write History<br>Send email with tier to parent<br>Refresh summary cards and tab counts |
| On double click | Saves once |
| Two users at once | First confirmation wins<br>Second user sees: This application was already decided by {user} on {DD/MM/YYYY}.<br>Dialog closes, drawer read only, list refreshes |
| On error | Something went wrong. Please try again.<br>Nothing saved, dialog stays open |
| On success | Toast: Subsidy applied to the student's EA fees. |
| Source in FS | FS 6.1 item 7, sections 8 and 9, BR3, BR4, BR10, BR20, T20, T21, T23, T24, T30 |


## 7.3. Open points of screen E


| Field | Open point |
| :--- | :--- |
| E1 Tier | Figma C3 has no hint ML suggests Tier X, Figma A3 (MOEFAS) has it. FS 6.1 item 1 says the hint shows for both. FS does not say what is preselected when ML gives no tier. |
| E2 Comment (optional) | Figure shows no n/500 counter. |
| E3 Fees that will be subsidised | Figure Tier 3: Miscellaneous S$ 19.50 gives 9.75, School Meal S$ 64.80 gives 12.96, total 22.71. Not clear if amounts include GST. |


# 8. Screen F. Approve MOEFAS dialog


Opens from Approve MOEFAS in the MOEFAS drawer. MOE HQ. Same as the Approve SBFAS dialog plus the budget note. Source: FS 6.1, section 8, BR17.

Figure F, Figma screen A3

## 8.1. Field summary


| Code | Field | Type |
| :--- | :--- | :--- |
| F1 | Tier | Selection |
| F2 | Comment (optional) | Text input |
| F3 | Fees that will be subsidised | Display only |
| F4 | MOEFAS budget note | Display only |
| F5 | Cancel button | Button |
| F6 | Confirm approval button | Button |


## 8.2. Field rules


### F1. Tier


| Item | Rule |
| :--- | :--- |
| Options | Tier 1 · High need<br>Tier 2 · Medium need<br>Tier 3 · Low need |
| Default | Tier ML suggests, with hint ML suggests Tier X<br>No selection when ML gives Borderline, Do not grant or no tier (QA proposal) |
| Required | Yes |
| Depends on | Active scheme |
| On change | Fee list recalculates<br>Total subsidy recalculates<br>Budget note recalculates |
| Message | Not chosen: Select a tier to approve. (QA proposal)<br>Confirm approval disabled<br>Scheme not Active: No active MOEFAS scheme. |
| Source in FS | FS 6.1 item 1, BR8 |


### F2. Comment (optional)


| Rule | Valid | Invalid | Message |
| :--- | :--- | :--- | :--- |
| Required | Empty or filled | None | None |
| Length | 0 to 500 characters | 501 or more characters | Counter turns red, for example 501/500<br>Error: Comment must be 500 characters or fewer.<br>Confirm approval disabled |
| Counter | Shows n/500<br>Line break counts 1<br>Emoji counts 1 | None | None |
| Paste over 500 | Text is kept, not cut | None | Counter shows for example 600/500 in red |
| Leading and trailing spaces and blank lines | Removed on save | None | None |
| Spaces only | Saved as empty | None | None |
| Allowed characters | Any printable Unicode character<br>Line break and tab | None | None |
| Control characters other than line break and tab | Removed | None | None |
| Null byte | Removed before save | None | None |
| Special characters ' " % \ ; | Saved exactly as typed | None | None |
| SQL string, for example ' OR 1=1 -- | Saved as text, parameterized query | None | No data changed |
| Script and HTML, for example <script>, <img onerror>, <b>text</b> | Saved as typed | None | Shown as plain text<br>Encoded in drawer, History, CSV and parent email |
| JSON, XML, template, for example {{7*7}}, ${7*7} | Saved as plain text, never parsed | None | API payload escapes quotes and backslash |
| CSV export | Value starting with =, +, - or @ gets an apostrophe prefix | None | None |
| Save fails | None | None | Something went wrong. Please try again.<br>Dialog stays open, text kept |
| Valid examples | A comment of exactly 500 characters<br>Two lines separated by a line break<br><b>ok</b><br>Approved after review | None | None |
| Invalid examples | 501 or more characters | None | None |
| Placeholder | Add a note for the record | Add a note for the record | Add a note for the record |
| Source in FS | FS 6.1 item 3, BR15 | FS 6.1 item 3, BR15 | FS 6.1 item 3, BR15 |


| Code | Field | Shows | Rule | Source in FS |
| :--- | :--- | :--- | :--- | :--- |
| F3 | Fees that will be subsidised | Open fee name and amount, subsidy in S$ and percent, Total subsidy | Updates when Tier changes<br>Subsidy = amount x tier percent / 100, rounded half up to the cent<br>No open fee: No open fees right now. Fees issued later are subsidised automatically.<br>Paid fees unchanged, not refunded | FS 6.1 item 4 |
| F4 | MOEFAS budget note | MOEFAS budget left: S$ X. After this approval: S$ Y. | Budget left = MOEFAS budget minus subsidies already granted<br>Total subsidy above budget left: red message, Confirm approval disabled<br>Total equal to budget left: allowed, After is S$ 0.00<br>Total 0.01 above budget left: blocked<br>No budget set: no limit<br>Message: Not enough MOEFAS budget. This approval needs S$ X but only S$ Y is left. | FS 6.1 item 5, BR17, section 8, T11 |


### F5. Cancel button


| Item | Rule |
| :--- | :--- |
| Function | Close the dialog without saving |
| Shown when | Dialog open |
| On click | Dialog closes<br>Tier and Comment discarded<br>Application stays Pending<br>Drawer stays open |
| Source in FS | FS 6.1 item 6 |


### F6. Confirm approval button


| Item | Rule |
| :--- | :--- |
| Function | Approve the application and apply the subsidy |
| Disabled when | No Tier chosen<br>Comment over 500 characters<br>Scheme has no Active version<br>MOEFAS budget not enough |
| On click | Status becomes Approved<br>Save tier, effective date (today), comment, decider, date and time<br>Apply subsidy to open and future EA fees<br>Write History<br>Send email with tier to parent<br>Refresh summary cards and tab counts<br>Subsidy added to the amount granted in the budget function |
| On double click | Saves once |
| Two users at once | First confirmation wins<br>Second user sees: This application was already decided by {user} on {DD/MM/YYYY}. |
| On error | Something went wrong. Please try again.<br>Nothing saved, dialog stays open |
| On success | Toast: Subsidy applied to the student's EA fees. |
| Source in FS | FS 6.1 item 7, sections 8 and 9, BR17, T11, T20, T21 |


## 8.3. Open points of screen F


| Field | Open point |
| :--- | :--- |
| F1 Tier | FS does not say what is preselected when ML gives Borderline, Do not grant or no tier. |
| F4 MOEFAS budget note | Note when no budget is set, and whether After follows the Tier, are not in FS. QA proposal: After follows the Tier. Figure: left S$ 2,896.20, after S$ 2,883.70. |
| F2 Comment (optional) | Figma A3 shows no n/500 counter. FS 6.1 item 3 says the counter shows. |


# 9. Screen G. Reject application dialog


Opens from Reject in a drawer. MOEFAS (MOE HQ) and SBFAS (School Admin). Source: FS 6.2, sections 8 and 9, BR9, BR12.

Figure G, Figma screen B2

## 9.1. Field summary


| Code | Field | Type |
| :--- | :--- | :--- |
| G1 | Reason | Selection |
| G2 | Comment | Text input |
| G3 | Reasons hint line | Display only |
| G4 | SBFAS note | Display only |
| G5 | Cancel button | Button |
| G6 | Reject application button | Button |


## 9.2. Field rules


### G1. Reason


| Item | Rule |
| :--- | :--- |
| Options | Income above limit<br>Not eligible nationality<br>Incomplete documents<br>Other |
| Default | No selection |
| Required | Yes |
| Depends on | None |
| On change | Reason is sent to the parent by email |
| Message | Not chosen: Select a reason to reject. (QA proposal)<br>Reject application disabled |
| Source in FS | FS 6.2 item 1, BR9 |


### G2. Comment


| Rule | Valid | Invalid | Message |
| :--- | :--- | :--- | :--- |
| Required | 1 to 500 characters after trim | Empty or spaces only | Comment is required. |
| Length | 1 to 500 characters | 501 or more characters | Counter turns red, for example 501/500<br>Error: Comment must be 500 characters or fewer.<br>Reject application disabled |
| Counter | Shows n/500<br>Line break counts 1<br>Emoji counts 1 | None | None |
| Paste over 500 | Text is kept, not cut | None | Counter shows for example 600/500 in red |
| Leading and trailing spaces and blank lines | Removed on save | None | None |
| Spaces only | Not valid | Spaces only | Comment is required. |
| Allowed characters | Any printable Unicode character<br>Line break and tab | None | None |
| Control characters other than line break and tab | Removed | None | None |
| Null byte | Removed before save | None | None |
| Special characters ' " % \ ; | Saved exactly as typed | None | None |
| SQL string, for example ' OR 1=1 -- | Saved as text, parameterized query | None | No data changed |
| Script and HTML, for example <script>, <img onerror>, <b>text</b> | Saved as typed | None | Shown as plain text<br>Encoded in drawer, History, CSV and parent email |
| JSON, XML, template, for example {{7*7}}, ${7*7} | Saved as plain text, never parsed | None | API payload escapes quotes and backslash |
| CSV export | Value starting with =, +, - or @ gets an apostrophe prefix | None | None |
| Save fails | None | None | Something went wrong. Please try again.<br>Dialog stays open, text kept |
| Valid examples | A comment of exactly 500 characters<br>Two lines separated by a line break<br><b>ok</b><br>Income above the limit based on NOA 2025. | None | None |
| Invalid examples | Empty<br>Spaces only<br>501 or more characters | None | None |
| Placeholder | Explain the decision. Parent receives the reason by email. | Explain the decision. Parent receives the reason by email. | Explain the decision. Parent receives the reason by email. |
| Source in FS | FS 6.2 item 2, BR9, BR15, T12, T14 | FS 6.2 item 2, BR9, BR15, T12, T14 | FS 6.2 item 2, BR9, BR15, T12, T14 |


| Code | Field | Shows | Rule | Source in FS |
| :--- | :--- | :--- | :--- | :--- |
| G3 | Reasons hint line | Reasons and the four reasons separated by a middle dot | Lists exactly the four options of Reason | FS 6.2 item 1 |
| G4 | SBFAS note | Yes: The parent asked to also be considered for SBFAS, so a new SBFAS application goes to {school} for its decision.<br>No: The parent did not ask for SBFAS. The application closes as Rejected. | MOEFAS only<br>Text follows the parent's Also consider for SBFAS choice | FS 6.2 item 3, BR12, T16, T17 |


### G5. Cancel button


| Item | Rule |
| :--- | :--- |
| Function | Close the dialog without saving |
| Shown when | Dialog open |
| On click | Dialog closes<br>Reason and Comment discarded<br>Application stays Pending<br>Drawer stays open |
| Source in FS | FS 6.2 item 4 |


### G6. Reject application button


| Item | Rule |
| :--- | :--- |
| Function | Reject the application and notify the parent |
| Disabled when | No Reason chosen<br>Comment empty or over 500 characters |
| On click | Status becomes Rejected<br>Save reason, comment, decider, date and time<br>Send reason to parent by email<br>Write History<br>MOEFAS with Also consider for SBFAS = Yes: create a new Pending SBFAS application for the school, old one records Moved to SBFAS<br>Also consider = No: process ends |
| On double click | Saves once |
| Two users at once | First decision wins<br>Second user sees: This application was already decided by {user} on {DD/MM/YYYY}. |
| On error | Something went wrong. Please try again.<br>Nothing saved, dialog stays open |
| On success | Toast: Application rejected. Parent notified by email. |
| Source in FS | FS 6.2 item 5, sections 8 and 9, BR3, BR9, BR12, T15, T16, T17, T20, T21, T30 |


## 9.3. Figma state D2: Reject dialog of an SBFAS application (School Admin, application 00398)


Figure G, Figma screen D2

| Item | Rule |
| :--- | :--- |
| Title tag | FUNCTION 4 · SBFAS (the MOEFAS dialog shows FUNCTION 4 · MOEFAS) |
| Subtitle | APP-2026-00398 · Daniel Ong · P2 Care (class, the MOEFAS dialog shows the school) |
| Fields | Reason, Comment and the reasons hint line, same as the MOEFAS dialog |
| SBFAS note | Not shown<br>The note belongs to the MOEFAS dialog only<br>Settles the open point of G4 |
| Reason in the figure | Not eligible nationality is already selected<br>FS 6.2: nothing selected by default<br>The figure shows a filled example |
| Buttons | Cancel and Reject application, same as the MOEFAS dialog |
| Source in Figma | Screen D2 |


## 9.4. Open points of screen G


| Field | Open point |
| :--- | :--- |
| G1 Reason | Figma B2 and D2 show a reason already selected (Income above limit, Not eligible nationality), FS says nothing selected by default. |
| G4 SBFAS note | Figma D2 (SBFAS) shows no SBFAS note and Figma B2 (MOEFAS) shows it, so the note is MOEFAS only. Figma B2 shows the Yes case. The No case text is in FS 6.2 item 3. |


# 10. Screen H. FAS schemes list (MOE HQ and School Admin view)


Menu Financial assistance, MOEFAS schemes (for MOE HQ) or SBFAS schemes (for School Admin). MOE HQ manages national MOEFAS schemes covering all schools. School Admin manages school-specific SBFAS tiers. Source: FS F4 v1.3 section 6.1 and 7.1; Test cases TC-168 to TC-180 (Suite F4.13).

## 10.1. Field summary


| Code | Field | Type | Scope | Source in FS |
| :--- | :--- | :--- | :--- | :--- |
| H1 | New scheme button | Button / Link | MOE HQ / School Admin | FS 6.1 item 1 |
| H2 | Summary cards (Active, Upcoming, Closed, Draft) | Display counters | Both roles | FS 6.1 item 2 |
| H3 | Schemes data table | Data table | Both roles (Role isolated) | FS 6.1 item 3, 7.1 |
| H4 | Status badge (Active, Upcoming, Closed, Draft) | Badge indicator | Both roles | FS 6.1 item 4 |
| H5 | Actions menu (View, Add fee, Publish, Suspend) | Dropdown menu | Both roles | FS 6.1 item 5 |


## 10.2. Validation and Business Rules for Schemes List


| Rule ID | Rule Name | Condition / Trigger | Expected System Behavior / Validation Message | Source |
| :--- | :--- | :--- | :--- | :--- |
| VR-SCH-01 | Role Data Isolation | MOE HQ accesses scheme list | MOE HQ sees MOEFAS schemes only. Cannot see SBFAS schemes of schools. | TC-168, TC-165, FS 6.1 |
| VR-SCH-02 | School Scheme Isolation | School Admin accesses scheme list | School Admin sees only the SBFAS schemes belonging to their own school. Cannot view MOEFAS management or other schools' SBFAS. | TC-169, TC-165, FS 6.1 |
| VR-SCH-03 | Summary Cards Calculation | Page load / Scheme status change | Cards count exact numbers of Active (effective today), Upcoming (published, effective later), Closed (past effective to), and Draft schemes. | TC-171, FS 6.1 |
| VR-SCH-04 | Upcoming Scheme Definition | Scheme with Effective from > Today | Status must show 'Upcoming' with descriptive hint 'Published, not yet in effect'. | TC-171, TC-175, FS 6.1 |
| VR-SCH-05 | Table Column Structure | Display table | Mandatory columns: SCHEME, ELIGIBILITY, APPLICATION FORM, EFFECTIVE FROM, EFFECTIVE TO, STATUS, ACTIONS. | TC-172, TC-173, FS 7.1 |
| VR-SCH-06 | Action Restrictions by Status | Scheme status check | Draft: allows Edit, Publish, Delete. Active/Upcoming: allows View, Add fee, Suspend (No Edit). Closed: allows View only (Add fee and Edit strictly blocked). | TC-178, TC-229, TC-231, TC-235 |


# 11. Screen I. New scheme wizard (4-step stepper)


Accessible via 'New scheme' button on Screen H. Stepper consists of Step 1 (General Information), Step 2 (Eligibility Criteria), Step 3 (Subsidy Components), and Step 4 (Review and Publish). Source: FS F4 v1.3 section 6.2; Test cases TC-181 to TC-218 (Suite F4.14).

## 11.1. Step 1: General Information Validation Rules


| Rule ID | Field / Item | Validation Condition | Validation Message / System Reaction | Source |
| :--- | :--- | :--- | :--- | :--- |
| VR-WIZ-01 | Scheme Name - Blank | User leaves Scheme Name empty | Validation error: 'Scheme name is required'. Cannot proceed to Step 2. | TC-183, TC-268, TC-293, TC-304, FS 6.2 |
| VR-WIZ-02 | Scheme Name - Length | Name < 3 or > 100 characters | Validation error: 'Scheme name must be between 3 and 100 characters'. | TC-269, TC-293, TC-306, TC-312, FS 6.2 |
| VR-WIZ-03 | Scheme Name - Duplicate | Name already exists within the same scope | Validation error: 'A scheme with this name already exists'. Must be unique per school/MOE. | TC-222, TC-303, TC-310, TC-314, FS 6.2 |
| VR-WIZ-04 | Academic Year | Academic year not selected | Validation error: 'Academic year is required'. | No case yet (field not in the build), FS 6.2 |
| VR-WIZ-05 | Form Opens vs Form Closes | Form opens date > Form closes date | Validation error: 'Form closing date cannot be earlier than opening date'. | TC-185, TC-271, TC-294, TC-305, FS 6.2 |
| VR-WIZ-06 | Effective From vs Effective To | Effective from date > Effective to date | Validation error: 'Effective end date cannot be earlier than start date'. | TC-187, TC-273, TC-294, TC-305, FS 6.2 |
| VR-WIZ-07 | Form Period vs Effective Period | Form opens date > Effective from date | Validation error: 'Application form period must start before or on scheme effective date'. | TC-186, TC-272, TC-294, TC-305, FS 6.2 |
| VR-WIZ-08 | Effective From in Past | Effective from date < Today (New scheme) | Validation error: 'Effective start date cannot be in the past for new schemes'. | TC-270, TC-295, TC-305, FS 6.2 |


## 11.2. Step 2: Eligibility Criteria Validation Rules


| Rule ID | Field / Item | Validation Condition | Validation Message / System Reaction | Source |
| :--- | :--- | :--- | :--- | :--- |
| VR-WIZ-09 | Nationalities Selection | No nationality option is checked | Validation error: 'At least one eligible nationality must be selected'. Cannot proceed. | TC-191, TC-275, TC-298, TC-308, FS 6.2 |
| VR-WIZ-10 | GHI Max Limit - Format | Gross Household Income is negative or non-numeric | Validation error: 'GHI limit must be a positive number'. Currency format S$ #,##0.00. | TC-194, TC-278, TC-279, TC-297, TC-313, FS 6.2 |
| VR-WIZ-11 | PCI Max Limit - Format | Per Capita Income is negative or non-numeric | Validation error: 'PCI limit must be a positive number'. Currency format S$ #,##0.00. | TC-194, TC-277, TC-279, TC-297, TC-313, FS 6.2 |
| VR-WIZ-12 | Income Matching Operator | Operator selection | Must select either 'ANY' (Meet GHI OR PCI) or 'ALL' (Must meet both GHI AND PCI). Default is 'ANY'. | TC-190, TC-280, TC-297, FS 6.2 |
| VR-WIZ-13 | At least One Income Metric | Both GHI and PCI are unchecked/disabled | Validation error: 'At least one income criterion (GHI or PCI) must be enabled'. | TC-192, TC-276, TC-297, TC-308, FS 6.2 |


## 11.3. Step 3: Subsidy Components Validation Rules


| Rule ID | Field / Item | Validation Condition | Validation Message / System Reaction | Source |
| :--- | :--- | :--- | :--- | :--- |
| VR-WIZ-14 | Subsidy Items Required | No fee subsidy components added | Validation error: 'At least one subsidy component must be configured'. Next button disabled. | TC-196, TC-282, TC-299, FS 6.2 |
| VR-WIZ-15 | Subsidy Percentage Limit | Percentage value < 0% or > 100% | Validation error: 'Subsidy rate must be between 0% and 100%'. Field highlighted in red. | TC-205, TC-206, TC-283, TC-284, TC-300, TC-301, TC-309, FS 6.2 |
| VR-WIZ-16 | Subsidy Fixed Amount | Fixed subsidy amount < 0 | Validation error: 'Subsidy amount cannot be negative'. | TC-207, FS 6.2 |
| VR-WIZ-17 | Level / Grade Completeness | A level or grade row is left blank | Validation error: 'All applicable grades/levels must have an assigned subsidy value (0% if none)'. | TC-205, TC-288, FS 6.2 |


# 12. Screen J. Review and publish scheme (Overlap Prevention rules)


Step 4 of the wizard or Review dialog. Summarizes the configured scheme and provides 'Save as Draft' and 'Publish'. Source: FS F4 v1.3 section 6.3; Test cases TC-219 to TC-230 (Suite F4.15).

| Rule ID | Rule Name | Validation Condition | Validation Message / System Reaction | Source |
| :--- | :--- | :--- | :--- | :--- |
| VR-PUB-01 | MOEFAS Effective Overlap Prevention | MOEFAS Effective period overlaps another active/upcoming MOEFAS scheme | SYSTEM BLOCKS PUBLISH: 'Effective period overlaps with an existing MOEFAS scheme. Close the existing scheme or adjust dates'. | TC-219, FS 6.3 |
| VR-PUB-02 | MOEFAS Form Overlap Prevention | MOEFAS Form period overlaps another active form period | SYSTEM BLOCKS PUBLISH: 'Application form period overlaps with an active form period'. | TC-220, FS 6.3 |
| VR-PUB-03 | Adjacent Periods Allowed | New Effective from is exactly the day after earlier Effective to | Publish permitted. Touching periods without day overlap are valid. | TC-221, FS 6.3 |
| VR-PUB-04 | SBFAS Same-Name Overlap | SBFAS with the same name in the same school overlaps period | SYSTEM BLOCKS PUBLISH: 'A scheme with this name already exists in this period for your school'. | TC-222, FS 6.3 |
| VR-PUB-05 | SBFAS Different Name Allowed | Different SBFAS tiers (e.g. Tier 1 and Tier 2) in the same period | Publish permitted. Different SBFAS schemes can run concurrently in the same school. | TC-223, FS 6.3 |
| VR-PUB-06 | Draft Flexibility Rule | Draft scheme with overlapping dates | Allowed to save draft: 'Draft saved successfully'. Overlap validation strictly enforced ONLY at Publish. | TC-225, FS 6.3 |
| VR-PUB-07 | Automatic Preceding Scheme End Date | Publishing scheme when earlier scheme has no Effective To date | System automatically sets Effective To of the earlier scheme to (New Scheme Effective From - 1 day). | TC-226, TC-228, FS 6.3 |
| VR-PUB-08 | Post-Publish Immutability | Attempt to edit published scheme via UI or API | Strictly prohibited. Published scheme cannot be modified. Only Add Fee or Suspend allowed. | TC-229, TC-230, FS 6.3 |


# 13. Screen K. Add fee to a published scheme dialog


Triggered from Screen H actions menu. Allows adding a newly created fee component to an already published scheme. Source: FS F4 v1.3 section 6.4; Test cases TC-231 to TC-241 (Suite F4.16).

| Rule ID | Rule Name | Validation Condition | Validation Message / System Reaction | Source |
| :--- | :--- | :--- | :--- | :--- |
| VR-FEE-01 | Allowed Scheme Statuses | Add fee action invoked | Offered ONLY on Active and Upcoming schemes. Action hidden/disabled for Closed schemes. | TC-231, FS 6.4 |
| VR-FEE-02 | Closed Scheme Rejection | Direct URL or API access to add fee on Closed scheme | HTTP 400 / 403: 'Cannot add fee components to a closed scheme'. | TC-235, FS 6.4 |
| VR-FEE-03 | Component Filter | Component selection dropdown | Dropdown lists ONLY fee components not yet present in the scheme. Existing components displayed as read-only. | TC-232, TC-291, TC-292, FS 6.4 |
| VR-FEE-04 | Cell Validation & Button State | Invalid rate entered (negative, > 100%, non-numeric, or blank) | Validation error on cell. 'Add to scheme' button remains DISABLED until all cells are valid. | TC-234, TC-289, TC-290, TC-311, FS 6.4 |
| VR-FEE-05 | Existing Components Locked | Dialog open | Existing fee components cannot be edited, removed, or modified during Add Fee operation. | TC-238, TC-291, FS 6.4 |
| VR-FEE-06 | Immediate Retroactive Application | New component successfully added to Active scheme | Toast notification shown. System automatically recalculates unpaid and future charges for enrolled students. | TC-236, TC-239, TC-240, TC-241 |


# 14. Shared rules: AI/ML Need Score and Deny Rules engine


The ML Recommendation engine calculates a household Need Score and evaluates fraudulent/invalid data patterns. Source: FS F4 v1.3 section 7.2; Test cases TC-249 to TC-263 (Suite F4.19).

## 14.1. Hard Deny Rules Matrix


| Rule Code | Deny Condition | System Reaction | Risk Level | Source |
| :--- | :--- | :--- | :--- | :--- |
| DENY-NO-CHILDREN | Application household contains 0 school-age children | Need Score = 0.00. Automatic flag for manual verification. | Low Risk (Score 0) | TC-258, FS 7.2 |
| DENY-ONLY-CHILDREN | Household consists entirely of minors without an adult guardian | Need Score = 0.00. Flagged as invalid household structure. | Low Risk (Score 0) | TC-259, FS 7.2 |
| DENY-INVALID-SIZE | Household member count <= 0 | Need Score = 0.00. Flagged as data inconsistency error. | Low Risk (Score 0) | TC-260, FS 7.2 |
| DENY-WORKERS-EXCEED-SIZE | Reported employed workers > Total household members | Need Score = 0.00. Immediate audit flag for conflicting declaration. | Low Risk (Score 0) | TC-261, FS 7.2 |
| DENY-NEGATIVE-MONTHS | Declared employment or residency months < 0 | Need Score = 0.00. Immediate validation error flag. | Low Risk (Score 0) | TC-262, FS 7.2 |


## 14.2. Need Score Weighting & Risk Thresholds


| Parameter | Formula / Range | System Rule / Classification | Source |
| :--- | :--- | :--- | :--- |
| Score Weights | Score = 0.70*Income + 0.05*Size + 0.10*Housing + 0.10*JobStability + 0.05*SpecialNeeds | Linear weighted combination between 0.00 and 100.00. | TC-263, FS 7.2 |
| High Risk Band | Need Score >= 75.00 | Classified as 'High'. Red risk indicator on Review Drawer. | TC-256, FS 7.2 |
| Medium Risk Band | 50.00 <= Need Score <= 74.99 | Classified as 'Medium'. Amber risk indicator on Review Drawer. | TC-256, TC-257, FS 7.2 |
| Low Risk Band | Need Score < 50.00 (or triggered Deny Rule) | Classified as 'Low'. Green risk indicator on Review Drawer. | TC-257, TC-258, FS 7.2 |


## 14.3. Standard Display and Input Format Rules


| Data Type | Standard Format | Example | Validation Constraint | Source |
| :--- | :--- | :--- | :--- | :--- |
| Currency | S$ #,##0.00 | S$ 4,200.00 | Always prefixed with 'S$', thousands separator comma, exactly 2 decimal places. | TC-264, FS 8.1 |
| Date | DD/MM/YYYY | 31/12/2026 | Zero-padded 2-digit day and month, 4-digit year. Slash separator. | TC-265, FS 8.1 |
| Time | HH:mm (SGT UTC+8) | 09:30, 23:59 | 24-hour clock format. Converted to Singapore timezone regardless of browser locale. | TC-266, TC-267, FS 8.1 |


# 15. Shared messages


| Situation | Message or display | Behavior | Fields | Source |
| :--- | :--- | :--- | :--- | :--- |
| Confirm or Reject is not allowed yet | Select a tier to approve.<br>Select a reason to reject.<br>Comment is required.<br>Comment must be 500 characters or fewer. | Field error, action button disabled | E1 Tier<br>F1 Tier<br>G1 Reason<br>E2 Comment (optional)<br>F2 Comment (optional)<br>G2 Comment | QA proposal. FS defines only the counter n/500 and the disabled button |
| Not enough MOEFAS budget | Not enough MOEFAS budget. This approval needs S$ X but only S$ Y is left. | Confirm approval disabled, nothing saved | F4 MOEFAS budget note<br>F6 Confirm approval button | FS section 8 |
| Scheme has no Active version | No active {MOEFAS or SBFAS} scheme. | Confirm approval disabled | E5 Confirm approval button<br>F6 Confirm approval button | FS section 8 |
| Someone else decided first | This application was already decided by {user} on {DD/MM/YYYY}. | Dialog closes, drawer read only, list refreshes | A13 Review or View button<br>B16 Review or View button<br>E5 Confirm approval button<br>F6 Confirm approval button<br>G6 Reject application button | FS section 8 |
| School Admin opens another school's application | You do not have access to this application. | No data shown | A12 Applications table<br>A13 Review or View button<br>C1 Header | FS section 8 |
| System error on save or export | Something went wrong. Please try again. | Nothing saved, dialog stays open | A1 Export button<br>B1 Export button<br>E5 Confirm approval button<br>F6 Confirm approval button<br>G6 Reject application button | FS section 8 |
| Approval succeeded | Subsidy applied to the student's EA fees. | Toast | E5 Confirm approval button<br>F6 Confirm approval button | FS section 9 |
| Rejection succeeded | Application rejected. Parent notified by email. | Toast | G6 Reject application button | FS section 9 |
| Empty list or empty search result | No applications found. | Empty table | A3 Status tabs<br>A4 Search box<br>A14 Footer and paging<br>B3 Status tabs<br>B4 Search box<br>B17 Footer and paging | FS 3.5 |
| Student has no open fee | No open fees right now. Fees issued later are subsidised automatically. | Shown in the fee list | E3 Fees that will be subsidised<br>F3 Fees that will be subsidised | FS 6.1 item 4 |
| Pasted search text over 100 characters | Search is limited to 100 characters. | Helper text, text cut to 100 | A4 Search box<br>B4 Search box | QA proposal |


# 16. Open points for BA


| Code | Topic | Detail | Fields |
| :--- | :--- | :--- | :--- |
| O1 | Tabs, Status filter and tab counts | The FS does not say whether tab counts follow filters and search, or what the Pending tab shows when Status is Approved. Figure: All 46 while Submitted defaults to 30 days. | A3 Status tabs<br>A9 Status filter<br>B3 Status tabs |
| O2 | Search box rules | The FS gives no maximum length, whitespace rule, special character handling, trigger, or page reset on a new term. The rules in this document are QA proposals. | A4 Search box<br>B4 Search box |
| O3 | Export scope | Not stated whether the export covers all pages or the visible page, and whether tab and search apply. File name is also open. | A1 Export button<br>B1 Export button |
| O4 | Definition of this year | Cards SBFAS approved and rejected say This year. Calendar year or school year is not stated. | A2 Summary cards |
| O5 | Pass rule of System check | FS 3.4 says Pass when all criteria pass. FS 4.2 says Pass when nationality passes and at least one of GHI or PCI passes. The two give different results when only one of GHI or PCI passes. | B14 System check column<br>D2 Eligibility check |
| O6 | Tier 4 and Ineligible | FS 5.3 has Base Tier and Adjusted Tier 4 and Ineligible. FS 1.3 and the dropdown in 6.1 have Tier 1 to 3 only, and so does the Tier filter. The engine can suggest Tier 4 that the approver cannot choose. | B9 Tier filter<br>C5 ML suggestion<br>E1 Tier<br>F1 Tier |
| O7 | Preselected Tier when ML gives no tier | Not stated what the dropdown preselects when ML is Reject, Borderline, Do not grant or has no suggestion. | E1 Tier<br>F1 Tier |
| O8 | Confidence range | FS 5.4 states 55 to 95 percent but the score starts at 92 and only subtracts, so the maximum is 92. Subtracting everything gives 46, below 55, so a lower bound rule is needed. | C5 ML suggestion<br>D4 ML recommendation |
| O9 | Fee amount and subsidy rounding | Not clear whether the fee amounts include GST. The Dev data design says the subsidy applies to the amount before tax and rounds half up to the cent. | E3 Fees that will be subsidised<br>F3 Fees that will be subsidised |
| O10 | Display of PCI | The figure shows PCI rounded to the dollar (4,350 divided by 4 shows 1,088). The Dev data design rounds to two decimals. The display rule is not stated. | C4 Household and income<br>D3 Household and income |
| O11 | Figures differ from the FS text | The SBFAS approve dialog lacks the hint ML suggests Tier X. No dialog shows the n/500 counter. The Reject dialog preselects Income above limit while the FS says no default. The drawer lacks Score breakdown, the no scheme warning, and value, limit and percent above in Eligibility check. The ML recommendation header wraps. The search placeholder is cut. The Application ID wraps. | A4 Search box<br>A12 Applications table<br>B4 Search box<br>B13 Applications table<br>B15 ML recommendation column<br>C5 ML suggestion<br>D2 Eligibility check<br>E1 Tier<br>E2 Comment (optional)<br>G1 Reason |
| O12 | Sample numbers between two figures | The HQ card says Approved 2 for all schools while the School Admin card says 34 for one school. Tab All is 46 and 9. | A2 Summary cards<br>B2 Summary cards |
| O13 | Role name | FS F4 says School Admin. The menu in the figure says School user. FS 03 and the tender say School User. | All fields A1 to A14 of the School Admin list |
| O14 | FS F4 v1.1 differs from Database Design Func4 v0.1 | The Dev design (14/10) has seven application statuses, an automatic decision type MoefasAuto, ML for SBFAS only and PCI with two decimals. FS F4 v1.1 (18/10) has three statuses, no auto approval and ML shown for MOEFAS as well. Align before the seed data is loaded. | All fields<br>Seed data sheet SD-08 Applications |
| O15 | Tier income bands and subsidy percentages | BR5 and BR7 take them from scheme setup and the FS has no numbers. Backlog PB-17 says Needs client decision. The seed uses the Tier 3 values from the figure and QA proposals for the others, clearly marked. | E3 Fees that will be subsidised<br>F3 Fees that will be subsidised<br>Seed data sheets SD-05a Schemes and SD-05b Tiers |
| O16 | SBFAS eligibility numbers | The FS says SBFAS is for Citizens and PRs with PCI in the scheme band but gives no numbers. | C5 ML suggestion<br>Seed data sheets SD-05a Schemes and SD-05b Tiers |
| O17 | Time and date format | BR16 requires DD/MM/YYYY and Singapore time (UTC+8). The Function 9 payment screen shows Oct 15, 2026, 6:37 PM. See BUG-R9-002. | A12 Applications table<br>B13 Applications table |
| O18 | List of T scenarios | The list T1 to T35 has no T13 and T32 sits after T19. | Appendix B |
| O19 | Borderline can never occur | FS 5.4 gives Grant lowest tier when income is up to 5 percent over the limit and Need Score is 50 or more, otherwise Borderline. By the formula in 5.2, GHI up to 4,200 gives x_inc of at least 0.65, so the smallest Need Score is 0.70 times 0.65 plus 0.10 times 0.20 plus 0.10 times 0.30, which is 50.50. No application inside the 5 percent margin falls below 50, so Borderline never appears. BA to confirm the threshold or the formula. | B15 ML recommendation column<br>D4 ML recommendation<br>Seed data sheet SD-09 Engine |
| O20 | Order of deny rules | The FS lists five deny rules but does not say which one is recorded when two apply, nor the Confidence of a denied case. SD-09 uses cases that match one rule only. | C5 ML suggestion<br>Seed data sheet SD-09 Engine |
| O21 | Messages and field rules not in the FS | Select a tier to approve.<br>Select a reason to reject.<br>Comment is required.<br>Comment must be 500 characters or fewer.<br>Search is limited to 100 characters. All field level messages, the 100 character search limit, the 300 ms search trigger and the security handling (escaping, CSV formula prefix) are QA proposals. | A4 Search box<br>B4 Search box<br>E1 Tier<br>E2 Comment (optional)<br>F1 Tier<br>F2 Comment (optional)<br>G1 Reason<br>G2 Comment |
| O22 | Cards after a decision, School Admin list | Figma C4 keeps Pending 3 and SBFAS approved 34 after application 00412 is approved, while the tabs change to Pending 2 and Approved 35. FS 9 says summary cards and tab counts update. Expected: Pending 2 and SBFAS approved 35. | A2 Summary cards<br>A3 Status tabs |
| O23 | Tab counts and footer | Figma A4 shows Approved (3) with 2 rows and Figma C4 shows Approved (35) with 2 rows. Tab counts seem not to follow the filters while the footer does. Same question as O1: do tab counts follow the Submitted filter? | A3 Status tabs<br>A14 Footer and paging<br>B3 Status tabs<br>B17 Footer and paging |
| O24 | Drawer of a student who is not a Citizen or PR | Figma D1 (application 00398) shows Student with Full name and Citizenship only, no Parent and no Documents section, the value International Student, and an ML box with Confidence and Factors only. FS 4.1 lists NRIC/FIN, Class, Parent, Documents, Risk, Need Score, Base Tier and Adjusted Tier. BA to say which rows show for this case and the list of Citizenship values. | C2 Student<br>C3 Parent<br>C5 ML suggestion<br>C6 Documents |
| O25 | Eligibility check rows | Figma A2 (Fail) shows Pass or Fail only. Figma B1 (Pass) shows value and limit with no badge. FS 4.1 item 3 says value, limit, percent above and Pass or Fail for every row. BA to confirm the FS text. | D2 Eligibility check |
| O26 | Role names | Figma shows the School Admin as School user (footer of the menu, wireframe overview) and MOE HQ as MOE HQ Administrator. FS and Dev design use School Admin and MOE HQ (HQ Admin). | All fields |
| O27 | FAS schemes screens | The Figma canvas F4 FAS schemes (create SBFAS in 4 steps, scheme list, view SBFAS) is not part of FS F4 FAS Applications (FS 1.1 lists it as out of scope). It needs its own FS and validation rules. | None |


| Item | Rule |
| :--- | :--- |
| Tender row 4 and function tree 4.5 | MOEFAS is auto-granted |
| FS F4 v1.1 (BR1, T7) | No auto grant, every MOEFAS application waits for MOE HQ |
| This document | Follows FS F4 v1.1. Project convention says the tender wins, so BA and customer must settle it |


# Appendix A. Engine calculation (FS section 5)


| Item | Rule |
| :--- | :--- |
| Deny rules (checked first) | DENY-NO-CHILDREN: no member under 21.<br>DENY-ONLY-CHILDREN: every member is under 21.<br>DENY-INVALID-SIZE: household size is 0 or less.<br>DENY-WORKERS-EXCEED-SIZE: workers are more than household size.<br>DENY-NEGATIVE-MONTHS: months since last aid is below 0.<br>When one applies, Need Score is 0 and both tiers are Ineligible. |
| Need Score | 100 times the sum of weight times feature.<br>Each feature is between 0 and 1 and the weights add up to 1.0. |
| Income, weight 0.70 | The larger of x_ghi equal to 1 minus GHI divided by 12,000, and x_pci equal to 1 minus PCI divided by 3,000, each clamped between 0 and 1. |
| Dependency, weight 0.05 | (household size minus workers) divided by household size. |
| Stability, weight 0.10 | Stable 0.20 (3 month average against 12 month average from 0.70 to 1.30).<br>Interrupted 0.50 (ratio below 0.70).<br>Unemployed short 0.80 (1 to 5 months without income).<br>Unemployed long 1.00 (6 months or more). |
| Recency, weight 0.10 | Last aid within 3 months: 0.90 with Fast-track. 4 to 12 months: 0.50. 13 to 24 months: 0.30.<br>Never or over 24 months: 0.30. |
| Vulnerability, weight 0.05 | Added up: single parent 0.15, a member aged 65 or over 0.10, a member with disability 0.20, a child under 6 years 0.10.<br>Maximum 1.0. |
| Base Tier (legal thresholds, GHI or PCI) | Tier 1: GHI up to 4,000 or PCI up to 1,000.<br>Tier 2: GHI up to 5,500 or PCI up to 1,375.<br>Tier 3: GHI up to 9,000 or PCI up to 2,250.<br>Tier 4: GHI up to 12,000 or PCI up to 3,000.<br>Ineligible: GHI above 12,000 and PCI above 3,000. |
| Adjusted Tier and ML risk (from Need Score) | Tier 1: 75.00 to 100, risk High.<br>Tier 2: 50.00 to 74.99, Medium.<br>Tier 3: 25.00 to 49.99, Low.<br>Tier 4: 1.00 to 24.99, Low.<br>Ineligible: 0, Low. |
| Suggested tier and recommendation | The suggested tier is the scheme tier whose band and nationality match.<br>Income up to 5 percent over the limit suggests the lowest tier.<br>MOEFAS: Grant · Tier X when a tier matches.<br>Up to 5 percent over: Grant · lowest tier when Need Score is 50 or more, otherwise Borderline.<br>Anything else: Do not grant.<br>SBFAS: Tier X · High, Medium or Low need, or Reject when no tier matches. |
| Confidence | Starts at 92.<br>Minus 18 when income is up to 5 percent over the limit.<br>Minus 8 when income is not from the API.<br>Minus 10 when the name differs from government data.<br>Minus 6 when the household profile is assumed.<br>Minus 4 when no tier is suggested.<br>The result is stated to stay between 55 and 95 percent. |


# Appendix B. FS scenarios mapped to fields


| Scenario | Description | Related fields |
| :--- | :--- | :--- |
| T1 | MOE HQ opens the list | B3 Status tabs<br>B13 Applications table<br>B16 Review or View button |
| T2 | School Admin opens the list | A2 Summary cards<br>A12 Applications table |
| T3 | School Admin opens another school's link | A12 Applications table<br>A13 Review or View button<br>C1 Header |
| T4 | School Admin does not see MOEFAS | A12 Applications table |
| T5 | MOE HQ opens a Pending MOEFAS application | D2 Eligibility check<br>D4 ML recommendation<br>D5 Reject button<br>D6 Approve MOEFAS button |
| T6 | System check Fail can still be approved | D2 Eligibility check<br>D6 Approve MOEFAS button |
| T7 | MOEFAS Pass or Fail both stay Pending | B14 System check column |
| T8 | Open Approve, Tier preselected | F1 Tier<br>F3 Fees that will be subsidised |
| T9 | Choose Tier 2, no comment, confirm | E1 Tier<br>E2 Comment (optional)<br>E5 Confirm approval button |
| T10 | Change Tier, fee list changes | E1 Tier<br>E3 Fees that will be subsidised |
| T11 | Approve over the budget | F4 MOEFAS budget note<br>F6 Confirm approval button |
| T12 | Reject without Reason or Comment | G1 Reason<br>G2 Comment<br>G6 Reject application button |
| T14 | Comment of 501 characters | E2 Comment (optional)<br>G2 Comment |
| T15 | Reject with Reason and Comment | G6 Reject application button |
| T16 | Reject MOEFAS, consider SBFAS is Yes | G4 SBFAS note<br>G6 Reject application button |
| T17 | Reject MOEFAS, consider SBFAS is No | G4 SBFAS note<br>G6 Reject application button |
| T18 | SBFAS decided by School Admin, HQ read only | B13 Applications table<br>B16 Review or View button |
| T19 | MOE HQ opens a Pending SBFAS application | B16 Review or View button |
| T20 | Two users confirm | E5 Confirm approval button<br>F6 Confirm approval button<br>G6 Reject application button |
| T21 | Double click on Confirm | E5 Confirm approval button<br>F6 Confirm approval button<br>G6 Reject application button |
| T22 | Open a decided application | D5 Reject button<br>D6 Approve MOEFAS button<br>C1 Header |
| T23 | Approval lowers EA fees and sends email | E5 Confirm approval button<br>F6 Confirm approval button |
| T24 | Cards and tab counts refresh | A2 Summary cards<br>A3 Status tabs<br>B2 Summary cards<br>B3 Status tabs |
| T25 | Combined filters | A5 to A11<br>B5 to B12 |
| T26 | Search by NRIC, name, Application ID | A4 Search box<br>B4 Search box |
| T27 | Filter with no match | A4 Search box<br>A14 Footer and paging<br>B17 Footer and paging |
| T28 | More than 10 results | A14 Footer and paging<br>B17 Footer and paging |
| T29 | Export while filtered | A1 Export button<br>B1 Export button |
| T30 | Save error | E5 Confirm approval button<br>F6 Confirm approval button<br>G6 Reject application button |
| T31 | Date, time and money format | A12 Applications table<br>B13 Applications table<br>E3 Fees that will be subsidised |
| T32 | PR student | B13 Applications table<br>C2 Student |
| T33 | Sample Need Score calculation | C5 ML suggestion<br>D4 ML recommendation |
| T34 | Deny rule | C5 ML suggestion |
| T35 | Fast-track | C5 ML suggestion |


# Appendix C. Figma screens mapped to this document


| Figma id | Canvas | Content | Screen here | Use |
| :--- | :--- | :--- | :--- | :--- |
| A1 | F4 canvas, flow A | FAS applications, Pending tab, MOE HQ | Screen B | Annotated figure |
| A2 | F4 canvas, flow A | MOEFAS review drawer, application 00377 (Fail) | Screen D | Annotated figure |
| A3 | F4 canvas, flow A | Approve MOEFAS dialog | Screen F | Annotated figure |
| A4 | F4 canvas, flow A | Result, Approved tab, MOE HQ | Screen B | Figma state |
| B1 | F4 canvas, flow B | MOEFAS review drawer, application 00390 (Pass) | Screen D | Figma state |
| B2 | F4 canvas, flow B | Reject application dialog, MOEFAS | Screen G | Annotated figure |
| C1 | F4 canvas, flow C | FAS applications, Pending tab, School Admin | Screen A | Annotated figure |
| C2 | F4 canvas, flow C | SBFAS review drawer, application 00412 | Screen C | Annotated figure |
| C3 | F4 canvas, flow C | Approve SBFAS dialog | Screen E | Annotated figure |
| C4 | F4 canvas, flow C | Result, Approved tab, School Admin | Screen A | Figma state |
| D1 | F4 canvas, flow D | SBFAS review drawer, application 00398 (not a Citizen or PR) | Screen C | Figma state |
| D2 | F4 canvas, flow D | Reject application dialog, SBFAS | Screen G | Figma state |


Figma screens of other canvases that are not covered:

| Canvas | Reason |
| :--- | :--- |
| F4 canvas, FAS schemes (A1 to A7, B1, B2) | Scheme setup, not FS F4 FAS Applications (FS 1.1, scope). Not covered, open point O27 |
| F1 Education account, F2 Top-up, F3 School setup and fees | Other functions |
| F5 Paper applications | Other function, creates the applications that F4 lists |
| F6 Budget and statistics | Other function, source of the MOEFAS budget left in Figure F |
| F7 Simulation, F8 Parent portal, F9 Payments, F10 Parent FAS application | Other functions |


# Appendix D. Figma versus FS


| Code | Figma | Figma shows | FS says | Handling |
| :--- | :--- | :--- | :--- | :--- |
| FG1 | A2, B1 | Eligibility check rows differ between the two states: badge only (A2) or value and limit (B1) | FS 4.1 item 3: value, limit, percent above, Pass or Fail | Follow the FS text, open point O25 |
| FG2 | D1 | Student who is not a Citizen or PR: two Student rows, no Parent, no Documents, ML box without Risk and Need score | FS 4.1 items 4, 5, 7, 8 | Open point O24 |
| FG3 | C4 | Cards stay at Pending 3 and SBFAS approved 34 after an approval | FS 9: cards and tab counts update | Follow the FS, open point O22 |
| FG4 | A4, C4 | Tab count (3 and 35) is higher than the rows shown (2) | FS 3.1: tab shows its count, filters combine by AND | Open point O23 and O1 |
| FG5 | B2, D2 | Reason already selected | FS 6.2 item 1: nothing selected by default | Follow the FS |
| FG6 | A3, C3 | Hint ML suggests Tier 3 shown in the MOEFAS dialog and missing in the SBFAS dialog | FS 6.1 item 1: hint shows for both | Follow the FS |
| FG7 | A3, C3, B2 | No n/500 counter under Comment | FS 6.1 item 3, 6.2 item 2: counter n/500 | Follow the FS |
| FG8 | D2 | SBFAS reject dialog has no SBFAS note | FS 6.2 item 3: note for MOEFAS only | Matches the FS |
| FG9 | A1, C1 | Search placeholder is cut off | FS 3.1 item 4: matches student name, NRIC/FIN or Application ID | Open points in Screen A and B |
| FG10 | A1, C1 | Application ID wraps inside the number | Not in FS | Open points in Screen A and B |
| FG11 | C1 to C4, A1 to A4 | Role shown as School user and MOE HQ Administrator | FS 1.2: School Admin and MOE HQ | Open point O26 |
| FG12 | B1 | Recommendation Grant · Tier 2 while Adjusted Tier is Tier 1 | FS 5.3 and 5.4: two different values | Matches the FS |
| FG13 | A1, B1, C1, C2, D1 | Routing rules, ML suggestion rule and ML Reject note in the sticky notes | FS 2.1, 5.4, BR1, BR6, BR19 | Matches the FS |
| FG14 | A3 | Budget note: left S$ 2,896.20, after S$ 2,883.70. Total subsidy S$ 12.50 (50 percent of S$ 25.00) | FS 6.1 item 5, BR17. Figma F6 shows budget S$ 3,000.00, used S$ 103.80, remaining S$ 2,896.20 | Matches the FS and F6 |
| FG15 | C3 | Subsidy: Miscellaneous S$ 9.75 (50 percent of S$ 19.50), School Meal S$ 12.96 (20 percent of S$ 64.80), total S$ 22.71 | FS 6.1 item 4 | Matches the FS |
| FG16 | C2, D1, A2 | No History section and no Decision section in any drawer | FS 4.1 item 9, 4.3 | Not drawn in Figma, rules stay in section 5.3 and 6.3 |
