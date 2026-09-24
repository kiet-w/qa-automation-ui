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
    Interceptor wrapping Playwright interactions to monitor and standardize infrastructure errors.
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
        Execute an action_fn under Interceptor surveillance.

        Args:
            action_fn: Zero-argument callable containing Playwright action (e.g. lambda: page.click("button")).
            action_name: Human-readable action name (e.g. "submit_form", "click_save").
            context: Detailed execution context.
            retry: Maximum retry attempts for transient infrastructure errors (default: 0).

        Returns:
            Result of action_fn() upon successful execution.

        Raises:
            InfrastructureError: When a Playwright/infrastructure technical error occurs.
        """
        # Note: retry parameter reserved for future exponential backoff extension.
        try:
            return action_fn()
        except InfrastructureError:
            # Re-raise existing InfrastructureError from lower layers directly
            raise
        except Exception as exc:
            # Classify error through the Error Catalog
            category, hint = classify(exc)

            # Re-raise as standardized InfrastructureError, preserving stack trace via 'from exc'
            raise InfrastructureError(
                category=category,
                action_name=action_name,
                original_exception=exc,
                context=context,
                hint=hint,
            ) from exc
