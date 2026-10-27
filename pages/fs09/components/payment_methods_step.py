"""
pages/fs09/components/payment_methods_step.py - Step 2: Payment Method Selection Component.
Encapsulates payment method radio options, split amount calculations, inline errors, and funding breakdown.
Complies strictly with Invariant 1 (Zero assertions in Page Objects/Components).
"""
from typing import Dict, List, Optional
from playwright.sync_api import Page
from pages.fs09.locators import BillingPaymentLocators as Loc


class PaymentMethodsStep:
    """Component managing Step 2: Payment Method Selection & Split calculation."""

    def __init__(self, page: Page):
        self.page = page

    def is_loaded(self) -> bool:
        """Check if Step 2 (Payment Method Selection) is currently active."""
        return self.page.locator(Loc.METHOD_HEADING).is_visible()

    def wait_for_loaded(self, timeout: int = 10000) -> None:
        """Wait for the Step 2 payment method selection heading to be visible."""
        self.page.wait_for_selector(Loc.METHOD_HEADING, timeout=timeout)

    def is_ea_option_enabled(self) -> bool:
        """Check if EducationAccount radio button is enabled."""
        radio = self.page.locator(Loc.RADIO_EA).first
        return radio.is_enabled() if radio.count() > 0 else False

    def is_split_option_enabled(self) -> bool:
        """Check if Both (Split) radio button exists and is enabled."""
        radio = self.page.locator(Loc.RADIO_SPLIT).first
        return radio.is_enabled() if radio.count() > 0 else False

    def is_online_option_enabled(self) -> bool:
        """Check if OnlineGateway radio button is enabled."""
        radio = self.page.locator(Loc.RADIO_ONLINE).first
        return radio.is_enabled() if radio.count() > 0 else False

    def get_available_payment_methods(self) -> List[str]:
        """Return list of values for all rendered payment method radio options."""
        radios = self.page.locator("input[type='radio'][name='billing-payment-method']")
        count = radios.count()
        methods: List[str] = []
        for i in range(count):
            val = radios.nth(i).get_attribute("value")
            if val:
                methods.append(val)
        return methods

    def get_selected_payment_method(self) -> Optional[str]:
        """Return the value of the currently checked payment method radio button."""
        radios = self.page.locator("input[type='radio'][name='billing-payment-method']")
        for i in range(radios.count()):
            r = radios.nth(i)
            if r.is_checked():
                return r.get_attribute("value")
        return None

    def select_payment_method(self, method: str) -> None:
        """Select a payment method radio option: 'EducationAccount' | 'Both' | 'OnlineGateway'."""
        radio = self.page.locator(f"input[type='radio'][value='{method}']").first
        radio.check()

    def is_ea_radio_checked(self) -> bool:
        return self.get_selected_payment_method() == "EducationAccount"

    def is_split_radio_checked(self) -> bool:
        return self.get_selected_payment_method() == "Both"

    def is_online_radio_checked(self) -> bool:
        return self.get_selected_payment_method() == "OnlineGateway"

    def select_ea_radio(self) -> None:
        self.select_payment_method("EducationAccount")

    def select_split_radio(self) -> None:
        self.select_payment_method("Both")

    def select_online_radio(self) -> None:
        self.select_payment_method("OnlineGateway")

    def is_both_option_present(self) -> bool:
        return self.page.locator(Loc.RADIO_SPLIT).count() > 0

    def fill_ea_split_amount(self, amount: str) -> None:
        inp = self.page.locator(Loc.SPLIT_EA_INPUT).first
        inp.fill(amount)

    def get_ea_split_amount(self) -> str:
        inp = self.page.locator(Loc.SPLIT_EA_INPUT).first
        return inp.input_value().strip() if inp.count() > 0 else ""

    def has_split_amount_error(self) -> bool:
        return self.page.locator(Loc.SPLIT_ERROR_ALERT).is_visible()

    def get_split_amount_error_text(self) -> Optional[str]:
        loc = self.page.locator(Loc.SPLIT_ERROR_ALERT)
        if loc.count() > 0 and loc.first.is_visible():
            return loc.first.inner_text().strip()
        return None

    def is_continue_disabled(self) -> bool:
        btn = self.page.locator(Loc.STEP2_CONTINUE_BTN).first
        return not btn.is_enabled() if btn.count() > 0 else True

    def get_funding_breakdown(self) -> Dict[str, str]:
        breakdown: Dict[str, str] = {}
        container = self.page.locator(Loc.FUNDING_BREAKDOWN)
        if container.count() == 0:
            return breakdown
        items = container.locator("dl div, dl [class*='item']")
        for i in range(items.count()):
            item = items.nth(i)
            dt = item.locator("dt")
            dd = item.locator("dd")
            if dt.count() > 0 and dd.count() > 0:
                breakdown[dt.first.inner_text().strip()] = dd.first.inner_text().strip()
        return breakdown

    def click_continue(self) -> None:
        self.page.locator(Loc.STEP2_CONTINUE_BTN).first.click()

    def click_back(self) -> None:
        self.page.locator(Loc.STEP2_BACK_BTN).first.click()
