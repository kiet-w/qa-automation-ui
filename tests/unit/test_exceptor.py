"""
tests/unit/test_exceptor.py - Comprehensive Unit tests for Exceptor assertion gate.
"""
import pytest
from core.exceptor import Exceptor
from core.exceptions import BusinessAssertionError


class MockSnapshotObj:
    """Mock object representing UI snapshot as an object instance."""

    def __init__(self, success_visible: bool, visible_errors: dict):
        self.success_visible = success_visible
        self.visible_errors = visible_errors


def test_expect_success_pass():
    """Verify expect_success passes when success_visible=True and no errors."""
    snapshot = {"success_visible": True, "visible_errors": {}}
    Exceptor.expect_success(snapshot, context="Testing happy path submit")


def test_expect_success_fail_when_success_false():
    """Verify expect_success raises BusinessAssertionError when success_visible=False."""
    snapshot = {"success_visible": False, "visible_errors": {}}
    with pytest.raises(BusinessAssertionError) as exc_info:
        Exceptor.expect_success(snapshot, context="Testing happy path fail")

    msg = str(exc_info.value)
    assert "[BUSINESS ASSERTION FAILED]" in msg
    assert "Expected: success_visible=True" in msg
    assert "actual: success_visible=false" in msg.lower()


def test_expect_success_fail_when_errors_exist():
    """Verify expect_success raises BusinessAssertionError when errors exist."""
    snapshot = {"success_visible": True, "visible_errors": {"email": "Email format invalid"}}
    with pytest.raises(BusinessAssertionError) as exc_info:
        Exceptor.expect_success(snapshot, context="Submit with hidden error")

    assert "Email format invalid" in str(exc_info.value)


def test_expect_rejection_pass():
    """Verify expect_rejection passes when success_visible=False and error message matches."""
    snapshot = {
        "success_visible": False,
        "visible_errors": {"code": "Course code cannot be blank"},
    }
    Exceptor.expect_rejection(
        snapshot,
        field="code",
        message_contains="cannot be blank",
        context="Unhappy path empty code",
    )


def test_expect_rejection_fail_when_success_true():
    """Verify expect_rejection fails when system unexpectedly accepts invalid input."""
    snapshot = {"success_visible": True, "visible_errors": {}}
    with pytest.raises(BusinessAssertionError) as exc_info:
        Exceptor.expect_rejection(
            snapshot,
            field="code",
            message_contains="cannot be blank",
            context="Testing invalid input accepted",
        )

    msg = str(exc_info.value)
    assert "unexpectedly ACCEPTED" in msg or "accepted" in msg.lower()


def test_expect_rejection_fail_when_field_missing():
    """Verify expect_rejection fails when expected field error is missing."""
    snapshot = {
        "success_visible": False,
        "visible_errors": {"name": "Name is too short"},
    }
    with pytest.raises(BusinessAssertionError) as exc_info:
        Exceptor.expect_rejection(
            snapshot,
            field="code",
            message_contains="cannot be blank",
        )

    assert "Field 'code' was NOT found in visible errors" in str(exc_info.value)


def test_expect_rejection_fail_when_message_mismatch():
    """Verify expect_rejection fails when error message text does not match."""
    snapshot = {
        "success_visible": False,
        "visible_errors": {"code": "Course code already exists"},
    }
    with pytest.raises(BusinessAssertionError) as exc_info:
        Exceptor.expect_rejection(
            snapshot,
            field="code",
            message_contains="cannot be blank",
        )

    assert "does not contain expected substring 'cannot be blank'" in str(exc_info.value)


def test_expect_bug_if_rejected_pass():
    """Verify expect_bug_if_rejected passes when action succeeds as expected."""
    snapshot = {"success_visible": True, "visible_errors": {}}
    Exceptor.expect_bug_if_rejected(snapshot, field="phone", context="Valid international phone number")


def test_expect_bug_if_rejected_raises_bug_detected():
    """Verify expect_bug_if_rejected raises [BUG DETECTED] when valid input is rejected."""
    snapshot = {
        "success_visible": False,
        "visible_errors": {"phone": "Invalid phone number"},
    }
    with pytest.raises(BusinessAssertionError) as exc_info:
        Exceptor.expect_bug_if_rejected(
            snapshot,
            field="phone",
            context="Valid international phone number rejected",
        )

    msg = str(exc_info.value)
    assert "[BUG DETECTED]" in msg
    assert "Valid business input was rejected" in msg


def test_expect_bug_if_accepted_pass():
    """Verify expect_bug_if_accepted passes when invalid input is properly rejected."""
    snapshot = {
        "success_visible": False,
        "visible_errors": {"email": "Invalid email"},
    }
    Exceptor.expect_bug_if_accepted(snapshot, context="Testing SQL injection payload")


def test_expect_bug_if_accepted_raises_bug_detected():
    """Verify expect_bug_if_accepted raises [BUG DETECTED] when invalid input is accepted."""
    snapshot = {"success_visible": True, "visible_errors": {}}
    with pytest.raises(BusinessAssertionError) as exc_info:
        Exceptor.expect_bug_if_accepted(snapshot, context="Testing XSS payload accepted")

    msg = str(exc_info.value)
    assert "[BUG DETECTED]" in msg
    assert "Validation Bypass" in msg


def test_expect_success_with_object_snapshot():
    """Verify Exceptor supports object-based snapshot instances."""
    snapshot_obj = MockSnapshotObj(success_visible=True, visible_errors={})
    Exceptor.expect_success(snapshot_obj, context="Object snapshot test")

    snapshot_fail_obj = MockSnapshotObj(
        success_visible=False,
        visible_errors={"code": "System error"},
    )
    with pytest.raises(BusinessAssertionError):
        Exceptor.expect_success(snapshot_fail_obj)
