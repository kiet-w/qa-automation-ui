"""
core/field_matrix_engine.py - Generic Field Matrix Validation Engine.

Executes data-driven test cases across the 12 validation matrix layers
(Empty, Whitespace ASM-15, BVA length, Charset, Regex, Security/XSS, etc.)
with zero assertion logic in Page Objects, maintaining full evidence instrumentation.
Strictly compliant with Invariant 1 (Zero assertions in POM) and Invariant 9 (< 250 lines).
"""
import copy
from typing import Any, Callable, Dict, Optional, Union
from playwright.sync_api import expect, Locator, Page


class FieldMatrixEngine:
    """
    Central execution engine for data-driven field matrix testing.
    Handles standard field lifecycle:
    1. Enter input value (resolving repetitions or dynamic generators)
    2. Trigger validation event (blur/change)
    3. Assert UI feedback (aria-invalid, error message, raw i18n protection)
    4. Assert form lifecycle (save button status, modal blocking)
    5. Emit evidence (step logging, visual highlight, set_actual)
    """

    def __init__(self, test: Any):
        self.test = test
        self.page: Page = test.page

    @staticmethod
    def resolve_input_value(case: Dict[str, Any]) -> str:
        """Resolve scalar strings or pattern dicts (repeat/count/suffix) into test input."""
        value = case.get("input", "")
        if isinstance(value, dict):
            repeat_char = value.get("repeat") or value.get("prefix", "a")
            count = value.get("count", 1)
            suffix = value.get("suffix", "")
            return repeat_char * count + suffix
        return str(value) if value is not None else ""

    def run_case(
        self,
        case: Dict[str, Any],
        selector: Union[str, Locator],
        page_object: Optional[Any] = None,
        custom_action: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> None:
        """
        Execute a single matrix test case against a target field selector or page object.
        Preserves deterministic step names, highlighting, and failure triaging.
        """
        if custom_action is not None:
            custom_action(case)
            return

        case_id = case.get("id", "TC-MATRIX")
        title = case.get("title", "Field Matrix Test")
        source = case.get("source", "Field Matrix Specification")
        kind = case.get("kind", "valid")

        field = self.page.locator(selector).first if isinstance(selector, str) else selector.first
        entered = self.resolve_input_value(case)
        dialogs = []
        dialog_handler = lambda dialog: dialogs.append(dialog.message)
        self.page.on("dialog", dialog_handler)

        try:
            with self.test.step(f"{case_id}: {title}", expected=source):
                assert field.count() == 1, f"Field '{case.get('field')}' must exist exactly once in form"
                baseline = field.input_value()
                field.fill(entered)
                field.blur()
                actual = field.input_value()

                if kind in {"invalid", "invalid_or_clipped"} and actual == entered:
                    self._assert_invalid_state(field, case, page_object)
                elif kind in {"overflow", "invalid_or_clipped"}:
                    self._assert_overflow_state(field, actual, case, dialogs)
                elif kind == "trim":
                    expected_norm = case.get("normalized", entered.strip())
                    assert actual == expected_norm, f"Field not trimmed as specified: expected {expected_norm!r}, got {actual!r}"
                    expect(field).not_to_have_attribute("aria-invalid", "true")
                else:  # valid, optional, safe_text
                    self._assert_valid_state(field, actual, entered, baseline, kind, case, page_object, dialogs)

                self.test.highlight_actual_result(locator=selector, text=f"{case_id}: {kind}")
                self.test.step.set_actual(
                    f"{case.get('field')}: {actual!r}; aria-invalid={field.get_attribute('aria-invalid')}"
                )
        finally:
            self.page.remove_listener("dialog", dialog_handler)

    def _assert_invalid_state(self, field: Locator, case: Dict[str, Any], page_object: Any) -> None:
        """Assert invalid state: blocked submission, aria-invalid, error message, 0 raw i18n."""
        if page_object and hasattr(page_object, "is_save_disabled"):
            if not page_object.is_save_disabled() and hasattr(page_object, "click_save_changes"):
                page_object.click_save_changes()
        if page_object and hasattr(page_object, "is_confirm_dialog_open"):
            assert not page_object.is_confirm_dialog_open(timeout=500), "Invalid input opened confirmation dialog"

        expect(field).to_have_attribute("aria-invalid", "true")

        if case.get("message"):
            expect(self.page.get_by_text(case["message"], exact=True).first).to_be_visible()

        if page_object and hasattr(page_object, "get_field_error_text"):
            error_text = page_object.get_field_error_text(case.get("field", ""))
            if hasattr(page_object, "is_raw_i18n_key"):
                assert not page_object.is_raw_i18n_key(error_text), f"Raw i18n key leaked: {error_text}"

    def _assert_overflow_state(self, field: Locator, actual: str, case: Dict[str, Any], dialogs: list) -> None:
        """Assert overflow boundary: clipped or flagged invalid."""
        limit = case.get("limit", 0)
        if limit and len(actual) > limit:
            expect(field).to_have_attribute("aria-invalid", "true")
            if case.get("message"):
                expect(self.page.get_by_text(case["message"], exact=True).first).to_be_visible()
        assert not dialogs, f"Input processing triggered unexpected browser dialog: {dialogs}"

    def _assert_valid_state(
        self, field: Locator, actual: str, entered: str, baseline: str,
        kind: str, case: Dict[str, Any], page_object: Any, dialogs: list
    ) -> None:
        """Assert valid state: accepted value, aria-invalid cleared, save enabled on changes."""
        assert actual == entered, f"Expected {entered!r}, got {actual!r}"
        expect(field).not_to_have_attribute("aria-invalid", "true")

        if case.get("length") is not None:
            assert len(actual) == case["length"], f"Boundary length mismatch: expected {case['length']}, got {len(actual)}"

        if kind == "safe_text":
            assert not dialogs, f"Safe text input executed an unexpected browser dialog: {dialogs}"

        if kind != "optional" and actual != baseline and page_object:
            if hasattr(page_object, "is_save_disabled"):
                assert not page_object.is_save_disabled(), "Valid field change did not enable Save button"
