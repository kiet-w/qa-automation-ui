"""
conftest.py - Master Pytest configuration delegating hooks and fixtures to modular plugins.
Modularized to eliminate monolithic 820-line file into:
- core.pytest_plugins.browser_engine: Multi-browser management & stealth flags
- core.pytest_plugins.ticket_isolation: Ticket & run_id artifact directory isolation
- core.pytest_plugins.step_and_video_hook: StepTracker timeline & dual-gate error classification
"""

pytest_plugins = [
    "core.pytest_plugins.browser_engine",
    "core.pytest_plugins.ticket_isolation",
    "core.pytest_plugins.step_and_video_hook",
]
