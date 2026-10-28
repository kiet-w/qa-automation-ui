"""
core/interceptor.py - Infrastructure Interceptor for Playwright Actions.

Explicitly wraps individual Playwright actions (click, fill, navigate, save, etc.).
Catches technical infrastructure errors (Timeout, Browser crash, Stale DOM, Network disconnect),
classifies them using the Error Catalog, and raises InfrastructureError with actionable diagnostics.

Preserves the original root cause exception (`original_exception`) for transparent debugging.
"""
from typing import Callable, Any, Optional
from core.catalog import classify
from core.exceptions import InfrastructureError


class Interceptor:
    """
    Interceptor wrapping Playwright interactions (now simplified pass-through).
    Centralized error classification is handled in pytest hooks (pytest_runtest_makereport).
    """

    @classmethod
    def run(
        cls,
        action_fn: Callable[[], Any],
        *,
        action_name: str = "action",
        context: str = "",
        retry: int = 0,
    ) -> Any:
        """
        Execute an action_fn. Classifies errors as InfrastructureError if an exception occurs.
        Maintained for backward compatibility. In modern tests, call actions directly.
        """
        try:
            return action_fn()
        except InfrastructureError:
            raise
        except Exception as exc:
            category, hint = classify(exc)
            raise InfrastructureError(
                category=category,
                action_name=action_name,
                original_exception=exc,
                context=context,
                hint=hint,
            ) from exc
