"""
core/exceptor.py - Gatekeeper duy nhất đánh giá kỳ vọng nghiệp vụ / UI (Business Assertion Gate).

Tách biệt hoàn toàn việc thu thập dữ liệu (Page Object) và đánh giá đúng/sai (Exceptor).
Chỉ làm việc trên `snapshot` dữ liệu thu thập sẵn, không tự gọi lại Playwright.

Cung cấp các phương thức theo đúng ý định kiểm thử (Intent-driven assertion methods):
- expect_success: Kỳ vọng thao tác thành công (Happy path).
- expect_rejection: Kỳ vọng bị từ chối đúng field và thông điệp lỗi (Unhappy path).
- expect_bug_if_rejected: Kỳ vọng thành công, nếu bị từ chối thì báo [BUG DETECTED].
- expect_bug_if_accepted: Kỳ vọng bị từ chối, nếu lại thành công thì báo [BUG DETECTED].
"""
from typing import Any, Dict, Union, Tuple, Optional
from core.exceptions import BusinessAssertionError


class Exceptor:
    """
    Cửa khẩu duy nhất quyết định pass/fail về mặt nghiệp vụ.
    Nhận snapshot trạng thái UI và kiểm tra theo các phương thức kỳ vọng.
    """

    @staticmethod
    def _parse_snapshot(snapshot: Union[Dict[str, Any], object]) -> Tuple[bool, Dict[str, str]]:
        """
        Helper trích xuất thông tin từ snapshot (hỗ trợ cả Dict và Object).
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
        Kỳ vọng: Thao tác phải THÀNH CÔNG (Happy path).
        Kiểm tra: success_visible = True, và không có thông điệp lỗi nào hiển thị trên form.

        Args:
            snapshot: Snapshot dữ liệu UI ({ "success_visible": bool, "visible_errors": dict })
            context: Ngữ cảnh của test case / bước kiểm thử.

        Raises:
            BusinessAssertionError: Khi thao tác không thành công hoặc tồn tại lỗi trên UI.
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
        Kỳ vọng: Thao tác phải BỊ TỪ CHỐI (Unhappy path — input sai, hệ thống phải chặn đúng).
        Kiểm tra: success_visible = False, lỗi hiển thị đúng tại `field`, và nội dung chứa `message_contains`.

        Args:
            snapshot: Snapshot dữ liệu UI ({ "success_visible": bool, "visible_errors": dict })
            field: ID / tên trường dữ liệu kỳ vọng bị báo lỗi.
            message_contains: Chuỗi con kỳ vọng xuất hiện trong thông điệp lỗi của field.
            context: Ngữ cảnh kiểm thử.

        Raises:
            BusinessAssertionError: Khi thao tác lại thành công, hoặc sai field lỗi, hoặc nội dung lỗi không khớp.
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
        Dùng cho Bug-Hunting: Input này ĐÚNG theo thực tế nghiệp vụ.
        Nếu hệ thống lại từ chối (rejection), đó chính là BUG THẬT của hệ thống!

        Args:
            snapshot: Snapshot dữ liệu UI.
            field: Tên trường dự đoán bị hệ thống báo lỗi nhầm (nếu có).
            context: Ngữ cảnh kiểm thử.

        Raises:
            BusinessAssertionError: Gắn nhãn [BUG DETECTED] khi bị từ chối.
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
        Dùng cho Bug-Hunting: Input này SAI theo thực tế nghiệp vụ.
        Nếu hệ thống lại chấp nhận (submit thành công), đó là lỗ hổng validation (BUG THẬT)!

        Args:
            snapshot: Snapshot dữ liệu UI.
            context: Ngữ cảnh kiểm thử.

        Raises:
            BusinessAssertionError: Gắn nhãn [BUG DETECTED] khi hệ thống lỡ chấp nhận.
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
