# Bug Traceability Matrix (from Deliverable 3, section 5)

| Bug ID | Defect Title | Module | Linked Test Cases | Traceability Source |
|---|---|---|---|---|
| BUG-001 | Missing duplicate Email check (FSD 5.3) | Save Action | TC_SAV_003, TC_SAV_004 | FSD 5.3 & Equivalence Partitioning / Data Integrity |
| BUG-002 | Missing duplicate ID Number check (FSD 5.3) | Save Action | TC_SAV_005 | FSD 5.3 & Equivalence Partitioning / Data Integrity |
| BUG-003 | Non-SG Country dropdown includes "Singapore" | Non-SG Address | TC_NSG_002 | FSD Section 4.4.2 & Decision Table |
| BUG-004 | Multiple rapid Save actions may trigger duplicate account creation processing | Save Action | TC_SAV_006 | Error Guessing / Concurrency Robustness |
| BUG-005 | Relationship Enum displays Father/Mother instead of FSD 4.3 list | Emergency Contact | TC_EC_003 | FSD Table 4.3 vs Mock App behavior. |
| BUG-006 | Cancel button misses Dirty State on Radio/Dropdown | Cancel Action | TC_CAN_004 | CQ-10 & FSD Section 5.4 |
| BUG-007 | Maximum-length validation does not comply with FSD on five fields | Form Input Fields | TC_PI_003, TC_PI_009, TC_EC_002, TC_SG_007, TC_SG_008 | FSD Tables 4.1, 4.3, 4.4.1 & BVA |
| BUG-008 | Mandatory messages non-standard vs FSD 5.2 | Mandatory Fields | TC_PI_019, TC_CI_009, TC_EC_005, TC_SG_010 | FSD Section 5.2 Mandatory Standard |
| BUG-009 | ID Type dropdown contains undocumented option "S-Pass" | Personal Info | TC_PI_006 | FSD Table 4.1 vs narrative section mismatch; clarification required. |
| BUG-010 | Missing ID Number Checksum algorithm (Mock App does not implement any checksum logic) | Personal Info | TC_PI_008 | FSD Section 5d (Provisional pending BA/PO confirmation) |