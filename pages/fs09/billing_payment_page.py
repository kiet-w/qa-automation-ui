"""
pages/fs09/billing_payment_page.py - Modular Page Object for Billing & Payment Flow (/billing/{studentId}).
Decomposed into sub-components for high maintainability, low memory, and clean separation of concerns:
  - Step 1: ChargesSelectionStep (charges, filter, amounts, select all)
  - Step 2: PaymentMethodsStep (methods, split calculations, inline validation)
  - Step 3: PaymentReviewStep (review breakdown, authorization, confirmation)
Complies strictly with Invariant 1 (Zero assertions in Page Objects).
"""
import os
from typing import Any, Dict, List, Optional
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.fs09.locators import BillingPaymentLocators as Loc
from pages.fs09.components.charges_step import ChargesSelectionStep
from pages.fs09.components.payment_methods_step import PaymentMethodsStep
from pages.fs09.components.review_step import PaymentReviewStep


class BillingPaymentPage(BasePage):
    """Page Object orchestrator for /billing/{studentId} payment flow."""

    URL_PATTERN = Loc.URL_PATTERN
    PAGE_HEADING = Loc.PAGE_HEADING
    PAGE_DESCRIPTION = Loc.PAGE_DESCRIPTION
    WALLET_META = Loc.WALLET_META
    CHARGES_HEADING = Loc.CHARGES_HEADING
    METHOD_HEADING = Loc.METHOD_HEADING
    REVIEW_HEADING = Loc.REVIEW_HEADING
    SUMMARY_CARDS_CONTAINER = Loc.SUMMARY_CARDS_CONTAINER
    OUTSTANDING_FEES_SUMMARY = Loc.OUTSTANDING_FEES_SUMMARY
    EA_BALANCE_SUMMARY = Loc.EA_BALANCE_SUMMARY
    SELECTED_TOTAL_SUMMARY = Loc.SELECTED_TOTAL_SUMMARY
    CHILD_NAME_SUMMARY = Loc.CHILD_NAME_SUMMARY
    STATUS_FILTER_SELECT = Loc.STATUS_FILTER_SELECT
    CHARGES_TABLE = Loc.CHARGES_TABLE
    CHARGES_ROWS = Loc.CHARGES_ROWS
    TABLE_CAPTION = Loc.TABLE_CAPTION
    SELECT_ALL_CHECKBOX = Loc.SELECT_ALL_CHECKBOX
    ROW_CHECKBOX = Loc.ROW_CHECKBOX
    SELECTED_COUNTER = Loc.SELECTED_COUNTER
    STEP1_CONTINUE_BTN = Loc.STEP1_CONTINUE_BTN
    EMPTY_CHARGES_NOTICE = Loc.EMPTY_CHARGES_NOTICE
    CHARGES_LOADING = Loc.CHARGES_LOADING
    METHOD_RADIO_GROUP = Loc.METHOD_RADIO_GROUP
    RADIO_EA = Loc.RADIO_EA
    RADIO_SPLIT = Loc.RADIO_SPLIT
    RADIO_ONLINE = Loc.RADIO_ONLINE
    FUNDING_BREAKDOWN = Loc.FUNDING_BREAKDOWN
    SPLIT_EA_INPUT = Loc.SPLIT_EA_INPUT
    SPLIT_ERROR_ALERT = Loc.SPLIT_ERROR_ALERT
    STEP2_BACK_BTN = Loc.STEP2_BACK_BTN
    STEP2_CONTINUE_BTN = Loc.STEP2_CONTINUE_BTN
    REVIEW_TABLE = Loc.REVIEW_TABLE
    STEP3_BACK_BTN = Loc.STEP3_BACK_BTN
    CONFIRM_PAY_BTN = Loc.CONFIRM_PAY_BTN
    ALERT = Loc.ALERT
    STALE_FEES_ALERT = Loc.STALE_FEES_ALERT
    INVALID_CONTEXT_HEADING = Loc.INVALID_CONTEXT_HEADING
    WALLET_ERROR_HEADING = Loc.WALLET_ERROR_HEADING
    RETRY_BTN = Loc.RETRY_BTN
    HOME_LINK = Loc.HOME_LINK

    def __init__(self, page: Page):
        super().__init__(page)
        self.portal_base_url = os.environ.get("BASE_URL", "http://localhost:5174").rstrip("/")
        self.step1_charges = ChargesSelectionStep(page)
        self.step2_methods = PaymentMethodsStep(page)
        self.step3_review = PaymentReviewStep(page)
        # Convenient aliases
        self.charges = self.step1_charges
        self.methods = self.step2_methods
        self.review = self.step3_review

    # Navigation & Step Identification
    def open_for_student(self, student_id: str, base_url: Optional[str] = None) -> "BillingPaymentPage":
        target_base = (base_url or self.portal_base_url).rstrip("/")
        url = f"{target_base}/billing/{student_id}"
        self.page.goto(url)
        self.wait_for_selection_loaded()
        return self

    def wait_for_selection_loaded(self, timeout: int = 15000) -> None:
        self.step1_charges.wait_for_loaded(timeout=timeout)

    def is_selection_step_loaded(self) -> bool:
        return self.step1_charges.is_loaded()

    def is_method_step_loaded(self) -> bool:
        return self.step2_methods.is_loaded()

    def is_review_step_loaded(self) -> bool:
        return self.step3_review.is_loaded()

    def get_heading_text(self) -> str:
        loc = self.page.locator(self.PAGE_HEADING)
        return loc.inner_text().strip() if loc.count() > 0 else ""

    def get_student_id_text(self) -> str:
        loc = self.page.locator(self.WALLET_META)
        if loc.count() > 0 and loc.first.is_visible():
            return loc.first.inner_text().strip()
        url = self.page.url
        if "/billing/" in url:
            return url.split("/billing/")[-1].split("?")[0].split("/")[0]
        return ""

    # Step 1: Delegated methods
    def get_summary_amounts(self) -> Dict[str, str]:
        return self.step1_charges.get_summary_amounts()

    def set_status_filter(self, filter_value: str) -> None:
        self.step1_charges.set_status_filter(filter_value)

    def get_status_filter(self) -> str:
        return self.step1_charges.get_status_filter()

    def get_selected_total_amount(self) -> str:
        return self.step1_charges.get_selected_total_amount()

    def get_charge_count(self) -> int:
        return self.step1_charges.get_charge_count()

    def get_charge_rows_data(self) -> List[Dict[str, Any]]:
        return self.step1_charges.get_charge_rows_data()

    def select_all_charges(self) -> None:
        self.step1_charges.select_all_charges()

    def unselect_all_charges(self) -> None:
        self.step1_charges.unselect_all_charges()

    def is_all_selected(self) -> bool:
        return self.step1_charges.is_all_selected()

    def select_charge_by_index(self, index: int) -> None:
        self.step1_charges.select_charge_by_index(index)

    def unselect_charge_by_index(self, index: int) -> None:
        self.step1_charges.unselect_charge_by_index(index)

    def toggle_charge_by_description(self, description_substring: str) -> None:
        self.step1_charges.toggle_charge_by_description(description_substring)

    def get_selected_charges_count_text(self) -> str:
        return self.step1_charges.get_selected_charges_count_text()

    def click_continue_to_method(self) -> None:
        self.step1_charges.click_continue()
        self.wait_for_method_loaded()

    def has_empty_charges_notice(self) -> bool:
        return self.step1_charges.has_empty_charges_notice()

    def get_empty_charges_text(self) -> str:
        return self.step1_charges.get_empty_charges_text()

    # Step 2: Delegated methods
    def wait_for_method_loaded(self, timeout: int = 10000) -> None:
        self.step2_methods.wait_for_loaded(timeout=timeout)

    def is_ea_option_enabled(self) -> bool:
        return self.step2_methods.is_ea_option_enabled()

    def is_split_option_enabled(self) -> bool:
        return self.step2_methods.is_split_option_enabled()

    def is_online_option_enabled(self) -> bool:
        return self.step2_methods.is_online_option_enabled()

    def get_available_payment_methods(self) -> List[str]:
        return self.step2_methods.get_available_payment_methods()

    def get_selected_payment_method(self) -> Optional[str]:
        return self.step2_methods.get_selected_payment_method()

    def select_payment_method(self, method: str) -> None:
        self.step2_methods.select_payment_method(method)

    def is_ea_radio_checked(self) -> bool:
        return self.step2_methods.is_ea_radio_checked()

    def is_split_radio_checked(self) -> bool:
        return self.step2_methods.is_split_radio_checked()

    def is_online_radio_checked(self) -> bool:
        return self.step2_methods.is_online_radio_checked()

    def select_ea_radio(self) -> None:
        self.step2_methods.select_ea_radio()

    def select_split_radio(self) -> None:
        self.step2_methods.select_split_radio()

    def select_online_radio(self) -> None:
        self.step2_methods.select_online_radio()

    def is_both_option_present(self) -> bool:
        return self.step2_methods.is_both_option_present()

    def fill_ea_split_amount(self, amount: str) -> None:
        self.step2_methods.fill_ea_split_amount(amount)

    def get_ea_split_amount(self) -> str:
        return self.step2_methods.get_ea_split_amount()

    def has_split_amount_error(self) -> bool:
        return self.step2_methods.has_split_amount_error()

    def get_split_amount_error_text(self) -> Optional[str]:
        return self.step2_methods.get_split_amount_error_text()

    def is_method_continue_disabled(self) -> bool:
        return self.step2_methods.is_continue_disabled()

    def get_funding_breakdown(self) -> Dict[str, str]:
        return self.step2_methods.get_funding_breakdown()

    def click_continue_to_review(self) -> None:
        self.step2_methods.click_continue()
        self.wait_for_review_loaded()

    def click_back_to_selection(self) -> None:
        self.step2_methods.click_back()
        self.wait_for_selection_loaded()

    # Step 3: Delegated methods
    def wait_for_review_loaded(self, timeout: int = 10000) -> None:
        self.step3_review.wait_for_loaded(timeout=timeout)

    def get_review_summary(self) -> Dict[str, Any]:
        return self.step3_review.get_review_summary()

    def click_confirm_pay(self) -> None:
        self.step3_review.click_confirm_pay()

    def click_back_to_method(self) -> None:
        self.step3_review.click_back()
        self.wait_for_method_loaded()

    def is_pay_button_disabled(self) -> bool:
        return self.step3_review.is_pay_button_disabled()

    def is_pay_button_loading(self) -> bool:
        return self.step3_review.is_pay_button_loading()

    # Shell Alerts & Navigation
    def has_error_alert(self) -> bool:
        return self.is_visible(self.ALERT)

    def get_error_alert_text(self) -> Optional[str]:
        loc = self.page.locator(self.ALERT)
        return loc.first.inner_text().strip() if loc.count() > 0 and loc.first.is_visible() else None

    def has_stale_fees_alert(self) -> bool:
        return self.is_visible(self.STALE_FEES_ALERT)

    def has_invalid_context_alert(self) -> bool:
        return self.is_visible(self.INVALID_CONTEXT_HEADING)

    def has_wallet_error_alert(self) -> bool:
        return self.is_visible(self.WALLET_ERROR_HEADING)

    def click_retry_wallet(self) -> None:
        self.click_element(self.RETRY_BTN)

    def click_home_link(self) -> None:
        self.click_element(self.HOME_LINK)
