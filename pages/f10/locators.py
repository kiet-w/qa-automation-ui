"""Accessible Playwright locators verified against the live FAS form.

Use these role/name selectors with ``page.locator`` or a scoped ``Locator.locator``.
Repeated fields should be scoped to the corresponding article before interaction.
"""

# Portal shell
LANG_SELECT = 'role=button[name="Switch language to Vietnamese"]'
BTN_LOGOUT = 'role=button[name="Log out"]'

# Current single-page form (the old step wizard selectors are obsolete)
FORM_HEADING = 'role=heading[name="Apply for Financial Assistance"]'
MAIN_FORM = 'role=form[name=/Academic year/]'
APPLICANT_CARD = 'role=article[name="Applicant details"]'
CARD_APPLICANT = APPLICANT_CARD
APPLICANT_FULL_NAME = 'role=textbox[name="Full name"]'
APPLICANT_NRIC = 'role=textbox[name="NRIC / FIN"]'
APPLICANT_DOB = 'label=Date of birth'
APPLICANT_GENDER = 'role=combobox[name="Gender"]'
APPLICANT_NATIONALITY = 'role=combobox[name="Nationality"]'
APPLICANT_RACE = 'role=combobox[name="Race"]'
APPLICANT_RELATIONSHIP = 'role=combobox[name="Relationship to beneficiary"]'
APPLICANT_PHONE = 'role=textbox[name="Phone number"]'
APPLICANT_EMAIL = 'role=textbox[name="Email address"]'
APPLICANT_ADDRESS = 'role=textbox[name="Address"]'
APPLICANT_EMPLOYMENT_STATUS = 'role=textbox[name="Employment status"]'
APPLICANT_COMMITMENT = 'role=checkbox[name="I agree to the declaration and commitment."]'

# Repeatable beneficiary and family-member cards. Scope field locators to each card.
BENEFICIARY_REGION = 'role=region[name="Beneficiary details"]'
CARDS_BENEFICIARY = 'role=article[name=/Beneficiary details/]'
BENEFICIARY_FULL_NAME = 'role=textbox[name="Full name"]'
BENEFICIARY_NRIC = 'role=textbox[name="NRIC / FIN"]'
BENEFICIARY_DOB = 'label=Date of birth'
BENEFICIARY_GENDER = 'role=combobox[name="Gender"]'
BENEFICIARY_SCHOOL = 'role=textbox[name="School name"]'
BENEFICIARY_CLASS_LEVEL = 'role=combobox[name="Class level"]'
BENEFICIARY_GRADE = 'role=textbox[name="Grade"]'
BTN_ADD_BENEFICIARY = 'role=button[name="Add beneficiary"]'
BTN_REMOVE_BENEFICIARY = 'role=button[name="Remove beneficiary"]'

FAMILY_REGION = 'role=region[name="Family member details"]'
CARDS_FAMILY = 'role=article[name="Family member details"]'
FAMILY_FULL_NAME = 'role=textbox[name="Full name"]'
FAMILY_NRIC = 'role=textbox[name="NRIC / FIN"]'
FAMILY_DOB = 'label=Date of birth'
FAMILY_GENDER = 'role=combobox[name="Gender"]'
FAMILY_RELATIONSHIP = 'role=combobox[name="Relationship"]'
FAMILY_HAS_INCOME_GROUP = 'role=group[name="Has income"]'
FAMILY_HAS_INCOME_YES = 'role=radio[name="Yes"]'
FAMILY_HAS_INCOME_NO = 'role=radio[name="No"]'
BTN_ADD_FAMILY = 'role=button[name="Add family member"]'
BTN_REMOVE_FAMILY = 'role=button[name=/Remove family member/]'

# Submission/result elements
BTN_SUBMIT = 'role=button[name="Submit application"]'
ALERT_SERVER_ERROR = 'role=alert'
CONFIRMATION_TITLE = 'role=heading[name="Application submitted"]'
CONFIRMATION_CARD = 'role=article[name=/Application submitted/]'
CONFIRMATION_CODE = 'role=term[name="Application reference"]'
CONFIRMATION_STATUS = 'role=term[name="Status"]'
CONFIRMATION_SUBMITTED_AT = 'role=term[name="Submitted at"]'
BTN_START_NEW = 'role=button[name="Start a new application"]'
