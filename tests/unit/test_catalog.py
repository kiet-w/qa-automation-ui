"""
tests/unit/test_catalog.py - Unit tests for infrastructure Error Catalog and classification.
"""
from core.catalog import classify, ERROR_RULES, ErrorRule, UNKNOWN_CATEGORY


class CustomTimeoutError(Exception):
    """Simulated TimeoutError exception."""
    pass


class TimeoutError(Exception):
    pass


def test_classify_timeout_by_class_name():
    """Classify TIMEOUT based on TimeoutError class name."""
    exc = TimeoutError("Page navigation timed out after 30000ms")
    category, hint = classify(exc)
    assert category == "TIMEOUT"
    assert "selector" in hint.lower() or "timeout" in hint.lower()


def test_classify_timeout_by_message_pattern():
    """Classify TIMEOUT based on regex message pattern."""
    exc = Exception("Timeout 10000ms exceeded while waiting for selector '#submit'")
    category, hint = classify(exc)
    assert category == "TIMEOUT"


def test_classify_browser_crash():
    """Classify BROWSER_CRASH when browser closes unexpectedly."""
    exc1 = Exception("Target closed")
    cat1, _ = classify(exc1)
    assert cat1 == "BROWSER_CRASH"

    exc2 = Exception("Target page, context or browser has been closed")
    cat2, _ = classify(exc2)
    assert cat2 == "BROWSER_CRASH"


def test_classify_stale_element():
    """Classify STALE_ELEMENT when element is detached from DOM."""
    exc = Exception("Element is not attached to the DOM")
    cat, hint = classify(exc)
    assert cat == "STALE_ELEMENT"
    assert "DOM" in hint


def test_classify_network_error():
    """Classify NETWORK when connection error net::ERR_ occurs."""
    exc = Exception("net::ERR_NAME_NOT_RESOLVED at https://example.invalid")
    cat, hint = classify(exc)
    assert cat == "NETWORK"
    assert "network" in hint.lower() or "connection" in hint.lower()


def test_classify_unknown_error():
    """Unhandled exceptions default to UNKNOWN category."""
    exc = ValueError("Invalid data format in test runner")
    cat, hint = classify(exc)
    assert cat == UNKNOWN_CATEGORY
    assert "unclassified" in hint.lower()


def test_catalog_extensibility():
    """Verify extensibility of Error Catalog by registering a dynamic rule."""
    new_rule = ErrorRule(
        category="DATABASE_LOCKED",
        hint="Database is temporarily locked.",
        message_pattern=r"sqlite3\.OperationalError: database is locked",
    )
    ERROR_RULES.append(new_rule)

    try:
        exc = Exception("sqlite3.OperationalError: database is locked")
        cat, hint = classify(exc)
        assert cat == "DATABASE_LOCKED"
        assert "database" in hint.lower()
    finally:
        ERROR_RULES.remove(new_rule)
