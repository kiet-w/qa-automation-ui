"""
core/exceptor.py - Central Business Assertion Gatekeeper (Exceptor).

Decouples UI data collection (Page Object) from business validation logic (Exceptor).
Operates exclusively on static UI state snapshots without invoking Playwright directly.

Provides intent-driven assertion methods:
- expect_success: Expects action to succeed with success indicator visible and no errors (Happy path).
- expect_rejection: Expects action to be rejected with expected field error (Unhappy path).
- expect_bug_if_rejected: Expects action to succeed; if rejected, raises [BUG DETECTED].
- expect_bug_if_accepted: Expects action to fail; if accepted, raises [BUG DETECTED] (Validation Bypass).
"""
from typing import Any, Dict, Union, Tuple, Optional
from core.exceptions import BusinessAssertionError


class Exceptor:
    """
    Central gatekeeper deciding test pass/fail outcome for business expectations.
    Consumes UI state snapshots and validates against expected conditions.
    """

    @staticmethod
    def _parse_snapshot(snapshot: Union[Dict[str, Any], object]) -> Tuple[bool, Dict[str, str]]:
        """
        Helper method to extract fields from snapshot (supports both dict and object).
        """
        if isinstance(snapshot, dict):
            success_visible = bool(snapshot.get("success_visible", False))
            visible_errors = snapshot.get("visible_errors") or {}
        else:
            success_visible = bool(getattr(snapshot, "success_visible", False))
            visible_errors = getattr(snapshot, "visible_errors", {}) or {}

        if not isinstance(visible_errors, dict):
            visible_errors = {}

        return success_visible, visible_errors

    @classmethod
    def expect_success(cls, snapshot: Union[Dict[str, Any], object], context: str = "") -> None:
        """
        Expectation: Action must SUCCEED (Happy path).
        Verifies: success_visible is True, and visible_errors is empty.

        Args:
            snapshot: UI data snapshot ({ "success_visible": bool, "visible_errors": dict }).
            context: Test case or step context description.

        Raises:
            BusinessAssertionError: When action failed or UI validation errors exist.
        """
        success_visible, visible_errors = cls._parse_snapshot(snapshot)

        if not success_visible or len(visible_errors) > 0:
            details = [
                f"[BUSINESS ASSERTION FAILED] Action expected to SUCCEED.",
                f"Context: {context}" if context else None,
                f"Expected: success_visible=True and visible_errors={{}}",
                f"Actual: success_visible={success_visible}, visible_errors={visible_errors}",
            ]
            msg = " | ".join(d for d in details if d)
            raise BusinessAssertionError(msg)

    @classmethod
    def expect_rejection(
        cls,
        snapshot: Union[Dict[str, Any], object],
        field: str,
        message_contains: str,
        context: str = "",
    ) -> None:
        """
        Expectation: Action must be REJECTED (Unhappy path - invalid input properly blocked).
        Verifies: success_visible is False, error is displayed on `field`, and error text contains `message_contains`.

        Args:
            snapshot: UI data snapshot ({ "success_visible": bool, "visible_errors": dict }).
            field: Expected error field identifier (e.g. 'primaryPhone').
            message_contains: Expected substring in the field's validation error message.
            context: Test execution context.

        Raises:
            BusinessAssertionError: When action unexpectedly succeeded or error message/field mismatches.
        """
        success_visible, visible_errors = cls._parse_snapshot(snapshot)
        actual_field_msg = visible_errors.get(field)

        reasons = []
        if success_visible:
            reasons.append("System unexpectedly ACCEPTED the action (success indicator is visible)")

        if field not in visible_errors:
            reasons.append(f"Field '{field}' was NOT found in visible errors (found: {list(visible_errors.keys())})")
        elif message_contains not in (actual_field_msg or ""):
            reasons.append(
                f"Field '{field}' error message '{actual_field_msg}' does not contain expected substring '{message_contains}'"
            )

        if reasons:
            details = [
                f"[BUSINESS ASSERTION FAILED] Action expected to be REJECTED at field '{field}'.",
                f"Context: {context}" if context else None,
                f"Failure Reasons: {'; '.join(reasons)}",
                f"Actual State: success_visible={success_visible}, visible_errors={visible_errors}",
            ]
            msg = " | ".join(d for d in details if d)
            raise BusinessAssertionError(msg)

    @classmethod
    def expect_bug_if_rejected(
        cls,
        snapshot: Union[Dict[str, Any], object],
        field: str = "",
        context: str = "",
    ) -> None:
        """
        Used for Bug-Hunting: Input is VALID according to business specifications.
        If system rejects the action, a true defect is present in the system!

        Args:
            snapshot: UI data snapshot.
            field: Target field suspected of improper validation (optional).
            context: Test execution context.

        Raises:
            BusinessAssertionError: Tagged with [BUG DETECTED] when rejected.
        """
        success_visible, visible_errors = cls._parse_snapshot(snapshot)

        is_rejected = not success_visible or (field and field in visible_errors) or len(visible_errors) > 0

        if is_rejected:
            details = [
                f"[BUG DETECTED] Valid business input was rejected by system!",
                f"Context: {context}" if context else None,
                f"Target Field: '{field}'" if field else None,
                f"Actual State: success_visible={success_visible}, visible_errors={visible_errors}",
            ]
            msg = " | ".join(d for d in details if d)
            raise BusinessAssertionError(msg)

    @classmethod
    def expect_bug_if_accepted(
        cls,
        snapshot: Union[Dict[str, Any], object],
        context: str = "",
    ) -> None:
        """
        Used for Bug-Hunting: Input is INVALID according to business specifications.
        If system accepts the submission, a validation bypass defect is detected!

        Args:
            snapshot: UI data snapshot.
            context: Test execution context.

        Raises:
            BusinessAssertionError: Tagged with [BUG DETECTED] when improperly accepted.
        """
        success_visible, visible_errors = cls._parse_snapshot(snapshot)

        if success_visible:
            details = [
                f"[BUG DETECTED] Invalid business input was ACCEPTED by system (Validation Bypass)!",
                f"Context: {context}" if context else None,
                f"Actual State: success_visible={success_visible}, visible_errors={visible_errors}",
            ]
            msg = " | ".join(d for d in details if d)
            raise BusinessAssertionError(msg)
