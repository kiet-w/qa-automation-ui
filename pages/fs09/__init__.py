"""
pages/fs09 - UI Automation Page Objects for Feature Set 09 (Billing & Payment).
Compliant with Framework Invariant 1 (Zero assertions in Page Objects).
"""
from pages.fs09.billing_account_selection_page import BillingAccountSelectionPage
from pages.fs09.billing_payment_page import BillingPaymentPage
from pages.fs09.payment_gateway_simulator_page import PaymentGatewaySimulatorPage
from pages.fs09.payment_result_page import PaymentResultPage

__all__ = [
    "BillingAccountSelectionPage",
    "BillingPaymentPage",
    "PaymentGatewaySimulatorPage",
    "PaymentResultPage",
]
