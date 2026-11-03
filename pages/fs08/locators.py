"""
pages/fs08/locators.py - DOM Locators for Citizen Portal / EduSave E-Service (/parent/*, /transactions, /profile).
Centralizes all CSS selectors and XPath queries for the Citizen Portal.
"""

class ParentLoginLocators:
    """Locators for Singpass Login & MockPass Portal."""
    LOGIN_HEADING = 'role=heading[name="Parent portal login"]'
    SIGN_IN_WITH_SINGPASS_BTN = 'role=button[name="Sign in with Singpass"]'
    MOCKPASS_HEADING = 'role=heading[name="Log in with Singpass"]'
    MOCKPASS_TAB_APP = 'role=tab[name="Singpass app"]'
    MOCKPASS_TAB_PASSWORD = 'role=tab[name="Password login"]'
    MOCKPASS_CITIZEN_SELECT = 'role=combobox[name="Test Citizen Profile"]'
    MOCKPASS_SUBMIT_BTN = 'role=button[name="Log in with Singpass"]'
    MOCKPASS_PASSWORD_NRIC_INPUT = 'role=textbox[name="SINGPASS ID (NRIC / FIN)"]'
    MOCKPASS_PASSWORD_INPUT = 'role=textbox[name="PASSWORD"]'
    MOCKPASS_PASSWORD_UUID_INPUT = 'role=textbox[name="SINGPASS UUID"]'
    MOCKPASS_PASSWORD_SUBMIT_BTN = 'role=button[name="Log in"]'


class EServiceShellLocators:
    """Shared authenticated portal controls observed in the live accessibility tree."""
    SKIP_TO_MAIN = 'role=link[name="Skip to main content"]'
    BRAND_HOME = 'role=link[name="EduFAMS E-Service"]'
    GUIDED_TOUR = 'role=button[name="Guided tour"]'
    OPEN_USER_OPTIONS = 'role=button[name="Open user options"]'
    USER_OPTIONS_NAV = 'role=navigation[name="User options"]'
    PROFILE_LINK = 'role=link[name="My Profile"]'
    FAS_LINK = 'role=link[name="FAS Application"]'
    LOGOUT_BUTTON = 'role=button[name="Log out"]'
    SWITCH_TO_VIETNAMESE = 'role=button[name="Switch language to Vietnamese"]'


class DashboardLocators:
    """Dashboard locator set for account cards and invoice navigation."""
    HEADING = 'role=heading[name="Your family’s education, at a glance"]'
    WALLETS_HEADING = 'role=heading[name=/Education wallets/]'
    ACCOUNTS_LIST = 'role=list[name="Education accounts"]'
    ACCOUNT_ITEMS = 'role=list[name="Education accounts"] >> role=listitem'
    ACCOUNT_ARTICLES = 'role=list[name="Education accounts"] >> role=article'
    ACCOUNT_DETAILS_LINK = 'role=link[name=/View education account details for/]'
    INVOICES_REGION = 'role=region[name="Invoices & payments"]'
    INVOICES_LINK = 'role=link[name="View invoices & payments"]'


class EducationAccountLocators:
    REGION = 'role=region[name="Education Account details"]'
    BREADCRUMB = 'role=navigation[name="Breadcrumb"]'
    BACK_BUTTON = 'role=button[name="Back"]'
    HEADING = 'role=heading[name="Education Account details"]'
    ACCOUNT_ARTICLE = 'role=article'
    DETAIL_TERMS = 'role=term'
    INVOICES_LINK = 'role=link[name=/View invoices and payments for/]'
    BILLING_LINK = 'role=link[name=/View billing for/]'


class BillingLocators:
    OVERVIEW_REGION = 'role=region[name="Choose an education account"]'
    OVERVIEW_HEADING = 'role=heading[name="Choose an education account"]'
    ACCOUNTS_LIST = 'role=list[name="Education accounts"]'
    ACCOUNT_ITEMS = 'role=list[name="Education accounts"] >> role=listitem'
    FEES_LINK = 'role=link[name=/View fees for/]'
    DETAIL_REGION = 'role=region[name="Pay education charges"]'
    DETAIL_HEADING = 'role=heading[name="Pay education charges"]'
    CHARGES_ARTICLE = 'role=article[name="Outstanding charges"]'
    STATUS_FILTER = 'role=combobox[name="Filter by status"]'
    SELECT_ALL_FEES = 'role=checkbox[name="Select all outstanding fees"]'
    CHARGES_TABLE = 'role=table[name=/Outstanding charges for/]'
    CHARGE_CHECKBOXES = 'role=checkbox[name=/Select charge:/]'
    PREVIOUS_PAGE = 'role=button[name="Previous"]'
    NEXT_PAGE = 'role=button[name="Next"]'
    CONTINUE = 'role=button[name="Continue"]'


class FasListLocators:
    HEADING = 'role=heading[name="My FAS Applications"]'
    SEARCH = 'role=searchbox[name="Search Applications"]'
    NEW_APPLICATION = 'role=button[name="New Application"]'
    EMPTY_REGION = 'role=region[name="No Applications Found"]'
    EMPTY_STATE_CTA = 'role=button[name="Submit an Application"]'


class PaymentResultLocators:
    REGION = 'role=region[name="Payment result"]'
    HEADING = 'role=heading[name="Payment result"]'
    ALERT = 'role=alert'


