# FAS Application Validation (R10) \- Draft

Page: e-Service Portal → Financial Assistance Scheme application *(route to confirm with Dev)*

Some auto-filled fields that are disabled from input have not been updated yet. To be updated after new UI and function completed&nbsp;

## Applicant details

| Field | Rule | Message |
| :---- | :---- | :---- |
| Full name | Required; maximum 150 characters *(Assume rule, same as Parent\_Profile FullName)*; letters, spaces and `, . ' - / @ ( )` only *(Assume rule)*; leading and trailing spaces are trimmed | Blank: `MSG-0001` — “Enter your full name”. Over limit: “Enter no more than 150 characters.” *(Assume message)* Invalid: “Full name can only contain letters, spaces and , . ' \- / @ ( )” *(Assume message)* |
| NRIC / FIN | Required; exactly 9 characters: first letter S, T, F, G or M, 7 digits, last letter A–Z; must pass the Singapore NRIC/FIN checksum; not case sensitive, saved in upper case *(Assume rule)* | Blank: `MSG-0001` — “Enter your NRIC / FIN”. Invalid: “Enter a valid NRIC / FIN, like S1234567D.” *(Assume message)* |
| Date of birth | Required; valid date; not in the future; applicant is 18 or older *(Assume rule)* | Blank: `MSG-0001` — “Enter your date of birth”. Invalid: “Enter a valid date.” *(Assume message)* Future: “Date of birth cannot be in the future.” *(Assume message)* Under 18: “The applicant must be 18 or older.” *(Assume message)* |
| Gender | Required; one of Male, Female, Other | Blank: `MSG-0001` — “Select your gender” |
| Nationality | Required; one option from the list *(list to confirm with BA)* | Blank: `MSG-0001` — “Select your nationality” |
| Race | Required; one of Chinese, Malay, Indian, Eurasian, Others *(Assume rule, list taken from FS10)* | Blank: `MSG-0001` — “Select your race” |
| Relationship to beneficiary | Required; one of Father, Mother, Legal guardian, Grandfather, Grandmother, Sibling, Uncle, Aunt, Cousin, Other (FS10) | Blank: `MSG-0001` — “Select your relationship to the beneficiary” |
| Phone number | Required; exactly 8 digits; starts with 6, 8 or 9 (same as R8) | Blank: `MSG-0001` — “Enter your phone number”. Invalid: `MSG-0805` — “Enter a mobile number in the correct format, like 9123 4567” |
| Email address | Required; valid email format; maximum 150 characters (same as R8) | Blank: `MSG-0001` — “Enter your email address”. Invalid or over 150 characters: `MSG-0806` — “Enter an email address in the correct format, like [name@example.com](mailto:name@example.com)” |
| Address | Required; maximum 255 characters *(Assume rule)*; leading and trailing spaces are trimmed | Blank: `MSG-0001` — “Enter your address”. Over limit: “Enter no more than 255 characters.” *(Assume message)* |
| I agree to the declaration and commitment. | Required tick (BR7) | Not ticked: “Agree to the declaration and commitment to submit.” *(Assume message)* |
| I agree that this application may be forwarded to the school. | Optional; unticked by default. Saved as Also consider SBFAS (ConsiderSbfas). | None |

## Beneficiary details (one block per child)

