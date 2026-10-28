"""
pages/fs09/payment_gateway_simulator_page.py - Page Object for Payment Gateway Simulator.
Represents the hosted checkout sandbox page (typically on port 5286 or path /checkout/...).
Complies strictly with Invariant 1 (Zero assertions in Page Objects).
"""
import os
from typing import Dict, Optional
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class PaymentGatewaySimulatorPage(BasePage):
    """Page Object for hosted payment checkout simulator."""

    # Header Elements
    BRAND_LINK = "header a.checkout-brand, header a:has-text('EduSave')"
    SECURE_LABEL = "header .checkout-secure-label, header span:has-text('Secure checkout')"

    # Main Content
    TITLE = "h1#checkout-title"
    SUMMARY_CARD = "div.summary-card, [class*='summary-card']"
    AMOUNT_DUE = "div.summary-amount strong, .summary-amount strong"
    STATUS_BADGE = "div.summary-status [class*='badge'], .summary-status span"
    REFERENCE_CODE = ".checkout-details-list code, dt:has-text('Reference') + dd code, dt:has-text('Reference') + dd"
    MERCHANT_VALUE = "dt:has-text('Merchant') + dd"
    CURRENCY_VALUE = "dt:has-text('Currency') + dd"
    METHOD_VALUE = "dt:has-text('Payment method') + dd"
    EXPIRES_VALUE = "dt:has-text('Expires') + dd"

    # Outcome Action Buttons
    PAY_SUCCESSFUL_BTN = "button[type='submit']:has-text('Pay successful')"
    PAY_FAILED_BTN = "button[type='submit']:has-text('Pay failed')"

    # Outcome Forms
    OUTCOME_CARD = "div.outcome-card, [class*='outcome-card']"

    # Alerts
    ALERT = "div[role='alert'], .checkout-content div[role='alert']"
    EXPIRED_ALERT = "div[role='alert']:has-text('expired'), div[role='alert']:has-text('Expired')"
    COMPLETED_ALERT = "div[role='alert']:has-text('already completed'), div[role='alert']:has-text('already failed')"

    # Loading indicator
    LOADING_STATE = "div[role='status'][aria-label='Loading checkout']"

    def __init__(self, page: Page):
        super().__init__(page)

    def wait_for_simulator_loaded(self, timeout: int = 15000) -> None:
        """Wait for checkout details or outcome buttons to appear."""
        try:
            loading = self.page.locator(self.LOADING_STATE)
            if loading.count() > 0:
                loading.first.wait_for(state="detached", timeout=timeout)
        except Exception:
            pass

        self.page.wait_for_selector(
            f"{self.AMOUNT_DUE}, {self.PAY_SUCCESSFUL_BTN}, {self.ALERT}",
            timeout=timeout,
        )

    def is_loaded(self) -> bool:
        """Check if simulator title and summary card or outcome buttons are visible."""
        return self.is_visible(self.TITLE) and (
            self.is_visible(self.AMOUNT_DUE) or self.is_visible(self.PAY_SUCCESSFUL_BTN)
        )

    def get_heading_text(self) -> str:
        """Get the main title text of the checkout page."""
        loc = self.page.locator(self.TITLE)
        return loc.inner_text().strip() if loc.count() > 0 else ""

    def get_amount_due(self) -> str:
        """Extract the amount due string from the summary card."""
        loc = self.page.locator(self.AMOUNT_DUE)
        return loc.inner_text().strip() if loc.count() > 0 else ""

    def get_reference_id(self) -> str:
        """Extract the payment reference ID from the checkout details."""
        loc = self.page.locator(self.REFERENCE_CODE)
        return loc.inner_text().strip() if loc.count() > 0 else ""

    def get_status_badge(self) -> str:
        """Extract the status badge text (e.g. 'Pending', 'Succeeded', 'Failed', 'Expired')."""
        loc = self.page.locator(self.STATUS_BADGE)
        return loc.inner_text().strip() if loc.count() > 0 else ""

    def get_merchant_id(self) -> str:
        """Extract merchant ID from checkout details list."""
        loc = self.page.locator(self.MERCHANT_VALUE)
        return loc.inner_text().strip() if loc.count() > 0 else ""

    def get_checkout_details(self) -> Dict[str, str]:
        """Extract all key-value items from the checkout details description list."""
        details: Dict[str, str] = {
            "amount_due": self.get_amount_due(),
            "status": self.get_status_badge(),
        }
        items = self.page.locator(".checkout-details-list div, .checkout-details-list [class*='item']")
        count = items.count()
        for i in range(count):
            item = items.nth(i)
            dt = item.locator("dt")
            dd = item.locator("dd")
            if dt.count() > 0 and dd.count() > 0:
                details[dt.inner_text().strip()] = dd.inner_text().strip()
        return details

    def click_pay_successful(self) -> None:
        """Click the 'Pay successful' outcome button."""
        btn = self.page.locator(self.PAY_SUCCESSFUL_BTN).first
        btn.click()

    def click_pay_failed(self) -> None:
        """Click the 'Pay failed' outcome button."""
        btn = self.page.locator(self.PAY_FAILED_BTN).first
        btn.click()

    def has_outcome_buttons(self) -> bool:
        """Check if payment outcome action buttons are visible and selectable."""
        return self.is_visible(self.PAY_SUCCESSFUL_BTN) and self.is_visible(self.PAY_FAILED_BTN)

    def has_expired_alert(self) -> bool:
        """Check if checkout expired alert is visible."""
        return self.is_visible(self.EXPIRED_ALERT)

    def has_completed_alert(self) -> bool:
        """Check if payment already completed or failed alert is visible."""
        return self.is_visible(self.COMPLETED_ALERT)
