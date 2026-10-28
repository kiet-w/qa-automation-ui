"""
conftest.py - Master Pytest configuration and plugin delegation.
"""
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

pytest_plugins = [
    "core.pytest_plugins.browser_engine",
    "core.pytest_plugins.ticket_isolation",
    "core.pytest_plugins.step_and_video_hook",
]
