"""
tests/unit/test_exceptor.py - Unit tests kiểm tra toàn bộ logic của Exceptor.
"""
import pytest
from core.exceptor import Exceptor
from core.exceptions import BusinessAssertionError


class MockSnapshotObj:
    """Mock object đại diện cho snapshot dưới dạng class instance."""

    def __init__(self, success_visible: bool, visible_errors: dict):
        self.success_visible = success_visible
        self.visible_errors = visible_errors


def test_expect_success_pass():
    """Kiểm tra expect_success vượt qua khi success_visible=True và không có lỗi."""
    snapshot = {"success_visible": True, "visible_errors": {}}
    # Không raise exception
    Exceptor.expect_success(snapshot, context="Testing happy path submit")


def test_expect_success_fail_when_success_false():
    """Kiểm tra expect_success raise BusinessAssertionError khi success_visible=False."""
    snapshot = {"success_visible": False, "visible_errors": {}}
    with pytest.raises(BusinessAssertionError) as exc_info:
        Exceptor.expect_success(snapshot, context="Testing happy path fail")

    msg = str(exc_info.value)
    assert "[BUSINESS ASSERTION FAILED]" in msg
    assert "Expected: success_visible=True" in msg
    assert "actual_state: success_visible=False" in msg.lower() or "success_visible=false" in msg.lower()


def test_expect_success_fail_when_errors_exist():
    """Kiểm tra expect_success raise BusinessAssertionError khi có lỗi hiển thị."""
    snapshot = {"success_visible": True, "visible_errors": {"email": "Email format invalid"}}
    with pytest.raises(BusinessAssertionError) as exc_info:
        Exceptor.expect_success(snapshot, context="Submit with hidden error")

    assert "Email format invalid" in str(exc_info.value)


def test_expect_rejection_pass():
    """Kiểm tra expect_rejection pass khi success_visible=False và thông điệp lỗi khớp."""
    snapshot = {
        "success_visible": False,
        "visible_errors": {"code": "Mã khóa học không được để trống"},
    }
    Exceptor.expect_rejection(
        snapshot,
        field="code",
        message_contains="không được để trống",
        context="Unhappy path empty code",
    )


def test_expect_rejection_fail_when_success_true():
    """Kiểm tra expect_rejection fail khi hệ thống lỡ chấp nhận input sai."""
    snapshot = {"success_visible": True, "visible_errors": {}}
    with pytest.raises(BusinessAssertionError) as exc_info:
        Exceptor.expect_rejection(
            snapshot,
            field="code",
            message_contains="không được để trống",
            context="Testing invalid input accepted",
        )

    msg = str(exc_info.value)
    assert "unexpectedly ACCEPTED" in msg or "accepted" in msg.lower()


def test_expect_rejection_fail_when_field_missing():
    """Kiểm tra expect_rejection fail khi lỗi báo sai trường."""
    snapshot = {
        "success_visible": False,
        "visible_errors": {"name": "Tên quá ngắn"},
    }
    with pytest.raises(BusinessAssertionError) as exc_info:
        Exceptor.expect_rejection(
            snapshot,
            field="code",
            message_contains="không được để trống",
        )

    assert "Field 'code' was NOT found in visible errors" in str(exc_info.value)


def test_expect_rejection_fail_when_message_mismatch():
    """Kiểm tra expect_rejection fail khi nội dung thông điệp lỗi không khớp."""
    snapshot = {
        "success_visible": False,
        "visible_errors": {"code": "Mã khóa học đã tồn tại"},
    }
    with pytest.raises(BusinessAssertionError) as exc_info:
        Exceptor.expect_rejection(
            snapshot,
            field="code",
            message_contains="không được để trống",
        )

    assert "does not contain expected substring 'không được để trống'" in str(exc_info.value)


def test_expect_bug_if_rejected_pass():
    """Kiểm tra expect_bug_if_rejected pass khi hành động thành công đúng như thực tế nghiệp vụ."""
    snapshot = {"success_visible": True, "visible_errors": {}}
    Exceptor.expect_bug_if_rejected(snapshot, field="phone", context="Valid international phone number")


def test_expect_bug_if_rejected_raises_bug_detected():
    """Kiểm tra expect_bug_if_rejected raise lỗi [BUG DETECTED] khi input đúng lại bị từ chối."""
    snapshot = {
        "success_visible": False,
        "visible_errors": {"phone": "Số điện thoại không hợp lệ"},
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
    """Kiểm tra expect_bug_if_accepted pass khi input sai bị hệ thống từ chối chuẩn."""
    snapshot = {
        "success_visible": False,
        "visible_errors": {"email": "Invalid email"},
    }
    Exceptor.expect_bug_if_accepted(snapshot, context="Testing SQL injection payload")


def test_expect_bug_if_accepted_raises_bug_detected():
    """Kiểm tra expect_bug_if_accepted raise lỗi [BUG DETECTED] khi input sai lại được hệ thống chấp nhận."""
    snapshot = {"success_visible": True, "visible_errors": {}}
    with pytest.raises(BusinessAssertionError) as exc_info:
        Exceptor.expect_bug_if_accepted(snapshot, context="Testing XSS payload accepted")

    msg = str(exc_info.value)
    assert "[BUG DETECTED]" in msg
    assert "Validation Bypass" in msg


def test_expect_success_with_object_snapshot():
    """Kiểm tra Exceptor hỗ trợ snapshot dạng Object class bên cạnh dict."""
    snapshot_obj = MockSnapshotObj(success_visible=True, visible_errors={})
    Exceptor.expect_success(snapshot_obj, context="Object snapshot test")

    snapshot_fail_obj = MockSnapshotObj(
        success_visible=False,
        visible_errors={"code": "Lỗi hệ thống"},
    )
    with pytest.raises(BusinessAssertionError):
        Exceptor.expect_success(snapshot_fail_obj)
