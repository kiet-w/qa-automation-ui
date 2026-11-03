"""
pages/fs03/admin_dashboard_shell_locators.py - Verified BSK Locators for Admin Dashboard Shell.
Strictly locator constants. Complies with Invariant 1 and modularity limits (<100 lines).
"""

class AdminDashboardShellLocators:
    """BSK-verified locators for EduFAMS Admin Portal Shell & Navigation (:5173)."""

    # Global Header & Controls
    # The app also renders headers inside other page regions. The dashboard's
    # global header is the one containing its breadcrumb navigation landmark.
    HEADER = 'header:has(nav[aria-label="Breadcrumb"])'
    COLLAPSE_SIDEBAR_BTN = 'header button[aria-label="Collapse sidebar"], header button[aria-label="Expand sidebar"]'
    MOBILE_NAVIGATION_BTN = 'header button[aria-label="Open navigation"]'
    BREADCRUMB = 'nav[aria-label="Breadcrumb"]'
    ACCOUNT_IDENTITY = 'header [aria-label*="("]:has(strong)'
    USER_NAME = f"{ACCOUNT_IDENTITY} strong"
    USER_ROLE_OR_CODE = ACCOUNT_IDENTITY
    SKIP_LINK = 'a[href="#admin-main-content"]'

    # Sidebar Navigation Container & Elements
    SIDEBAR_CONTAINER = 'aside[aria-label="Admin navigation sidebar"]'
    BRAND_LINK = 'aside a[aria-label="EduFAMS Admin Portal"][href="/"]'
    NAV = 'aside nav[aria-label="Admin navigation"]'
    NAV_LINKS = 'aside nav[aria-label="Admin navigation"] a[href]'
    NAV_ACTIVE_LINK = 'aside nav[aria-label="Admin navigation"] a[aria-current="page"]'
    SIGN_OUT_BTN = 'aside button[aria-label="Sign out"]'

    # Main Content Area & Fallbacks
    MAIN_CONTENT = "main#admin-main-content"
    PAGE_BODY = "body"
    PAGE_HEADING = "h1"
    NOT_FOUND_CONTAINER = "#admin-main-content, main"
    BACK_TO_HOME_LINK = 'main#admin-main-content a[href="/"]'

    # Feedback, Banners & Notifications
    ALERT = '[role="alert"]'
    ACCESS_RESTRICTED_ALERT = '[role="alert"]:has-text("Access restricted"), [role="status"]:has-text("Access restricted"), :has-text("Access restricted")'
    NOTIFICATIONS_LIST = 'ul[aria-label="Notifications"], [role="status"]'
    SCHOOL_BADGE = '[class*="schoolBadge"]'
    SCHOOL_BADGE_CODE = '[class*="schoolBadgeCode"]'

    @staticmethod
    def nav_link_by_href(href: str) -> str:
        return f'aside nav[aria-label="Admin navigation"] a[href="{href}"]'

    @staticmethod
    def action_by_label(label: str) -> str:
        return f'button:has-text("{label}"), a:has-text("{label}")'
