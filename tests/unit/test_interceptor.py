"""
tests/unit/test_interceptor.py - Comprehensive Unit tests for Interceptor module.
"""
import pytest
from core.interceptor import Interceptor
from core.exceptions import InfrastructureError


def test_interceptor_run_success():
    """Interceptor executes normal actions successfully and returns result."""
    result = Interceptor.run(
        lambda: "success_result",
        action_name="navigate_home",
        context="Opening homepage",
    )
    assert result == "success_result"


def test_interceptor_catches_timeout_and_raises_infrastructure_error():
    """Interceptor catches timeout and raises InfrastructureError with TIMEOUT category."""
    def raise_timeout():
        raise Exception("Timeout 10000ms exceeded while waiting for selector '#btn'")

    with pytest.raises(InfrastructureError) as exc_info:
        Interceptor.run(
            raise_timeout,
            action_name="click_submit",
            context="Submitting form in US01",
        )

    infra_err = exc_info.value
    assert isinstance(infra_err, Exception)
    assert not isinstance(infra_err, AssertionError)  # Decoupled from business assertion failures
    assert infra_err.category == "TIMEOUT"
    assert infra_err.action_name == "click_submit"
    assert infra_err.context == "Submitting form in US01"
    assert isinstance(infra_err.original_exception, Exception)
    assert "[INFRA ERROR:TIMEOUT]" in str(infra_err)


def test_interceptor_catches_browser_crash():
    """Interceptor catches target closed error and raises BROWSER_CRASH."""
    def raise_crash():
        raise Exception("Target page, context or browser has been closed")

    with pytest.raises(InfrastructureError) as exc_info:
        Interceptor.run(
            raise_crash,
            action_name="upload_avatar",
        )

    assert exc_info.value.category == "BROWSER_CRASH"
    assert "[INFRA ERROR:BROWSER_CRASH]" in str(exc_info.value)


def test_interceptor_catches_stale_element():
    """Interceptor catches detached/stale DOM element error."""
    def raise_stale():
        raise Exception("Element is not attached to the DOM")

    with pytest.raises(InfrastructureError) as exc_info:
        Interceptor.run(
            raise_stale,
            action_name="read_table_row",
        )

    assert exc_info.value.category == "STALE_ELEMENT"


def test_interceptor_catches_network_error():
    """Interceptor catches network connection errors."""
    def raise_net_err():
        raise Exception("net::ERR_CONNECTION_REFUSED")

    with pytest.raises(InfrastructureError) as exc_info:
        Interceptor.run(
            raise_net_err,
            action_name="fetch_api_data",
        )

    assert exc_info.value.category == "NETWORK"


def test_interceptor_catches_unknown_error():
    """Interceptor classifies unhandled errors as UNKNOWN."""
    def raise_unknown():
        raise RuntimeError("Unexpected internal engine error")

    with pytest.raises(InfrastructureError) as exc_info:
        Interceptor.run(
            raise_unknown,
            action_name="custom_script",
        )

    assert exc_info.value.category == "UNKNOWN"
    assert "[INFRA ERROR:UNKNOWN]" in str(exc_info.value)


def test_interceptor_re_raises_existing_infrastructure_error():
    """Interceptor does not double-wrap an existing InfrastructureError."""
    original_infra = InfrastructureError(
        category="TIMEOUT",
        action_name="inner_action",
        context="inner_context",
    )

    def raise_infra():
        raise original_infra

    with pytest.raises(InfrastructureError) as exc_info:
        Interceptor.run(
            raise_infra,
            action_name="outer_action",
        )

    assert exc_info.value is original_infra
