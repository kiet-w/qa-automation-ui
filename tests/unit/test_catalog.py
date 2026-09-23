"""
tests/unit/test_catalog.py - Unit tests cho Error Catalog phân loại lỗi hạ tầng.
"""
from core.catalog import classify, ERROR_RULES, ErrorRule, UNKNOWN_CATEGORY


class CustomTimeoutError(Exception):
    """Exception giả lập TimeoutError."""
    pass


# Đặt tên class là TimeoutError để test nhận diện tên class
class TimeoutError(Exception):
    pass


def test_classify_timeout_by_class_name():
    """Phân loại TIMEOUT dựa theo tên class TimeoutError."""
    exc = TimeoutError("Page navigation timed out after 30000ms")
    category, hint = classify(exc)
    assert category == "TIMEOUT"
    assert "selector" in hint.lower() or "timeout" in hint.lower()


def test_classify_timeout_by_message_pattern():
    """Phân loại TIMEOUT dựa theo regex message."""
    exc = Exception("Timeout 10000ms exceeded while waiting for selector '#submit'")
    category, hint = classify(exc)
    assert category == "TIMEOUT"


def test_classify_browser_crash():
    """Phân loại BROWSER_CRASH khi trình duyệt bị đóng."""
    exc1 = Exception("Target closed")
    cat1, _ = classify(exc1)
    assert cat1 == "BROWSER_CRASH"

    exc2 = Exception("Target page, context or browser has been closed")
    cat2, _ = classify(exc2)
    assert cat2 == "BROWSER_CRASH"


def test_classify_stale_element():
    """Phân loại STALE_ELEMENT khi phần tử bị gỡ khỏi DOM."""
    exc = Exception("Element is not attached to the DOM")
    cat, hint = classify(exc)
    assert cat == "STALE_ELEMENT"
    assert "DOM" in hint


def test_classify_network_error():
    """Phân loại NETWORK khi có lỗi kết nối mạng net::ERR_."""
    exc = Exception("net::ERR_NAME_NOT_RESOLVED at https://example.invalid")
    cat, hint = classify(exc)
    assert cat == "NETWORK"
    assert "mạng" in hint.lower() or "kết nối" in hint.lower()


def test_classify_unknown_error():
    """Ngoại lệ không khớp rule nào trả về UNKNOWN."""
    exc = ValueError("Invalid data format in test runner")
    cat, hint = classify(exc)
    assert cat == UNKNOWN_CATEGORY
    assert "chưa được phân loại" in hint


def test_catalog_extensibility():
    """Kiểm tra tính dễ mở rộng của Error Catalog bằng cách thêm 1 quy tắc mới."""
    new_rule = ErrorRule(
        category="DATABASE_LOCKED",
        hint="Cơ sở dữ liệu bị khóa tạm thời.",
        message_pattern=r"sqlite3\.OperationalError: database is locked",
    )
    ERROR_RULES.append(new_rule)

    try:
        exc = Exception("sqlite3.OperationalError: database is locked")
        cat, hint = classify(exc)
        assert cat == "DATABASE_LOCKED"
        assert "Cơ sở dữ liệu" in hint
    finally:
        ERROR_RULES.remove(new_rule)
