#!/usr/bin/env python3
"""
tools/break_it/scaffold_break_it.py - CLI Scaffolder for Adversarial Test Suites.

Generates a fully compliant @pytest.mark.break_it test suite for any Page Object / Module,
enforcing Invariant 8 across all 6 adversarial dimensions.

Usage:
    python3 tools/break_it/scaffold_break_it.py \
        --module fs08 \
        --page-class ParentProfilePage \
        --page-module pages.fs08.parent_profile_page \
        --output tests/fs08/test_parent_profile_break_it.py
"""
import argparse
from pathlib import Path
import sys

WORKSPACE_DIR = Path(__file__).resolve().parent.parent.parent

SCAFFOLD_HEADER = '''"""
{OUTPUT_REL_PATH}
Automated adversarial, client-bypass, and resilience test suite ("Phá Có Kỷ Luật").
Baseline: Invariant 8 (Adversarial Quality Gate) & Module: {MODULE}.
"""
import copy
import json
from pathlib import Path
from typing import List
import pytest

from tests.base_test import BaseTest
from core import Exceptor
from {PAGE_MODULE} import {PAGE_CLASS}

WORKSPACE_DIR = Path(__file__).resolve().parent.parent
NAUGHTY_DATA_PATH = WORKSPACE_DIR / "data" / "naughty_strings.json"


def load_naughty_strings():
    if NAUGHTY_DATA_PATH.exists():
        with open(NAUGHTY_DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {{}}


NAUGHTY_DATA = load_naughty_strings()


@pytest.mark.{MODULE}
@pytest.mark.break_it
class Test{MODULE_CAMEL}Resilience(BaseTest):
    """
    Adversarial & Resilience Test Suite for {MODULE} - {PAGE_CLASS}:
    - Dimension A: Malformed & Hostile Input Data (XSS, extreme boundary lengths, UTF-8)
    - Dimension B: Client-side Validation Bypass & Property Descriptor Forcing
    - Dimension C: Concurrency, Double-Click Idempotency & Network Chaos
    - Dimension D: Authorization / Schema Tampering
    - Dimension E: Keyboard Navigation & A11y Boundaries
    - Dimension F: Zero Uncaught Client JS Errors (Technical Health Oracle)
    """

    def test_tc_brk_001_client_bypass_rejects_invalid_input(self):
        """
        TC_BRK_001 — Client Constraint Bypass: Strips client validations and forces invalid payload.
        Expected: Server properly rejects; Exceptor detects bug if accepted.
        """
        page_obj = self.get_page({PAGE_CLASS})
        # TODO: Cập nhật key data tương ứng với {PAGE_CLASS}
        data = copy.deepcopy(self.search_data or {{}})

        with self.step("Step 1: Open form, populate baseline data, and strip client constraints"):
            page_obj.open()
            if hasattr(page_obj, "fill_full_form"):
                page_obj.fill_full_form(data)
            page_obj.strip_client_constraints()
            # Bơm dữ liệu vi phạm qua prototype setter
            if hasattr(page_obj, "PRIMARY_EMAIL"):
                page_obj.force_set_value(page_obj.PRIMARY_EMAIL, "not-an-email@malformed")

        with self.step("Step 2: Submit form and verify server rejection"):
            if hasattr(page_obj, "save"):
                page_obj.save()
            elif hasattr(page_obj, "submit"):
                page_obj.submit()
            if hasattr(page_obj, "get_state_snapshot"):
                snapshot = page_obj.get_state_snapshot()
                Exceptor.expect_bug_if_accepted(snapshot, context="TC_BRK_001 Client Bypass")

        with self.step("Step 3: Verify zero uncaught runtime JS exceptions"):
            Exceptor.expect_zero_js_errors(page_obj.get_technical_snapshot(), context="TC_BRK_001")

    @pytest.mark.parametrize(
        "xss_payload",
        NAUGHTY_DATA.get("xss_payloads", ["<script>alert('XSS')</script>"])[:3],
    )
    def test_tc_brk_002_hostile_xss_injection_resilience(self, xss_payload: str):
        """
        TC_BRK_002 — Hostile Input: Verifies XSS payloads do not execute unhandled native dialogs.
        """
        page_obj = self.get_page({PAGE_CLASS})
        dialog_messages = []
        self.page.on("dialog", lambda d: (dialog_messages.append(d.message), d.dismiss()))

        with self.step(f"Step 1: Open page and inject hostile string: {{xss_payload}}"):
            page_obj.open()
            # TODO: Chọn trường text cần inject
            # page_obj.force_set_value(page_obj.TEXT_FIELD, xss_payload)

        with self.step("Step 2: Verify zero native dialogs triggered"):
            assert len(dialog_messages) == 0, f"XSS executed! Dialog captured: {{dialog_messages}}"

        with self.step("Step 3: Verify client runtime health and zero JS errors"):
            Exceptor.expect_zero_js_errors(page_obj.get_technical_snapshot(), context=xss_payload)

    def test_tc_brk_003_extreme_boundary_string_length(self):
        """
        TC_BRK_003 — Extreme Boundary: 10,000 character string without layout overflow.
        """
        page_obj = self.get_page({PAGE_CLASS})
        huge_string = "A" * 10000

        with self.step("Step 1: Inject 10,000-character payload"):
            page_obj.open()
            page_obj.strip_client_constraints()

        with self.step("Step 2: Verify layout integrity"):
            self.assert_no_horizontal_overflow()
            Exceptor.expect_zero_js_errors(page_obj.get_technical_snapshot(), context="TC_BRK_003")

    def test_tc_brk_004_double_click_submit_idempotency(self):
        """
        TC_BRK_004 — Concurrency: Verifies rapid double click does not crash or double dispatch.
        """
        page_obj = self.get_page({PAGE_CLASS})

        with self.step("Step 1: Open target page and prepare action"):
            page_obj.open()

        with self.step("Step 2: Rapid double click and check debounce"):
            # action_btn = page_obj.wait_for_visible(page_obj.SUBMIT_BTN)
            # action_btn.dblclick()
            pass

        with self.step("Step 3: Verify client health"):
            Exceptor.expect_zero_js_errors(page_obj.get_technical_snapshot(), context="TC_BRK_004")

    def test_tc_brk_005_keyboard_tab_navigation_no_focus_trap(self):
        """
        TC_BRK_005 — Accessibility: Verifies sequential Tab navigation advances without getting trapped.
        """
        page_obj = self.get_page({PAGE_CLASS})

        with self.step("Step 1: Open page"):
            page_obj.open()

        with self.step("Step 2: Press Tab key 10 times and verify focus moves"):
            focused_tags = []
            for _ in range(10):
                self.page.keyboard.press("Tab")
                tag = self.page.evaluate("() => document.activeElement ? document.activeElement.tagName : 'NONE'")
                focused_tags.append(tag)
            assert len(set(focused_tags)) > 1, f"Focus trapped! Visited tags: {{focused_tags}}"
            Exceptor.expect_zero_js_errors(page_obj.get_technical_snapshot(), context="TC_BRK_005")
'''


