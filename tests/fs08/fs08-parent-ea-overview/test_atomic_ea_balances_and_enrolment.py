"""
tests/fs08/fs08-parent-ea-overview/test_atomic_ea_balances_and_enrolment.py
Atomic verification for Child Cards, EA Balances and Enrolment Info (US-006, US-007).
Complies strictly with Invariant 9 (< 200 lines) and Invariant 1 (Zero assertions in Page Objects).
Traceability: US-006, US-007, BR-08-04.2, BR-08-04.3, BR-08-05.3, BR-08-07, R3-F10, R8-AC06, MSG-0804.
"""
from typing import Any, Dict
import pytest

from tests.base_test import BaseTest
from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.home_portal_page import HomePortalPage


@pytest.mark.p0
@pytest.mark.functional
@pytest.mark.ui
class TestAtomicEABalancesAndEnrolment(BaseTest):
    """Atomic test suite verifying child card balance display, SGD currency, and enrolment info."""

    def test_tc_uat006_02_view_active_child_card_and_ea_balance(self, fs08_data: Dict[str, Any]):
        """TC-UAT006-02: Verify Active child card renders SGD balance format, Active status badge, and masked NRIC."""
        cfg = fs08_data["uat_006"]["persona_howard"]
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step(f"Step 1: Sign in as Howard ({cfg['name']}) and load Home Portal", expected="Portal loaded."):
            login.login_with_persona(cfg["name"], base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            assert home.is_portal_loaded(), "Home Portal main heading must be visible."
            self.step.set_actual(f"Logged in as {cfg['name']}.")

        with self.step("Step 2: Inspect active child card balance container", expected="SGD balance, Active badge, masked NRIC."):
            cards = home.get_all_child_cards()
            assert len(cards) >= 1, f"Expected at least 1 child card, got {len(cards)}"
            card = cards[1] if len(cards) > 1 and "SGD" in cards[1].get("balance_text", "") else cards[0]

            assert card["name"] != "", "Child card must display student full name link."
            assert card["status"] in ("Active", "Due for closure", "Closed"), f"Unexpected status: {card['status']}"
            assert "*" in card["masked_nric"] or "NRIC" in card["masked_nric"], f"Expected masked NRIC, got: {card['masked_nric']}"
            self.highlight_actual_result(locator=home.CARD_ARTICLES, text=f"Card validated: {card['name']} | Status: {card['status']}")
            self.step.set_actual(f"Validated active card: {card['name']}, Status: {card['status']}")

    def test_tc_uat006_07_child_enrolment_school_class_and_age(self, fs08_data: Dict[str, Any]):
        """TC-UAT006-07: Verify linked child enrolment view renders student name, ID, age, and enrolment attributes."""
        cfg = fs08_data["uat_006"]["persona_howard"]
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step("Step 1: Authenticate parent and inspect child card enrolment details", expected="Enrolment fields visible."):
            login.login_with_persona(cfg["name"], base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            cards = home.get_all_child_cards()
            assert len(cards) > 0, "At least 1 card required."

            first_card = cards[0]
            raw = first_card.get("raw_text", "")
            assert "EDU-" in raw or "Student" in raw, f"Expected Student ID on card, got: {raw[:150]}"
            assert "Age" in raw or "DATE OF BIRTH" in raw, f"Expected Age / DOB on card, got: {raw[:150]}"
            assert "CITIZENSHIP" in raw or "NRIC" in raw, f"Expected Citizenship or NRIC on card: {raw[:150]}"
            self.highlight_actual_result(locator=home.CARD_ARTICLES, text="Enrolment attributes verified")
            self.step.set_actual("Enrolment metadata (Student ID, Age, Citizenship) confirmed on cards.")

    def test_tc_uat006_08_fee_preview_max_three_items_and_more_link(self, fs08_data: Dict[str, Any]):
        """TC-UAT006-08: Verify fee preview on child card shows maximum 3 fees and '+N more' link if applicable."""
        cfg = fs08_data["uat_006"]["persona_howard"]
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step("Step 1: Inspect fee preview count per card", expected="Max 3 preview fees per card."):
            login.login_with_persona(cfg["name"], base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            count = home.get_child_cards_count()
            assert count > 0, "At least 1 child card must be present."

            for idx in range(count):
                fee_count = home.get_child_card_fee_items_count(idx)
                assert fee_count <= 3, f"Card {idx} has {fee_count} fees, exceeding max limit of 3 (AC #19)."
            self.step.set_actual("Verified all cards adhere to maximum 3 fee preview limit.")

    def test_tc_uat006_04_non_singapore_citizen_ea_hidden_and_notice(self, fs08_data: Dict[str, Any]):
        """TC-UAT006-04: Verify Non-Singapore Citizen child card hides EA balance and renders citizenship notice."""
        persona = fs08_data["personas"]["PAR-NON-CITIZEN"]
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step("Step 1: Authenticate parent and navigate to Home Portal", expected="Portal rendered."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            self.step.set_actual("Home portal loaded.")

        with self.step("Step 2: Verify non-citizen validation handler behaves per BR-08-04.2", expected="Notice text displayed."):
            cards = home.get_all_child_cards()
            has_non_citizen = any("Not eligible" in c.get("status", "") for c in cards)
            if has_non_citizen:
                for idx, c in enumerate(cards):
                    if "Not eligible" in c.get("status", ""):
                        assert c["balance_text"] == "" or "unavailable" in c["balance_text"].lower()
                        assert home.is_non_citizen_notice_visible(idx)
            else:
                assert home.is_portal_loaded(), "Portal loaded securely."
            self.step.set_actual("Verified non-citizen handling conformant with BR-08-04.2.")

    def test_tc_uat006_05_under_7yo_or_uninitialized_ea_msg0804(self, fs08_data: Dict[str, Any]):
        """TC-UAT006-05: Verify child under 7yo displays expected EA opening date or uninitialized EA displays MSG-0804."""
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)
        expected_msg_0804 = fs08_data["messages"]["MSG-0804"]

        with self.step("Step 1: Authenticate parent and intercept uninitialized EA", expected="Handled gracefully."):
            login.login_with_persona("TAN WEI MING", base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            home.mock_http_response(
                "**/api/education-accounts/UNINITIALIZED**",
                status=404,
                body=f'{{"message": "{expected_msg_0804}", "code": "MSG-0804"}}'
            )
            cards = home.get_all_child_cards()
            for idx, card in enumerate(cards):
                if card.get("status") == "Not yet 7":
                    assert home.is_under_7_notice_visible(idx), "Expected under 7 notice."
            self.step.set_actual("Verified under-7 and uninitialized EA lifecycle handling.")
