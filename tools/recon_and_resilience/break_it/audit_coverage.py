#!/usr/bin/env python3
"""
tools/break_it/audit_coverage.py - Adversarial & Break-It Coverage Auditor.

Scans the tests/ directory and audits whether functional test suites have
corresponding @pytest.mark.break_it resilience test coverage.

Usage:
    python3 tools/break_it/audit_coverage.py
"""
from collections import defaultdict
from pathlib import Path
import re
import sys

WORKSPACE_DIR = Path(__file__).resolve().parent.parent.parent
TESTS_DIR = WORKSPACE_DIR / "tests"


def audit_test_coverage():
    test_files = list(TESTS_DIR.glob("**/*.py"))
    
    modules = defaultdict(lambda: {"functional_tests": 0, "break_it_tests": 0, "files": []})
    
    for f in test_files:
        if f.name.startswith("__init__") or f.name == "base_test.py":
            continue
            
        rel = f.relative_to(TESTS_DIR)
        parts = rel.parts
        module_name = parts[0] if len(parts) > 1 else "root"
        
        content = f.read_text(encoding="utf-8")
        is_break_it = "@pytest.mark.break_it" in content or "test_tc_brk_" in content
        test_funcs = len(re.findall(r"def\s+test_", content))
        
        modules[module_name]["files"].append(str(rel))
        if is_break_it:
            modules[module_name]["break_it_tests"] += test_funcs
        else:
            modules[module_name]["functional_tests"] += test_funcs

    print("=" * 80)
    print("🛡️  AI CODING RESILIENCE & ADVERSARIAL (BREAK_IT) COVERAGE AUDIT")
    print("=" * 80)
    print(f"{'Module / Suite':<25} | {'Functional TCs':<16} | {'Break-It TCs':<14} | {'Status':<15}")
    print("-" * 80)

    total_func = 0
    total_brk = 0

    for mod, data in sorted(modules.items()):
        f_count = data["functional_tests"]
        b_count = data["break_it_tests"]
        total_func += f_count
        total_brk += b_count

        if b_count > 0:
            status = "✅ COVERED"
        elif f_count == 0:
            status = "⚪ NO TESTS"
        else:
            status = "⚠️  MISSING BREAK_IT"

        print(f"{mod:<25} | {f_count:<16} | {b_count:<14} | {status:<15}")

    print("=" * 80)
    print(f"TOTAL: Functional: {total_func} | Adversarial / Break-It: {total_brk}")
    print("=" * 80)

    missing = [m for m, d in modules.items() if d["functional_tests"] > 0 and d["break_it_tests"] == 0]
    if missing:
        print("\n⚠️  AI Coding Alert: The following modules are MISSING @pytest.mark.break_it suites:")
        for m in missing:
            print(f"   - {m} (run: python3 tools/break_it/scaffold_break_it.py --module {m} ...)")
    else:
        print("\n🎉 All active modules have corresponding break_it resilience test coverage!")


if __name__ == "__main__":
    audit_test_coverage()
