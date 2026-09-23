"""
example_usage.py - Ví dụ minh họa cách sử dụng module Exceptor và Interceptor.

File này hướng dẫn cách gọi 2 module độc lập trong test case mà không can thiệp
vào cấu trúc test case cũ.
"""
from core import Exceptor, Interceptor, BusinessAssertionError, InfrastructureError


def simulate_save_form_success():
    """Giả lập một hành động lưu form thành công."""
    print("Executing Playwright action: save_form()...")
    return {"status": "ok"}


def simulate_save_form_timeout():
    """Giả lập một hành động Playwright bị Timeout."""
    print("Executing Playwright action: save_form() -> Timeout!")
    raise Exception("Timeout 10000ms exceeded while waiting for selector '#save-btn'")


def mock_collect_snapshot(success: bool, errors: dict = None):
    """
    Giả lập việc thu thập snapshot trạng thái UI từ Page Object.
    (Trách nhiệm thu thập là của Page Object, Exceptor chỉ nhận snapshot đã thu thập).
    """
    return {
        "success_visible": success,
        "visible_errors": errors or {},
    }


def demo_happy_path():
    print("\n--- 1. DEMO HAPPY PATH (Thao tác thành công & Kiểm tra kỳ vọng) ---")

    # 1. Bọc hành động Playwright bằng Interceptor
    Interceptor.run(
        simulate_save_form_success,
        action_name="click_save_curricula",
        context="Lưu thông tin chương trình đào tạo",
    )

    # 2. Thu thập snapshot trạng thái trang từ Page Object
    snapshot = mock_collect_snapshot(success=True)

    # 3. Đánh giá kỳ vọng nghiệp vụ thông qua Exceptor
    Exceptor.expect_success(snapshot, context="Lưu chương trình đào tạo hợp lệ")
    print("=> RESULT: PASS (Happy path thành công đúng kỳ vọng!)")


def demo_unhappy_path():
    print("\n--- 2. DEMO UNHAPPY PATH (Kỳ vọng hệ thống chặn đúng input sai) ---")

    snapshot = mock_collect_snapshot(
        success=False,
        errors={"course_code": "Mã khóa học không được để trống"},
    )

    Exceptor.expect_rejection(
        snapshot,
        field="course_code",
        message_contains="không được để trống",
        context="Để trống trường Mã khóa học",
    )
    print("=> RESULT: PASS (Hệ thống đã chặn đúng lỗi nghiệp vụ!)")


def demo_bug_hunting():
    print("\n--- 3. DEMO BUG HUNTING (Phát hiện lỗi nghiệp vụ thật) ---")

    # Giả lập trường hợp: Input đúng thực tế nghiệp vụ nhưng hệ thống lại báo lỗi
    snapshot_rejected = mock_collect_snapshot(
        success=False,
        errors={"phone": "Số điện thoại không đúng định dạng 10 số"},
    )

    try:
        Exceptor.expect_bug_if_rejected(
            snapshot_rejected,
            field="phone",
            context="Nhập số điện thoại quốc tế hợp lệ +84912345678",
        )
    except BusinessAssertionError as e:
        print(f"=> CAUGHT EXPECTED BUSINESS BUG:\n   {e}")


def demo_infrastructure_error():
    print("\n--- 4. DEMO INFRASTRUCTURE ERROR (Bắt và phân loại lỗi kỹ thuật) ---")

    try:
        Interceptor.run(
            simulate_save_form_timeout,
            action_name="save_curricula",
            context="Kiểm thử timeout nút Save",
        )
    except InfrastructureError as e:
        print(f"=> CAUGHT CLASSIFIED INFRASTRUCTURE ERROR:\n   Category: {e.category}\n   Message: {e}")


if __name__ == "__main__":
    print("==========================================================")
    print("  HƯỚNG DẪN SỬ DỤNG MODULE EXCEPTOR & INTERCEPTOR")
    print("==========================================================")
    demo_happy_path()
    demo_unhappy_path()
    demo_bug_hunting()
    demo_infrastructure_error()
    print("\n==========================================================")
    print("  HOÀN THÀNH TẤT CẢ CÁC VÍ DỤ MINH HỌA!")
    print("==========================================================")
