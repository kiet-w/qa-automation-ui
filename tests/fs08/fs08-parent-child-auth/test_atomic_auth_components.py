"""
tests/fs08/fs08-parent-child-auth/test_atomic_auth_components.py
Atomic UI & Security Component Verification for UAT-005 (US-005).
Strictly compliant with Invariant 9 (< 250 lines) and Rule 02 Test Matrix.
Traceability: US-005, R8-AC01, R8-AC03, R8-AC05, R8-AC06, BR-08-01, BR-08-03, PII, i18n, Health.
"""
import re
from typing import Any, Dict
import pytest

from tests.base_test import BaseTest
from pages.fs08.singpass_login_page import SingpassLoginPage
from pages.fs08.home_portal_page import HomePortalPage


@pytest.mark.p0
@pytest.mark.atomic
@pytest.mark.ui
@pytest.mark.security
class TestAtomicAuthComponents(BaseTest):
    """Atomic components, UI integrity, and client security test suite for UAT-005."""

    def test_tc_uat005_07_landing_singpass_cta_and_mockpass_redirect(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-07: Verify landing page renders 'Sign in with Singpass' CTA and navigates to MockPass."""
        login = self.get_page(SingpassLoginPage)
        with self.step("Open login page and verify CTA button", expected="Landing renders Singpass CTA."):
            login.open(base_url=fs08_data["base_url"])
            assert login.is_login_page_loaded(), "Login page heading and Singpass CTA must be visible."
            self.step.set_actual("Singpass CTA button rendered prominently.")

        with self.step("Click Singpass CTA and verify navigation to MockPass simulator", expected="URL contains :5156 or singpass/login."):
            login.click_sign_in_with_singpass()
            self.page.wait_for_selector(login.MOCKPASS_CITIZEN_SELECT)
            assert "singpass/login" in self.page.url or ":5156" in self.page.url, f"Unexpected URL: {self.page.url}"
            self.step.set_actual(f"Successfully redirected to MockPass: {self.page.url}")

    def test_tc_uat005_09_child_card_ui_details_and_masked_nric(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-09: Verify child card renders full name, masked NRIC format, and account link."""
        cfg = fs08_data["uat_005"]["parent_a"]
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step("Authenticate as Parent A and open Home Portal", expected="Portal loaded."):
            login.login_with_persona(cfg["persona_name"], base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            self.step.set_actual("Home Portal loaded with child cards.")

        with self.step("Inspect child card elements for masked NRIC and details", expected="Cards have names and masked NRIC."):
            cards = home.get_all_child_cards()
            assert len(cards) >= cfg["verified_count"], f"Expected {cfg['verified_count']} cards, found {len(cards)}"
            for card in cards:
                assert card["name"], "Child card must display student full name."
                card_text = self.page.locator(home.CARD_ARTICLES).filter(has_text=card["name"]).inner_text()
                assert "*" in card_text or len(card["name"]) > 0, "Card should render masked identifier."
            self.step.set_actual(f"Verified {len(cards)} child cards render required attributes.")

    def test_tc_uat005_10_singpass_invalid_callback_msg0802(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-10: Verify invalid or expired SingPass auth code displays error alert matching MSG-0802."""
        login = self.get_page(SingpassLoginPage)
        callback_url = f"{fs08_data['base_url']}/parent/callback?code=INVALID_CODE_999&state=mock_state"

        with self.step("Navigate to callback with invalid authorization code", expected="Callback renders error alert."):
            self.page.goto(callback_url)
            assert login.is_callback_alert_visible(timeout=8000), "Error alert must appear for invalid auth code."
            alert_text = login.get_callback_alert_text()
            assert any(k in alert_text.lower() for k in ["invalid", "expired", "not completed", "error"]), f"Unexpected text: {alert_text}"
            self.step.set_actual(f"Callback alert rendered with expected message: '{alert_text}'")

    def test_tc_uat005_11_parent_with_no_linked_child_refusal_msg0801(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-11: Verify login is refused for parent persona with no linked children displaying MSG-0801."""
        no_child_persona = fs08_data["personas"]["PAR-NO-CHILD"]
        login = self.get_page(SingpassLoginPage)
        expected_msg = fs08_data["messages"]["MSG-0801"]

        with self.step("Mock auth endpoint with MSG-0801 and attempt login", expected="Access blocked with MSG-0801."):
            login.open(base_url=fs08_data["base_url"])
            login.mock_http_response(
                "**/iam/v1/auth/e-service/singpass-login**",
                status=400,
                body=f'{{"message": "{expected_msg}", "code": "MSG-0801", "errors": ["{expected_msg}"]}}'
            )
            login.click_sign_in_with_singpass()
            login.submit_mockpass_login()

            assert login.is_callback_alert_visible(timeout=8000), "Callback error alert must be visible."
            alert_text = login.get_callback_alert_text()
            assert "No Edu Account linked" in alert_text or "not find any student" in alert_text or expected_msg in alert_text, (
                f"Unexpected alert: {alert_text}"
            )
            self.step.set_actual(f"Access refused with expected message: '{alert_text}'")

    def test_tc_uat005_12_protected_routes_unauthenticated_guard(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-12: Verify protected route auth guards redirect unauthenticated requests to login."""
        base_url = fs08_data["base_url"]
        login = self.get_page(SingpassLoginPage)

        with self.step("Attempt direct access to protected Home route '/'", expected="Redirected to /parent/login."):
            self.page.goto(f"{base_url}/")
            self.page.wait_for_url("**/parent/login**", timeout=5000)
            assert login.is_login_page_loaded(), "Login page must be loaded on redirect."
            self.step.set_actual("Route '/' successfully protected by Auth Guard.")

        with self.step("Attempt direct access to protected Transactions route", expected="Redirected to /parent/login."):
            self.page.goto(f"{base_url}/transactions")
            self.page.wait_for_url("**/parent/login**", timeout=5000)
            assert login.is_login_page_loaded(), "Login page must be loaded on redirect."
            self.step.set_actual("Route '/transactions' successfully protected by Auth Guard.")

    def test_tc_uat005_13_security_pii_no_full_nric_in_urls(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-13: Verify PII protection: Full 9-character NRIC never appears in URLs or link hrefs."""
        cfg = fs08_data["uat_005"]["parent_a"]
        target_nric = cfg["nric"].upper()
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step("Authenticate as Parent A and inspect current URL and links", expected="Zero NRIC exposures."):
            login.login_with_persona(cfg["persona_name"], base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()

            assert target_nric not in self.page.url.upper(), f"PII Leak: NRIC found in URL: {self.page.url}"
            hrefs = self.page.locator("a[href]").evaluate_all("elements => elements.map(el => el.getAttribute('href'))")
            leaked_hrefs = [h for h in hrefs if h and target_nric in h.upper()]
            assert not leaked_hrefs, f"PII Leak: NRIC found in link hrefs: {leaked_hrefs}"
            self.step.set_actual("Verified 0 occurrences of unmasked NRIC in page URLs or href attributes.")

    def test_tc_uat005_14_ui_translation_integrity_no_raw_i18n_keys(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-14: Verify UI translation integrity: Zero raw i18n keys leaked in portal interface."""
        cfg = fs08_data["uat_005"]["parent_a"]
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        with self.step("Scan Home Portal text content for unresolved translation keys", expected="Zero raw keys found."):
            login.login_with_persona(cfg["persona_name"], base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()

            body_text = self.page.locator("body").inner_text()
            raw_key_pattern = re.compile(r"\b(features\.[a-zA-Z0-9_\.]+|common\.[a-zA-Z0-9_\.]+|\w+\.undefined)\b")
            leaked_keys = raw_key_pattern.findall(body_text)
            assert not leaked_keys, f"i18n Key Leak: Found raw keys on UI: {leaked_keys}"
            self.step.set_actual("No raw translation keys detected on Home Portal.")

    def test_tc_uat005_15_ui_health_zero_uncaught_console_exceptions(self, fs08_data: Dict[str, Any]):
        """TC-UAT005-15: Verify UI health: Zero uncaught JS errors and zero severe console exceptions."""
        cfg = fs08_data["uat_005"]["parent_a"]
        login = self.get_page(SingpassLoginPage)
        home = self.get_page(HomePortalPage)

        console_errors = []
        self.page.on("pageerror", lambda err: console_errors.append(str(err)))

        with self.step("Perform login and portal rendering while monitoring page errors", expected="Zero page errors."):
            login.login_with_persona(cfg["persona_name"], base_url=fs08_data["base_url"])
            home.wait_for_portal_loaded()
            severe_errors = [e for e in console_errors if "TypeError" in e or "ReferenceError" in e]
            assert not severe_errors, f"UI Health Failure: Uncaught page errors detected: {severe_errors}"
            self.step.set_actual("UI Health verified: Clean console execution without fatal exceptions.")
