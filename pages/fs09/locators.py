"""
pages/fs09/locators.py - DOM Locators for Billing & Payment Flow (/billing/{studentId}).
Centralizes all CSS selectors and XPath queries for the 3-step payment flow.
"""

class BillingPaymentLocators:
    """Selectors for /billing/{studentId} payment flow."""

    URL_PATTERN = "/billing/{student_id}"

    # General / Header Elements
    PAGE_HEADING = "h1#billing-page-heading"
    PAGE_DESCRIPTION = "section[aria-labelledby='billing-page-heading'] header p:first-of-type"
    WALLET_META = "p[class*='walletMeta']"

    # Step Headings
    CHARGES_HEADING = "h2#billing-charges-heading, article[class*='tableCard'] h2"
    METHOD_HEADING = "h2#billing-method-heading"
    REVIEW_HEADING = "h2#billing-review-heading"

    # Summary Cards (Step 1)
    SUMMARY_CARDS_CONTAINER = "div[class*='selectionSummaryCards']"
    OUTSTANDING_FEES_SUMMARY = (
        "[class*='selectionSummaryCards'] [class*='summaryCard']:has-text('Outstanding fees') strong, "
        "[class*='summaryCard']:has-text('Outstanding fees') strong"
    )
    EA_BALANCE_SUMMARY = (
        "[class*='selectionSummaryCards'] [class*='summaryCard']:has-text('Education Account balance') strong, "
        "[class*='summaryCard']:has-text('Education Account balance') strong"
    )
    SELECTED_TOTAL_SUMMARY = (
        "[class*='selectionSummaryCards'] [class*='summaryCard']:has-text('Selected total') strong, "
        "[class*='summaryCard']:has-text('Selected total') strong"
    )
    CHILD_NAME_SUMMARY = "[class*='summaryCard']:has-text('Child') span, table caption, [class*='summaryValue']"

    # Step 1: Outstanding Charges Table & Filter
    STATUS_FILTER_SELECT = "select:has(option[value='All']), [class*='filterField'] select, select[aria-label*='Filter']"
    CHARGES_TABLE = "table"
    CHARGES_ROWS = "table tbody tr"
    TABLE_CAPTION = "table caption"
    SELECT_ALL_CHECKBOX = (
        "input[type='checkbox'][aria-label*='Select all'], "
        "div[class*='selectAll'] input[type='checkbox'], "
        "label:has-text('Select all') input[type='checkbox']"
    )
    ROW_CHECKBOX = "input[type='checkbox']"
    SELECTED_COUNTER = "span[class*='selectionSummary']"
    STEP1_CONTINUE_BTN = "button:has-text('Continue')"
    EMPTY_CHARGES_NOTICE = "div[class*='emptyState'][role='status'], td[class*='emptyCell'], td:has-text('No outstanding charges')"
    CHARGES_LOADING = "div[role='status']:has-text('Loading charges')"

    # Step 2: Payment Method Radio Options & Split Input
    METHOD_RADIO_GROUP = "fieldset, div[class*='method']"
    RADIO_EA = "input[type='radio'][value='EducationAccount']"
    RADIO_SPLIT = "input[type='radio'][value='Both']"
    RADIO_ONLINE = "input[type='radio'][value='OnlineGateway']"
    FUNDING_BREAKDOWN = "div[class*='fundingBreakdown'], div[class*='splitBreakdown']"
    SPLIT_EA_INPUT = "input[inputmode='decimal'], [class*='splitAmountField'] input, input[type='number']"
    SPLIT_ERROR_ALERT = "[class*='splitBreakdown'] [role='alert'], [class*='splitAmountField'] [role='alert'], [class*='method'] div[role='alert']"
    STEP2_BACK_BTN = "div[class*='method'] button:has-text('Back'), [class*='reviewActions'] button:has-text('Back')"
    STEP2_CONTINUE_BTN = "div[class*='method'] button:has-text('Continue'), [class*='reviewActions'] button:has-text('Continue')"

    # Step 3: Payment Review & Confirmation
    REVIEW_TABLE = "table[class*='reviewTable'], [class*='reviewTable'] table, table"
    STEP3_BACK_BTN = "[class*='reviewActions'] button:has-text('Back')"
    CONFIRM_PAY_BTN = (
        "button:has-text('Authorize & pay'), "
        "button:has-text('Authorize and pay'), "
        "button:has-text('Pay'), "
        "button:has-text('Confirm')"
    )

    # Alerts & Errors
    ALERT = "div[role='alert']"
    STALE_FEES_ALERT = "div[role='alert']:has-text('stale'), div[role='alert']:has-text('Stale')"
    INVALID_CONTEXT_HEADING = "h1#billing-invalid-context-heading"
    WALLET_ERROR_HEADING = "h1#billing-wallet-error-heading"
    RETRY_BTN = "button:has-text('Retry')"
    HOME_LINK = "a[class*='homeLink'], a:has-text('Home')"
