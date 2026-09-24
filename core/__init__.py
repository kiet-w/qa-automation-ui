"""
core package - Exceptor, Interceptor, and Error Catalog for Enterprise UI Automation Framework.
"""
from core.exceptions import BusinessAssertionError, InfrastructureError
from core.catalog import classify, ERROR_RULES, ErrorRule
from core.exceptor import Exceptor
from core.interceptor import Interceptor

__all__ = [
    "BusinessAssertionError",
    "InfrastructureError",
    "classify",
    "ERROR_RULES",
    "ErrorRule",
    "Exceptor",
    "Interceptor",
]
