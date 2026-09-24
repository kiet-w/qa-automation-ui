"""
core/catalog.py - Infrastructure Error Catalog and Classification Engine.

Provides an extensible registry of error matching rules (`ERROR_RULES`) and the `classify(exc)` function
to automatically map Playwright and environment exceptions to standardized categories and diagnostic hints.
"""
import re
from typing import NamedTuple, List, Optional, Tuple, Type


class ErrorRule(NamedTuple):
    """
    Data structure representing a single error classification rule.

    Attributes:
        category (str): Error category identifier (e.g. TIMEOUT, BROWSER_CRASH, STALE_ELEMENT, NETWORK).
        hint (str): Concise diagnostic and troubleshooting hint.
        exception_types (Optional[Tuple[Type[Exception], ...]]): Specific exception classes to match directly.
        message_pattern (Optional[str]): Regex pattern matching exception message text.
    """
    category: str
    hint: str
    exception_types: Optional[Tuple[Type[Exception], ...]] = None
    message_pattern: Optional[str] = None


# Attempt to import Playwright TimeoutError if installed
try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
    PLAYWRIGHT_TIMEOUT_TYPES = (PlaywrightTimeoutError, TimeoutError)
except ImportError:
    PLAYWRIGHT_TIMEOUT_TYPES = (TimeoutError,)


# Registry of infrastructure error rules
# Add new rules to this list to extend framework error classification
ERROR_RULES: List[ErrorRule] = [
    ErrorRule(
        category="TIMEOUT",
        hint="Element did not appear/become ready in time; check selector or increase timeout.",
        exception_types=PLAYWRIGHT_TIMEOUT_TYPES,
        message_pattern=r"(?i)Timeout \d+ms exceeded|timed out",
    ),
    ErrorRule(
        category="BROWSER_CRASH",
        hint="Browser or target page closed unexpectedly during execution.",
        message_pattern=r"(?i)Target closed|Target page, context or browser has been closed|Browser closed",
    ),
    ErrorRule(
        category="STALE_ELEMENT",
        hint="DOM changed (re-rendered); locator reference is detached from the DOM.",
        message_pattern=r"(?i)Element is not attached to the DOM|stale element reference|is detached from the DOM",
    ),
    ErrorRule(
        category="NETWORK",
        hint="Network connection failure occurred while requesting resource.",
        message_pattern=r"(?i)net::ERR_|NS_ERROR_CONNECTION_REFUSED",
    ),
]

UNKNOWN_CATEGORY = "UNKNOWN"
UNKNOWN_HINT = "Unclassified infrastructure error — add to catalog once root cause is diagnosed."


def classify(exception: Exception) -> Tuple[str, str]:
    """
    Classify an infrastructure exception based on the ERROR_RULES catalog.

    Args:
        exception (Exception): Exception encountered during test execution.

    Returns:
        Tuple[str, str]: (category, hint). Returns ("UNKNOWN", UNKNOWN_HINT) if no rules match.
    """
    exc_type_name = type(exception).__name__
    exc_msg = str(exception)

    for rule in ERROR_RULES:
        # Check by exception class type
        if rule.exception_types and isinstance(exception, rule.exception_types):
            return rule.category, rule.hint

        # Check by exception class name (e.g. "TimeoutError")
        if rule.exception_types:
            for t in rule.exception_types:
                if exc_type_name == t.__name__:
                    return rule.category, rule.hint

        # Check by regex pattern matching message
        if rule.message_pattern and re.search(rule.message_pattern, exc_msg):
            return rule.category, rule.hint

    return UNKNOWN_CATEGORY, UNKNOWN_HINT
