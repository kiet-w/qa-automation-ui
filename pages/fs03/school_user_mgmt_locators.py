"""
pages/fs03/school_user_mgmt_locators.py - Verified BSK DOM locators for School User Management
(Bulk CSV tab, Detail/Assignment screen) per specs/ui_bsk/.../04_school_user_management.md §1.2/§1.3.
Strictly locator constants. Complies with Invariant 1 and modularity limits (<100 lines).
"""


class BulkCsvLocators:
    """BSK-verified locators for Bulk CSV mode on /school-user-management/new (DOM §1.2)."""

    BULK_TAB = "button[role='tab']:has-text('Bulk CSV'), button:has-text('Bulk CSV')"
    FILE_INPUT = "input[type='file'][accept*='.csv'], #school-users-csv"
    IMPORT_BUTTON = "button:has-text('Upload CSV'), button:has-text('Import')"
    TEMPLATE_BUTTON = "button:has-text('Download template'), button:has-text('Get Template')"
    RESET_BUTTON = "button:has-text('Reset')"
    # Feedback surfaces: inline alert, toast, aria-live result region (DOM §4.1/§4.2).
    FEEDBACK = "[role='alert'], [role='status'], div[aria-live='polite']"
    RESULT_REGION = "div[aria-live='polite'], table[class*='preview'], [role='dialog'] table"


class SchoolUserDetailLocators:
    """BSK-verified locators for /school-user-management/:id (DOM §1.3)."""

    PAGE_HEADING = "h1"
    BACK_TO_LIST = "button:has-text('Back to school users'), button:has-text('Back to list')"
    ACCOUNT_CARD = "section:has(h2:has-text('User account'))"
    PROFILE_CARD = "section:has(h2:has-text('Profile'))"
    SCHOOL_CARD = "section:has(h2:has-text('School'))"
    SCHOOL_COMBOBOX = "#school-user-school"
    ASSIGN_BUTTON = "button:has-text('Assign school')"
    # Security audit helpers (TC-FS03-SUM-010 / SUM-067).
    PASSWORD_FIELDS = "input[type='password'], input[autocomplete*='password' i]"
    UNSAFE_VALUE_ATTRS = "[data-nric], [data-email], [aria-label*='NRIC' i]"


class SchoolUserListLocators:
    """Extra list-screen locators not covered by SchoolUserManagementPage (DOM §1.1)."""

    HEADING = "h1:has-text('School user management')"
    ROWS = "table tbody tr"
    ROW_DETAIL = "button[aria-label='Detail'], tbody tr a[href*='school-user-management/']"
    EMPTY_STATE = "tbody tr:has-text('No school users'), [role='status']:has-text('No school users')"
    ALERT = "[role='alert']"
