"""
core/interceptor.py - Module bọc và bắt lỗi hạ tầng / tiến trình thực thi (Infrastructure Interceptor).

Bọc quanh một thao tác Playwright cụ thể (click, fill, navigate, save...) một cách tường minh.
Bắt các lỗi kỹ thuật (Timeout, Browser crash, Stale DOM, Network...), phân loại chúng
qua Error Catalog, và raise thành InfrastructureError kèm nhãn rõ ràng.

Đảm bảo không nuốt mất exception gốc (giữ lại original_exception để hỗ trợ debug).
"""
from typing import Callable, Any, Optional
from core.catalog import classify
from core.exceptions import InfrastructureError


class Interceptor:
    """
    Interceptor bọc các thao tác Playwright để quản lý lỗi kỹ thuật/hạ tầng.
    """

    @classmethod
    def run(
        cls,
        action_fn: Callable[[], Any],
        *,
        action_name: str,
        context: str = "",
        retry: int = 0,
    ) -> Any:
        """
        Thực thi một action_fn dưới sự giám sát của Interceptor.

        Args:
            action_fn: Callable không tham số chứa hành động Playwright (vd: lambda: page.click("button")).
            action_name: Tên gợi nhớ của hành động (vd: "submit_form", "click_save").
            context: Ngữ cảnh thực thi chi tiết.
            retry: Số lần thử lại tối đa khi gặp lỗi hạ tầng (mặc định 0 - chưa kích hoạt).

        Returns:
            Kết quả của action_fn() nếu thực thi thành công.

        Raises:
            InfrastructureError: Khi gặp lỗi hạ tầng/kỹ thuật Playwright.
        """
        # Lưu ý: Tham số retry dành cho mở rộng tương lai. Mặc định thực thi 1 lần.
        try:
            return action_fn()
        except InfrastructureError:
            # Nếu đã là InfrastructureError từ cấp thấp hơn thì ném tiếp ra ngoài
            raise
        except Exception as exc:
            # Phân loại lỗi thông qua Error Catalog
            category, hint = classify(exc)

            # Raise lại thành InfrastructureError, giữ vết exception gốc với 'from exc'
            raise InfrastructureError(
                category=category,
                action_name=action_name,
                original_exception=exc,
                context=context,
                hint=hint,
            ) from exc
