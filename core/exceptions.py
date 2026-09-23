"""
core/exceptions.py - Định nghĩa các Exception tùy chỉnh cho framework QA Automation UI.

Bao gồm:
- BusinessAssertionError: Dùng cho các lỗi vi phạm kỳ vọng nghiệp vụ / UI (kế thừa AssertionError).
- InfrastructureError: Dùng cho các lỗi kỹ thuật / hạ tầng Playwright & tiến trình (kế thừa Exception).
"""
from typing import Optional


class BusinessAssertionError(AssertionError):
    """
    Ngoại lệ raise khi kỳ vọng nghiệp vụ (Business Expectation) không thỏa mãn.
    Kế thừa từ AssertionError để Pytest nhận diện là test assertion failure chuẩn.
    """
    pass


class InfrastructureError(Exception):
    """
    Ngoại lệ raise khi gặp lỗi hạ tầng / kỹ thuật Playwright trong quá trình thực thi.
    Kế thừa từ Exception (KHÔNG kế thừa AssertionError) để phân biệt rõ ràng với lỗi nghiệp vụ.

    Attributes:
        category (str): Phân loại lỗi (TIMEOUT, BROWSER_CRASH, STALE_ELEMENT, NETWORK, UNKNOWN).
        action_name (str): Tên thao tác/hành động đang thực hiện khi gặp lỗi.
        original_exception (Optional[Exception]): Exception gốc từ Playwright/Python để hỗ trợ debug.
        context (str): Ngữ cảnh thực thi.
        hint (str): Gợi ý khắc phục/debug từ Error Catalog.
    """

    def __init__(
        self,
        category: str,
        action_name: str,
        original_exception: Optional[Exception] = None,
        context: str = "",
        hint: str = "",
    ):
        self.category = category
        self.action_name = action_name
        self.original_exception = original_exception
        self.context = context
        self.hint = hint

        # Xây dựng thông điệp lỗi rõ ràng có tiền tố [INFRA ERROR:<category>]
        msg_parts = [f"[INFRA ERROR:{category}] Failed during action '{action_name}'"]
        if context:
            msg_parts.append(f"Context: {context}")
        if original_exception:
            msg_parts.append(f"Original Error: ({type(original_exception).__name__}) {original_exception}")
        if hint:
            msg_parts.append(f"Hint: {hint}")

        super().__init__(" | ".join(msg_parts))
