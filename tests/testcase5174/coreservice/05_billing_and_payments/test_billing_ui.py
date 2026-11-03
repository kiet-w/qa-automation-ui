"""UI automation mapped to live-confirmed billing overview and charge selection."""
import pytest
from playwright.sync_api import expect

from pages.fs08.locators import BillingLocators as Loc
from tests.base_test import BaseTest
from tests.testcase5174.coreservice.conftest import dismiss_welcome_dialog


@pytest.mark.ui
@pytest.mark.ac
class TestBillingUI(BaseTest):
    def test_tc_bil_ac_01_billing_overview_lists_linked_accounts(self, authenticated_parent, fs08_data):
        """TC-BIL-AC-01: billing overview lists education accounts and View fees actions."""
        self.page.goto(f"{fs08_data['base_url'].rstrip('/')}/billing")
        with self.step("Mở danh sách tài khoản thanh toán", expected="Heading, list tài khoản và link View fees hiển thị."):
            expect(self.page.locator(Loc.OVERVIEW_HEADING)).to_be_visible()
            expect(self.page.locator(Loc.ACCOUNTS_LIST)).to_be_visible()
            expect(self.page.locator(Loc.FEES_LINK).first).to_be_visible()
            self.step.set_actual("Billing overview hiển thị tài khoản liên kết và hành động xem phí.")

    def test_tc_bil_val_15_select_all_toggles_charge_selection_and_continue(self, authenticated_parent, fs08_data):
        """TC-BIL-VAL-15: selecting and clearing all outstanding charges changes Continue state."""
        self.page.goto(f"{fs08_data['base_url'].rstrip('/')}/billing")
        dismiss_welcome_dialog(self.page)
        self.page.locator(Loc.FEES_LINK).first.click()
        dismiss_welcome_dialog(self.page)
        with self.step("Chọn toàn bộ khoản phí", expected="Checkbox Select all và Continue chuyển sang enabled."):
            select_all = self.page.locator(Loc.SELECT_ALL_FEES)
            continue_button = self.page.locator(Loc.CONTINUE)
            expect(self.page.locator(Loc.DETAIL_HEADING)).to_be_visible()
            expect(select_all).to_be_visible()
            select_all.check()
            expect(continue_button).to_be_enabled()
            select_all.uncheck()
            expect(continue_button).to_be_disabled()
            self.step.set_actual("Chọn hết bật Continue; bỏ chọn hết khóa Continue lại.")
