#!/usr/bin/env python3
"""
Generate enterprise 19-column Excel workbook (.xlsx) matching the exact
AvePoint / Client Google Sheet tender format.
Supports parsing directly from markdown test case specifications (.md).
Spreadsheet reference: https://docs.google.com/spreadsheets/d/1ViSPLgggDsBI13SCPjfO_i0QoyUXy35A/edit?gid=1612531667

Usage:
  python3 tools/generate_19col_xlsx.py [path_to_spec.md] [-o path_to_output.xlsx]
  (Defaults to testcases/fs08/fs08-parent-profile/TC_FS08_Parent_Profile.md)
"""

import sys
import argparse
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def parse_markdown_table(md_path: Path):
    """Parse 19-column table from a markdown specification file."""
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    header_idx = -1
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if line_clean.startswith("|") and "| ID |" in line_clean and "Test Steps" in line_clean and "Expected Result" in line_clean:
            header_idx = i
            break

    if header_idx == -1:
        raise ValueError(f"Could not locate 19-column markdown table header in {md_path}")

    header_cols = [c.strip() for c in lines[header_idx].strip().split("|")[1:-1]]
    
    rows = []
    # Skip separator line (header_idx + 1)
    for line in lines[header_idx + 2:]:
        line_clean = line.strip()
        if not line_clean.startswith("|"):
            if rows:  # End of table
                break
            continue
        
        # Split row by | but respect escaped \|
        raw_cells = line_clean.split("|")[1:-1]
        if len(raw_cells) < 19:
            continue
        
        parsed_row = {}
        for idx, col_name in enumerate(header_cols):
            val = raw_cells[idx].strip() if idx < len(raw_cells) else ""
            # Unescape markdown
            val = val.replace("<br>", "\n").replace("\\|", "|")
            parsed_row[col_name] = val
        rows.append(parsed_row)

    return header_cols, rows

def build_19col_excel(md_path: Path, output_path: Path):
    headers, rows = parse_markdown_table(md_path)
    print(f"[*] Parsed {len(rows)} test cases from {md_path}")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "R8 TC"
    ws.views.sheetView[0].showGridLines = True

    font_name = "Segoe UI"
    header_font = Font(name=font_name, size=10, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")

    data_font = Font(name=font_name, size=9.5)
    id_font = Font(name="Consolas", size=9, bold=True, color="1B365D")

    # Severity / Priority Fills
    s1_font = Font(name=font_name, size=9, bold=True, color="9C0006")
    s1_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

    s2_font = Font(name=font_name, size=9, bold=True, color="9C6500")
    s2_fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")

    s3_font = Font(name=font_name, size=9, bold=True, color="006100")
    s3_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")

    passed_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    passed_font = Font(name=font_name, size=9, bold=True, color="006100")

    failed_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    failed_font = Font(name=font_name, size=9, bold=True, color="9C0006")

    not_run_fill = PatternFill(start_color="EDEDED", end_color="EDEDED", fill_type="solid")
    not_run_font = Font(name=font_name, size=9, color="595959")

    zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

    thin_border_side = Side(border_style="thin", color="D3D3D3")
    cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    # 19 Columns
    expected_headers = [
        "ID", "Scenario ID", "Title", "Test Suite", "Page",
        "Severity", "Priority", "Execution Status", "Test Type", "Environment",
        "Preconditions", "Test Data", "Test Steps", "Expected Result", "Actual Result",
        "Assumption Ref", "Defect ID", "Traceability", "Note"
    ]

    # Write Header Row
    ws.row_dimensions[1].height = 28
    for col_idx, h in enumerate(expected_headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = cell_border

    # Write Data Rows
    for row_idx, tc in enumerate(rows, 2):
        ws.row_dimensions[row_idx].height = 54
        is_even = (row_idx % 2 == 0)
        row_fill = zebra_fill if is_even else white_fill

        for col_idx, h in enumerate(expected_headers, 1):
            val = tc.get(h, "")
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = data_font
            cell.fill = row_fill
            cell.border = cell_border

            # Column-specific alignments & badge styles
            if col_idx in [1, 2]:  # ID & Scenario ID
                cell.font = id_font
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx in [6, 7, 8, 9]:  # Severity, Priority, Status, Type
                cell.alignment = Alignment(horizontal="center", vertical="center")
                
                # Severity / Priority badges
                if col_idx in [6, 7]:
                    val_str = str(val)
                    if "S1" in val_str or "Critical" in val_str:
                        cell.fill = s1_fill
                        cell.font = s1_font
                    elif "S2" in val_str or "High" in val_str:
                        cell.fill = s2_fill
                        cell.font = s2_font
                    elif "S3" in val_str or "Medium" in val_str:
                        cell.fill = s3_fill
                        cell.font = s3_font
                
                # Execution Status badge
                if col_idx == 8:
                    val_str = str(val)
                    if val_str == "Passed":
                        cell.fill = passed_fill
                        cell.font = passed_font
                    elif val_str == "Failed":
                        cell.fill = failed_fill
                        cell.font = failed_font
                    elif val_str == "Not Run":
                        cell.fill = not_run_fill
                        cell.font = not_run_font
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # Column Widths optimized for readability
    col_widths = {
        "A": 15,  # ID
        "B": 15,  # Scenario ID
        "C": 38,  # Title
        "D": 26,  # Test Suite
        "E": 22,  # Page
        "F": 13,  # Severity
        "G": 12,  # Priority
        "H": 16,  # Execution Status
        "I": 15,  # Test Type
        "J": 26,  # Environment
        "K": 28,  # Preconditions
        "L": 28,  # Test Data
        "M": 38,  # Test Steps
        "N": 42,  # Expected Result
        "O": 28,  # Actual Result
        "P": 28,  # Assumption Ref
        "Q": 14,  # Defect ID
        "R": 30,  # Traceability
        "S": 28   # Note
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    ws.auto_filter.ref = f"A1:S{len(rows) + 1}"
    ws.freeze_panes = "A2"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
    print(f"[+] Successfully generated 19-column Google Sheet format Excel: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert 19-column Markdown Test Cases to styled Excel (.xlsx)")
    parser.add_argument("md_path", nargs="?", default="testcases/fs08/fs08-parent-profile/TC_FS08_Parent_Profile.md", help="Path to markdown test spec")
    parser.add_argument("-o", "--output", default=None, help="Path to output .xlsx file")

    args = parser.parse_args()
    md_file = Path(args.md_path)
    if not md_file.exists():
        print(f"Error: Markdown file not found at {md_file}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        out_file = Path(args.output)
    else:
        out_file = md_file.with_suffix(".xlsx")

    build_19col_excel(md_file, out_file)

if __name__ == "__main__":
    main()
