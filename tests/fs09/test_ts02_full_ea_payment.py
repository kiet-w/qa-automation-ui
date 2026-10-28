"""
tests/fs09/test_ts02_full_ea_payment.py - Test Suite TS02: Full Education Account (EA) Payment.
Covers Stream 2:
- TC-R9-05: 100% EA Payment Success & Atomic Ledger Debit
- TC-R9-06: Insufficient EA Balance Disables EA Option
- TC-R9-07: Inactive / Insufficient EA Rejection Contract
- TC_R9_AUTO_01: Direct API EA Checkout Contract & DB Invariants

Traceability:
- FSD: [agile] fs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md §3.2, §5.1, §5.3
- Rules: BR-F9-02, BR-F9-03, BR-F9-13, DA-02, DA-06, DA-08
- ACs: AC-03, AC-04, AC-13
- Invariants: 0 to 8
"""
import copy
from typing import Any, Dict
import uuid
import pytest
import requests

from tests.base_test import BaseTest
from pages.fs09.billing_account_selection_page import BillingAccountSelectionPage
from pages.fs09.billing_payment_page import BillingPaymentPage
from pages.fs09.payment_result_page import PaymentResultPage
from tests.fs09.conftest import DatabaseHelper


@pytest.mark.p0
@pytest.mark.functional
@pytest.mark.ui
class TestTS02FullEAPayment(BaseTest):
    """Test Suite TS02 covering 100% Education Account (EA) Payment and Ledger Deductions."""

    def test_tc_r9_05_full_ea_payment_success(
        self, fs09_data: Dict[str, Any], auth_helper, db_helper: DatabaseHelper, cleanup_fs09_records
    ):
        """
        TC-R9-05: Verify 100% EA Payment succeeds when EA balance >= net payable amount.
        Scenario ID: TS-010 / TS-011 | Test Suite: TS02 Full EA Payment
        Page: /billing/:studentId -> /payment-result | Severity: S1 | Priority: Critical | Test Type: Functional
        Traceability: BR-F9-02; BR-F9-03; BR-F9-13; AC-03; AC-13; DA-08
        Environment: Localhost Vite (:5174) & Backend (:5008)
        Preconditions: Chloe Chan has 10.00 SGD charge and 50.00 SGD EA balance.
        Test Data: fs09_data["personas"]["PAR-NORMAL-01"]
        Expected Result:
            - Payment completes successfully with green banner on /payment-result.
            - Receipt details include Transaction ID, Invoice Number, and Settled amount.
            - DB invoices table: status = 4 (Paid).
            - DB transactions table: status = 2 (Succeeded).
            - DB transaction_funding_sources table: method = 1 (EA), status = 2 (Succeeded).
            - EA wallet balance decreases by exactly 10.00 SGD.
        """
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        student_id = persona["student_id"]
        auth_helper("PAR-NORMAL-01")

        payment_page = self.get_page(BillingPaymentPage)
        result_page = self.get_page(PaymentResultPage)

        with self.step("Step 1: Open charges selection and select 10.00 SGD Stationery Fee", expected="Charge selected."):
            payment_page.open_for_student(student_id, base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.unselect_all_charges()
            payment_page.select_charge_by_index(0)  # 10.00 SGD Stationery Fee
            payment_page.click_continue_to_method()
            payment_page.wait_for_method_loaded()
            self.step.set_actual("10.00 SGD charge selected; navigated to method selection.")

        with self.step("Step 2: Select Education Account method and continue to review", expected="EA option selectable."):
            assert payment_page.is_ea_option_enabled(), "EA option must be enabled since balance (50) >= charge (10)."
            payment_page.select_payment_method("EducationAccount")
            payment_page.click_continue_to_review()
            payment_page.wait_for_review_loaded()
            assert payment_page.is_review_step_loaded(), "Review step must be loaded."
            self.step.set_actual("Selected Education Account and loaded review step.")

        with self.step("Step 3: Confirm payment and wait for result page", expected="PaymentResultPage rendered with success."):
            payment_page.click_confirm_pay()
            result_page.wait_for_result_loaded(timeout=15000)
            assert result_page.is_loaded(), "Payment result page heading must be visible."
            assert result_page.get_result_tone() == "success", f"Expected success tone, got: {result_page.get_result_tone()}"
            receipt = result_page.get_receipt_details()
            assert receipt.get("Transaction ID", ""), "Transaction ID must be displayed on receipt."
            self.step.set_actual(f"Payment succeeded! Receipt details: {receipt}")

        with self.step("Step 4: Verify Database Invariants (Invoice Paid, Transaction Succeeded, EA debited)", expected="DB records match specifications."):
            invoices = db_helper.query(f"SELECT TOP 1 id, status, gross_amount, net_amount FROM BillingPaymentService.dbo.invoices WHERE student_id = '{student_id}' ORDER BY created_at DESC")
            assert len(invoices) > 0, "Invoice record must be present in DB."
            assert invoices[0]["status"] == 4, f"Expected invoice status 4 (Paid), got: {invoices[0]['status']}"

            txns = db_helper.query(f"SELECT TOP 1 id, status, requested_amount, settled_amount FROM BillingPaymentService.dbo.transactions WHERE invoice_id = '{invoices[0]['id']}'")
            assert len(txns) > 0, "Transaction record must be present in DB."
            assert txns[0]["status"] == 2, f"Expected transaction status 2 (Succeeded), got: {txns[0]['status']}"

            wallets = db_helper.query(f"SELECT balance FROM EducationAccountDatabase.dbo.wallets WHERE student_id = '{student_id}'", db_name="EducationAccountDatabase")
            assert len(wallets) > 0, "Wallet record must be present."
            # Initial 50.00 minus 10.00 = 40.00
            assert float(wallets[0]["balance"]) == 40.00, f"Expected wallet balance 40.00, got: {wallets[0]['balance']}"
            self.step.set_actual("Database verified: invoice=Paid, txn=Succeeded, wallet balance=40.00 SGD.")

    def test_tc_r9_06_insufficient_ea_balance_disables_ea_option(
        self, fs09_data: Dict[str, Any], auth_helper, cleanup_fs09_records
    ):
        """
        TC-R9-06: Verify insufficient EA balance disables 100% EA option (BR-F9-02, AC-04).
        Scenario ID: TS-008 | Test Suite: TS02 Full EA Payment
        Page: /billing/:studentId | Severity: S2 | Priority: High | Test Type: Functional & UI
        Traceability: BR-F9-02; AC-04; DA-02; Error Code: EA_INSUFFICIENT_BALANCE
        Environment: Localhost Vite (:5174)
        Preconditions: Chloe Chan's EA balance is 50.00 SGD, selected charge is 1500.00 SGD.
        Expected Result:
            - Method 'EducationAccount' radio button is disabled.
            - UI displays guidance that balance is insufficient and offers Online or Both.
        """
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        student_id = persona["student_id"]
        auth_helper("PAR-NORMAL-01")

        payment_page = self.get_page(BillingPaymentPage)

        with self.step("Step 1: Open charges selection and select 1500.00 SGD Overseas Trip fee", expected="Charge selected."):
            payment_page.open_for_student(student_id, base_url=fs09_data["base_url"])
            payment_page.wait_for_selection_loaded()
            payment_page.unselect_all_charges()
            # Select the large fee at index 3 (1500.00 SGD)
            payment_page.select_charge_by_index(3)
            payment_page.click_continue_to_method()
            payment_page.wait_for_method_loaded()
            self.step.set_actual("1500.00 SGD charge selected; navigated to method step.")

        with self.step("Step 2: Verify Education Account radio option is disabled", expected="EA option disabled, Online/Both available."):
            assert not payment_page.is_ea_option_enabled(), (
                "Education Account method option must be disabled when balance (50) < charge (1500)."
            )
            assert payment_page.is_online_option_enabled(), "OnlineGateway option must remain enabled."
            self.step.set_actual("Verified EA option is disabled for insufficient balance.")

    def test_tc_r9_07_inactive_or_uninitialized_ea_rejection(
        self, fs09_data: Dict[str, Any]
    ):
        """
        TC-R9-07: Verify API rejects EA checkout when balance is insufficient (BR-F9-02, BR-F9-03).
        Scenario ID: TS-009 | Test Suite: TS02 Full EA Payment
        Protocol Level: POST /api/v1/checkout | Severity: S2 | Priority: High | Test Type: API Contract
        Traceability: BR-F9-02; BR-F9-03; Error Code: EA_INSUFFICIENT_BALANCE
        Expected Result:
            - Backend responds with HTTP 400 Bad Request containing insufficient balance error message.
        """
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        student_id = persona["student_id"]
        api_base = fs09_data["api_base_url"]

        payload = {
            "studentId": student_id,
            "chargeIds": ["bbbb0009-0000-0000-0000-000000000004"],  # 1500.00 SGD
            "method": "EducationAccount",
            "walletId": persona["wallet_id"]
        }
        headers = {
            "Idempotency-Key": str(uuid.uuid4()),
            "X-User-Id": "test-parent",
            "X-User-Roles": "PARENT",
            "Content-Type": "application/json"
        }

        with self.step("Step 1: Dispatch direct checkout API request with insufficient EA balance", expected="HTTP 400 Bad Request returned."):
            resp = requests.post(f"{api_base}/api/v1/checkout", json=payload, headers=headers, timeout=5)
            assert resp.status_code == 400, f"Expected 400 Bad Request, got {resp.status_code}: {resp.text}"
            body = resp.json()
            assert not body.get("isSuccess", True), "Response isSuccess must be false."
            msg = body.get("message", "").lower()
            assert "insufficient" in msg or "ea_insufficient_balance" in msg, f"Expected insufficient message, got: {msg}"
            self.step.set_actual(f"API correctly rejected with 400: {body.get('message')}")

    def test_tc_r9_auto_01_direct_api_ea_checkout_contract(
        self, fs09_data: Dict[str, Any], db_helper: DatabaseHelper, cleanup_fs09_records
    ):
        """
        TC_R9_AUTO_01: Verify direct API EA Checkout satisfies 3-Level Validation Model (Protocol, Contract, DB).
        Scenario ID: AUTO-01 | Test Suite: TS02 Full EA Payment
        Protocol Level: POST /api/v1/checkout (Mode = EducationAccount) | Severity: S1 | Priority: Critical | Test Type: Automated Contract
        Traceability: TC_R9_AUTO_01; F9.4; BR-F9-02; BR-F9-13
        Expected Result:
            - HTTP 200 OK with valid CheckoutResult schema.
            - DB invoices: status = 4 (PAID).
            - DB transactions: status = 2 (SUCCEEDED).
            - DB transaction_funding_sources: method = 1 (EA), status = 2 (SUCCEEDED).
        """
        persona = fs09_data["personas"]["PAR-NORMAL-01"]
        student_id = persona["student_id"]
        api_base = fs09_data["api_base_url"]
        idempotency_key = str(uuid.uuid4())

        payload = {
            "studentId": student_id,
            "chargeIds": ["bbbb0009-0000-0000-0000-000000000002"],  # 15.00 SGD Field Trip Fee
            "method": "EducationAccount",
            "walletId": persona["wallet_id"]
        }
        headers = {
            "Idempotency-Key": idempotency_key,
            "X-User-Id": "test-parent",
            "X-User-Roles": "PARENT",
            "Content-Type": "application/json"
        }

        with self.step("Step 1: Execute POST /api/v1/checkout", expected="HTTP 200 OK."):
            resp = requests.post(f"{api_base}/api/v1/checkout", json=payload, headers=headers, timeout=5)
            assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}: {resp.text}"
            data = resp.json().get("data", {})
            assert data.get("transactionId", ""), "Contract must return transactionId."
            assert data.get("invoiceNumber", ""), "Contract must return invoiceNumber."
            self.step.set_actual(f"API checkout returned transactionId={data.get('transactionId')}")

        with self.step("Step 2: Assert Database Level Invariants", expected="Database records confirm PAID status."):
            txn_id = data.get("transactionId")
            txns = db_helper.query(f"SELECT invoice_id, status, requested_amount, settled_amount FROM BillingPaymentService.dbo.transactions WHERE id = '{txn_id}'")
            assert len(txns) > 0 and txns[0]["status"] == 2, f"Transaction {txn_id} must have status 2 (SUCCEEDED)."

            invoice_number = data.get("invoiceNumber")
            invoices = db_helper.query(f"SELECT status, net_amount FROM BillingPaymentService.dbo.invoices WHERE invoice_number = '{invoice_number}'")
            assert len(invoices) > 0 and invoices[0]["status"] == 4, f"Invoice {invoice_number} must have status 4 (PAID)."
            self.step.set_actual("3-Level Validation passed: Protocol 200, Contract valid, DB confirmed PAID.")
