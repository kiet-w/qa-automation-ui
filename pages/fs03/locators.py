"""
pages/fs03/locators.py - Verified BSK DOM Locators for Admin Login & Microsoft SSO.
Strictly locator constants. Complies with Invariant 1 and modularity limits (<100 lines).
"""

class AdminLoginLocators:
    """BSK-verified locators for Admin Portal Login (:5173)."""
    LOGIN_PATH = "/login"
    CALLBACK_PATH = "/login/microsoft/callback"

    # Form inputs & controls
    LANGUAGE_SELECT = 'select[aria-label="Language"], select[aria-label="Ngôn ngữ"]'
    MOCK_ROLE_SELECT = 'select:has(option[value="MOEHQ"])'
    USERNAME_INPUT = 'input[placeholder*="username" i], input[placeholder*="tên đăng nhập" i], input[autocomplete="username"]'
    PASSWORD_INPUT = 'input[placeholder*="password" i], input[placeholder*="mật khẩu" i], input[autocomplete="current-password"], input[type="password"]'
    SIGN_IN_MICROSOFT_BTN = 'button:has-text("Sign in with Microsoft"), button:has-text("Đăng nhập với Microsoft")'
    SIGN_IN_BTN = 'button[type="submit"]:has-text("Sign in"), button[type="submit"]:has-text("Đăng nhập")'
    PASSWORD_TOGGLE_BTN = 'button[aria-label*="password" i], button[aria-label*="mật khẩu" i]'
    PAGE_HEADING = '#login-heading, h1:has-text("Login"), h1:has-text("Đăng nhập")'
    PAGE_SUBTITLE = 'p:has-text("Enter your account details"), p:has-text("Nhập thông tin tài khoản"), #login-heading + p'
    DECORATION_IMAGE = 'img[src*="LoginDecoration"], [class*="loginDecoration"]'

    # Feedback & alerts
    MOCK_ALERT = '[role="alert"]:has-text("Mock development mode"), [role="alert"]:has-text("Chế độ phát triển Mock")'
    ALERT = '[role="alert"]'
    ALERT_FAILED = '[role="alert"]:has-text("Unable to sign in"), [role="alert"]:has-text("Không thể đăng nhập"), [role="alert"]:has-text("Sign in failed")'
    TOAST_STATUS = '[role="status"]'
    TOAST_ERROR = '[role="status"]:has-text("Unable to sign in"), [role="status"]:has-text("Không thể đăng nhập"), [role="alert"]'
    FIELD_ERROR = 'p[class*="text-destructive"], p[class*="error"], span[class*="error"], p[id$="-error"], [role="alert"]'


class MicrosoftSimulatorLocators:
    """BSK-verified locators for Entra Simulator (:5288)."""
    ENTRA_AUTHORIZE_PATH = "/microsoft-provider/oauth2/v2.0/authorize"
    PICK_ACCOUNT_HEADING = "h1:has-text('Pick an account'), h1#sign-in-title"
    MOEHQ_ACCOUNT_TILE = ".account-tile:has-text('admin@IAM.edu.vn')"
    SCHOOL_ACCOUNT_TILE = ".account-tile:has-text('staff1@IAM.edu.vn')"
    PARENT_ACCOUNT_TILE = ".account-tile:has-text('head1@IAM.edu.vn')"
    USE_ANOTHER_ACCOUNT_INPUT = 'input#other-email, input[placeholder*="name@example.com"]'
    USE_ANOTHER_ACCOUNT_BTN = 'button.other-account-button, button:has-text("Continue"), button:has-text("Use another account")'
    USE_ANOTHER_ACCOUNT_ERROR = 'p#other-email-error, [role="alert"]'
    CONTINUE_BTN = 'button.other-account-button, button:has-text("Continue")'


class SchoolDirectoryLocators:
    """BSK-verified locators for School Management directory (/school-management) - DOM-SCH §1.1/§4.2."""
    PAGE_HEADING = "#school-management-heading"
    SEARCH_INPUT = 'input[type="search"][placeholder="Search by MOE code or school name"]'
    TYPE_FILTER = 'select:has(option[value="GOVERNMENT"])'
    SEARCH_BUTTON = 'button:has-text("Search")'
    RESET_BUTTON = 'button:has-text("Reset filters")'
    CREATE_BUTTON = 'button:has-text("Create school")'
    TABLE_HEADERS = 'table:has(caption:has-text("School management table")) thead th'
    ROWS = 'table:has(caption:has-text("School management table")) tbody tr'
    ROW_BADGE = 'table:has(caption:has-text("School management table")) tbody tr [role="status"]'
    ROW_ACTION_BUTTON = "button[aria-label]"
    ROW_DETAIL_BUTTON = 'button[aria-label="Detail"]'
    ROW_EDIT_BUTTON = 'button[aria-label="Edit"]'
    ROW_DEACTIVE_BUTTON = 'button[aria-label="Deactive"]'
    ROW_ACTIVE_BUTTON = 'button[aria-label="Active"]'
    ROW_LIFECYCLE_BUTTON = 'button[aria-label="Deactive"], button[aria-label="Active"]'
    EMPTY_STATE = 'table:has(caption:has-text("School management table")) tbody tr:has-text("No schools")'
    ALERT = '[role="alert"]'
    INLINE_CODE = 'input[aria-label="MOE school code"]'
    INLINE_NAME = 'input[aria-label="School name"]'
    INLINE_TYPE = 'select[aria-label="School type"]'
    SAVE_INLINE = 'button[aria-label="Save changes"]'
    DISCARD_INLINE = 'button[aria-label="Discard changes"], button[aria-label="Cancel"]'
    DIALOG = '[role="dialog"]'
    DIALOG_CONFIRM = '[role="dialog"] button:has-text("Deactivate"), [role="dialog"] button:has-text("Confirm")'
    DIALOG_CANCEL = '[role="dialog"] button:has-text("Cancel")'
    DIALOG_ALERT = '[role="dialog"] [role="alert"]'


class SchoolDetailLocators:
    """BSK-verified locators for School detail screen (/school-management/:schoolId) - DOM-SCH §1.3."""
    PAGE_HEADING = '#school-detail-heading, h1'
    BACK_LINK = 'button:has-text("Back to schools"), a:has-text("Back to school list")'
    STATUS_BADGE = 'main :text-is("ACTIVE"), main :text-is("INACTIVE"), [class*="badge"]'
    OVERVIEW_SECTION = '[aria-label="School overview"], section:has(h2:has-text("Overview"))'
    STUDENTS_TABLE = 'table:has(caption:has-text("School students")), table'


class AdminShellLocators:
    """BSK-verified locators for Admin Dashboard Shell (:5173)."""
    DASHBOARD_SHELL = 'aside nav, header, [data-testid="admin-shell"], aside'
    PORTAL_HEADER = 'header [class*="brand"], header'
    LOGOUT_BTN = 'button:has-text("Log out"), button:has-text("Sign out"), a[href*="logout"]'
    CALLBACK_STATUS = '[role="status"]'
    CALLBACK_FAILURE = '[role="status"]:has-text("Sign in failed"), [role="status"]:has-text("Unable to sign in")'
    ASSIGNMENT_REQUIRED_ALERT = '[role="alert"]:has-text("assignment"), [role="alert"]:has-text("school"), [role="alert"]:has-text("Chưa được phân công")'
