"""
pages/f01/locators.py - Centralized selectors for Education Accounts (F01).
Extracted from BSK Live DOM reconnaissance on http://localhost:5173/education-accounts.
Complies with Invariant 9 (< 100 lines).

BSK Source: specs/ui_bsk/localhost-5173/finance-and-fas/01_education_accounts.md
Updated: 2026-10-27 — Sync dialog title verified as "Sync citizen data" (role="dialog"),
         with alertdialog fallback for compatibility.
"""

# Page Heading & Container
PAGE_HEADING = "h1#education-accounts-heading, h1:has-text('Education Accounts')"
PAGE_CONTAINER = "section[aria-labelledby='education-accounts-heading']"

# Filter and Search Controls (BSK: form[role="search"])
SEARCH_INPUT = "form[role='search'] input[type='search']"
SEARCH_INPUT_FALLBACK = "input[type='search'], input[placeholder*='Search by NRIC' i]"
STATUS_SELECT = "form[role='search'] select:has(option[value='1'])"
CITIZENSHIP_SELECT = "form[role='search'] select:has(option[value='5'])"
APPLY_SEARCH_BTN = "form[role='search'] button[type='submit']:has-text('Search')"
CLEAR_SEARCH_BTN = "form[role='search'] button[aria-label='Clear search']"
MANUAL_SYNC_BTN = "button:has-text('Manual sync')"

# Sync Confirmation Dialog (BSK-Verified: title "Sync citizen data", role="dialog")
# Dual selector supports both role="dialog" (live BSK) and role="alertdialog" (spec fallback)
SYNC_DIALOG = "[role='dialog']:has-text('Sync citizen data'), [role='alertdialog']"
SYNC_DIALOG_TITLE = "[role='dialog'] h2, [role='alertdialog'] h2"
SYNC_DIALOG_DESC = "[role='dialog'] p, [role='alertdialog'] p"
SYNC_CONFIRM_BTN = "button:has-text('Confirm')"
SYNC_CANCEL_BTN = "button:has-text('Cancel')"

# Legacy selectors — retained for backward compatibility with existing tests
SYNC_ALERT_DIALOG = "[role='alertdialog']"
SYNC_ALERT_DIALOG_TITLE = "[role='alertdialog'] h2"
SYNC_ALERT_DIALOG_DESC = "[role='alertdialog'] p"
SYNC_ALERT_CONFIRM_BTN = "[role='alertdialog'] button:has-text('Confirm')"
SYNC_ALERT_CANCEL_BTN = "[role='alertdialog'] button:has-text('Cancel')"

# Data Table & Pagination
ACCOUNTS_TABLE = "table"
TABLE_ROWS = "table tbody tr"
TABLE_ROW_CELLS = "td"
VIEW_DETAILS_BTN = "button:has-text('View details')"
NRIC_CELL_BTN = "tbody tr td:nth-child(2) button"
ACCOUNT_STATUS_BADGE = "table tbody tr td:nth-child(7) span"
ACCOUNT_CODE_CELL = "table tbody tr td:nth-child(1) code"
PAGINATION_NEXT_BTN = "button[aria-label='Next']"
PAGINATION_PREV_BTN = "button[aria-label='Previous']"
PAGE_SIZE_SELECT = "select:has(option[value='10']):has(option[value='25'])"

# Student Profile Dialog (BSK-Verified: title "Student Profile", role="dialog")
PROFILE_DIALOG = "[role='dialog']:has-text('Student Profile')"
PROFILE_DIALOG_HEADING = "[role='dialog'] h2"
PROFILE_CLOSE_BTN = "[role='dialog'] button:has-text('Close')"
PROFILE_X_BTN = "[role='dialog'] button:has-text('×')"

# Error/Retry States
ERROR_ALERT = "[role='alert']"
RETRY_BTN = "button:has-text('Retry')"
