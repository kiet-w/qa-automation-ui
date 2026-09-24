"""
example_usage.py - Demonstration of Exceptor and Interceptor architectural usage.

Demonstrates how to decouple Playwright execution from business assertions:
- Interceptor wraps action execution and classifies infrastructure errors.
- Exceptor analyzes UI state snapshots and validates business expectations.
"""
from pathlib import Path
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core import Exceptor, Interceptor, BusinessAssertionError, InfrastructureError


def simulate_save_form_success():
    """Simulate a successful Playwright form submission."""
    print("Executing Playwright action: save_form()...")
    return {"status": "ok"}


def simulate_save_form_timeout():
    """Simulate a Playwright action encountering a timeout."""
    print("Executing Playwright action: save_form() -> Timeout!")
    raise Exception("Timeout 10000ms exceeded while waiting for selector '#save-btn'")


def mock_collect_snapshot(success: bool, errors: dict = None):
    """
    Simulate UI state snapshot collection from Page Object.
    Page Object collects the data; Exceptor evaluates it independently.
    """
    return {
        "success_visible": success,
        "visible_errors": errors or {},
    }


def demo_happy_path():
    print("\n--- 1. DEMO HAPPY PATH (Successful submission & verification) ---")

    # 1. Wrap Playwright interaction with Interceptor
    Interceptor.run(
        simulate_save_form_success,
        action_name="click_save_curricula",
        context="Save valid curricula trainer account profile",
    )

    # 2. Collect UI snapshot from Page Object
    snapshot = mock_collect_snapshot(success=True)

    # 3. Validate business expectation through Exceptor
    Exceptor.expect_success(snapshot, context="Valid trainer account registration")
    print("=> RESULT: PASS (Happy path succeeded as expected!)")


def demo_unhappy_path():
    print("\n--- 2. DEMO UNHAPPY PATH (Validating system properly blocks invalid input) ---")

    snapshot = mock_collect_snapshot(
        success=False,
        errors={"course_code": "Course code cannot be blank"},
    )

    Exceptor.expect_rejection(
        snapshot,
        field="course_code",
        message_contains="cannot be blank",
        context="Blank course code validation",
    )
    print("=> RESULT: PASS (System correctly blocked invalid input with proper error message!)")


def demo_bug_hunting():
    print("\n--- 3. DEMO BUG HUNTING (Catching real application defects) ---")

    # Simulate scenario: Valid business input incorrectly rejected by strict regex
    snapshot_rejected = mock_collect_snapshot(
        success=False,
        errors={"phone": "Phone number must be exactly 10 digits"},
    )

    try:
        Exceptor.expect_bug_if_rejected(
            snapshot_rejected,
            field="phone",
            context="Valid international phone number (+84912345678)",
        )
    except BusinessAssertionError as e:
        print(f"=> CAUGHT EXPECTED BUSINESS BUG:\n   {e}")


def demo_infrastructure_error():
    print("\n--- 4. DEMO INFRASTRUCTURE ERROR (Handling and classifying technical failures) ---")

    try:
        Interceptor.run(
            simulate_save_form_timeout,
            action_name="save_curricula",
            context="Testing timeout handling on Save button",
        )
    except InfrastructureError as e:
        print(f"=> CAUGHT CLASSIFIED INFRASTRUCTURE ERROR:\n   Category: {e.category}\n   Message: {e}")


if __name__ == "__main__":
    print("==========================================================")
    print("  EXCEPTOR & INTERCEPTOR ARCHITECTURAL DEMO")
    print("==========================================================")
    demo_happy_path()
    demo_unhappy_path()
    demo_bug_hunting()
    demo_infrastructure_error()
    print("\n==========================================================")
    print("  ALL DEMO EXAMPLES EXECUTED SUCCESSFULLY!")
    print("==========================================================")
