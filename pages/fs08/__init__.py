"""
pages/fs08 - Page Object Model package for FS-08: Parent Portal.
Modules encapsulate locators, page actions, and DOM inspection without assertions.
"""

from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.home_portal_page import HomePortalPage
from pages.fs08.transactions_page import TransactionsPage
from pages.fs08.parent_profile_page import ParentProfilePage

__all__ = [
    "SingpassLoginPage",
    "HomePortalPage",
    "TransactionsPage",
    "ParentProfilePage",
]