class ParentProfileLocators:
    """Locators for Parent Profile & Contact Details Editing."""
    PROFILE_HEADING = 'role=heading[name="My Profile"]'
    UPDATE_DETAILS_BTN = 'role=button[name="Update details"]'
    SHOW_NRIC_BTN = 'role=button[name="Show NRIC"]'
    HIDE_NRIC_BTN = 'role=button[name="Hide NRIC"]'
    IDENTITY_REGION = 'role=region[name="Singpass verified identity (read-only)"]'
    CONTACT_REGION = 'role=region[name="Contact information"]'
    MAILING_REGION = 'role=region[name="Mailing address"]'
    UPDATE_FORM = 'role=form[name="Update details"]'
    FULL_NAME_VAL = 'role=term[name="Full Name"] >> xpath=following-sibling::dd[1]'
    NRIC_VAL = 'role=term[name="NRIC / FIN"] >> xpath=following-sibling::dd[1]'
    RESIDENTIAL_ADDRESS_VAL = 'role=region[name="Singpass verified identity (read-only)"]'
    CONTACT_MOBILE_VAL = 'role=region[name="Contact information"]'
    CONTACT_EMAIL_VAL = 'role=region[name="Contact information"]'
    MAILING_ADDRESS_VAL = 'role=region[name="Mailing address"]'
    INPUT_PHONE = 'role=textbox[name="Mobile Number"]'
    INPUT_EMAIL = 'role=textbox[name="Email Address"]'
    INPUT_BLOCK = 'role=textbox[name="Block"]'
    INPUT_STREET = 'role=textbox[name="Street"]'
    INPUT_UNIT = 'role=textbox[name="Unit"]'
    INPUT_POSTAL = 'role=textbox[name="Postal code"]'
    INPUT_COUNTRY = 'role=textbox[name="Country"]'
    DIRTY_STATE_HINT = "p:has-text('Make a change to enable saving.'), p:has-text('Hãy thay đổi một mục để bật nút lưu.')"
    SAVE_CHANGES_BTN = 'role=button[name="Save changes"]'
    CANCEL_BTN = 'role=button[name="Cancel"]'
    CONFIRM_ALERTDIALOG = "[role='alertdialog'], [role='dialog']"
    DIALOG_KEEP_EDITING_BTN = '[role="alertdialog"] button:has-text("Keep editing"), [role="dialog"] button:has-text("Keep editing")'
    DIALOG_CONFIRM_SAVE_BTN = '[role="alertdialog"] button:has-text("Save changes"), [role="dialog"] button:has-text("Save changes")'
    DIALOG_ERROR_MSG = "[role='alertdialog'] [role='alert'], [role='dialog'] [role='alert']"
    SUCCESS_TOAST = "p[role='status'], [role='status']:has-text('Your details have been updated.'), [role='status']:has-text('Thông tin của bạn đã được cập nhật.')"


class TransactionsLocators:
    """Locators for Transaction History, Filtering, and Invoice Details."""
    PAGE_HEADING = 'role=heading[name="Invoices & payments"]'
    BREADCRUMB = 'role=navigation[name="Breadcrumb"]'
    BACK_BUTTON = 'role=button[name="Back"]'
    STUDENT_FILTER_LABEL = 'role=combobox[name="Child"]'
    STUDENT_SELECT = 'role=combobox[name="Child"]'
    INVOICES_HEADING = 'role=heading[name="Invoices & payments"]'
    INVOICE_SECTION_TITLE = "h2[class*='invoiceSectionTitle']"
    INVOICE_COUNT = "span[class*='invoiceCount']"
    TABLE = "table"
    TABLE_CAPTION = "table caption"
    TABLE_HEADERS = "table thead th, table tr:first-child th"
    TABLE_ROWS = "table tbody tr"
    INVOICE_NUMBER = "span[class*='invoiceNumber']"
    INVOICE_STATUS = "span[class*='invoiceStatus']"
    DISCLOSURE_BUTTON = "button[class*='disclosureButton'], button[aria-expanded]"
    DISCLOSURE_CELL = "td[class*='disclosureCell'], td[id^='invoice-details-']"
    FUNDING_TABLE = "table[class*='fundingTable']"
    CHARGES_HEADING = "h3[class*='chargeHeading']"
    CHARGES_ERROR_ALERT = "section[aria-label*='charges'] div[role='alert']"
    PAGE_SIZE_SELECT = "div[class*='paginationBar'] select, select[class*='pageSize']"
    PAGINATION_CONTAINER = "nav[aria-label*='Pagination'], [class*='paginationBar']"
    PAGINATION_PREV = "button[aria-label*='Previous'], button:has-text('Previous')"
    PAGINATION_NEXT = "button[aria-label*='Next'], button:has-text('Next')"
    ALERT_ERROR = "div[role='alert'][class*='error'], div[role='alert']"
    ALERT_WARNING = "div[role='alert'][class*='warning']"
    RETRY_BTN = "button:has-text('Retry'), button:has-text('Try again')"
    EMPTY_STATE_REGION = 'role=region[name="No invoices yet"]'
    EMPTY_STATE = 'role=heading[name="No invoices yet"]'
    LOADING_SPINNER = "p[role='status']:has-text('Loading')"
