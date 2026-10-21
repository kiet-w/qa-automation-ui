"""
tests/break_it/test_curricula_resilience.py
Automated adversarial, client-bypass, and resilience test suite ("Phá Có Kỷ Luật").
Baseline: Invariant 8 (Adversarial Quality Gate) & Deliverable 3 (US04 Curricula Trainer).
"""
import copy
import json
from pathlib import Path
from typing import List
import pytest

from tests.base_test import BaseTest
from core import Exceptor

WORKSPACE_DIR = Path(__file__).resolve().parent.parent.parent
CURRICULA_DATA_PATH = WORKSPACE_DIR / "data" / "curricula_trainer_data.json"
NAUGHTY_DATA_PATH = WORKSPACE_DIR / "data" / "naughty_strings.json"


def load_curricula_data():
    with open(CURRICULA_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_naughty_strings():
    with open(NAUGHTY_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


CURRICULA_DATA = load_curricula_data()
NAUGHTY_DATA = load_naughty_strings()


@pytest.mark.curricula
@pytest.mark.break_it
class TestCurriculaResilience(BaseTest):
    """
    Test suite applying disciplined adversarial testing techniques to Curricula Trainer Form:
    - Dimension A: Malformed & hostile inputs (XSS, extreme boundary lengths, UTF-8 strings)
    - Dimension B: Client-side validation stripping & forced values via React/Vue descriptor
    - Dimension C: Double-click rapid submission & idempotency
    - Dimension D: Select dropdown tampering (unauthorized enum option injection)
    - Dimension E: Keyboard accessibility & focus traps
    - Dimension F: Silent client defect & zero unhandled JS exceptions verification
    """

    def test_tc_brk_001_client_bypass_rejects_malformed_email(self):
        """
        TC_BRK_001 — Client-side constraint bypass: Stripping form validations and forcing malformed email.
        Scenario: Strip HTML5 form attributes (novalidate, pattern, required), force an invalid email string,
                  and submit form.
        Expected Behavior: Validator properly rejects submission; success box must NOT appear.
        """
        curricula = self.curricula
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])

        with self.step("Step 1: Open form, populate valid baseline data, and strip client constraints"):
            curricula.open()
            curricula.fill_full_form(data)
            # Adversarial bypass: Remove HTML5 validations from DOM
            curricula.strip_client_constraints("form, .content")
            # Force invalid email bypassing input restrictions
            curricula.force_set_value(curricula.PRIMARY_EMAIL, "not-an-email@malformed")

        with self.step("Step 2: Submit form and verify system rejection"):
            curricula.save()
            snapshot = curricula.get_state_snapshot()
            # Gatekeeper: Must detect bug if submission was accepted
            Exceptor.expect_bug_if_accepted(snapshot, context="TC_BRK_001: Client Bypass Email")
            assert not snapshot["success_visible"], "System unexpectedly accepted malformed email after client bypass"
            assert "primaryEmail" in snapshot["visible_errors"], "Expected error message on primaryEmail field"

        with self.step("Step 3: Verify zero uncaught JS exceptions during adversarial bypass"):
            tech_snapshot = curricula.get_technical_snapshot()
            Exceptor.expect_zero_js_errors(tech_snapshot, context="TC_BRK_001 Technical Check")

    @pytest.mark.parametrize(
        "xss_payload",
        NAUGHTY_DATA.get("xss_payloads", ["<script>alert('XSS')</script>"])[:3],
    )
    def test_tc_brk_002_hostile_xss_payload_handling_no_dialog_execution(self, xss_payload: str):
        """
        TC_BRK_002 — Hostile input injection: Verify XSS payloads do not trigger unhandled alerts or JS errors.
        Scenario: Populate preferred name field with hostile script tags and submit.
        Expected Behavior: Input is escaped / treated as literal text; no unhandled native alert() dialog is executed.
        """
        curricula = self.curricula
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        dialog_messages: List[str] = []

        # Passive listener for native alerts triggered by reflected XSS
        self.page.on("dialog", lambda d: (dialog_messages.append(d.message), d.dismiss()))

        with self.step(f"Step 1: Populate form with XSS payload: {xss_payload}"):
            curricula.open()
            curricula.fill_full_form(data)
            curricula.force_set_value(curricula.PREFERRED_NAME, xss_payload)
            curricula.save()

        with self.step("Step 2: Verify no unhandled XSS dialog was executed"):
            assert len(dialog_messages) == 0, f"XSS executed! Dialog captured: {dialog_messages}"

        with self.step("Step 3: Verify client runtime health and zero JS errors"):
            tech_snapshot = curricula.get_technical_snapshot()
            Exceptor.expect_zero_js_errors(tech_snapshot, context=f"XSS payload {xss_payload}")

    def test_tc_brk_003_extreme_boundary_string_length(self):
        """
        TC_BRK_003 — Extreme input boundary: 10,000 character string in name field.
        Scenario: Force a 10,000-character payload into preferredName field, bypassing maxlength.
        Expected Behavior: DOM handles payload without crashing or breaking layout overflow.
        """
        curricula = self.curricula
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])
        huge_string = "A" * 10000

        with self.step("Step 1: Open form and inject 10,000-character string"):
            curricula.open()
            curricula.fill_full_form(data)
            curricula.strip_client_constraints()
            curricula.force_set_value(curricula.PREFERRED_NAME, huge_string)

        with self.step("Step 2: Submit form and verify layout and technical health"):
            curricula.save()
            self.assert_no_horizontal_overflow()
            tech_snapshot = curricula.get_technical_snapshot()
            Exceptor.expect_zero_js_errors(tech_snapshot, context="TC_BRK_003 10K String")

    def test_tc_brk_004_double_click_submit_idempotency(self):
        """
        TC_BRK_004 — Concurrency & double-click: Submit button rapid double-click.
        Scenario: Populate valid form and trigger double-click on Save button.
        Expected Behavior: UI does not throw unhandled race errors or runtime JS exceptions.
        """
        curricula = self.curricula
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])

        with self.step("Step 1: Populate valid form data"):
            curricula.open()
            curricula.fill_full_form(data)

        with self.step("Step 2: Rapidly double-click Save button"):
            btn = curricula.wait_for_visible(curricula.SAVE_BTN)
            btn.dblclick()
            self.page.wait_for_load_state("domcontentloaded")

        with self.step("Step 3: Verify success state and zero runtime JS crashes"):
            snapshot = curricula.get_state_snapshot()
            Exceptor.expect_success(snapshot, context="TC_BRK_004 Double Click")
            tech_snapshot = curricula.get_technical_snapshot()
            Exceptor.expect_zero_js_errors(tech_snapshot, context="TC_BRK_004 Technical Check")

    def test_tc_brk_005_dropdown_unauthorized_enum_injection(self):
        """
        TC_BRK_005 — Schema tampering: Injecting synthetic <option> into Select element.
        Scenario: Dynamically inject an unauthorized nationality option into the DOM and submit.
        Expected Behavior: Injection does not crash DOM or produce unhandled script errors.
        """
        curricula = self.curricula
        data = copy.deepcopy(CURRICULA_DATA["valid_singapore_resident"])

        with self.step("Step 1: Inject synthetic unauthorized option into nationality select"):
            curricula.open()
            curricula.fill_full_form(data)
            curricula.inject_select_option(
                curricula.NATIONALITY,
                value="SYNTHETIC_UNKNOWN_COUNTRY",
                label="Synthetic Country 999",
            )

        with self.step("Step 2: Submit form and verify DOM resilience"):
            curricula.save()
            tech_snapshot = curricula.get_technical_snapshot()
            Exceptor.expect_zero_js_errors(tech_snapshot, context="TC_BRK_005 Dropdown Injection")

    def test_tc_brk_006_keyboard_tab_navigation_no_focus_trap(self):
        """
        TC_BRK_006 — Accessibility boundary: Sequential keyboard Tab navigation without focus trap.
        Scenario: Open form and trigger sequential Tab keystrokes across form controls.
        Expected Behavior: Focus moves sequentially without getting trapped indefinitely in any element.
        """
        curricula = self.curricula

        with self.step("Step 1: Open form and focus first interactive element"):
            curricula.open()
            self.page.locator(curricula.PREFERRED_NAME).focus()

        with self.step("Step 2: Press Tab key 10 times and verify focus advances"):
            focused_tags = []
            for _ in range(10):
                self.page.keyboard.press("Tab")
                active_tag = self.page.evaluate("() => document.activeElement ? document.activeElement.tagName : 'NONE'")
                focused_tags.append(active_tag)

            # Ensure focus did not get trapped at single element
            assert len(set(focused_tags)) > 1, f"Focus appears trapped! Observed sequence: {focused_tags}"
            tech_snapshot = curricula.get_technical_snapshot()
            Exceptor.expect_zero_js_errors(tech_snapshot, context="TC_BRK_006 Tab Navigation")
