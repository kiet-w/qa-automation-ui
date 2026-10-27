"""
pages/f10/locators.py - Centralized Playwright Locators for FAS Direct Application.
Extracted and verified via BSK (Browser-Skill Reconnaissance) live DOM.
Compliant with Invariant 9 (< 100 lines) and Invariant 6.
"""

# Shell & Authentication
LANG_SELECT = "select"
BTN_LOGOUT = "button:has-text('Log out')"

# Section 1: Applicant Details Card
CARD_APPLICANT = "article:has-text('Applicant details')"
APPLICANT_FULL_NAME = "#applicant-fullName"
APPLICANT_NRIC = "#applicant-nric"
APPLICANT_DOB = "#applicant-dateOfBirth"
APPLICANT_GENDER = "input[name='applicant-gender']"
APPLICANT_NATIONALITY = "#applicant-nationality"
APPLICANT_RACE = "#applicant-race"
APPLICANT_RELATIONSHIP = "#applicant-relationship"
APPLICANT_PHONE = "#applicant-phoneNumber"
APPLICANT_EMAIL = "#applicant-email"
APPLICANT_ADDRESS = "#applicant-address"
APPLICANT_COMMITMENT = "#applicant-commitmentAgreed"
APPLICANT_FORWARD_SCHOOL = "#applicant-forwardToSchoolAgreed"

# Section 2: Beneficiary Details Cards
CARDS_BENEFICIARY = "section[aria-labelledby='beneficiaries-heading'] article"
BENEFICIARY_FULL_NAME = "input[id^='beneficiary-'][id$='-fullName']"
BENEFICIARY_NRIC = "input[id^='beneficiary-'][id$='-nric']"
BENEFICIARY_DOB = "input[id^='beneficiary-'][id$='-dateOfBirth']"
BENEFICIARY_SCHOOL = "input[id^='beneficiary-'][id$='-schoolName']"
BENEFICIARY_CLASS_LEVEL = "select[id^='beneficiary-'][id$='-classLevel']"
BENEFICIARY_GRADE = "input[id^='beneficiary-'][id$='-grade']"
BTN_ADD_BENEFICIARY = "button:has-text('Add beneficiary')"
BTN_REMOVE_BENEFICIARY = "button:has-text('Remove beneficiary')"

# Section 3: Family Member Details Cards
CARDS_FAMILY = "section[aria-labelledby='family-members-heading'] article"
FAMILY_FULL_NAME = "input[id^='family-member-'][id$='-fullName']"
FAMILY_NRIC = "input[id^='family-member-'][id$='-nric']"
FAMILY_DOB = "input[id^='family-member-'][id$='-dateOfBirth']"
BTN_ADD_FAMILY = "button:has-text('Add family member')"
BTN_REMOVE_FAMILY = "button:has-text('Remove family member')"

# Section 4: Actions, Server Feedback & Confirmation Card
BTN_SUBMIT = "button[type='submit'], button:has-text('Submit application')"
ALERT_SERVER_ERROR = "#fas-server-error"
CONFIRMATION_TITLE = "#fas-confirmation-title"
CONFIRMATION_CARD = "div[class*='confirmation']"
CONFIRMATION_CODE = "dt:has-text('Application reference') + dd"
CONFIRMATION_STATUS = "dt:has-text('Status') + dd"
CONFIRMATION_SUBMITTED_AT = "dt:has-text('Submitted at') + dd"
BTN_START_NEW = "button:has-text('Start a new application')"
