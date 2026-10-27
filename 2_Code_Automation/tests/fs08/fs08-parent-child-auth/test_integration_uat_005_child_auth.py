"""
tests/fs08/fs08-parent-child-auth/test_integration_uat_005_child_auth.py
Integration & End-to-End Workflow Verification for UAT-005 (US-005).
Strictly compliant with Invariant 9 (< 250 lines) and the 5 Pillars Architecture.
Traceability: US-005, PB-06, PB-07, BR-08-01, BR-08-03, BR-08-04, BR-08-10, D-19, R8-AC01, R8-AC13, R8-AC28.
"""
import json
from typing import Any, Dict
import pytest

from tests.base_test import BaseTest
from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.home_portal_page import HomePortalPage
from pages.fs08.transactions_page import TransactionsPage


@pytest.mark.p0
@pytest.mark.functional
@pytest.mark.security
@pytest.mark.integration
class TestIntegrationUAT005ChildAuth(BaseTest):
    """Integration test suite for UAT-005 SingPass Auth, IDOR Tampering & Session Isolation."""

    def test_tc_uat005_01_parent_a_singpass_login_verified_children(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-01: Step 1 — Parent A Singpass login displays verified children and mock session labels."""
        cfg = fs08_data["uat_005"]["parent_a"]
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step(f"Sign in with Singpass as Parent A ({cfg['persona_name']})", expected="Redirected to Home Portal."):
            login.login_with_persona(cfg["persona_name"], base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            assert home.is_portal_loaded(), "Home Portal heading must be visible after login."
            self.step.set_actual(f"Authenticated successfully as {cfg['persona_name']}.")

        with self.step("Verify verified children list matches MOE guardianship", expected=f"{cfg['verified_count']} children."):
            cards = home.get_all_child_cards()
            names = [c["name"] for c in cards]
            assert len(cards) == cfg["verified_count"], f"Expected {cfg['verified_count']} cards, got {len(cards)}"
            for expected_child in cfg["expected_children"]:
                assert expected_child in names, f"Child '{expected_child}' missing from cards: {names}"
            self.highlight_actual_result(locator=home.CARD_ARTICLES, text=f"Verified children: {names}")
            self.step.set_actual(f"Displayed exact verified children: {names}")

        with self.step("Verify mock session and identity source label", expected=f"Username {cfg['username']}"):
            raw_user = self.page.evaluate("() => window.sessionStorage.getItem('edusave.parent-auth.user')")
            assert raw_user is not None, "sessionStorage must contain 'edusave.parent-auth.user'"
            user_obj = json.loads(raw_user)
            assert user_obj.get("username") == cfg["username"], f"Expected {cfg['username']}, got {user_obj.get('username')}"
            self.step.set_actual(f"Mock session validated with username: {cfg['username']}")

    def test_tc_uat005_02_idor_cross_family_url_tampering_blocked(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-02: Step 2 — Verify IDOR cross-family child access via URL tampering is rejected."""
        cfg_a = fs08_data["uat_005"]["parent_a"]
        idor_cfg = fs08_data["uat_005"]["idor_test"]
        login = self.get_page(SingpassLoginPage)
        tx_page = self.get_page(TransactionsPage)

        with self.step("Authenticate as Parent A and tamper URL with unauthorized student ID", expected="Blocked safely."):
            login.login_with_persona(cfg_a["persona_name"], base_url=fs08_data["base_url"])
            tx_page.open(student_id=idor_cfg["target_unauthorized_student"], base_url=fs08_data["base_url"])
            assert tx_page.is_unable_to_load_visible(timeout=8000), "Error container 'Unable to load data' must appear."
            self.highlight_actual_result(locator=tx_page.UNABLE_TO_LOAD, text="IDOR Blocked: Unable to load data")
            self.step.set_actual("URL tampering rejected safely with 'Unable to load data'.")

        with self.step("Verify student dropdown contains zero data leakage of unauthorized child", expected="Only Parent A children."):
            options = tx_page.get_student_options()
            assert idor_cfg["target_student_name"] not in " ".join(options), f"Security breach: {idor_cfg['target_student_name']} leaked!"
            for child in cfg_a["expected_children"]:
                assert any(child in opt for opt in options), f"Parent A child '{child}' must be in options."
            self.step.set_actual(f"Student dropdown strictly isolated: {options}")

    def test_tc_uat005_03_idor_cross_family_api_tampering_blocked(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-03: Step 2 — Verify direct API tampering for unauthorized student wallet is rejected."""
        cfg_a = fs08_data["uat_005"]["parent_a"]
        idor_cfg = fs08_data["uat_005"]["idor_test"]
        login = self.get_page(SingpassLoginPage)

        with self.step("Authenticate as Parent A and send direct backend API request", expected="HTTP 400/401/403 rejection."):
            login.login_with_persona(cfg_a["persona_name"], base_url=fs08_data["base_url"])
            api_res = self.page.request.get(f"{fs08_data['base_url']}/api/iam/v1/edu-account/students/{idor_cfg['target_unauthorized_student']}/wallet")
            assert api_res.status in idor_cfg["expected_api_status"], f"Unexpected HTTP status: {api_res.status}"
            res_json = api_res.json()
            assert res_json.get("isSuccess") is False, "Direct API must return isSuccess=False on IDOR"
            self.step.set_actual(f"Direct API rejected with HTTP {api_res.status} and isSuccess=False.")

    def test_tc_uat005_04_logout_flushes_session_and_cleans_session_storage(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-04: Step 3 — Verify logout completely flushes sessionStorage and redirects to login."""
        cfg_a = fs08_data["uat_005"]["parent_a"]
        login = self.get_page(SingpassLoginPage)

        with self.step("Log in as Parent A and then trigger header logout", expected="Session flushed and redirected to login."):
            login.login_with_persona(cfg_a["persona_name"], base_url=fs08_data["base_url"])
            login.logout()
            assert login.is_login_page_loaded(), "Login page must be visible after logout."
            raw_user = self.page.evaluate("() => window.sessionStorage.getItem('edusave.parent-auth.user')")
            assert raw_user is None, f"Security leak: sessionStorage still retains user data: {raw_user}"
            self.step.set_actual("Session storage completely flushed (value is null).")

    def test_tc_uat005_05_returning_parent_relogin_reuses_existing_profile(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-05: Verify returning parent re-login reuses existing profile cleanly without duplication."""
        cfg_a = fs08_data["uat_005"]["parent_a"]
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step("Log in as Parent A, log out, and re-login immediately", expected="Re-login succeeds cleanly."):
            login.login_with_persona(cfg_a["persona_name"], base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            login.logout()
            login.login_with_persona(cfg_a["persona_name"], base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()

            cards = home.get_all_child_cards()
            assert len(cards) == cfg_a["verified_count"], f"Duplicate cards found upon re-login: {len(cards)}"
            self.step.set_actual(f"Re-login successful; verified {len(cards)} cards intact.")

    def test_tc_uat005_06_dual_parent_equality_independent_logins(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-06: Verify dual-parent equality (D-19): Parents access independently with equal rights."""
        p1 = fs08_data["personas"]["PAR-NORMAL-01"]
        p2 = fs08_data["personas"]["PAR-NORMAL-02"]
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step("Log in as Parent 1 and verify child cards", expected="Parent 1 sees linked children."):
            login.login_with_persona(p1["name"], base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            assert home.get_child_cards_count() > 0, "Parent 1 must see linked children."
            login.logout()

        with self.step("Log in as Parent 2 and verify child cards independently", expected="Parent 2 sees linked children."):
            login.login_with_persona(p2["name"], base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            assert home.get_child_cards_count() > 0, "Parent 2 must see linked children."
            self.step.set_actual("Dual-Parent Equality confirmed with independent sessions.")

    def test_tc_uat005_08_parent_b_login_verified_children_zero_overlap(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-08: Step 3 — Verify Parent B login displays verified children with 0% overlap with Parent A."""
        cfg_a = fs08_data["uat_005"]["parent_a"]
        cfg_b = fs08_data["uat_005"]["parent_b"]
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step("Authenticate as Parent B and retrieve child list", expected=f"{cfg_b['verified_count']} children."):
            login.login_with_persona(cfg_b["persona_name"], base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            cards_b = home.get_all_child_cards()
            names_b = [c["name"] for c in cards_b]
            assert len(cards_b) == cfg_b["verified_count"], f"Expected {cfg_b['verified_count']} cards, got {len(cards_b)}"
            for child in cfg_b["expected_children"]:
                assert child in names_b, f"Parent B child '{child}' missing from cards: {names_b}"

            overlap = set(names_b).intersection(set(cfg_a["expected_children"]))
            assert len(overlap) == 0, f"Privacy violation: Found cross-family overlap: {overlap}"
            self.highlight_actual_result(locator=home.CARD_ARTICLES, text=f"Zero Overlap: {names_b}")
            self.step.set_actual(f"Parent B children verified with 0% overlap: {names_b}")

    def test_tc_uat005_16_complete_uat005_three_step_workflow_e2e(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-16: Verify complete UAT-005 3-step workflow in seamless execution."""
        cfg_a = fs08_data["uat_005"]["parent_a"]
        cfg_b = fs08_data["uat_005"]["parent_b"]
        idor_cfg = fs08_data["uat_005"]["idor_test"]
        base_url = fs08_data["base_url"]
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)
        tx_page = self.get_page(TransactionsPage)

        with self.step("E2E Step 1: Sign in as Parent A & verify verified children", expected="3 children displayed."):
            login.login_with_persona(cfg_a["persona_name"], base_url=base_url)
            home.wait_for_portal_loaded()
            cards_a = home.get_all_child_cards()
            assert len(cards_a) == cfg_a["verified_count"], "Parent A children count mismatch."

        with self.step("E2E Step 2: Attempt IDOR URL tampering & verify safe blocking", expected="Blocked with error panel."):
            tx_page.open(student_id=idor_cfg["target_unauthorized_student"], base_url=base_url)
            assert tx_page.is_unable_to_load_visible(timeout=8000), "Error container must appear on IDOR attempt."

        with self.step("E2E Step 3: Logout, session flush, and Parent B login with zero overlap", expected="Zero overlap."):
            login.logout()
            login.login_with_persona(cfg_b["persona_name"], base_url=base_url)
            home.wait_for_portal_loaded()
            cards_b = home.get_all_child_cards()
            names_b = [c["name"] for c in cards_b]
            overlap = set(names_b).intersection(set(cfg_a["expected_children"]))
            assert len(overlap) == 0, f"Found overlap: {overlap}"
            self.highlight_actual_result(locator=home.CARD_ARTICLES, text=f"UAT-005 Passed: {names_b}")
            self.step.set_actual("Complete UAT-005 3-step lifecycle verified successfully.")
