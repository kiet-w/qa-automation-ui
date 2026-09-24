"""
core/exceptions.py - Custom Exception definitions for Enterprise UI Automation Framework.

Includes:
- BusinessAssertionError: Used for business/UI assertion failures (inherits from AssertionError).
- InfrastructureError: Used for technical/infrastructure issues during Playwright execution (inherits from Exception).
"""
from typing import Optional


class BusinessAssertionError(AssertionError):
    """
    Raised when a business expectation or functional assertion is violated.
    Inherits from AssertionError so Pytest recognizes it as a standard assertion failure.
    """
    pass


class InfrastructureError(Exception):
    """
    Raised when an underlying infrastructure/technical error occurs during Playwright execution.
    Inherits from Exception (NOT AssertionError) to clearly differentiate technical failures
    from business/functional bugs.

    Attributes:
        category (str): Error category (TIMEOUT, BROWSER_CRASH, STALE_ELEMENT, NETWORK, UNKNOWN).
        action_name (str): Action name being executed when the error occurred.
        original_exception (Optional[Exception]): Root cause exception from Playwright/Python.
        context (str): Test execution context.
        hint (str): Troubleshooting hint provided by Error Catalog.
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

        # Construct informative error message with [INFRA ERROR:<category>] prefix
        msg_parts = [f"[INFRA ERROR:{category}] Failed during action '{action_name}'"]
        if context:
            msg_parts.append(f"Context: {context}")
        if original_exception:
            msg_parts.append(f"Original Error: ({type(original_exception).__name__}) {original_exception}")
        if hint:
            msg_parts.append(f"Hint: {hint}")

        super().__init__(" | ".join(msg_parts))
