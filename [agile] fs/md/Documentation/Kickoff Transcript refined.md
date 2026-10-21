**CLEANED MEETING TRANSCRIPT**  
**CLIENT REQUIREMENT CLARIFICATION**

*Source recording: client-meeting\_sprint-1.m4a | Approx. 28 minutes*

**Editing note:** The wording below has been cleaned up for readability while preserving the discussion and its meaning. It is not a strict verbatim transcript. Speaker labels are based on the conversation context; unclear or incomplete details are explicitly flagged for verification.

# **1\. Overview of the Proposed Solution (00:00–09:00)**

**Delivery Team:** Based on the initial requirements, we have grouped the proposed solution into several functional areas. First, core data and setup: the system will maintain student and school information and link each student to their parent or guardian. When a parent or guardian signs in through Singpass, the system can identify the student account(s) linked to them.

**Delivery Team:** Second, the education-account lifecycle: the system will check whether a student meets the eligibility rules, create an account where applicable, and manage account closure. The eligibility rules may include age, nationality and other criteria that still need to be confirmed.

**Delivery Team:** Third, account funding and top-ups: authorised MOE HQ users will be able to manage individual or batch top-ups according to configurable rules. Fourth, fee management: schools will maintain fee structures and manage charges and outstanding fees.

**Delivery Team:** The solution will also support parent access to linked education-account information, Financial Assistance Scheme (FAS) applications and eligibility assessment, processing of approved assistance, budget tracking, reporting, and user-access simulation. AI-assisted features were also mentioned in the high-level overview.

**Delivery Team:** This is our initial interpretation of the requirements, not a final design. We would like to check whether these functional areas broadly match your expectations and whether there are any major gaps.

**Client:** The main functional areas appear to be covered, but it is too early to confirm the details at this stage. The arrows in the diagram represent the flow between functions; they should not be interpreted as meaning that every step is automatically processed by the system.

**Delivery Team:** Understood. We do not have prototypes ready yet, so we will proceed with the clarification questions.

# **2\. Proposed Sprint 1 Scope (08:45–11:15)**

**Delivery Team:** We do not expect to resolve every question in this meeting. For Sprint 1, we propose focusing on the requirements related to parents accessing the system and viewing their linked child’s education-account details. Does that seem like a suitable starting scope?

**Client:** The proposed scope is reasonable. However, the parent-facing portal will need a backend database to store and retrieve education-account details. The work cannot focus only on the front end.

**Delivery Team:** Agreed. Sprint 1 will cover the parent-facing portal, the necessary backend data work, and part of the administration portal.

**Transcript note:** The discussion refers to requirement/user-story numbers 1, 3, 8 and 9, but the exact mapping is not sufficiently clear in the recording/transcript. Verify these references against the requirements list before using them in formal documentation.

# **3\. Account Closure and Student Data (11:15–13:15)**

**Delivery Team:** The initial understanding is that an education account is activated at age 7 and closed at age 16\. If the account is closed, how should the system handle any pending transactions or remaining balance?

**Client:** There should be no pending transactions when the account is closed. Any remaining balance should be transferred to CPF.

**Delivery Team:** To create the education account, we also need to confirm which student data can be retrieved from the third-party system. Which fields should be included?

**Client:** The fields discussed were the student’s name, date of birth, citizenship and address, if the address is available.

**Transcript note:** The activation/closure ages and the availability of each data field should be checked against the formal requirements and source-system capabilities.

# **4\. Education Account and FAS Eligibility (13:15–16:30)**

**Delivery Team:** Our initial understanding was that only Singapore citizens can have an education account. We would like to clarify how this relates to nationality criteria for FAS eligibility.

**Client:** An education account is similar to a bank account for education purposes, not a login account. The government deposits money into it for eligible education expenses. Permanent residents and foreign students may attend schools in Singapore without having an education account. They would pay school fees from their own funds rather than from an education account.

**Delivery Team:** Understood. Education-account eligibility and FAS eligibility should therefore be treated as separate rules. We will need to confirm the detailed criteria for each.

# **5\. Parent/Guardian Access and School Hierarchy (16:30–19:45)**

**Delivery Team:** We propose establishing the parent/guardian-to-student relationship when student information is obtained from the third-party system. After the parent or guardian signs in through Singpass, the system will check the relationship and allow access only to the relevant linked child account(s). We also need to confirm which parent profile fields may be edited.

**Delivery Team:** We would also like to clarify the relationship between school level, cohort, class and student.

**Client:** Schools may use the terms “level” and “cohort” interchangeably. For example, Primary 1 and Primary 2 refer to levels. Class is a separate concept.

**Delivery Team:** What records should MOE HQ users and school users be able to create, update or manage?

**Client:** HQ users should be able to manage all relevant records. School users should be able to manage records at their own school level and below.

**Delivery Team:** We also need to clarify the rules for class assignment, class transfers, school transfers and progression, including how these changes affect the student’s records.

**Client:** School enrolment status and education-account status are separate; one should not be treated as determining the other.

# **6\. Fee Management and Reusable Components (19:45–23:53)**

**Delivery Team:** For fee management, our initial interpretation was that school users could assign education fees to student accounts. Could you provide a real use case so we can confirm how this should work?

**Client:** It would be useful if a fee component could be reused across multiple fee types. For example, GST is a common component and should not need to be configured separately for every fee type.

**Delivery Team:** Could you provide the expected fee categories, examples and mandatory attributes for each fee component?

**Client:** Examples include school fees, miscellaneous fees, extracurricular activities such as music classes or school trips, and ad hoc charges. Some charges may apply to a particular level or class. There may also be charges for damage to classroom property, such as a broken window.

**Delivery Team:** We will need the fee-type definitions and the required attributes to define the fee-component model. The detailed fee-assignment use case also needs to be confirmed.

# **7\. Performance Testing and Concurrent Users (24:15–27:20)**

**Technical/Performance Team:** For performance testing, could you provide the expected user population and likely peak usage periods for the administration and parent-facing portals?

**Client:** The indicative population is around 500 HQ users, approximately 300 schools with an estimated 200 users per school, and potentially 2 million parents. These figures represent potential users, not users accessing the system simultaneously.

**Technical/Performance Team:** Could you clarify the expected usage hours and peak periods?

**Client:** HQ and school users may actively use the system from around 8:00 a.m. to 7:00 p.m. The parent-facing portal may be accessed from around 6:00 a.m. to 2:00 a.m. There is no fixed peak period, but usage may increase around bill-payment periods.

**Client:** Based on these figures and usage patterns, the delivery team should propose appropriate concurrent-user targets for both the administration portal and the parent-facing portal.

# **8\. Close (27:20–28:15)**

**Delivery Team:** Thank you for clarifying the initial requirements. We will capture the outstanding points and continue refining the requirements in the upcoming workshops.

**Client:** Thank you.

# **Items to Verify Before Formal Use**

* Exact requirement/user-story numbers proposed for Sprint 1\.  
* Education-account activation and closure ages.  
* Complete list of student fields available from the third-party system.  
* Detailed education-account eligibility and FAS eligibility rules.  
* Exact meaning of “level” and “cohort” in the client’s data model.  
* Detailed fee-assignment use case, fee types and mandatory fee-component attributes.  
* Whether any additional speaker statements or details are unclear in the source recording.