"""Black-box checkout UI coverage using the live-confirmed payment flow."""

import pytest
from playwright.sync_api import expect

from tests.base_test import BaseTest
from tests.testcase5174.coreservice.conftest import dismiss_welcome_dialog


@pytest.mark.ui
@pytest.mark.flow
class TestCheckoutUI(BaseTest):
    def test_tc_chk_flow_08_back_from_review_keeps_selected_charge(
        self, authenticated_parent
    ):
        """TC-CHK-08: Back from review returns to charge selection with the fee retained."""
        page = self.page
        page.get_by_role("link", name="View education account details for Liam Pham").click()
        dismiss_welcome_dialog(page)
        page.get_by_role("link", name="View billing for Liam Pham").click()
        dismiss_welcome_dialog(page)

        charge_name = "Standard Miscellaneous Fee - Term 4 2026"
        page.get_by_role("checkbox", name=f"Select charge: {charge_name}").check()
        page.get_by_role("button", name="Continue", exact=True).click()
        page.get_by_role("radio", name="Online Gateway Pay securely through the online payment gateway.").check()
        page.get_by_role("button", name="Continue", exact=True).click()

        with self.step(
            "Quay lại từ bước Review & authorize",
            expected="Trở về danh sách phí và giữ nguyên khoản phí đã chọn.",
        ):
            expect(page.get_by_role("heading", name="Review & authorize")).to_be_visible()
            # The page also renders a breadcrumb-level Back action; the last
            # matching button belongs to the active wizard step.
            page.get_by_role("button", name="Back", exact=True).last.click()
            expect(page.get_by_role("heading", name="Payment summary")).to_be_visible()
            page.get_by_role("button", name="Back", exact=True).last.click()
            expect(page.get_by_role("heading", name="Pay education charges")).to_be_visible()
            expect(page.get_by_role("checkbox", name=f"Select charge: {charge_name}")).to_be_checked()
            expect(page.get_by_role("button", name="Continue", exact=True)).to_be_enabled()
            self.step.set_actual("Quay về danh sách khoản phí; khoản đã chọn vẫn được giữ.")
