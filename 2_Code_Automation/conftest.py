"""
conftest.py - Master Pytest configuration delegating hooks and fixtures to modular plugins.
"""
import sys
from pathlib import Path

# Ensure 2_Code_Automation and 3_Bao_Cao_va_Ket_Qua are discoverable by python
_ROOT = Path(__file__).resolve().parent.parent
_CODE_DIR = _ROOT / "2_Code_Automation"
_REPORT_DIR = _ROOT / "3_Bao_Cao_va_Ket_Qua"
_SPECS_DIR = _ROOT / "1_Nghiep_Vu_va_Specs"

for d in [_CODE_DIR, _REPORT_DIR, _SPECS_DIR, _ROOT]:
    p = str(d)
    if p not in sys.path and d.exists():
        sys.path.insert(0, p)

pytest_plugins = [
    "core.pytest_plugins.browser_engine",
    "core.pytest_plugins.ticket_isolation",
    "core.pytest_plugins.step_and_video_hook",
]
