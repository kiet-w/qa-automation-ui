"""UI automation mapped to observed transaction-history states."""
import pytest
from playwright.sync_api import expect

from pages.fs08.locators import TransactionsLocators as Loc
from tests.base_test import BaseTest


@pytest.mark.ui
@pytest.mark.ac
class TestTransactionHistoryUI(BaseTest):
    def test_tc_txn_flow_06_empty_invoice_state_has_accessible_heading(self, authenticated_parent, fs08_data):
        """TC-TXN-FLOW-06: an account with no invoices receives the observed empty state."""
        self.page.goto(f"{fs08_data['base_url'].rstrip('/')}/transactions")
        with self.step("Mở lịch sử hóa đơn", expected="Tiêu đề, bộ lọc Child và empty state đã quét xuất hiện."):
            expect(self.page.locator(Loc.PAGE_HEADING)).to_be_visible()
            expect(self.page.get_by_role("combobox", name="Child", exact=True)).to_be_visible()
            expect(self.page.get_by_role("region", name="No invoices yet", exact=True)).to_be_visible()
            expect(self.page.get_by_role("heading", name="No invoices yet", exact=True)).to_be_visible()
            self.step.set_actual("Trang giao dịch hiển thị bộ lọc Child và trạng thái No invoices yet.")
