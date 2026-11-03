"""UI automation mapped to testcase5174 dashboard cases."""
import pytest
from playwright.sync_api import expect

from pages.fs08.locators import DashboardLocators as Loc
from tests.base_test import BaseTest
from tests.testcase5174.coreservice.conftest import dismiss_welcome_dialog


@pytest.mark.ui
@pytest.mark.ac
class TestDashboardUI(BaseTest):
    def test_tc_dsh_03_dashboard_shows_accounts_and_invoice_entry(self, authenticated_parent):
        """TC-DSH-03: dashboard shows the observed account list and invoice entry point."""
        with self.step("Kiểm tra dashboard", expected="Tiêu đề và danh sách Education accounts xuất hiện."):
            expect(self.page.locator(Loc.HEADING)).to_be_visible()
            expect(self.page.locator(Loc.ACCOUNTS_LIST)).to_be_visible()
            expect(self.page.locator(Loc.INVOICES_REGION)).to_be_visible()
            expect(self.page.locator(Loc.INVOICES_LINK)).to_be_visible()
            self.step.set_actual("Dashboard có danh sách tài khoản và liên kết hóa đơn.")

    def test_tc_dsh_07_account_detail_link_opens_selected_account(self, authenticated_parent):
        """TC-DSH-07: a child account's accessible action opens its account details."""
        link = self.page.locator(Loc.ACCOUNT_DETAILS_LINK).first
        with self.step("Mở chi tiết tài khoản từ dashboard", expected="Điều hướng đến trang Education Account details."):
            dismiss_welcome_dialog(self.page)
            expect(link).to_be_visible()
            link.click()
            dismiss_welcome_dialog(self.page)
            expect(self.page.get_by_role("heading", name="Education Account details", exact=True)).to_be_visible()
            self.step.set_actual(f"Trang chi tiết tài khoản đã mở tại {self.page.url}.")
