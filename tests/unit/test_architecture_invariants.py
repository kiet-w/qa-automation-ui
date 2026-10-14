# tests/unit/test_architecture_invariants.py
"""
tests/unit/test_architecture_invariants.py
AST-based architectural tests that automatically guard the core framework invariants:
- Invariant 1: Zero assertions in Page Objects and UI Components
- Invariant 2: Zero raw time.sleep calls across execution paths
- Invariant 7: Zero external CDN references in offline reporting
- Code Hygiene: Zero leftover debug print() statements in page objects & components
"""
import ast
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


class _StripMainBlockTransformer(ast.NodeTransformer):
    """Strip `if __name__ == '__main__':` blocks from AST to prevent false positives for CLI tools."""

    def visit_If(self, node: ast.If):
        if (
            isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == "__name__"
            and len(node.test.comparators) == 1
            and isinstance(node.test.comparators[0], ast.Constant)
            and node.test.comparators[0].value == "__main__"
        ):
            return None
        return self.generic_visit(node)


def _iter_python_files(subdirs: list[str]) -> list[Path]:
    files: list[Path] = []
    for subdir in subdirs:
        target = REPO_ROOT / subdir
        if target.exists():
            files.extend(target.rglob("*.py"))
    return files


def test_invariant_1_zero_asserts_in_pages_and_components():
    """Invariant 1: Page Objects and Components must never contain `assert` statements."""
    violations = []
    for py_file in _iter_python_files(["pages", "components"]):
        tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                violations.append(f"{py_file.relative_to(REPO_ROOT)}:{node.lineno}")
    assert not violations, f"Invariant 1 Violated - Found `assert` in Page/Component: {violations}"


def test_invariant_2_zero_raw_time_sleep():
    """Invariant 2: Ban `time.sleep()` or `from time import sleep` in production and test paths."""
    violations = []
    for py_file in _iter_python_files(["pages", "components", "tests", "core"]):
        if py_file.name == "test_architecture_invariants.py":
            continue
        tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        imported_time_sleep_aliases: set[str] = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "time":
                for alias in node.names:
                    if alias.name == "sleep":
                        imported_time_sleep_aliases.add(alias.asname or "sleep")

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Pattern 1: time.sleep(...)
                if (
                    isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "time"
                    and node.func.attr == "sleep"
                ):
                    violations.append(f"{py_file.relative_to(REPO_ROOT)}:{node.lineno}")
                # Pattern 2: from time import sleep -> sleep(...)
                elif (
                    isinstance(node.func, ast.Name)
                    and node.func.id in imported_time_sleep_aliases
                ):
                    violations.append(f"{py_file.relative_to(REPO_ROOT)}:{node.lineno}")

    assert not violations, f"Invariant 2 Violated - Found `time.sleep()`: {violations}"


def test_hygiene_zero_debug_print_in_pages_and_components():
    """Code Hygiene: Zero debug print() statements in pages/ and components/."""
    violations = []
    for py_file in _iter_python_files(["pages", "components"]):
        tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        clean_tree = _StripMainBlockTransformer().visit(tree)
        for node in ast.walk(clean_tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "print"
            ):
                violations.append(f"{py_file.relative_to(REPO_ROOT)}:{node.lineno}")
    assert not violations, f"Code Hygiene Violated - Leftover print() in Page/Component: {violations}"


def test_invariant_7_zero_external_cdn_in_reporting():
    """Invariant 7: Ensure reporting/ is 100% self-contained and zero external CDNs."""
    forbidden_hosts = (
        "cdn.jsdelivr.net",
        "unpkg.com",
        "cdnjs.cloudflare.com",
        "fonts.googleapis.com",
        "cdn.tailwindcss.com",
    )
    violations = []
    for file_path in (REPO_ROOT / "reporting").rglob("*.*"):
        if file_path.suffix in {".py", ".js", ".css", ".html"}:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            for host in forbidden_hosts:
                if host in content:
                    violations.append(f"{file_path.relative_to(REPO_ROOT)} ({host})")
    assert not violations, f"Invariant 7 Violated - External CDN reference in reporting: {violations}"
