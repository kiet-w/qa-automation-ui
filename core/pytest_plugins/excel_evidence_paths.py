"""Path handling for screenshot hyperlinks in execution-evidence workbooks."""

from pathlib import Path
import os
import re
from typing import Any, Dict, Iterable, Optional
from urllib.parse import urlparse


def test_slug_candidates(nodeid: str) -> Iterable[str]:
    """Return slugs in the same format used by the screenshot capture hook."""
    raw_name = nodeid.split("::")[-1].lower()
    base_name = re.sub(r"\[.*?\]$", "", raw_name)
    seen = set()
    for name in (raw_name, base_name):
        slug = re.sub(r"[^\w]+", "_", name).strip("_")
        if slug and slug not in seen:
            seen.add(slug)
            yield slug


def find_actual_result_screenshot(
    reports_dir: Path,
    nodeid: str,
    metadata: Dict[str, Any],
    repo_root: Path,
) -> Optional[Path]:
    """Find the canonical actual-result image before considering step fallbacks."""
    screenshots_dir = reports_dir / "screenshots"
    for slug in test_slug_candidates(nodeid):
        canonical = screenshots_dir / slug / "actual_result.png"
        if canonical.is_file():
            return canonical
        legacy = screenshots_dir / f"{slug}_actual_result.png"
        if legacy.is_file():
            return legacy

    steps = metadata.get("steps", []) or []
    ordered_steps = [step for step in reversed(steps) if step.get("is_actual_result")]
    ordered_steps.extend(step for step in reversed(steps) if not step.get("is_actual_result"))
    for step in ordered_steps:
        screenshot = step.get("screenshot")
        if not screenshot:
            continue
        path = Path(screenshot)
        if not path.is_absolute():
            path = repo_root / path
        if path.is_file():
            return path
    return None


def relative_excel_target(asset: Path, workbook_dir: Path) -> str:
    """Create a portable relative target from an XLSX location to a local asset."""
    return Path(os.path.relpath(asset.resolve(), workbook_dir.resolve())).as_posix()


def rebase_local_target(target: str, old_base: Path, new_base: Path) -> str:
    """Rebase a workbook hyperlink while preserving web/mail links unchanged."""
    parsed = urlparse(target)
    if parsed.scheme or target.startswith("#"):
        return target
    asset = Path(target)
    if not asset.is_absolute():
        asset = old_base / asset
    return relative_excel_target(asset, new_base)
