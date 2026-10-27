      **MINUTES OF AGILE PROJECT KICK-OFF MEETING**

**12 OCT (MONDAY) AT 1:30 PM VIA TEAMS**

**Reference Document:**

| Meeting’s Transcript | [Transcript](https://docs.google.com/document/d/1F_BRbQKK_YRrj0phpMIZ5IeY8tiH2hwq5fnV6AesLPQ/edit?usp=sharing) |
| :---- | :---- |

**Agenda**

| S/N | Agenda | Action By |
| :---- | :---- | ----- |
| **1** | **High-level Solution & Functional Scope**  |  |
|  | The delivery team presented the proposed functional areas: core data and setup; education-account eligibility and lifecycle; funding/top-up; fee management; parent access; Financial Assistance Scheme (FAS); and monitoring/reporting. The client said the main areas appeared to be covered, but detailed confirmation would be premature. Arrows in the diagram indicate process flow and do not necessarily imply automated processing. Notes: The client considered the high-level modules broadly aligned, but detailed confirmation will continue during requirement workshops/sprints.  | **For Info** |
| **2** | **Sprint 1 Scope**  |  |
|  | The initial focus discussed was parent/guardian access to view the education account linked to their child. The scope also requires backend/database work and part of the administration portal. The exact requirement/user-story references were unclear and should be checked against the formal requirements. **\[Action Item\] Update the Sprint 1 scope and dependencies in the requirements, and verify the referenced requirement/user-story numbers.**  |  **For Info**   |
| **3** | **Education Account Lifecycle & Source Data**  |  |
|  | The discussion covered account activation and closure ages; these age rules require confirmation against the formal requirements. At closure, pending transactions should be cleared and any remaining balance transferred to CPF. Student data discussed for retrieval included name, date of birth, citizenship and address where available; this is not yet a complete data specification. **Notes:** The client clarified that an education account is a government-funded account, not a login account. At closure, there should be no pending transactions and any remaining balance should be transferred to CPF.  **\[Action Item\] Confirm the complete student data fields available from third-party sources**. **\[Action Item\] Document the closure handling, including pending transactions and remaining-balance transfer, in the requirements.**  |  **For Info**  |
| **4** | **Education Account Eligibility & FAS** |  |
|  | The client clarified that an education account is a government-funded account for eligible education expenses, not a system login. Permanent residents and foreign students may attend school without an education account and may need to pay school fees from their own funds. Education-account eligibility and FAS eligibility are separate criteria; detailed rules remain open.  **Notes:** **\[Action Item\] Confirm the eligibility criteria for education accounts and the separate FAS eligibility and assessment rules.** |  **For Info**  |
| **5** | **Parent/Guardian Access & School Hierarchy** |  |
|  | The proposed approach is to establish parent/guardian-to-student links when data is loaded and validate the relationship after Singpass authentication. Fields parents/guardians may edit require confirmation.  The client noted that “level” and “cohort” may be used interchangeably depending on school terminology, while class is a separate concept. MOE HQ users should manage all relevant records; school users should manage records for their own school level and below. School-enrolment status and education-account status must remain separate. **Notes:** **\[Action Item\] Confirm the parent/guardian fields that may be edited and the parent-to-student linking/access rules.  \[Action Item\] Clarify the definitions of level, cohort and class, plus rules for class assignment, class transfers, school transfers and progression.**  |  **For Info**  |
| **6** | **Fee Management & Reusable Fee Components** |  |
|  | The delivery team’s initial interpretation was that school users assign fees to student accounts; a concrete use case is needed to validate the workflow.  The client highlighted the value of reusable fee components across fee types (e.g., configuring GST once for reuse). Examples discussed included school fees, miscellaneous fees, extracurricular activities/trips and ad hoc charges such as damage to classroom property.  Some charges may apply only to a particular level or class. Fee categories, assignment rules and mandatory component attributes remain to be confirmed. **\[Action Item\] Provide representative fee use cases and confirm fee categories, assignment rules, mandatory attributes and reusable-component requirements**.  |  **For Info** |
| **7** | **Performance Testing & Concurrent Users** |  |
|  | Indicative user populations discussed were approximately 500 HQ users, 300 schools with around 200 users per school, and up to 2 million parents. These are total potential users, not concurrent-user targets.  HQ/school usage was estimated at 8:00 a.m.–7:00 p.m.; the parent portal may be used from 6:00 a.m.–2:00 a.m. No fixed peak period was identified, although usage may rise around bill-payment periods. **Notes:** **\[Action Item\] Propose concurrent-user targets and performance-test scenarios for both portals, considering the indicative populations, usage windows and variable peaks**   |  **For Info**  |

**(The meeting ended at 2:00PM)**

Prepared By: Daniel Tran