| Field | Rule | Message |
| :---- | :---- | :---- |
| Full name | Required; maximum 150 characters; same character rule as the applicant name *(Assume rule)* | Blank: `MSG-0001` — “Enter the beneficiary's full name”. Over limit: “Enter no more than 150 characters.” *(Assume message)* |
| NRIC / FIN | Required; same format and checksum as the applicant; must not repeat another beneficiary, the applicant or a family member *(Assume rule)* | Blank: `MSG-0001` — “Enter the beneficiary's NRIC / FIN”. Invalid: “Enter a valid NRIC / FIN, like T1234567J.” *(Assume message)* Duplicate: “This NRIC / FIN is already used in this application.” *(Assume message)* |
| Date of birth | Required; valid date; not in the future; younger than 16 on the submit date (BR1) | Blank: `MSG-0001` — “Enter the beneficiary's date of birth”. Future: “Date of birth cannot be in the future.” *(Assume message)* 16 or older: “This child has turned 16 and cannot apply.” *(Assume message, based on FS10 “turned 16, cannot apply”)* |
| Gender | Required; one of Male, Female, Other | Blank: `MSG-0001` — “Select the beneficiary's gender” |
| School name | Required; maximum 150 characters *(Assume rule)* | Blank: `MSG-0001` — “Enter the school name”. Over limit: “Enter no more than 150 characters.” *(Assume message)* |
| Class level | Required; one option from the list *(list to confirm with BA)* | Blank: `MSG-0001` — “Select the class level” |
| Grade | Required; maximum 20 characters *(Assume rule)* | Blank: `MSG-0001` — “Enter the grade”. Over limit: “Enter no more than 20 characters.” *(Assume message)* |
| Add beneficiary | Adds an empty block; maximum 10 beneficiaries *(Assume rule)* | At limit: button disabled, “You can add up to 10 beneficiaries.” *(Assume message)* |
| Remove beneficiary | Disabled when only one beneficiary is left; at least 1 beneficiary is required | None (button disabled) |

## Family member details (one block per member)

| Field | Rule | Message |
| :---- | :---- | :---- |
| Full name | Required; maximum 150 characters; same character rule as the applicant name *(Assume rule)* | Blank: `MSG-0001` — “Enter the family member's full name”. Over limit: “Enter no more than 150 characters.” *(Assume message)* |
| NRIC / FIN | Required; same format and checksum as the applicant; must not repeat the applicant, a beneficiary or another member *(Assume rule)* | Blank: `MSG-0001` — “Enter the family member's NRIC / FIN”. Invalid: “Enter a valid NRIC / FIN, like S1234567D.” *(Assume message)* Duplicate: “This NRIC / FIN is already used in this application.” *(Assume message)* |
| Date of birth | Required; valid date; not in the future | Blank: `MSG-0001` — “Enter the family member's date of birth”. Future: “Date of birth cannot be in the future.” *(Assume message)* |
| Gender | Required; one of Male, Female, Other | Blank: `MSG-0001` — “Select the family member's gender” |
| Has income | Required; Yes or No | Blank: `MSG-0001` — “Select whether the family member has income” |
| Add family member | Adds an empty block; maximum 15 members *(Assume rule)* | At limit: button disabled, “You can add up to 15 family members.” *(Assume message)* |
| Remove family member | Always available; the application can have 0 family members *(Assume rule, the button is enabled with one member)* | None |

## Submit behavior

- Submit application checks all fields. If a required field is blank or a value is invalid, show the message beside that field, scroll to the first error, and do not submit.  
- Before saving, the system checks BR1 for each beneficiary: younger than 16, no Pending application, and the MOEFAS form or the school's SBFAS form is open. Has a Pending application: “{Beneficiary name} already has an application under review.” *(Assume message)* Form closed: “The application form is closed. It opens on DD/MM/YYYY.” *(Assume message)*  
- On success, the system creates one application per beneficiary with the same applicant and family data (BR4). Toast: “Application submitted for assessment.” (1 beneficiary) or “Applications submitted.” (2 or more), from FS10.  
- If submit fails, nothing is saved and the entered values stay on the page. “We could not submit your application. Please try again.” *(Assume message)*  
- Pressing Submit application twice must not create duplicate applications *(Assume rule)*.

## Notes

- `MSG-0001` is the required-field message: “Enter your <field>” / “Select <field>”, reused from R8. `MSG-0805` and `MSG-0806` are reused from R8 for phone and email.  
- Messages marked *(Assume message)* are suggested copy. Message codes for R10 are not defined yet.  
- Main rules to confirm: NRIC/FIN format and checksum, duplicate NRIC/FIN, name and address lengths, applicant minimum age, maximum beneficiaries and members, whether 0 family members is allowed, and the Nationality and Class level lists.