"""
core/catalog.py - Danh mục lỗi hạ tầng & cơ chế phân loại (Error Catalog).

Cung cấp danh sách các quy tắc nhận diện lỗi Playwright / hạ tầng và hàm `classify(exc)`
để tự động gán category và gợi ý debug (hint).
Dễ dàng mở rộng bằng cách bổ sung thêm Rule vào danh sách `ERROR_RULES`.
"""
import re
from typing import NamedTuple, List, Optional, Tuple, Type


class ErrorRule(NamedTuple):
    """
    Cấu trúc đại diện cho 1 Quy tắc phân loại lỗi.

    Attributes:
        category (str): Tên phân loại lỗi (vd: TIMEOUT, BROWSER_CRASH, STALE_ELEMENT, NETWORK).
        hint (str): Gợi ý khắc phục/debug ngắn gọn.
        exception_types (Optional[Tuple[Type[Exception], ...]]): Các loại Exception class khớp trực tiếp.
        message_pattern (Optional[str]): Chuỗi regex khớp với nội dung thông điệp lỗi (message).
    """
    category: str
    hint: str
    exception_types: Optional[Tuple[Type[Exception], ...]] = None
    message_pattern: Optional[str] = None


# Thử import Playwright TimeoutError nếu môi trường có sẵn
try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
    PLAYWRIGHT_TIMEOUT_TYPES = (PlaywrightTimeoutError, TimeoutError)
except ImportError:
    PLAYWRIGHT_TIMEOUT_TYPES = (TimeoutError,)


# Danh mục các quy tắc phân loại lỗi hạ tầng (Error Catalog Registry)
# Bổ sung quy tắc mới chỉ cần thêm 1 nguyên tố ErrorRule vào danh sách này
ERROR_RULES: List[ErrorRule] = [
    ErrorRule(
        category="TIMEOUT",
        hint="Phần tử không xuất hiện/sẵn sàng kịp thời gian chờ; kiểm tra selector hoặc tăng timeout.",
        exception_types=PLAYWRIGHT_TIMEOUT_TYPES,
        message_pattern=r"(?i)Timeout \d+ms exceeded|timed out",
    ),
    ErrorRule(
        category="BROWSER_CRASH",
        hint="Trình duyệt/tab bị đóng đột ngột giữa lúc thao tác.",
        message_pattern=r"(?i)Target closed|Target page, context or browser has been closed|Browser closed",
    ),
    ErrorRule(
        category="STALE_ELEMENT",
        hint="DOM đã thay đổi (re-render), locator cũ không còn hợp lệ.",
        message_pattern=r"(?i)Element is not attached to the DOM|stale element reference|is detached from the DOM",
    ),
    ErrorRule(
        category="NETWORK",
        hint="Lỗi kết nối mạng khi tải trang/tài nguyên.",
        message_pattern=r"(?i)net::ERR_|NS_ERROR_CONNECTION_REFUSED",
    ),
]

UNKNOWN_CATEGORY = "UNKNOWN"
UNKNOWN_HINT = "Lỗi hạ tầng chưa được phân loại — cần bổ sung vào catalog sau khi xác định nguyên nhân."


def classify(exception: Exception) -> Tuple[str, str]:
    """
    Phân loại ngoại lệ hạ tầng dựa trên danh mục quy tắc ERROR_RULES.

    Args:
        exception (Exception): Exception nhận được từ quá trình thực thi Playwright.

    Returns:
        Tuple[str, str]: (category, hint) tương ứng. Nếu không khớp quy tắc nào sẽ trả về ("UNKNOWN", UNKNOWN_HINT).
    """
    exc_type_name = type(exception).__name__
    exc_msg = str(exception)

    for rule in ERROR_RULES:
        # Check by exception class type
        if rule.exception_types and isinstance(exception, rule.exception_types):
            return rule.category, rule.hint

        # Check by exception class name (vd: "TimeoutError")
        if rule.exception_types:
            for t in rule.exception_types:
                if exc_type_name == t.__name__:
                    return rule.category, rule.hint

        # Check by regex pattern matching message
        if rule.message_pattern and re.search(rule.message_pattern, exc_msg):
            return rule.category, rule.hint

    return UNKNOWN_CATEGORY, UNKNOWN_HINT
