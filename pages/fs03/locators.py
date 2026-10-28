"""
pages/fs03/locators.py - Verified BSK DOM Locators for Admin Login & Microsoft SSO.
Strictly locator constants. Complies with Invariant 1 and modularity limits (<100 lines).
"""

class AdminLoginLocators:
    """BSK-verified locators for Admin Portal Login (:5173)."""
    LOGIN_PATH = "/login"
    CALLBACK_PATH = "/login/microsoft/callback"

    # Form inputs & controls
    LANGUAGE_SELECT = 'select[aria-label="Language"]'
    MOCK_ROLE_SELECT = 'select:has(option[value="MOEHQ"])'
    USERNAME_INPUT = 'input[autocomplete="username"]'
    PASSWORD_INPUT = 'input[autocomplete="current-password"]'
    SIGN_IN_MICROSOFT_BTN = 'button:has-text("Sign in with Microsoft"), button:has-text("Đăng nhập với Microsoft")'
    SIGN_IN_BTN = 'button[type="submit"]:has-text("Sign in"), button[type="submit"]:has-text("Đăng nhập")'
    PASSWORD_TOGGLE_BTN = 'button[aria-label*="password" i]'
    PAGE_HEADING = 'h1:has-text("Sign in to your account"), h1'

    # Feedback & alerts
    MOCK_ALERT = '[role="alert"]:has-text("Mock environment")'
    ALERT = '[role="alert"]'
    ALERT_FAILED = '[role="alert"]:has-text("Sign in failed")'


class MicrosoftSimulatorLocators:
    """BSK-verified locators for Entra Simulator (:5288)."""
    ENTRA_AUTHORIZE_PATH = "/microsoft-provider/oauth2/v2.0/authorize"
    PICK_ACCOUNT_HEADING = "text='Pick an account'"
    MOEHQ_ACCOUNT_TILE = ".account-tile:has-text('admin@IAM.edu.vn'), :text('admin@IAM.edu.vn')"
    SCHOOL_ACCOUNT_TILE = ".account-tile:has-text('staff1@IAM.edu.vn'), :text('staff1@IAM.edu.vn')"
    PARENT_ACCOUNT_TILE = ".account-tile:has-text('head1@IAM.edu.vn'), :text('head1@IAM.edu.vn')"
    USE_ANOTHER_ACCOUNT_BTN = 'button:has-text("Use another account")'
    CONTINUE_BTN = 'button:has-text("Continue")'
    CANCEL_BTN = 'a:has-text("Cancel"), button:has-text("Cancel")'


class SchoolDirectoryLocators:
    """BSK-verified locators for School Management directory (/school-management) - DOM-SCH §1.1/§4.2."""
    PAGE_HEADING = "h1"
    SEARCH_INPUT = 'input[placeholder*="Search by MOE code" i]'
    TYPE_FILTER = 'select:has(option[value="GOVERNMENT"])'
    SEARCH_BUTTON = 'button[type="submit"]:has-text("Search")'
    RESET_BUTTON = 'button:has-text("Reset filters")'
    CREATE_BUTTON = 'button:has-text("Create school")'
    TABLE_HEADERS = "table thead th"
    ROWS = "tbody tr"
    ROW_BADGE = '[class*="badge"]'
    ROW_ACTION_BUTTON = "button"
    ROW_DETAIL_BUTTON = 'button[aria-label="Detail"]'
    ROW_EDIT_BUTTON = 'button[aria-label="Edit"]'
    ROW_DEACTIVE_BUTTON = 'button[aria-label="Deactive"]'
    ROW_ACTIVE_BUTTON = 'button[aria-label="Active"]'
    ROW_LIFECYCLE_BUTTON = 'button[aria-label="Deactive"], button[aria-label="Active"]'
    EMPTY_STATE = 'tbody tr:has-text("No schools"), [role="status"]:has-text("No schools")'
    ALERT = '[role="alert"]'
    INLINE_CODE = 'input[aria-label="MOE school code"]'
    INLINE_NAME = 'input[aria-label="School name"]'
    INLINE_TYPE = 'select[aria-label="School type"]'
    SAVE_INLINE = 'button[aria-label="Save changes"]'
    DISCARD_INLINE = 'button[aria-label="Discard changes"]'
    DIALOG = '[role="dialog"]'
    DIALOG_CONFIRM = '[role="dialog"] button:has-text("Deactivate"), [role="dialog"] button:has-text("Confirm")'
    DIALOG_CANCEL = '[role="dialog"] button:has-text("Cancel")'
    DIALOG_ALERT = '[role="dialog"] [role="alert"]'


class SchoolDetailLocators:
    """BSK-verified locators for School detail screen (/school-management/:schoolId) - DOM-SCH §1.3."""
    BACK_LINK = 'a:has-text("Back to school list")'
    STATUS_BADGE = 'header [class*="badge"]'
    OVERVIEW_SECTION = 'section:has(h2:has-text("Overview"))'
    STUDENTS_TABLE = 'table:has-text("School students")'


class AdminShellLocators:
    """BSK-verified locators for Admin Dashboard Shell (:5173)."""
    DASHBOARD_SHELL = 'aside nav, header, [data-testid="admin-shell"], aside'
    PORTAL_HEADER = 'header [class*="brand"], header'
    LOGOUT_BTN = 'button:has-text("Log out"), button:has-text("Sign out"), a[href*="logout"]'
    CALLBACK_STATUS = '[role="status"]'
    CALLBACK_FAILURE = '[role="status"]:has-text("Sign in failed")'
    ASSIGNMENT_REQUIRED_ALERT = '[role="alert"]:has-text("assignment"), [role="alert"]:has-text("school")'