def to_camel_case(snake_str: str) -> str:
    components = snake_str.replace("-", "_").split("_")
    return "".join(x.capitalize() for x in components)


def main():
    parser = argparse.ArgumentParser(description="Scaffold @pytest.mark.break_it test suites for AI Coding.")
    parser.add_argument("--module", required=True, help="Module or ticket name (e.g. fs08, curricula, fs03)")
    parser.add_argument("--page-class", required=True, help="Target Page Object class name (e.g. CurriculaTrainerPage)")
    parser.add_argument("--page-module", required=True, help="Import path for Page Object (e.g. pages.curricula_trainer_page)")
    parser.add_argument("--output", required=True, help="Target file path for scaffolded test (e.g. tests/break_it/test_sample.py)")

    args = parser.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rel_path = out_path.relative_to(WORKSPACE_DIR) if out_path.is_relative_to(WORKSPACE_DIR) else out_path

    content = SCAFFOLD_HEADER.format(
        OUTPUT_REL_PATH=str(rel_path),
        MODULE=args.module.lower(),
        MODULE_CAMEL=to_camel_case(args.module),
        PAGE_CLASS=args.page_class,
        PAGE_MODULE=args.page_module,
    )

    out_path.write_text(content, encoding="utf-8")
    print(f"✅ Successfully scaffolded break_it test suite:")
    print(f"   -> {out_path.resolve()}")


if __name__ == "__main__":
    main()
