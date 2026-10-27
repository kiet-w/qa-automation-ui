

|  | Gap | Assumption | Question |
| --- | --- | --- | --- |
| Q01 | Sprint 1 scope: Functional boundaries and expected deliverables for R1, R3, R8 are not yet confirmed. | Sprint 1 focuses on account lifecycle, parent account inquiry and foundational school master data. | What are the minimum business capabilities you expect to see in the Sprint 1 demo, particularly for R1, R3 and R8? |
| Q02 | Account Lifecycle: Exact creation/closure triggers and handling of remaining balance or pending transactions are undefined. | Accounts are automatically activated at age 7 and closed at age 16. Transaction history remains accessible, but balance handling is undecided. | What should happen to remaining balances and pending transactions when an Education Account closes at age 16? Are there any exceptions to the automatic lifecycle? |
| Q03 | Citizen Data Source & Synchronization: Authoritative data source, integration approach, permissible storage and synchronization frequency are unspecified. | Use mock citizen data for Sprint 1, storing only essential fields until integration requirements are confirmed. | What is the authoritative source for citizenship, date of birth and student information? Can we use mock data for Sprint 1, and are there any restrictions on storing or synchronizing this information? |
| Q04 | Parent–Child Relationship: The verified relationship source and authorization mechanism are undefined. | Parents can access only verified linked children. Mock relationship mappings can support Sprint 1 development. | How should the system verify which children a parent is authorized to access after Singpass login? Can we simulate these relationships using mock data? |
| Q05 | Personal Details: Required fields, editable fields, MyInfo address retrieval and contact verification are unclear. | Parents can view basic details and edit selected contact information. MyInfo integration and verification mechanisms remain unconfirmed. | Which personal information fields should parents be able to view or update? Should residential addresses come from MyInfo as read-only data? Is verification required when updating email addresses or mobile numbers? |
| Q06 | School Data Structure & Permissions: Relationships between School, Level, Cohort, Class and Student, and the respective management permissions, are unclear. | Each student has one active enrollment/class assignment at a time. MOE HQ has cross-school visibility, while School users manage only authorized school records. | Could you clarify the relationships between School, Level, Cohort, Class and Student, and which records MOE HQ users versus School users should be allowed to create, update or manage? |


B. P1 — Early Refinement / Architecture Dependencies



| ID | Gap | Working Assumption (Unconfirmed) | Client Question |
| --- | --- | --- | --- |
| Q07 | Enrollment Lifecycle: Rules for class assignment, class transfer, school transfer and academic year progression are undefined. | Historical enrollment records are preserved when a student transfers or progresses. | How should class transfers, school transfers and progression to the next academic year be managed? Must historical enrollment records be retained? |
| Q08 | Fee Type–Component Relationship: Cardinality, composition and reusability are unclear. | A Fee Type may contain multiple Fee Components. Whether components are reusable is not yet decided. | How are Fee Types related to Fee Components? Can one Fee Component be shared across multiple Fee Types? |
| Q09 | Fee Management Ownership & Permissions: It is unclear whether MOE HQ or Schools can create, edit or deactivate Fee Types and Components. | MOE HQ manages standardized fee definitions, while schools may manage school-specific fees, subject to approval. | Which fee information should be centrally managed by MOE HQ, and which can School users create, modify or deactivate? |
| Q10 | Fee Component Catalog: Component types, definitions and mandatory attributes are unavailable. | A preliminary set of sample components can support initial development. | Could you provide the expected Fee Component categories and examples, including the attributes required for each component? |
| Q11 | Fee Applicability: The rules for assigning fees to schools, levels, classes, students and academic years are unspecified. | Fees may be assigned based on school, education level and academic year, with student-specific exceptions where applicable. | At which levels should fees be configured and assigned: school, education level, class, individual student or academic year? |
| Q12 | Payment Eligibility: Detailed conditions under which Singaporean students may use their Education Account balance are unspecified. | Only eligible students with active Education Accounts can use their available balance for education-related fees. | Besides Singapore citizenship and having an active Education Account, are there other restrictions on which fees can be paid using the account balance? |
| Q13 | Insufficient Balance: Partial payment and combining payment methods are not defined. | No partial or split-payment behavior is assumed until confirmed. | If the Education Account balance is insufficient, can parents make a partial payment and pay the remaining amount using another method? |
| Q14 | Outstanding Charges: Charge categories, due dates and parent-level versus child-level presentation are undefined. | Charges are associated with individual children and displayed separately, with a possible consolidated parent view. | Which outstanding charges and due dates should parents see? Should these be grouped by child or consolidated at the family level? |
| Q15 | Online Payment Integration: Supported payment methods, gateway and security requirements are unspecified. | External payment integration can initially be simulated until a gateway is selected. | Which online payment methods must be supported, and is there an existing payment gateway we are expected to integrate with? |
| Q16 | Payment Exceptions: Failed payment, refund eligibility, refund destination and responsibility are undefined. | Failed payments do not create successful payment records. Refund processing requires separately defined rules. | How should the system handle unsuccessful payments and refunds, and which users are responsible for approving or processing refunds? |
| Q17 | Transaction History & Statements: Audit fields, retention period and PDF statement requirements are unclear. | Transaction details are retained for inquiry, while the retention duration and PDF functionality remain unconfirmed. | What transaction details must be retained and displayed, for how long, and do parents need downloadable PDF statements? |
| Q18 | Master Data Audit: Logging and tracking requirements for administrative changes are unspecified. | The system records the actor, timestamp and affected record for relevant master data changes. | Which master data changes require an audit trail, and must the system retain both previous and updated values? |


C. P2 — Later Sprint Clarification



| ID | Gap | Working Assumption (Unconfirmed) | Client Question |
| --- | --- | --- | --- |
| Q19 | FAS Fee Display: Presentation of original fees, subsidies and final payable amounts is unspecified. | Parents can see the final payable amount after approved subsidies, with a breakdown if required. | How should original fees, FAS subsidy amounts and final payable amounts be displayed to parents? |
| Q20 | AI Assistant Escalation: The fallback or escalation process when the AI cannot answer is undefined. | The assistant provides a fallback message and directs users to an approved support channel. | What should happen when the AI assistant cannot answer a parent's question? Should it direct them to an existing support channel? |
| Q21 | AI Content Governance: Knowledge ownership, content validation and updating responsibilities are not defined. | MOE HQ is the proposed content owner, subject to confirmation. | Who will provide, approve and maintain the official information used by the AI assistant? |
| Q22 | AI Accuracy Evaluation: Test questions, scoring methodology and acceptance thresholds are unspecified. | AI responses will be evaluated using an agreed test question set and measurable criteria. | Can you provide representative questions for testing the AI assistant, and what criteria should determine whether its responses are acceptable? |

