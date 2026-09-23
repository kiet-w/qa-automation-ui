"""
reporting/core/generator.py - Orchestrates report generation and file persistence.
"""

import shutil
from pathlib import Path
from typing import List, Optional

from reporting.core.document import assemble_html_document
from reporting.core.parser import load_report_json, process_report_data


class ReportGenerator:
    """Coordinates data loading, media encoding, SVG rendering, and file export."""

    def __init__(self, workspace_dir: Optional[Path] = None, reports_dir: Optional[Path] = None):
        self.workspace_dir = workspace_dir or Path(__file__).resolve().parent.parent.parent
        self.reports_dir = reports_dir or (self.workspace_dir / "reports")
        self.test_results_dir = self.reports_dir / "test-results"

    def generate(
        self,
        json_path: Optional[Path] = None,
        output_html_path: Optional[Path] = None,
    ) -> Path:
        """Executes full report generation and writes self-contained HTML file."""
        if json_path:
            json_file = Path(json_path)
            # If a specific ticket folder path is passed, isolate reports_dir to that folder
            if json_file.parent != self.workspace_dir:
                self.reports_dir = json_file.parent
                self.test_results_dir = self.reports_dir / "test-results"
        else:
            json_file = self.reports_dir / "report.json"

        self.reports_dir.mkdir(parents=True, exist_ok=True)
        report_data = load_report_json(json_file)

        # Scope video search to specific run_id subfolder if present
        run_id_hint = report_data.get("run_id")
        run_test_results = (self.test_results_dir / run_id_hint) if run_id_hint else None
        search_dir = run_test_results if (run_test_results and run_test_results.exists()) else self.test_results_dir

        all_videos: List[Path] = []
        if search_dir.exists():
            all_videos = sorted(list(search_dir.glob("**/*.webm")))
            if all_videos:
                folder_label = search_dir.relative_to(self.workspace_dir) if self.workspace_dir in search_dir.parents else search_dir.name
                print(f"📹 Found {len(all_videos)} video recording(s) in {folder_label}")
                for v in all_videos:
                    size_mb = v.stat().st_size / (1024 * 1024)
                    print(f"   -> {v.name} ({size_mb:.2f} MB)")

        parsed_data = process_report_data(
            report_data=report_data,
            all_videos=all_videos,
            reports_dir=self.reports_dir,
            workspace_dir=self.workspace_dir,
        )

        run_id = parsed_data.get("run_id", "RUN-UNKNOWN")
        history_dir = self.reports_dir / "history"
        history_dir.mkdir(parents=True, exist_ok=True)

        if output_html_path:
            target_html = Path(output_html_path)
        else:
            target_html = history_dir / f"{run_id}.html"

        print("=" * 65)
        print("🚀 [ExtentReports Generator]")
        print(f"   Input JSON : {json_file}")
        print(f"   Run ID     : {run_id}")
        print(f"   Output HTML: {target_html}")
        print("=" * 65)

        full_html = assemble_html_document(
            parsed=parsed_data,
            report_data=report_data,
        )

        target_html.parent.mkdir(parents=True, exist_ok=True)
        with open(target_html, "w", encoding="utf-8") as f:
            f.write(full_html)

        # Also maintain execution_report.html as the latest run reference at the root of reports_dir
        latest_html = self.reports_dir / "execution_report.html"
        if target_html.resolve() != latest_html.resolve():
            shutil.copyfile(target_html, latest_html)

        # Also copy to root workspace reports/execution_report.html so accessing the standard path always shows the latest run!
        root_reports_html = self.workspace_dir / "reports" / "execution_report.html"
        if target_html.resolve() != root_reports_html.resolve():
            root_reports_html.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(target_html, root_reports_html)

        file_size_mb = target_html.stat().st_size / (1024 * 1024)
        print("✅ ExtentReport successfully generated!")
        print(f"   Run Report (History): {target_html}")
        print(f"   Latest Report       : {latest_html}")
        if root_reports_html.resolve() != latest_html.resolve():
            print(f"   Root Report (Global): {root_reports_html}")
        print(f"   File Size           : {file_size_mb:.2f} MB (100% self-contained)")
        print("=" * 65)

        return target_html
